import type { AskResponse } from "@/features/assistant/types/ask.types";

export type AskViewState =
  | "idle"
  | "loading"
  | "pending"
  | "answered"
  | "unavailable";

export type AskOutcome = "answered" | "unavailable";

export interface AskHistoryItem {
  id: string;
  question: string;
  productIds: string[];
  outcome: AskOutcome;
  response: AskResponse | null;
}

export interface AskScreenResult {
  question: string;
  productIds: string[];
  outcome: AskOutcome;
  response: AskResponse | null;
}
