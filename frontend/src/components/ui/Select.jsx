import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Select = forwardRef(({ className, error, children, ...props }, ref) => (
  <select
    ref={ref}
    className={cn(
      "flex h-10 w-full rounded-lg border border-orange-200 bg-white px-3 py-2 text-sm",
      "focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-transparent",
      "disabled:cursor-not-allowed disabled:opacity-50",
      error && "border-red-500 focus:ring-red-500",
      className
    )}
    {...props}
  >
    {children}
  </select>
));
Select.displayName = "Select";
