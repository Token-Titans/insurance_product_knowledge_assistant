"use client";

import { useEffect } from "react";

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
  animate?: boolean;
  turnId?: string;
}

export function AnswerPanel({
  response,
  animate = false,
  turnId,
}: AnswerPanelProps) {
  const { shown, isTyping } = useTypedText(response.answer, animate);
  const showSource = hasSourceCitation(response.source);
  const isGrounded = isGroundedResponse(response.confidence);

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
      {!isTyping && (showSource || isGrounded) ? (
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          {showSource ? <SourceBadges source={response.source} /> : null}
          {isGrounded ? <FollowUpButton /> : null}
        </div>
      ) : null}
    </section>
  );
}
