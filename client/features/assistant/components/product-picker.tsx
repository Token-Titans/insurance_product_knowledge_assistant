"use client";

import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { SUPPORTED_PRODUCTS } from "@/features/assistant/constants/products";

interface ProductPickerProps {
  selectedIds: string[];
  disabled?: boolean;
  onToggle: (productId: string) => void;
}

export function ProductPicker({
  selectedIds,
  disabled = false,
  onToggle,
}: ProductPickerProps) {
  const { t } = useTranslation("assistant");

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-xs text-muted-foreground">
        {t("ask.products_label")}
      </span>
      {SUPPORTED_PRODUCTS.map((product) => {
        const isSelected = selectedIds.includes(product.id);

        return (
          <Button
            key={product.id}
            type="button"
            size="xs"
            disabled={disabled}
            variant={isSelected ? "default" : "outline"}
            onClick={() => onToggle(product.id)}
          >
            {t(product.labelKey)}
          </Button>
        );
      })}
    </div>
  );
}
