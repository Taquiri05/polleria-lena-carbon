import { Minus, Plus, Trash2 } from "lucide-react";
import { formatearPrecio } from "@/utils/formatters";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";

export function CarritoItem({ item, onUpdate, onRemove }) {
  return (
    <div className="flex items-center gap-3 py-3 border-b border-orange-100 last:border-0">
      <div className="flex-1 min-w-0">
        <p className="font-medium text-brand-brick truncate">{item.nombre}</p>
        <p className="text-sm text-brand-orange">{formatearPrecio(item.precio)}</p>
      </div>
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8"
          onClick={() => onUpdate(item.platillo_id, item.cantidad - 1)}
        >
          <Minus className="h-3 w-3" />
        </Button>
        <span className="w-6 text-center font-medium">{item.cantidad}</span>
        <Button
          variant="outline"
          size="icon"
          className="h-8 w-8"
          onClick={() => onUpdate(item.platillo_id, item.cantidad + 1)}
        >
          <Plus className="h-3 w-3" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 text-red-500"
          onClick={() => onRemove(item.platillo_id)}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}

export function ResumenCarrito({ items, total, children, renderItem }) {
  return (
    <Card className="sticky top-24">
      <CardContent className="pt-6">
        <h3 className="font-semibold text-brand-brick mb-4">Tu pedido</h3>
        {items.length === 0 ? (
          <p className="text-gray-500 text-sm text-center py-8">
            Agrega platillos desde la carta
          </p>
        ) : (
          <>
            <div className="divide-y divide-orange-100 mb-4">
              {renderItem
                ? items.map(renderItem)
                : items.map((item) => (
                    <div key={item.platillo_id} className="flex justify-between py-2 text-sm">
                      <span>{item.cantidad}x {item.nombre}</span>
                      <span className="font-medium">{formatearPrecio(item.precio * item.cantidad)}</span>
                    </div>
                  ))}
            </div>
            <div className="flex justify-between items-center pt-4 border-t border-orange-200">
              <span className="font-semibold text-brand-brick">Total</span>
              <span className="text-xl font-bold text-brand-orange">{formatearPrecio(total)}</span>
            </div>
          </>
        )}
        {children && <div className="mt-4">{children}</div>}
      </CardContent>
    </Card>
  );
}
