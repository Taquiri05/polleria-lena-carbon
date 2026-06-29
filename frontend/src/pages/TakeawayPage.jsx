import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ShoppingBag } from "lucide-react";
import { cartaService } from "@/services/cartaService";
import { takeawayService } from "@/services/takeawayService";
import { getErrorMessage } from "@/services/api";
import { takeawaySchema } from "@/schemas/takeawaySchema";
import { useCartStore } from "@/store/cartStore";
import { TarjetaPlatillo } from "@/components/carta/TarjetaPlatillo";
import { FiltroCategorias } from "@/components/carta/FiltroCategorias";
import { CarritoItem, ResumenCarrito } from "@/components/takeaway/CarritoTakeaway";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { FormField } from "@/components/ui/Label";
import { Alert, LoadingPage, Spinner } from "@/components/ui/Spinner";
import { Card, CardContent } from "@/components/ui/Card";

export default function TakeawayPage() {
  const navigate = useNavigate();
  const { items, agregarItem, actualizarCantidad, quitarItem, totalPrecio, getItemsParaPedido, limpiarCarrito } =
    useCartStore();
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [categoriaActiva, setCategoriaActiva] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(takeawaySchema) });

  useEffect(() => {
    cartaService
      .getCategorias()
      .then(setCategorias)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  const platillos = categoriaActiva
    ? categorias.find((c) => c.id === categoriaActiva)?.platillos || []
    : categorias.flatMap((c) => c.platillos || []);

  const onConfirmar = async (data) => {
    if (items.length === 0) {
      setError("Agrega al menos un platillo al carrito.");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const pedido = await takeawayService.crear({
        ...data,
        items: getItemsParaPedido(),
      });
      limpiarCarrito();
      navigate(`/takeaway/estado/${pedido.codigo_seguimiento}`);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingPage message="Cargando menú..." />;

  return (
    <div className="page-container">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-bold text-brand-brick flex items-center gap-2">
          <ShoppingBag className="h-8 w-8 text-brand-orange" />
          Pedido Takeaway
        </h1>
        <p className="text-gray-600 mt-2">
          Selecciona tus platillos favoritos y recógelos en el restaurante.
        </p>
      </div>

      {error && <Alert variant="error" className="mb-6">{error}</Alert>}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <FiltroCategorias
            categorias={categorias}
            activa={categoriaActiva}
            onChange={setCategoriaActiva}
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {platillos.map((p) => (
              <TarjetaPlatillo
                key={p.id}
                platillo={p}
                showAdd
                onAgregar={agregarItem}
              />
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <ResumenCarrito
            items={items}
            total={totalPrecio()}
            renderItem={(item) => (
              <CarritoItem
                key={item.platillo_id}
                item={item}
                onUpdate={actualizarCantidad}
                onRemove={quitarItem}
              />
            )}
          />

          {items.length > 0 && (
            <Card>
              <CardContent className="pt-6">
                <form onSubmit={handleSubmit(onConfirmar)} className="space-y-4">
                  <FormField label="Tu nombre" required error={errors.cliente_nombre?.message}>
                    <Input {...register("cliente_nombre")} placeholder="Nombre completo" />
                  </FormField>
                  <FormField label="Teléfono" required error={errors.cliente_contacto?.message}>
                    <Input {...register("cliente_contacto")} placeholder="987654321" />
                  </FormField>
                  <Button type="submit" variant="orange" className="w-full" disabled={submitting}>
                    {submitting ? <Spinner size="sm" /> : "Confirmar pedido"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
