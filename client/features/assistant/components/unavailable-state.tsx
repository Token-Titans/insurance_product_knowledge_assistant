"use client";

import { ShieldOff } from "lucide-react";
import { useTranslation } from "react-i18next";

interface UnavailableStateProps {
  message?: string;
}

export function UnavailableState({ message }: UnavailableStateProps) {
  const { t } = useTranslation("assistant");

  return (
    <section className="rounded-2xl bg-card px-5 py-6 ring-1 ring-border">
      <ShieldOff className="size-6 text-primary" />
      <h2 className="mt-3 font-heading text-lg font-medium">
        {t("unavailable.title")}
      </h2>
      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        {message ?? t("unavailable.body")}
      </p>
    </section>
  );
}
