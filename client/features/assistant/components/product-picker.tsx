"use client";

import { useState } from "react";
import { Check, ChevronsUpDown, Search } from "lucide-react";
import { Popover as PopoverPrimitive } from "radix-ui";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useProducts } from "@/shared/queries/products.query";

interface ProductPickerProps {
  value: string;
  disabled?: boolean;
  onChange: (productId: string) => void;
}

export function ProductPicker({
  value,
  disabled = false,
  onChange,
}: ProductPickerProps) {
  const { t } = useTranslation("assistant");
  const { data: products = [] } = useProducts();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const selected = products.find((product) => product.id === value);
  const needle = query.trim().toLowerCase();
  const filtered = needle
    ? products.filter((product) => {
        const category = product.category ?? "";

        return (
          product.name.toLowerCase().includes(needle) ||
          category.toLowerCase().includes(needle)
        );
      })
    : products;

  return (
    <div className="flex min-w-0 items-center gap-2">
      <span className="shrink-0 text-xs text-muted-foreground" id="product-picker-label">
        {t("ask.products_label")}
      </span>
      <PopoverPrimitive.Root
        open={open}
        onOpenChange={(nextOpen) => {
          setOpen(nextOpen);

          if (!nextOpen) {
            setQuery("");
          }
        }}
      >
        <PopoverPrimitive.Trigger asChild>
          <Button
            type="button"
            variant="outline"
            disabled={disabled || products.length === 0}
            aria-labelledby="product-picker-label"
            className="h-8 max-w-56 justify-between gap-2 rounded-full px-3 font-normal"
          >
            <span className="truncate">
              {selected?.name ?? t("ask.products_placeholder")}
            </span>
            <ChevronsUpDown className="size-3.5 shrink-0 opacity-60" />
          </Button>
        </PopoverPrimitive.Trigger>
        <PopoverPrimitive.Portal>
          <PopoverPrimitive.Content
            side="top"
            align="start"
            sideOffset={8}
            className="z-50 w-72 rounded-2xl bg-popover p-2 text-popover-foreground shadow-md ring-1 ring-border"
          >
            <div className="relative">
              <Search className="pointer-events-none absolute top-1/2 left-3 size-3.5 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={query}
                placeholder={t("ask.products_search")}
                className="h-8 rounded-full pl-8"
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
            <ul className="mt-2 max-h-56 overflow-y-auto">
              {filtered.length === 0 ? (
                <li className="px-2 py-3 text-sm text-muted-foreground">
                  {t("ask.products_empty")}
                </li>
              ) : (
                filtered.map((product) => {
                  const isSelected = product.id === value;

                  return (
                    <li key={product.id}>
                      <button
                        type="button"
                        className={cn(
                          "flex w-full items-center gap-2 rounded-xl px-2 py-2 text-left text-sm hover:bg-muted",
                          isSelected && "bg-muted",
                        )}
                        onClick={() => {
                          onChange(product.id);
                          setOpen(false);
                          setQuery("");
                        }}
                      >
                        <Check
                          className={cn(
                            "size-3.5 shrink-0",
                            isSelected ? "opacity-100" : "opacity-0",
                          )}
                        />
                        <span className="min-w-0 flex-1">
                          <span className="block truncate font-medium">
                            {product.name}
                          </span>
                          {product.category ? (
                            <span className="block truncate text-xs text-muted-foreground">
                              {product.category}
                            </span>
                          ) : null}
                        </span>
                      </button>
                    </li>
                  );
                })
              )}
            </ul>
          </PopoverPrimitive.Content>
        </PopoverPrimitive.Portal>
      </PopoverPrimitive.Root>
    </div>
  );
}
