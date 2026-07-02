import { formatearPrecio } from "@/utils/formatters";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { Plus, ShoppingBag } from "lucide-react";

const IMAGENES_PLATILLOS = {
  "Pollo Entero a la Brasa": "/images/pollo_entero.jpg",
  "1/2 Pollo a la Brasa": "/images/medio_pollo.jpg",
  "1/4 Pollo a la Brasa": "/images/cuarto_pollo.jpg",
  "1/8 Pollo a la Brasa": "/images/octavo_pollo.jpg",
  "1/4 Pollo mas Gaseosa Personal": "/images/pollo_gaseosa.jpg",
  "Papas Fritas Porcion": "/images/papas.jpg",
  "Ensalada Mixta": "/images/ensalada.jpg",
  "Yucas Fritas": "/images/yucas.jpg",
  "Crema Huancaina": "/images/huancaina.jpg",
  "Anticuchos de Corazon x6": "/images/anticuchos.jpg",
  "Parrilla Mixta Personal": "/images/parrilla.jpg",
  "Chuleta a la Brasa": "/images/chuleta.jpg",
  "Gaseosa Coca Cola Familiar 1.5L": "/images/cocacola.jpg",
  "Gaseosa Inca Kola Familiar 1.5L": "/images/inkakola.jpg",
  "Chicha Morada Jarra": "/images/chicha.jpg",
  "Jugo de Maracuya Jarra": "/images/maracuya.jpg",
  "Cerveza Cristal 330ml": "/images/cerveza.jpg",
  "Cerveza Pilsen Callao 330ml": "/images/pilsen.jpg",
  "Helado de Lucuma": "/images/lucuma.jpg",
  "Mazamorra Morada": "/images/mazamorra.jpg",
};

const IMAGEN_DEFAULT = "/images/pollo.jpg";

function obtenerImagen(platillo) {
  if (platillo.imagen_url) return platillo.imagen_url;
  return IMAGENES_PLATILLOS[platillo.nombre] || IMAGEN_DEFAULT;
}

export function TarjetaPlatillo({ platillo, onAgregar, showAdd = false }) {
  return (
    <Card className="overflow-hidden hover:shadow-xl transition-all duration-300 group hover:-translate-y-1">
      <div className="relative h-48 overflow-hidden">
        <img
          src={obtenerImagen(platillo)}
          alt={platillo.nombre}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => { e.target.src = IMAGEN_DEFAULT; }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
      </div>
      <CardContent className="p-4 space-y-2">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-brand-brick leading-tight">
            {platillo.nombre}
          </h3>
          <span className="font-bold text-brand-orange whitespace-nowrap text-lg">
            {formatearPrecio(platillo.precio)}
          </span>
        </div>
        {platillo.descripcion && (
          <p className="text-sm text-gray-500 line-clamp-2">{platillo.descripcion}</p>
        )}
        {showAdd && onAgregar && (
          <Button
            variant="orange"
            size="sm"
            className="w-full mt-2"
            onClick={() => onAgregar(platillo)}
          >
            <Plus className="h-4 w-4 mr-1" />
            Agregar al carrito
          </Button>
        )}
      </CardContent>
    </Card>
  );
}

export function HeroSection() {
  return (
    <section
      className="relative text-white overflow-hidden"
      style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1200')",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-r from-black/80 to-black/50" />
      <div className="relative max-w-6xl mx-auto px-4 py-20 md:py-32">
        <div className="max-w-2xl">
          <h1 className="font-bold text-4xl md:text-6xl mb-4 drop-shadow-lg">
            🔥 Pollería Leña y Carbón
          </h1>
          <p className="text-lg md:text-xl text-white/90 mb-8 drop-shadow">
            El auténtico sabor del pollo a la brasa, preparado con leña y carbón.
            Reserva tu mesa o pide para llevar.
          </p>
          <div className="flex flex-wrap gap-4">
            <a href="/reservas">
              <Button
                size="lg"
                className="bg-orange-600 hover:bg-orange-700 text-white font-bold px-8 py-3 rounded-xl shadow-lg"
              >
                🍽️ Reservar Mesa
              </Button>
            </a>
            <a href="/takeaway">
              <Button
                size="lg"
                className="bg-white/10 border-2 border-white text-white hover:bg-white hover:text-orange-800 font-bold px-8 py-3 rounded-xl backdrop-blur-sm"
              >
                <ShoppingBag className="h-5 w-5 mr-2" />
                Pedir Takeaway
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}