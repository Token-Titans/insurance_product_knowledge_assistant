"use client";

import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { AnswerMarkdown } from "@/features/assistant/components/answer-markdown";
import { FollowUpButton } from "@/features/assistant/components/follow-up-button";
import {
  SourceBadges,
  hasSourceCitation,
} from "@/features/assistant/components/source-badges";
import { useTypedText } from "@/features/assistant/hooks/use-typed-text";
import { isGroundedResponse } from "@/features/assistant/schemas/ask.schema";

import type { AskResponse } from "@/features/assistant/types/ask.types";

interface AnswerPanelProps {
  response: AskResponse;
  productId: string;
  animate?: boolean;
  turnId?: string;
}

function toBulletList(items: string[]) {
  return items
    .map((item) => item.trim().replace(/\s+/g, " "))
    .filter((item) => item.length > 0)
    .map((item) => `- ${item}`)
    .join("\n");
}

function buildFactsMarkdown(
  importantConditions: string[],
  exclusions: string[],
  headings: { importantPoints: string; conditions: string },
) {
  const sections: string[] = [];
  const conditionBullets = toBulletList(importantConditions);
  const exclusionBullets = toBulletList(exclusions);

  if (conditionBullets) {
    sections.push(`### ${headings.importantPoints}\n${conditionBullets}`);
  }

  if (exclusionBullets) {
    sections.push(`### ${headings.conditions}\n${exclusionBullets}`);
  }

  return sections.join("\n\n");
}

export function AnswerPanel({
  response,
  productId,
  animate = false,
  turnId,
}: AnswerPanelProps) {
  const { t } = useTranslation("assistant");
  const { shown, isTyping } = useTypedText(response.answer, animate);
  const showSource = hasSourceCitation(response.source);
  const isGrounded = isGroundedResponse(response.confidence);
  const factsMarkdown = buildFactsMarkdown(
    response.important_conditions,
    response.exclusions,
    {
      importantPoints: t("answered.important_points"),
      conditions: t("answered.conditions"),
    },
  );

  useEffect(() => {
    if (!isTyping || !turnId) {
      return;
    }

    document.getElementById(`ask-turn-${turnId}`)?.scrollIntoView({
      block: "end",
      behavior: "auto",
    });
  }, [isTyping, shown, turnId]);

  return (
    <section className="max-w-prose space-y-3">
      <AnswerMarkdown content={shown} isTyping={isTyping} />
      {!isTyping && factsMarkdown ? (
        <AnswerMarkdown content={factsMarkdown} />
      ) : null}
      {!isTyping && (showSource || isGrounded) ? (
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          {showSource ? <SourceBadges source={response.source} /> : null}
          {isGrounded ? <FollowUpButton productId={productId} /> : null}
        </div>
      ) : null}
    </section>
  );
}
