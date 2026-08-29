"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

import type { ReactNode } from "react";

interface HeaderNavLinkProps {
  href: string;
  children: ReactNode;
}

export function HeaderNavLink({ href, children }: HeaderNavLinkProps) {
  const pathname = usePathname();
  const isActive = href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <Link
      href={href}
      aria-current={isActive ? "page" : undefined}
      className={cn(
        "relative inline-flex h-9 items-center px-3 text-sm font-medium transition-colors",
        isActive
          ? "text-primary-foreground"
          : "text-primary-foreground/70 hover:text-primary-foreground",
      )}
    >
      {children}
      <span
        aria-hidden
        className={cn(
          "absolute inset-x-2 bottom-0 h-0.5 rounded-full bg-horizon transition-opacity",
          isActive ? "opacity-100" : "opacity-0",
        )}
      />
    </Link>
  );
}
