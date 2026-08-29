"use client";

import { useTranslation } from "react-i18next";

import { Badge } from "@/components/ui/badge";
import { AnswerMarkdown } from "@/features/assistant/components/answer-markdown";
import { FollowUpButton } from "@/features/assistant/components/follow-up-button";
import { isGroundedResponse } from "@/features/assistant/schemas/ask.schema";

import type { AskResponse, AskSource } from "@/features/assistant/types/ask.types";

interface AnswerPanelProps {
  response: AskResponse;
}

function hasSourceCitation(source: AskSource) {
  return Boolean(
    source.document.trim() ||
      source.section.trim() ||
      source.file.trim() ||
      source.page != null,
  );
}

export function AnswerPanel({ response }: AnswerPanelProps) {
  const { t } = useTranslation("assistant");
  const showSource = hasSourceCitation(response.source);
  const isGrounded = isGroundedResponse(response.confidence);

  return (
    <section className="max-w-prose space-y-3">
      <AnswerMarkdown content={response.answer} />
      {showSource ? (
        <div className="flex flex-wrap gap-1.5">
          <span className="sr-only">{t("answered.sources")}</span>
          {response.source.document.trim() ? (
            <Badge
              variant="outline"
              className="h-auto max-w-full whitespace-normal py-1"
            >
              {response.source.document}
            </Badge>
          ) : null}
          {response.source.section.trim() ? (
            <Badge
              variant="secondary"
              className="h-auto max-w-full whitespace-normal py-1"
            >
              {response.source.section}
            </Badge>
          ) : null}
          {response.source.page != null ? (
            <Badge
              variant="secondary"
              className="h-auto max-w-full whitespace-normal py-1"
            >
              {t("answered.page", { page: response.source.page })}
            </Badge>
          ) : null}
        </div>
      ) : null}
      {isGrounded ? <FollowUpButton /> : null}
    </section>
  );
}
