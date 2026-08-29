"use client";

import { useState } from "react";
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

export function FollowUpButton() {
  const { t } = useTranslation("assistant");
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button type="button" variant="outline" onClick={() => setIsOpen(true)}>
        {t("answered.follow_up")}
      </Button>
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("answered.follow_up_title")}</DialogTitle>
            <DialogDescription>{t("answered.follow_up_body")}</DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button type="button" onClick={() => setIsOpen(false)}>
              {t("answered.follow_up_close")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
