import { AppHeader } from "@/components/core/app-header";

import type { ReactNode } from "react";

interface AppShellProps {
  children: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex h-svh flex-col overflow-hidden overscroll-none bg-background">
      <AppHeader />
      <main className="bg-seigaiha flex min-h-0 flex-1 flex-col">{children}</main>
    </div>
  );
}
