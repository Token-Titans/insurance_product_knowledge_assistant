"use client";

import { useTranslation } from "react-i18next";

import { Skeleton } from "@/components/ui/skeleton";
import { AnswerMarkdown } from "@/features/assistant/components/answer-markdown";
import { AskErrorBanner } from "@/features/assistant/components/ask-error-banner";
import { FollowUpButton } from "@/features/assistant/components/follow-up-button";
import { SourceBadges } from "@/features/assistant/components/source-badges";
import { isGroundedResponse } from "@/features/assistant/schemas/ask.schema";
import { useProducts } from "@/shared/queries/products.query";

import type { CompareChatTurn, CompareColumnState } from "@/features/assistant/types/ask-screen.types";

interface ComparePanelProps {
  turn: CompareChatTurn;
}

interface FactListProps {
  title: string;
  items: string[];
}

function FactList({ title, items }: FactListProps) {
  if (items.length === 0) {
    return null;
  }

  return (
    <div>
      <p className="text-xs font-medium text-muted-foreground">{title}</p>
      <ul className="mt-1.5 space-y-1 text-xs leading-relaxed">
        {items.map((item) => (
          <li key={item} className="pl-3 -indent-3">
            <span className="text-muted-foreground">· </span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function productLabel(
  products: { id: string; name: string }[],
  productId: string,
) {
  return products.find((product) => product.id === productId)?.name ?? productId;
}

function CompareColumn({
  column,
  name,
}: {
  column: CompareColumnState;
  name: string;
}) {
  const { t } = useTranslation("assistant");
  const isGrounded =
    column.response != null && isGroundedResponse(column.response.confidence);

  return (
    <section className="flex min-w-0 flex-col gap-3 p-4">
      <h3 className="font-heading text-sm font-medium">{name}</h3>
      {column.status === "error" && column.errorCode ? (
        <AskErrorBanner code={column.errorCode} />
      ) : null}
      {column.response ? (
        <>
          {column.response.answer.trim() ? (
            <AnswerMarkdown content={column.response.answer} />
          ) : (
            <p className="text-sm text-muted-foreground">
              {t("compare.no_answer")}
            </p>
          )}
          <FactList
            title={t("answered.conditions")}
            items={[
              ...column.response.important_conditions,
              ...column.response.exclusions,
            ]}
          />
          <SourceBadges source={column.response.source} />
          {!isGrounded && !column.response.answer.trim() ? (
            <p className="text-xs text-muted-foreground">
              {t("unavailable.body")}
            </p>
          ) : null}
        </>
      ) : null}
    </section>
  );
}

export function ComparePending() {
  return (
    <div className="grid overflow-hidden rounded-2xl bg-card ring-1 ring-border sm:grid-cols-2">
      {[0, 1].map((index) => (
        <div
          key={index}
          className="space-y-3 border-border p-4 sm:border-r sm:last:border-r-0"
        >
          <Skeleton className="h-4 w-28" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-2/3" />
        </div>
      ))}
    </div>
  );
}

export function ComparePanel({ turn }: ComparePanelProps) {
  const { t } = useTranslation("assistant");
  const { data: products = [] } = useProducts();
  const showFollowUp =
    (turn.left.response != null &&
      isGroundedResponse(turn.left.response.confidence)) ||
    (turn.right.response != null &&
      isGroundedResponse(turn.right.response.confidence));

  return (
    <div className="space-y-3">
      <p className="text-xs text-muted-foreground">{t("compare.result_hint")}</p>
      <div className="grid overflow-hidden rounded-2xl bg-card ring-1 ring-border sm:grid-cols-2">
        <div className="border-b border-border sm:border-r sm:border-b-0">
          <CompareColumn
            column={turn.left}
            name={productLabel(products, turn.left.productId)}
          />
        </div>
        <CompareColumn
          column={turn.right}
          name={productLabel(products, turn.right.productId)}
        />
      </div>
      {showFollowUp ? (
        <div className="flex justify-start">
          <FollowUpButton />
        </div>
      ) : null}
    </div>
  );
}
