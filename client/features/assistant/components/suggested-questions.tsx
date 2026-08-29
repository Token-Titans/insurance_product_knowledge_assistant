"use client";

import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { SUGGESTED_QUESTIONS } from "@/features/assistant/constants/products";

interface SuggestedQuestionsProps {
  disabled?: boolean;
  onSelect: (question: string) => void;
}

export function SuggestedQuestions({
  disabled = false,
  onSelect,
}: SuggestedQuestionsProps) {
  const { t } = useTranslation("assistant");

  return (
    <div className="space-y-2">
      <p className="text-xs text-muted-foreground">{t("ask.suggested_label")}</p>
      <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
        {SUGGESTED_QUESTIONS.map((item) => (
          <Button
            key={item.id}
            type="button"
            variant="outline"
            disabled={disabled}
            className="h-auto max-w-full justify-start whitespace-normal font-myanmar text-left"
            onClick={() => onSelect(t(item.labelKey))}
          >
            {t(item.labelKey)}
          </Button>
        ))}
      </div>
    </div>
  );
}
