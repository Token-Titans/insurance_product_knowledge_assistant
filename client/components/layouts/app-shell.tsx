import { AppHeader } from "@/components/core/app-header";

import type { ReactNode } from "react";

interface AppShellProps {
  children: ReactNode;
  historyAction?: ReactNode;
}

export function AppShell({ children, historyAction }: AppShellProps) {
  return (
    <div className="flex min-h-svh flex-col bg-background">
      <AppHeader historyAction={historyAction} />
      <main className="bg-seigaiha flex flex-1 flex-col">{children}</main>
    </div>
  );
}
