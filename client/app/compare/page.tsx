import type { Metadata } from "next"

import { CompareShell } from "@/features/assistant/components/compare-shell"

export const metadata: Metadata = {
  title: "Compare",
  description: "Product comparison shell",
}

export default function ComparePage() {
  return <CompareShell />
}
