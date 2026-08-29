"use client";

import { useTranslation } from "react-i18next";

interface AskErrorBannerProps {
  code: string;
}

export function AskErrorBanner({ code }: AskErrorBannerProps) {
  const { t } = useTranslation("assistant");
  const messageKey = `ask.errors.${code}`;
  const message = t(messageKey, { defaultValue: t("ask.errors.generic") });

  return (
    <div
      role="alert"
      className="rounded-xl border border-alert/30 bg-card px-4 py-3 text-sm text-alert"
    >
      <p className="font-medium">{t("ask.error_title")}</p>
      <p className="mt-1">{message}</p>
    </div>
  );
}
