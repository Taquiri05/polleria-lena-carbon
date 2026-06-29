import { cn } from "@/lib/utils";

export function Spinner({ className, size = "md" }) {
  const sizes = { sm: "h-4 w-4", md: "h-6 w-6", lg: "h-8 w-8" };
  return (
    <div
      className={cn(
        "animate-spin rounded-full border-2 border-brand-orange border-t-transparent",
        sizes[size],
        className
      )}
    />
  );
}

export function LoadingPage({ message = "Cargando..." }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[40vh] gap-4">
      <Spinner size="lg" />
      <p className="text-gray-600">{message}</p>
    </div>
  );
}

export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      {Icon && <Icon className="h-12 w-12 text-brand-orange mb-4" />}
      <h3 className="text-lg font-semibold text-brand-brick">{title}</h3>
      {description && <p className="text-gray-600 mt-2 max-w-md">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

export function Alert({ variant = "error", children }) {
  const styles = {
    error: "bg-red-50 border-red-200 text-red-800",
    success: "bg-green-50 border-green-200 text-green-800",
    info: "bg-blue-50 border-blue-200 text-blue-800",
  };
  return (
    <div className={`rounded-lg border p-4 text-sm ${styles[variant]}`}>
      {children}
    </div>
  );
}
