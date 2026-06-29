import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Input = forwardRef(({ className, error, ...props }, ref) => (
  <input
    ref={ref}
    className={cn(
      "flex h-10 w-full rounded-lg border border-orange-200 bg-white px-3 py-2 text-sm",
      "placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-transparent",
      "disabled:cursor-not-allowed disabled:opacity-50",
      error && "border-red-500 focus:ring-red-500",
      className
    )}
    {...props}
  />
));
Input.displayName = "Input";

export const Textarea = forwardRef(({ className, error, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn(
      "flex min-h-[80px] w-full rounded-lg border border-orange-200 bg-white px-3 py-2 text-sm",
      "placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-transparent",
      "disabled:cursor-not-allowed disabled:opacity-50 resize-none",
      error && "border-red-500 focus:ring-red-500",
      className
    )}
    {...props}
  />
));
Textarea.displayName = "Textarea";
