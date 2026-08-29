"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowUp, LoaderCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ProductPicker } from "@/features/assistant/components/product-picker";
import { SuggestedQuestions } from "@/features/assistant/components/suggested-questions";
import { askRequestSchema } from "@/features/assistant/schemas/ask.schema";
import { useProducts } from "@/shared/queries/products.query";

import type { AskRequest } from "@/features/assistant/types/ask.types";

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
  const { data: products = [] } = useProducts();
  const form = useForm<AskRequest>({
    resolver: zodResolver(askRequestSchema),
    defaultValues: {
      question: "",
      product_id: "",
    },
  });

  const productId = form.watch("product_id");
  const questionField = form.register("question");
  const canSubmit = !isPending && Boolean(productId);

  useEffect(() => {
    if (productId || products.length === 0) {
      return;
    }

    form.setValue("product_id", products[0].id, { shouldValidate: true });
  }, [form, productId, products]);

  function submitAsk(values: AskRequest) {
    onSubmitAsk(values);
    form.reset({
      question: "",
      product_id: values.product_id,
    });
  }

  return (
    <form
      className="space-y-4"
      aria-busy={isPending}
      onSubmit={form.handleSubmit(submitAsk)}
    >
      <div className="rounded-2xl bg-card p-3 ring-1 ring-border">
        <Textarea
          rows={3}
          enterKeyHint="send"
          placeholder={t("ask.placeholder")}
          className="min-h-20 resize-none border-0 bg-transparent shadow-none focus-visible:ring-0"
          {...questionField}
          onKeyDown={(event) => {
            if (event.nativeEvent.isComposing || event.keyCode === 229) {
              return;
            }

            if (event.key !== "Enter" || event.shiftKey) {
              return;
            }

            event.preventDefault();

            if (!canSubmit) {
              return;
            }

            void form.handleSubmit(submitAsk)();
          }}
        />
        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <ProductPicker
            value={productId}
            disabled={isPending}
            onChange={(nextId) => {
              form.setValue("product_id", nextId, { shouldValidate: true });
            }}
          />
          <div className="flex items-center gap-3">
            <p className="hidden text-xs text-muted-foreground sm:block">
              {t("ask.enter_hint")}
            </p>
            <Button type="submit" disabled={!canSubmit}>
              {isPending ? t("ask.pending") : t("ask.submit")}
              {isPending ? (
                <LoaderCircle className="animate-spin" data-icon="inline-end" />
              ) : (
                <ArrowUp data-icon="inline-end" />
              )}
            </Button>
          </div>
        </div>
      </div>
      {showSuggestions ? (
        <SuggestedQuestions
          disabled={isPending || !productId}
          onSelect={(question) => {
            const selectedId = form.getValues("product_id");
            void onSubmitAsk({
              question,
              product_id: selectedId,
            });
            form.reset({
              question: "",
              product_id: selectedId,
            });
          }}
        />
      ) : null}
    </form>
  );
}
