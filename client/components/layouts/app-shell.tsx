import { AppHeader } from "@/components/core/app-header";

import type { ReactNode } from "react";

interface AppShellProps {
  children: ReactNode;
  historyAction?: ReactNode;
}

export function AppShell({ children, historyAction }: AppShellProps) {
  return (
    <div className="flex h-svh flex-col overflow-hidden bg-background">
      <AppHeader historyAction={historyAction} />
      <main className="bg-seigaiha flex min-h-0 flex-1 flex-col">{children}</main>
    </div>
  );
}
