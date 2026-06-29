import { formatearPrecio } from "@/utils/formatters";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { Plus, ShoppingBag } from "lucide-react";

export function TarjetaPlatillo({ platillo, onAgregar, showAdd = false }) {
  return (
    <Card className="overflow-hidden hover:shadow-elevated transition-shadow group">
      <div className="aspect-video bg-gradient-to-br from-brand-orange/20 to-brand-brick/10 flex items-center justify-center">
        {platillo.imagen_url ? (
          <img
            src={platillo.imagen_url}
            alt={platillo.nombre}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-5xl">🍗</span>
        )}
      </div>
      <CardContent className="space-y-2">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-brand-brick leading-tight">
            {platillo.nombre}
          </h3>
          <span className="font-bold text-brand-orange whitespace-nowrap">
            {formatearPrecio(platillo.precio)}
          </span>
        </div>
        {platillo.descripcion && (
          <p className="text-sm text-gray-600 line-clamp-2">{platillo.descripcion}</p>
        )}
        {showAdd && onAgregar && (
          <Button
            variant="orange"
            size="sm"
            className="w-full mt-2"
            onClick={() => onAgregar(platillo)}
          >
            <Plus className="h-4 w-4" />
            Agregar al carrito
          </Button>
        )}
      </CardContent>
    </Card>
  );
}

export function HeroSection() {
  return (
    <section className="relative bg-brand-brick text-white overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-brand-brick to-brand-brick-light opacity-90" />
      <div className="relative page-container py-16 md:py-24">
        <div className="max-w-2xl">
          <h1 className="font-display text-4xl md:text-5xl font-bold mb-4">
            Pollería Leña y Carbón
          </h1>
          <p className="text-lg text-white/90 mb-6">
            El auténtico sabor del pollo a la brasa, preparado con leña y carbón.
            Reserva tu mesa o pide para llevar.
          </p>
          <div className="flex flex-wrap gap-3">
            <a href="/reservas">
              <Button variant="orange" size="lg">Reservar mesa</Button>
            </a>
            <a href="/takeaway">
              <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-brand-brick">
                <ShoppingBag className="h-5 w-5" />
                Pedir takeaway
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
