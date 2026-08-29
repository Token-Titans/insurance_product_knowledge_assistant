"use client";

import { useState } from "react";
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

import type { ChatTurn } from "@/features/assistant/types/ask-screen.types";

interface ConversationHistoryProps {
  items: ChatTurn[];
  onSelect: (id: string) => void;
}

function historyBadgeKey(status: ChatTurn["status"]) {
  if (status === "answered") {
    return "history.grounded";
  }

  if (status === "unavailable") {
    return "history.unavailable";
  }

  return "history.error";
}

export function ConversationHistory({
  items,
  onSelect,
}: ConversationHistoryProps) {
  const { t } = useTranslation("assistant");
  const { t: tCommon } = useTranslation("common");
  const [isOpen, setIsOpen] = useState(false);
  const visibleItems = [...items]
    .filter((item) => item.status !== "pending")
    .reverse();

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button
          type="button"
          size="sm"
          variant="ghost"
          className="text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
        >
          <History />
          <span className="hidden sm:inline">{tCommon("app.history")}</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>{t("history.title")}</SheetTitle>
          <SheetDescription>{tCommon("app.tagline")}</SheetDescription>
        </SheetHeader>
        <div className="flex flex-1 flex-col gap-2 overflow-y-auto px-4 pb-6">
          {visibleItems.length === 0 ? (
            <p className="text-sm text-muted-foreground">{t("history.empty")}</p>
          ) : (
            visibleItems.map((item) => (
              <button
                key={item.id}
                type="button"
                className="rounded-xl bg-secondary p-3 text-left"
                onClick={() => {
                  onSelect(item.id);
                  setIsOpen(false);
                }}
              >
                <p className="font-myanmar text-sm">{item.question}</p>
                <Badge className="mt-2" variant="outline">
                  {t(historyBadgeKey(item.status))}
                </Badge>
              </button>
            ))
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}
