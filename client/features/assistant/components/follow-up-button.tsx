"use client";

import { useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarPlus } from "lucide-react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useScheduleFollowUp } from "@/features/assistant/queries/follow-up.query";
import {
  createFollowUpFormSchema,
  localTodayIso,
} from "@/features/assistant/schemas/follow-up.schema";
import { isApiError } from "@/shared/types/api-error";

import type {
  FollowUpRequest,
  FollowUpResponse,
} from "@/features/assistant/types/follow-up.types";

interface FollowUpButtonProps {
  productId: string;
}

function formatFollowUpDate(isoDate: string, language: string) {
  const [year, month, day] = isoDate.split("-").map(Number);
  const locale = language.startsWith("my") ? "my-MM" : "en-GB";

  return new Intl.DateTimeFormat(locale, {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(year, month - 1, day));
}

function followUpErrorCopy(
  error: unknown,
  t: (key: string, options?: { defaultValue: string }) => string,
) {
  if (isApiError(error) && error.code === "INVALID_REQUEST") {
    return t("answered.follow_up_invalid");
  }

  if (isApiError(error) && error.code === "PRODUCT_NOT_FOUND") {
    return t("answered.follow_up_pick_product");
  }

  if (isApiError(error)) {
    return t(`ask.errors.${error.code}`, {
      defaultValue: t("ask.errors.generic"),
    });
  }

  return t("ask.errors.generic");
}

export function FollowUpButton({ productId }: FollowUpButtonProps) {
  const { t, i18n } = useTranslation("assistant");
  const [isOpen, setIsOpen] = useState(false);
  const [success, setSuccess] = useState<FollowUpResponse | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const mutation = useScheduleFollowUp();
  const today = localTodayIso();
  const schema = useMemo(
    () =>
      createFollowUpFormSchema({
        customerName: t("answered.follow_up_customer_name_invalid"),
        followUpDate: t("answered.follow_up_date_invalid"),
        note: t("answered.follow_up_note_invalid"),
      }),
    [t],
  );
  const form = useForm<FollowUpRequest>({
    resolver: zodResolver(schema),
    defaultValues: {
      customer_name: "",
      product_id: productId,
      follow_up_date: today,
      note: "",
    },
  });

  function resetDialog() {
    setSuccess(null);
    setSubmitError(null);
    mutation.reset();
    form.reset({
      customer_name: "",
      product_id: productId,
      follow_up_date: localTodayIso(),
      note: "",
    });
  }

  function handleOpenChange(open: boolean) {
    setIsOpen(open);

    if (open) {
      resetDialog();
      return;
    }

    setSuccess(null);
    setSubmitError(null);
    mutation.reset();
  }

  async function onSubmit(values: FollowUpRequest) {
    setSubmitError(null);

    try {
      const result = await mutation.mutateAsync({
        ...values,
        product_id: productId,
      });
      setSuccess(result);
    } catch (error) {
      if (isApiError(error) && error.code === "INVALID_REQUEST") {
        form.setError("follow_up_date", {
          message: t("answered.follow_up_date_invalid"),
        });
      }

      setSubmitError(followUpErrorCopy(error, t));
    }
  }

  return (
    <>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        className="h-7 shrink-0 px-2 text-xs text-muted-foreground hover:text-foreground sm:ml-auto"
        onClick={() => handleOpenChange(true)}
      >
        <CalendarPlus data-icon="inline-start" />
        {t("answered.follow_up")}
      </Button>
      <Dialog open={isOpen} onOpenChange={handleOpenChange}>
        <DialogContent>
          {success ? (
            <>
              <DialogHeader>
                <DialogTitle>{t("answered.follow_up_title")}</DialogTitle>
                <DialogDescription>
                  {t("answered.follow_up_success", {
                    product: success.product,
                    date: formatFollowUpDate(
                      success.follow_up_date,
                      i18n.language,
                    ),
                  })}
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button type="button" onClick={() => handleOpenChange(false)}>
                  {t("answered.follow_up_close")}
                </Button>
              </DialogFooter>
            </>
          ) : (
            <form
              className="space-y-4"
              onSubmit={form.handleSubmit(onSubmit)}
            >
              <DialogHeader>
                <DialogTitle>{t("answered.follow_up_title")}</DialogTitle>
                <DialogDescription>
                  {t("answered.follow_up_body")}
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-3">
                <div className="space-y-1.5">
                  <Label htmlFor={`follow-up-customer-name-${productId}`}>
                    {t("answered.follow_up_customer_name")}
                  </Label>
                  <Input
                    id={`follow-up-customer-name-${productId}`}
                    autoComplete="name"
                    aria-invalid={Boolean(form.formState.errors.customer_name)}
                    {...form.register("customer_name")}
                  />
                  {form.formState.errors.customer_name ? (
                    <p className="text-xs text-destructive">
                      {form.formState.errors.customer_name.message}
                    </p>
                  ) : null}
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor={`follow-up-date-${productId}`}>
                    {t("answered.follow_up_date")}
                  </Label>
                  <Input
                    id={`follow-up-date-${productId}`}
                    type="date"
                    min={today}
                    aria-invalid={Boolean(form.formState.errors.follow_up_date)}
                    {...form.register("follow_up_date")}
                  />
                  {form.formState.errors.follow_up_date ? (
                    <p className="text-xs text-destructive">
                      {form.formState.errors.follow_up_date.message}
                    </p>
                  ) : null}
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor={`follow-up-note-${productId}`}>
                    {t("answered.follow_up_note")}
                  </Label>
                  <Textarea
                    id={`follow-up-note-${productId}`}
                    rows={3}
                    aria-invalid={Boolean(form.formState.errors.note)}
                    {...form.register("note")}
                  />
                  {form.formState.errors.note ? (
                    <p className="text-xs text-destructive">
                      {form.formState.errors.note.message}
                    </p>
                  ) : null}
                </div>
                {submitError ? (
                  <p role="alert" className="text-sm text-destructive">
                    {submitError}
                  </p>
                ) : null}
              </div>
              <DialogFooter>
                <Button type="submit" disabled={mutation.isPending}>
                  {mutation.isPending
                    ? t("answered.follow_up_pending")
                    : t("answered.follow_up_submit")}
                </Button>
              </DialogFooter>
            </form>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
