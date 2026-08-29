"use client";

import { AnswerPanel } from "@/features/assistant/components/answer-panel";
import { AskErrorBanner } from "@/features/assistant/components/ask-error-banner";
import {
  ComparePanel,
  ComparePending,
} from "@/features/assistant/components/compare-panel";
import { RetrieveLoading } from "@/features/assistant/components/retrieve-loading";
import { useProducts } from "@/shared/queries/products.query";

import type { ChatTurn } from "@/features/assistant/types/ask-screen.types";

interface ChatTurnItemProps {
  turn: ChatTurn;
}

function productLabel(
  products: { id: string; name: string }[],
  productId: string,
) {
  return products.find((product) => product.id === productId)?.name ?? productId;
}

export function ChatTurnItem({ turn }: ChatTurnItemProps) {
  const { data: products = [] } = useProducts();
  const compareCaption =
    turn.kind === "compare"
      ? `${productLabel(products, turn.left.productId)} · ${productLabel(products, turn.right.productId)}`
      : null;

  return (
    <article id={`ask-turn-${turn.id}`} className="space-y-3">
      <div className="flex justify-end">
        <div className="max-w-md space-y-1">
          {compareCaption ? (
            <p className="text-right text-xs text-muted-foreground">
              {compareCaption}
            </p>
          ) : null}
          <p className="rounded-2xl bg-primary px-4 py-2 font-myanmar text-sm text-primary-foreground">
            {turn.question}
          </p>
        </div>
      </div>
      {turn.kind === "compare" && turn.status === "pending" ? (
        <ComparePending />
      ) : null}
      {turn.kind === "ask" && turn.status === "pending" ? (
        <RetrieveLoading />
      ) : null}
      {turn.kind === "ask" && turn.status === "error" && turn.errorCode ? (
        <AskErrorBanner code={turn.errorCode} />
      ) : null}
      {turn.kind === "ask" &&
      (turn.status === "answered" || turn.status === "unavailable") &&
      turn.response ? (
        <AnswerPanel
          response={turn.response}
          productId={turn.productId}
          animate={turn.shouldType}
          turnId={turn.id}
        />
      ) : null}
      {turn.kind === "compare" && turn.status !== "pending" ? (
        <ComparePanel turn={turn} />
      ) : null}
    </article>
  );
}
