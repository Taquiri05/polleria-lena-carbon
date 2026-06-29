import { cn } from "@/lib/utils";

export function FiltroCategorias({ categorias, activa, onChange }) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onChange(null)}
        className={cn(
          "px-4 py-2 rounded-full text-sm font-medium transition-colors",
          activa === null
            ? "bg-brand-brick text-white"
            : "bg-white text-gray-600 border border-orange-200 hover:border-brand-orange"
        )}
      >
        Todas
      </button>
      {categorias.map((cat) => (
        <button
          key={cat.id}
          onClick={() => onChange(cat.id)}
          className={cn(
            "px-4 py-2 rounded-full text-sm font-medium transition-colors",
            activa === cat.id
              ? "bg-brand-brick text-white"
              : "bg-white text-gray-600 border border-orange-200 hover:border-brand-orange"
          )}
        >
          {cat.nombre}
        </button>
      ))}
    </div>
  );
}
