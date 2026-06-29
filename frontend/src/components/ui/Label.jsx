import { cn } from "@/lib/utils";

export function Label({ className, children, required, ...props }) {
  return (
    <label
      className={cn("text-sm font-medium text-gray-700 mb-1 block", className)}
      {...props}
    >
      {children}
      {required && <span className="text-red-500 ml-1">*</span>}
    </label>
  );
}

export function FormError({ message }) {
  if (!message) return null;
  return <p className="text-sm text-red-600 mt-1">{message}</p>;
}

export function FormField({ label, error, required, children }) {
  return (
    <div className="space-y-1">
      {label && <Label required={required}>{label}</Label>}
      {children}
      <FormError message={error} />
    </div>
  );
}
