"use client";

import { useQuery } from "@tanstack/react-query";

import { FALLBACK_PRODUCTS } from "@/features/products/constants/fallback-products";
import { listProducts } from "@/shared/services/products.service";

export const productKeys = {
  all: ["products"] as const,
  list: () => [...productKeys.all, "list"] as const,
};

export function useProducts() {
  const query = useQuery({
    queryKey: productKeys.list(),
    queryFn: listProducts,
    staleTime: 5 * 60_000,
    retry: 1,
  });

  const products =
    query.data && query.data.length > 0 ? query.data : FALLBACK_PRODUCTS;

  return {
    ...query,
    data: products,
  };
}
