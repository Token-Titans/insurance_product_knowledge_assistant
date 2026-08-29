import { z } from "zod";

export const askRequestSchema = z.object({
  question: z.string().trim().min(1).max(2000),
  product_id: z.string().trim().min(1).max(64),
});

export const compareRequestSchema = z
  .object({
    question: z.string().trim().min(1).max(2000),
    left_product_id: z.string().trim().min(1).max(64),
    right_product_id: z.string().trim().min(1).max(64),
  })
  .refine((value) => value.left_product_id !== value.right_product_id);

export const askSourceSchema = z.object({
  document: z.string(),
  file: z.string(),
  section: z.string(),
  page: z.number().int().nullable().optional(),
});

export const askResponseSchema = z.object({
  answer: z.string(),
  important_conditions: z.array(z.string()),
  exclusions: z.array(z.string()),
  source: askSourceSchema,
  confidence: z.number().min(0).max(1),
});

export function isGroundedResponse(confidence: number) {
  return confidence > 0;
}