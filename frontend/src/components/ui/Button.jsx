import { forwardRef } from "react";
import { cn } from "@/lib/utils";

const variants = {
  default: "bg-brand-brick text-white hover:bg-brand-brick-light",
  outline: "border-2 border-brand-brick text-brand-brick hover:bg-brand-brick hover:text-white",
  orange: "bg-brand-orange text-white hover:bg-brand-orange-light",
  ghost: "hover:bg-brand-cream text-brand-brick",
  destructive: "bg-red-600 text-white hover:bg-red-700",
};

const sizes = {
  sm: "h-8 px-3 text-sm",
  md: "h-10 px-4",
  lg: "h-12 px-6 text-lg",
  icon: "h-10 w-10",
};

export const Button = forwardRef(
  ({ className, variant = "default", size = "md", disabled, children, ...props }, ref) => (
    <button
      ref={ref}
      disabled={disabled}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-orange",
        "disabled:opacity-50 disabled:pointer-events-none",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
);
Button.displayName = "Button";
