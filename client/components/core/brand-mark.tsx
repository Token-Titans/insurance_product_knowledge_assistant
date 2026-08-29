interface BrandMarkProps {
  className?: string;
}

export function BrandMark({ className }: BrandMarkProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      className={className}
      aria-hidden
    >
      <path d="M5 27 16 5l11 22H5Z" className="fill-horizon" />
      <path d="M16 5 27 27H16V5Z" className="fill-primary-foreground/35" />
    </svg>
  );
}
