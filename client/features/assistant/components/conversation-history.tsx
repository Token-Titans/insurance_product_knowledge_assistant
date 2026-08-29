"use client";

import { History } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

import type { AskHistoryItem } from "@/features/assistant/types/ask-screen.types";

interface ConversationHistoryProps {
  items: AskHistoryItem[];
  onSelect: (item: AskHistoryItem) => void;
}

export function ConversationHistory({
  items,
  onSelect,
}: ConversationHistoryProps) {
  const { t } = useTranslation("assistant");
  const { t: tCommon } = useTranslation("common");

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          type="button"
          size="sm"
          variant="secondary"
          className="bg-primary-foreground/10 text-primary-foreground hover:bg-primary-foreground/20"
        >
          <History />
          {tCommon("app.history")}
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>{t("history.title")}</SheetTitle>
          <SheetDescription>{tCommon("app.tagline")}</SheetDescription>
        </SheetHeader>
        <div className="flex flex-1 flex-col gap-2 overflow-y-auto px-4 pb-6">
          {items.length === 0 ? (
            <p className="text-sm text-muted-foreground">{t("history.empty")}</p>
          ) : (
            items.map((item) => (
              <button
                key={item.id}
                type="button"
                className="rounded-xl bg-secondary p-3 text-left"
                onClick={() => onSelect(item)}
              >
                <p className="font-myanmar text-sm">{item.question}</p>
                <Badge className="mt-2" variant="outline">
                  {item.outcome === "answered"
                    ? t("history.grounded")
                    : t("history.unavailable")}
                </Badge>
              </button>
            ))
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}
