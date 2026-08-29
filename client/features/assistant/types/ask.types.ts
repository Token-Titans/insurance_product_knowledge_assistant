import type { z } from "zod";

import type {
  askRequestSchema,
  askResponseSchema,
  askSourceSchema,
  compareRequestSchema,
  compareResponseSchema,
} from "@/features/assistant/schemas/ask.schema";

export type AskRequest = z.infer<typeof askRequestSchema>;
export type AskResponse = z.infer<typeof askResponseSchema>;
export type AskSource = z.infer<typeof askSourceSchema>;
export type CompareRequest = z.infer<typeof compareRequestSchema>;
export type CompareResponse = z.infer<typeof compareResponseSchema>;
