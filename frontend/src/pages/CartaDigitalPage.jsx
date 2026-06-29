import { useState, useEffect } from "react";
import { cartaService } from "@/services/cartaService";
import { getErrorMessage } from "@/services/api";
import { HeroSection, TarjetaPlatillo } from "@/components/carta/TarjetaPlatillo";
import { FiltroCategorias } from "@/components/carta/FiltroCategorias";
import { LoadingPage, Alert } from "@/components/ui/Spinner";

export default function CartaDigitalPage() {
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [categoriaActiva, setCategoriaActiva] = useState(null);

  useEffect(() => {
    cartaService
      .getCategorias()
      .then(setCategorias)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  const platillosFiltrados = categoriaActiva
    ? categorias.find((c) => c.id === categoriaActiva)?.platillos || []
    : categorias.flatMap((c) => c.platillos || []);

  if (loading) return <LoadingPage message="Cargando carta..." />;

  return (
    <>
      <HeroSection />
      <div className="page-container">
        {error && (
          <Alert variant="error" className="mb-6">
            {error}
          </Alert>
        )}

        <div className="mb-8">
          <h2 className="font-display text-2xl font-bold text-brand-brick mb-4">
            Nuestra Carta
          </h2>
          <FiltroCategorias
            categorias={categorias}
            activa={categoriaActiva}
            onChange={setCategoriaActiva}
          />
        </div>

        {categoriaActiva ? (
          platillosFiltrados.length === 0 ? (
            <p className="text-center text-gray-500 py-12">
              No hay platillos disponibles en esta categoría.
            </p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {platillosFiltrados.map((platillo) => (
                <TarjetaPlatillo key={platillo.id} platillo={platillo} />
              ))}
            </div>
          )
        ) : (
          categorias.map((cat) => (
            <section key={cat.id} className="mb-12">
              <h3 className="font-display text-xl font-bold text-brand-brick mb-4 border-b border-orange-200 pb-2">
                {cat.nombre}
              </h3>
              {cat.descripcion && (
                <p className="text-gray-600 text-sm mb-4">{cat.descripcion}</p>
              )}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {(cat.platillos || []).map((p) => (
                  <TarjetaPlatillo key={p.id} platillo={p} />
                ))}
              </div>
            </section>
          ))
        )}
      </div>
    </>
  );
}
