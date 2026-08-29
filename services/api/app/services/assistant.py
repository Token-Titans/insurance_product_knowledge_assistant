"""Ask orchestration: retrieve one product file, then OpenAI or extractive fallback."""

import re

from app.core.config import Settings
from app.core.errors import invalid_request
from app.models.assistant import AssistantResponse, SourceReference
from app.services.ai.openai_client import chat_json
from app.services.retrieve import DocumentSection, RankedSection, search_documents

_MYANMAR = re.compile(r"[\u1000-\u109F]")
_GREETING = re.compile(
    r"^(hi|hello|hey|yo|thanks|thank you|thx|good morning|good afternoon|"
    r"good evening|how are you|what'?s up)[\s!.,?]*$",
    re.IGNORECASE,
)
_THANKS = re.compile(r"thank|thanks|thx|ကျေးဇူး", re.IGNORECASE)

SYSTEM_PROMPT = (
    "You are InsureAssist, a product-knowledge assistant for insurance sales agents. "
    "Write like a sharp coach: lead with the direct answer, then the numbers, "
    "then any condition or exclusion the agent must mention. "
    "Use short paragraphs or tight bullets. Sound natural, not like a copied brochure. "
    "Answer only from the approved excerpts. Never invent benefits, limits, ages, "
    "sums insured, waiting periods, or exclusions. "
    "Match the agent's language. If the question uses Myanmar script, write answer, "
    "important_conditions, and exclusions in natural Burmese. If the question is English, "
    "write English. Keep product names, MMK, and percentages as in the excerpts. "
    "If the question is a greeting or thanks, greet them, invite a product question, "
    "and do not invent product facts. "
    "If the excerpts do not support the question, say you don't know in the same language. "
    "This is not a quote, underwriting decision, or policy contract."
)

_UNAVAILABLE_EN = (
    "I don't know. The approved product documents do not contain enough "
    "information to answer this question."
)
_UNAVAILABLE_MY = (
    "ကျွန်ုပ် မသိပါ။ အတည်ပြုထားသော ထုတ်ကုန် စာရွက်စာတမ်းတွင် "
    "ဤမေးခွန်းအတွက် လုံလောက်သော အချက်အလက် မပါဝင်ပါ။"
)
_GREETING_EN = (
    "Hello — I'm InsureAssist, your product-knowledge assistant. "
    "Ask about eligibility, benefits, exclusions, or how this plan fits a customer. "
    "I only answer from approved product documents."
)
_GREETING_MY = (
    "မင်္ဂလာပါ။ InsureAssist ဖြစ်ပါတယ်။ "
    "အာမခံထားရှိနိုင်မှု၊ အကျိုးခံစားခွင့်၊ ချွင်းချက်များကို မေးနိုင်ပါတယ်။ "
    "အတည်ပြုထားသော ထုတ်ကုန် စာရွက်စာတမ်းများမှသာ ဖြေပါမယ်။"
)
_THANKS_EN = (
    "You're welcome. If you need a benefit, exclusion, or eligibility check "
    "from the approved documents, ask anytime."
)
_THANKS_MY = (
    "ကိစ္စမရှိပါဘူး။ အကျိုးခံစားခွင့်၊ ချွင်းချက် သို့မဟုတ် "
    "အာမခံထားရှိနိုင်မှုကို ဆက်မေးနိုင်ပါတယ်။"
)

_CONDITION_HINTS = (
    "waiting period",
    "pre-authorisation",
    "pre-authorization",
    "subject to",
    "must",
    "only after",
    "not payable",
    "annual aggregate",
)
_EXCLUSION_HINTS = (
    "does not pay",
    "not covered",
    "exclusion",
    "not pay for",
)


def _uses_myanmar(text: str) -> bool:
    return bool(_MYANMAR.search(text))


def _unavailable_answer(question: str) -> str:
    return _UNAVAILABLE_MY if _uses_myanmar(question) else _UNAVAILABLE_EN


def _is_small_talk(question: str) -> bool:
    stripped = question.strip()
    if len(stripped) > 80:
        return False
    if _GREETING.fullmatch(stripped):
        return True
    compact = stripped.replace(" ", "")
    greetings_my = ("မင်္ဂလာပါ", "ဟယ်လို", "ဟိုင်း")
    if any(item in stripped for item in greetings_my) and len(compact) < 24:
        return True
    return bool(_THANKS.search(stripped) and len(stripped) < 40)


def _small_talk_answer(question: str) -> str:
    myanmar = _uses_myanmar(question)
    if _THANKS.search(question) and not _GREETING.fullmatch(question.strip()):
        return _THANKS_MY if myanmar else _THANKS_EN
    return _GREETING_MY if myanmar else _GREETING_EN


def _empty_source() -> SourceReference:
    return SourceReference(document="", file="", section="", page=None)


def _source_from(section: DocumentSection) -> SourceReference:
    """Copy citation fields from a retrieved section only."""

    return SourceReference(
        document=section.document,
        file=section.filename,
        section=section.section,
        page=section.page,
    )


def _confidence(ranked: list[RankedSection]) -> float:
    """Map the top keyword score onto a 0.0–1.0 range."""

    if not ranked:
        return 0.0
    return round(min(1.0, ranked[0].score / 10.0), 2)


def _bullet_or_sentence_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in re.split(r"[\n;]", text):
        item = " ".join(raw.split()).strip(" -*")
        if len(item) >= 24:
            lines.append(item)
    return lines


def _extract_labeled(sections: list[DocumentSection], heading: str, hints: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for section in sections:
        relevant = heading in section.section.lower()
        for line in _bullet_or_sentence_lines(section.content):
            lowered = line.lower()
            if lowered in seen:
                continue
            if relevant or any(hint in lowered for hint in hints):
                seen.add(lowered)
                found.append(line)
            if len(found) >= 5:
                return found
    return found


def _context_block(sections: list[DocumentSection]) -> str:
    if not sections:
        return "Approved source excerpts: none were retrieved."
    parts = ["Approved source excerpts:"]
    for index, section in enumerate(sections, start=1):
        page = f" page={section.page}" if section.page is not None else ""
        parts.append(
            f"[{index}] document={section.document!r} file={section.filename!r} "
            f"section={section.section!r}{page}\n{section.content}"
        )
    return "\n\n".join(parts)


def build_prompt(question: str, sections: list[DocumentSection]) -> list[dict[str, str]]:
    """Build OpenAI chat messages from the top retrieved sections."""

    language = (
        "Write the JSON string values in natural Burmese (Myanmar script)."
        if _uses_myanmar(question)
        else "Write the JSON string values in clear English."
    )
    user_prompt = (
        f"Question: {question}\n\n{_context_block(sections)}\n\n"
        f"{language} "
        "Return JSON with keys: answer (string), important_conditions (array of strings), "
        "exclusions (array of strings). "
        "answer should be 2–5 short sentences or bullets a sales agent can say aloud. "
        "Copy conditions and exclusions only from the excerpts; keep them brief. "
        "If the excerpts do not support an answer, say you don't know in the same "
        "language as the question and use empty arrays. "
        "Do not invent benefits, limits, waiting periods, or exclusions."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _extractive_answer(question: str, sections: list[DocumentSection]) -> str:
    if not sections:
        return _unavailable_answer(question)
    text = " ".join(sections[0].content.split())
    if len(text) > 900:
        text = text[:897].rsplit(" ", 1)[0] + "..."
    if _uses_myanmar(question):
        return (
            "အတည်ပြု စာရွက်စာတမ်းမှ အချက်အလက်ဖြစ်ပါတယ်။ "
            "အေးဂျင့်အနေဖြင့် ဖောက်သည်ကို ပြောပြနိုင်သည်များ:\n\n"
            + text
        )
    return text


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


async def ask_product_question(
    product_id: str,
    question: str,
    settings: Settings,
) -> AssistantResponse:
    """Retrieve one product file, generate an answer, and attach a real citation."""

    cleaned_product = product_id.strip()
    cleaned_question = question.strip()
    if not cleaned_product:
        raise invalid_request("product_id must not be empty")
    if not cleaned_question:
        raise invalid_request("question must not be empty")

    if _is_small_talk(cleaned_question):
        return AssistantResponse(
            answer=_small_talk_answer(cleaned_question),
            important_conditions=[],
            exclusions=[],
            source=_empty_source(),
            confidence=1.0,
        )

    ranked = search_documents(cleaned_question, cleaned_product)
    sections = [item.section for item in ranked]
    generated = await chat_json(build_prompt(cleaned_question, sections), settings)

    source = _source_from(sections[0]) if sections else _empty_source()
    fallback_conditions = _extract_labeled(sections, "condition", _CONDITION_HINTS)
    fallback_exclusions = _extract_labeled(sections, "exclusion", _EXCLUSION_HINTS)

    if generated is None:
        return AssistantResponse(
            answer=_extractive_answer(cleaned_question, sections),
            important_conditions=fallback_conditions,
            exclusions=fallback_exclusions,
            source=source,
            confidence=_confidence(ranked),
        )

    answer = str(generated.get("answer", "")).strip() or _extractive_answer(
        cleaned_question, sections
    )
    return AssistantResponse(
        answer=answer,
        important_conditions=_string_list(generated.get("important_conditions"))
        or fallback_conditions,
        exclusions=_string_list(generated.get("exclusions")) or fallback_exclusions,
        source=source,
        confidence=_confidence(ranked),
    )
