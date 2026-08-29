import { productListSchema } from "@/features/products/schemas/product.schema";
import { api } from "@/shared/lib/api";

import type { ProductSummary } from "@/features/products/types/product.types";

export async function listProducts(): Promise<ProductSummary[]> {
  const response = await api.get<unknown>("/products");

  return productListSchema.parse(response.data);
}
