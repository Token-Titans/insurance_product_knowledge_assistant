"use client";

import { ShieldOff, UserRound, Wallet, type LucideIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

import { SUGGESTED_QUESTIONS } from "@/features/assistant/constants/products";

interface SuggestedQuestionsProps {
  disabled?: boolean;
  onSelect: (question: string) => void;
}

const SUGGESTION_ICONS: Record<
  (typeof SUGGESTED_QUESTIONS)[number]["id"],
  LucideIcon
> = {
  eligibility: UserRound,
  exclusion: ShieldOff,
  unavailable: Wallet,
};

export function SuggestedQuestions({
  disabled = false,
  onSelect,
}: SuggestedQuestionsProps) {
  const { t } = useTranslation("assistant");

  return (
    <div className="space-y-3">
      <p className="text-center text-xs text-muted-foreground">
        {t("ask.suggested_label")}
      </p>
      <div className="grid gap-2 sm:grid-cols-3">
        {SUGGESTED_QUESTIONS.map((item) => {
          const Icon = SUGGESTION_ICONS[item.id];
          const question = t(item.labelKey);

          return (
            <button
              key={item.id}
              type="button"
              disabled={disabled}
              aria-label={question}
              className="flex h-full flex-col gap-2 rounded-2xl bg-card p-3 text-left ring-1 ring-border transition-colors hover:bg-muted disabled:pointer-events-none disabled:opacity-50"
              onClick={() => onSelect(question)}
            >
              <Icon className="size-4 text-primary" />
              <span className="font-heading text-sm font-medium">
                {t(item.titleKey)}
              </span>
              <span className="font-myanmar text-xs leading-relaxed text-muted-foreground">
                {question}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
