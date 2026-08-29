"use client";

import { useTranslation } from "react-i18next";

interface AskPendingBarProps {
  isVisible: boolean;
}

export function AskPendingBar({ isVisible }: AskPendingBarProps) {
  const { t } = useTranslation("assistant");

  if (!isVisible) {
    return null;
  }

  return (
    <div
      aria-live="polite"
      className="flex items-center gap-3 rounded-xl bg-mist px-4 py-2 text-sm text-indigo"
    >
      <span className="size-2 animate-pulse rounded-full bg-brand" />
      {t("ask.pending")}
    </div>
  );
}
