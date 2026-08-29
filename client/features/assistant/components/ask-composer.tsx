"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowUp, LoaderCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ProductPicker } from "@/features/assistant/components/product-picker";
import { SuggestedQuestions } from "@/features/assistant/components/suggested-questions";
import { askRequestSchema } from "@/features/assistant/schemas/ask.schema";

import type { AskRequest } from "@/features/assistant/types/ask.types";

type ProductId = NonNullable<AskRequest["product_ids"]>[number];

interface AskComposerProps {
  isPending: boolean;
  showSuggestions: boolean;
  onSubmitAsk: (request: AskRequest) => void;
}

export function AskComposer({
  isPending,
  showSuggestions,
  onSubmitAsk,
}: AskComposerProps) {
  const { t } = useTranslation("assistant");
  const form = useForm<AskRequest>({
    resolver: zodResolver(askRequestSchema),
    defaultValues: {
      question: "",
      product_ids: ["product-a"],
    },
  });

  const selectedIds = form.watch("product_ids") ?? [];

  function toggleProduct(productId: string) {
    if (productId !== "product-a" && productId !== "product-b") {
      return;
    }

    const current = form.getValues("product_ids") ?? [];
    const next: ProductId[] = current.includes(productId)
      ? current.filter((id) => id !== productId)
      : [...current, productId];

    form.setValue("product_ids", next, { shouldValidate: true });
  }

  return (
    <form
      className="space-y-4"
      aria-busy={isPending}
      onSubmit={form.handleSubmit((values) => onSubmitAsk(values))}
    >
      {showSuggestions ? (
        <SuggestedQuestions
          disabled={isPending}
          onSelect={(question) => {
            form.setValue("question", question, { shouldValidate: true });
            void onSubmitAsk({
              question,
              product_ids: form.getValues("product_ids"),
            });
          }}
        />
      ) : null}
      <div className="rounded-2xl bg-card p-3 ring-1 ring-border">
        <Textarea
          rows={3}
          disabled={isPending}
          placeholder={t("ask.placeholder")}
          className="min-h-20 resize-none border-0 bg-transparent shadow-none focus-visible:ring-0"
          {...form.register("question")}
        />
        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <ProductPicker
            selectedIds={selectedIds}
            disabled={isPending}
            onToggle={toggleProduct}
          />
          <Button type="submit" disabled={isPending}>
            {isPending ? t("ask.pending") : t("ask.submit")}
            {isPending ? (
              <LoaderCircle className="animate-spin" data-icon="inline-end" />
            ) : (
              <ArrowUp data-icon="inline-end" />
            )}
          </Button>
        </div>
      </div>
    </form>
  );
}
