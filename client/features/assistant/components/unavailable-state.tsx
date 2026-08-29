"use client";

import { ShieldOff } from "lucide-react";
import { useTranslation } from "react-i18next";

interface UnavailableStateProps {
  question: string;
  message?: string;
}

export function UnavailableState({
  question,
  message,
}: UnavailableStateProps) {
  const { t } = useTranslation("assistant");

  return (
    <section className="flex flex-col items-center rounded-2xl bg-card px-6 py-16 text-center ring-1 ring-border">
      <ShieldOff className="size-8 text-primary" />
      <p className="mt-4 max-w-md font-myanmar text-sm text-muted-foreground">
        {question}
      </p>
      <h2 className="mt-4 font-heading text-xl font-medium">
        {t("unavailable.title")}
      </h2>
      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        {message ?? t("unavailable.body")}
      </p>
    </section>
  );
}
