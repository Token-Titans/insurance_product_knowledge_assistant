"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowUp, Columns2, LoaderCircle } from "lucide-react";
import { useForm, useWatch } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { ProductPicker } from "@/features/assistant/components/product-picker";
import { SuggestedQuestions } from "@/features/assistant/components/suggested-questions";
import { cn } from "@/lib/utils";
import { useProducts } from "@/shared/queries/products.query";

import type {
  AskRequest,
  CompareRequest,
} from "@/features/assistant/types/ask.types";

const composerSchema = z.object({
  question: z.string().max(2000),
  product_id: z.string().trim().min(1).max(64),
  compare_product_id: z.string(),
});

interface ComposerValues {
  question: string;
  product_id: string;
  compare_product_id: string;
}

interface AskComposerProps {
  isPending: boolean;
  isCompare: boolean;
  showSuggestions: boolean;
  onCompareChange: (value: boolean) => void;
  onSubmitAsk: (request: AskRequest) => void;
  onSubmitCompare: (request: CompareRequest) => void;
}

function otherProductId(productIds: string[], currentId: string) {
  return productIds.find((id) => id !== currentId) ?? "";
}

export function AskComposer({
  isPending,
  isCompare,
  showSuggestions,
  onCompareChange,
  onSubmitAsk,
  onSubmitCompare,
}: AskComposerProps) {
  const { t } = useTranslation("assistant");
  const { data: products = [] } = useProducts();
  const form = useForm<ComposerValues>({
    resolver: zodResolver(composerSchema),
    defaultValues: {
      question: "",
      product_id: "",
      compare_product_id: "",
    },
  });

  const productId = useWatch({
    control: form.control,
    name: "product_id",
    defaultValue: "",
  });
  const compareProductId = useWatch({
    control: form.control,
    name: "compare_product_id",
    defaultValue: "",
  });
  const questionValue = useWatch({
    control: form.control,
    name: "question",
    defaultValue: "",
  });
  const questionField = form.register("question");
  const canCompare = products.length >= 2;
  const hasDistinctProducts =
    Boolean(productId) &&
    Boolean(compareProductId) &&
    productId !== compareProductId;
  const hasQuestion = questionValue.trim().length > 0;
  const canSubmit =
    !isPending &&
    Boolean(productId) &&
    (isCompare ? hasDistinctProducts : hasQuestion);

  useEffect(() => {
    if (productId || products.length === 0) {
      return;
    }

    form.setValue("product_id", products[0].id, { shouldValidate: true });
  }, [form, productId, products]);

  useEffect(() => {
    if (products.length < 2) {
      return;
    }

    if (compareProductId && compareProductId !== productId) {
      return;
    }

    const nextId = products.find((product) => product.id !== productId)?.id;

    if (nextId) {
      form.setValue("compare_product_id", nextId, { shouldValidate: true });
    }
  }, [compareProductId, form, productId, products]);

  function submitComposer(values: ComposerValues) {
    if (isCompare) {
      if (!hasDistinctProducts) {
        return;
      }

      onSubmitCompare({
        question: values.question.trim() || t("compare.default_question"),
        left_product_id: values.product_id,
        right_product_id: values.compare_product_id,
      });
    } else {
      const question = values.question.trim();

      if (!question) {
        return;
      }

      onSubmitAsk({
        question,
        product_id: values.product_id,
      });
    }

    form.reset({
      question: "",
      product_id: values.product_id,
      compare_product_id: values.compare_product_id,
    });
  }

  function submitSuggestion(question: string) {
    const selectedId = form.getValues("product_id");
    const selectedCompareId = form.getValues("compare_product_id");

    if (isCompare) {
      onSubmitCompare({
        question,
        left_product_id: selectedId,
        right_product_id: selectedCompareId,
      });
    } else {
      onSubmitAsk({
        question,
        product_id: selectedId,
      });
    }

    form.reset({
      question: "",
      product_id: selectedId,
      compare_product_id: selectedCompareId,
    });
  }

  return (
    <form
      className="space-y-4"
      aria-busy={isPending}
      onSubmit={form.handleSubmit(submitComposer)}
    >
      <div
        className={cn(
          "rounded-2xl bg-card p-3 ring-1",
          isCompare ? "ring-2 ring-primary" : "ring-border",
        )}
      >
        {canCompare ? (
          <div
            className={cn(
              "mb-3 flex items-center justify-between gap-3 rounded-xl px-3 py-2",
              isCompare ? "bg-primary text-primary-foreground" : "bg-muted",
            )}
          >
            <div className="flex min-w-0 items-center gap-2">
              <Columns2 className="size-4 shrink-0" />
              <p className="truncate text-sm font-medium">
                {isCompare ? t("compare.active_banner") : t("compare.toggle")}
              </p>
            </div>
            <Switch
              size="sm"
              checked={isCompare}
              disabled={isPending}
              aria-label={t("compare.toggle")}
              className={
                isCompare
                  ? "border-primary-foreground/30 data-checked:bg-primary-foreground/30"
                  : undefined
              }
              onCheckedChange={onCompareChange}
            />
          </div>
        ) : null}
        <Textarea
          rows={3}
          enterKeyHint="send"
          placeholder={
            isCompare ? t("compare.placeholder") : t("ask.placeholder")
          }
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

            void form.handleSubmit(submitComposer)();
          }}
        />
        <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
          <div className="flex min-w-0 flex-wrap items-center gap-2">
            {isCompare ? (
              <>
                <ProductPicker
                  id="compare-left"
                  hideLabel
                  value={productId}
                  disabled={isPending}
                  onChange={(nextId) => {
                    form.setValue("product_id", nextId, {
                      shouldValidate: true,
                    });

                    if (nextId === form.getValues("compare_product_id")) {
                      form.setValue(
                        "compare_product_id",
                        otherProductId(
                          products.map((product) => product.id),
                          nextId,
                        ),
                        { shouldValidate: true },
                      );
                    }
                  }}
                />
                <span className="text-xs font-medium text-muted-foreground">
                  {t("compare.versus")}
                </span>
                <ProductPicker
                  id="compare-right"
                  hideLabel
                  value={compareProductId}
                  disabled={isPending}
                  onChange={(nextId) => {
                    form.setValue("compare_product_id", nextId, {
                      shouldValidate: true,
                    });

                    if (nextId === form.getValues("product_id")) {
                      form.setValue(
                        "product_id",
                        otherProductId(
                          products.map((product) => product.id),
                          nextId,
                        ),
                        { shouldValidate: true },
                      );
                    }
                  }}
                />
              </>
            ) : (
              <ProductPicker
                value={productId}
                disabled={isPending}
                onChange={(nextId) => {
                  form.setValue("product_id", nextId, { shouldValidate: true });
                }}
              />
            )}
          </div>
          <div className="flex items-center gap-3">
            <p className="hidden text-xs text-muted-foreground sm:block">
              {isCompare ? t("compare.enter_hint") : t("ask.enter_hint")}
            </p>
            <Button type="submit" disabled={!canSubmit}>
              {isPending
                ? isCompare
                  ? t("compare.pending")
                  : t("ask.pending")
                : isCompare
                  ? t("compare.submit")
                  : t("ask.submit")}
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
          disabled={
            isPending || !productId || (isCompare && !hasDistinctProducts)
          }
          onSelect={submitSuggestion}
        />
      ) : null}
    </form>
  );
}
