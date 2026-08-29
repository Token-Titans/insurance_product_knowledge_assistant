import type { z } from "zod";

import type { productSummarySchema } from "@/features/products/schemas/product.schema";

export type ProductSummary = z.infer<typeof productSummarySchema>;
