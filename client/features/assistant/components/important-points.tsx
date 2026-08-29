"use client";

import { CircleCheck } from "lucide-react";
import { useTranslation } from "react-i18next";

interface ImportantPointsProps {
  points: string[];
}

export function ImportantPoints({ points }: ImportantPointsProps) {
  const { t } = useTranslation("assistant");

  return (
    <section className="rounded-2xl bg-muted p-5 ring-1 ring-border">
      <h3 className="font-heading text-sm font-medium text-accent-foreground">
        {t("answered.important_points")}
      </h3>
      <ul className="mt-3 space-y-2">
        {points.map((point) => (
          <li key={point} className="flex items-start gap-2 text-sm">
            <CircleCheck className="mt-0.5 size-4 text-brand" />
            <span>{point}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
