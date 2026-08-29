import { z } from "zod";

export const productSummarySchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  category: z.string().nullable().optional(),
});

export const productListSchema = z.array(productSummarySchema);
