"""Prompt for grounded product-knowledge answers."""

from app.services.knowledge.corpus import KnowledgeChunk

SYSTEM_PROMPT = """You are InsureAssist, a product-knowledge assistant for insurance sales agents.
Answer only from the approved source excerpts provided in the user message.
Do not use general insurance knowledge when a product-specific fact is required.
Never invent a benefit, limit, waiting period, exclusion, eligibility rule, or coverage condition.
If the excerpts do not support an answer, say the information is unavailable, state what source would be needed, and set confidence to "unavailable".
Preserve material conditions, exclusions, waiting periods, and limits. Do not flatten them into unconditional claims.
You support sales agents with verifiable product facts. You do not make final customer, claims, underwriting, or coverage decisions.
Return JSON only with keys: answer, important_points, conditions, sources, confidence.
confidence must be "grounded" or "unavailable".
sources must be an array of objects with "document" and "section" copied from the provided excerpts.
important_points and conditions must be arrays of short strings.
"""


def build_user_prompt(question: str, chunks: list[KnowledgeChunk]) -> str:
    """Build the user message with numbered approved excerpts."""

    if not chunks:
        return (
            f"Question: {question}\n\n"
            "Approved source excerpts: none were retrieved.\n"
            "Return an unavailable response."
        )

    parts = [f"Question: {question}", "", "Approved source excerpts:"]
    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[{index}] document={chunk.document!r} section={chunk.section!r}\n{chunk.text}"
        )
    parts.append(
        "\nUse only these excerpts. Cite document and section values exactly as given."
    )
    return "\n\n".join(parts)
