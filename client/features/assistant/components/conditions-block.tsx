"use client";

import { TriangleAlert } from "lucide-react";
import { useTranslation } from "react-i18next";

interface ConditionsBlockProps {
  conditions: string[];
}

export function ConditionsBlock({ conditions }: ConditionsBlockProps) {
  const { t } = useTranslation("assistant");

  return (
    <section className="rounded-2xl border border-alert/30 bg-card p-5">
      <h3 className="font-heading text-sm font-medium text-alert">
        {t("answered.conditions")}
      </h3>
      <ul className="mt-3 space-y-2">
        {conditions.map((condition) => (
          <li key={condition} className="flex items-start gap-2 text-sm">
            <TriangleAlert className="mt-0.5 size-4 text-alert" />
            <span>{condition}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
