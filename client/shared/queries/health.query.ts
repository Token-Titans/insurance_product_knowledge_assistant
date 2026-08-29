"use client";

import { useQuery } from "@tanstack/react-query";

import { getHealth } from "@/shared/services/health.service";

export const healthKeys = {
  all: ["health"] as const,
  status: () => [...healthKeys.all, "status"] as const,
};

export function useHealth() {
  return useQuery({
    queryKey: healthKeys.status(),
    queryFn: getHealth,
    staleTime: 30_000,
  });
}
