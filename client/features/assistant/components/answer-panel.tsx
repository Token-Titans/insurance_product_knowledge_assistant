"use client";

import { useTranslation } from "react-i18next";

import { ConditionsBlock } from "@/features/assistant/components/conditions-block";
import { FollowUpButton } from "@/features/assistant/components/follow-up-button";
import { ImportantPoints } from "@/features/assistant/components/important-points";
import { SourceCard } from "@/features/assistant/components/source-card";

import type { AskResponse } from "@/features/assistant/types/ask.types";

interface AnswerPanelProps {
  question: string;
  response: AskResponse;
}

export function AnswerPanel({ question, response }: AnswerPanelProps) {
  const { t } = useTranslation("assistant");

  return (
    <section className="space-y-5">
      <p className="font-myanmar text-sm text-muted-foreground">{question}</p>
      <article className="rounded-2xl bg-card p-6 ring-1 ring-border">
        <p className="text-base leading-relaxed">{response.answer}</p>
      </article>
      <div className="grid gap-4 md:grid-cols-2">
        <ImportantPoints points={response.important_points} />
        <ConditionsBlock conditions={response.conditions} />
      </div>
      <div className="space-y-2">
        <h3 className="font-heading text-sm font-medium">{t("answered.sources")}</h3>
        {response.sources.map((source) => (
          <SourceCard
            key={`${source.document}-${source.section}`}
            source={source}
          />
        ))}
      </div>
      <FollowUpButton />
    </section>
  );
}
