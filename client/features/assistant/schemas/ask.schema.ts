import { z } from "zod";

export const supportedProductIdSchema = z.enum(["product-a", "product-b"]);

export const askRequestSchema = z.object({
  question: z.string().trim().min(1).max(2000),
  product_ids: z.array(supportedProductIdSchema).optional(),
});

export const askSourceSchema = z.object({
  document: z.string(),
  section: z.string(),
});

export const askResponseSchema = z.object({
  answer: z.string(),
  important_points: z.array(z.string()),
  conditions: z.array(z.string()),
  sources: z.array(askSourceSchema),
  confidence: z.enum(["grounded", "unavailable"]),
});
