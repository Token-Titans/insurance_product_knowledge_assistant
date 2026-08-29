import { z } from "zod";

export const askRequestSchema = z.object({
  question: z.string().trim().min(1).max(2000),
  product_id: z.string().trim().min(1).max(64),
});

export const askSourceSchema = z.object({
  document: z.string(),
  section: z.string(),
});

const apiSourceSchema = z.object({
  document: z.string().default(""),
  file: z.string().optional().default(""),
  section: z.string().default(""),
  page: z.number().nullable().optional(),
});

export const askResponseSchema = z
  .object({
    answer: z.string(),
    important_conditions: z.array(z.string()).default([]),
    exclusions: z.array(z.string()).default([]),
    source: apiSourceSchema,
    confidence: z.number().min(0).max(1),
  })
  .transform((data) => ({
    answer: data.answer,
    important_points: data.important_conditions,
    conditions: data.exclusions,
    sources:
      data.source.document || data.source.section
        ? [{ document: data.source.document, section: data.source.section }]
        : [],
    confidence: (data.confidence > 0 ? "grounded" : "unavailable") as
      | "grounded"
      | "unavailable",
  }));
