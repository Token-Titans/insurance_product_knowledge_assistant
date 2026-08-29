"use client";

import ReactMarkdown from "react-markdown";

import { cn } from "@/lib/utils";

interface AnswerMarkdownProps {
  content: string;
  className?: string;
}

export function AnswerMarkdown({ content, className }: AnswerMarkdownProps) {
  return (
    <div
      className={cn(
        "font-myanmar text-sm leading-relaxed [&_a]:text-primary [&_a]:underline-offset-4 hover:[&_a]:underline",
        className,
      )}
    >
      <ReactMarkdown
        components={{
          p: ({ children }) => (
            <p className="mb-3 last:mb-0">{children}</p>
          ),
          ul: ({ children }) => (
            <ul className="mb-3 list-disc space-y-1 pl-5 last:mb-0">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="mb-3 list-decimal space-y-1 pl-5 last:mb-0">
              {children}
            </ol>
          ),
          li: ({ children }) => <li className="leading-relaxed">{children}</li>,
          strong: ({ children }) => (
            <strong className="font-semibold">{children}</strong>
          ),
          h1: ({ children }) => (
            <h2 className="mb-2 font-heading text-base font-medium">{children}</h2>
          ),
          h2: ({ children }) => (
            <h3 className="mb-2 font-heading text-sm font-medium">{children}</h3>
          ),
          h3: ({ children }) => (
            <h4 className="mb-2 font-heading text-sm font-medium">{children}</h4>
          ),
          blockquote: ({ children }) => (
            <blockquote className="mb-3 border-l-2 border-border pl-3 text-muted-foreground last:mb-0">
              {children}
            </blockquote>
          ),
          code: ({ children }) => (
            <code className="rounded-md bg-muted px-1 py-0.5 font-mono text-xs">
              {children}
            </code>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
