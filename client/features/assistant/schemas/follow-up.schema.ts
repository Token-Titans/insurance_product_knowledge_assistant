import { z } from "zod";

export function localTodayIso(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);

export const followUpRequestSchema = z.object({
  customer_name: z.string().trim().min(1).max(120),
  product_id: z.string().trim().min(1).max(64),
  follow_up_date: isoDate.refine((value) => value >= localTodayIso()),
  note: z.string().trim().min(1).max(2000),
});

export const followUpResponseSchema = z.object({
  status: z.literal("scheduled"),
  customer_name: z.string(),
  product: z.string(),
  follow_up_date: isoDate,
});

interface FollowUpFormMessages {
  customerName: string;
  followUpDate: string;
  note: string;
}

export function createFollowUpFormSchema(messages: FollowUpFormMessages) {
  return z.object({
    customer_name: z
      .string()
      .trim()
      .min(1, messages.customerName)
      .max(120, messages.customerName),
    product_id: z.string().trim().min(1).max(64),
    follow_up_date: z
      .string()
      .regex(/^\d{4}-\d{2}-\d{2}$/, messages.followUpDate)
      .refine((value) => value >= localTodayIso(), {
        message: messages.followUpDate,
      }),
    note: z
      .string()
      .trim()
      .min(1, messages.note)
      .max(2000, messages.note),
  });
}
