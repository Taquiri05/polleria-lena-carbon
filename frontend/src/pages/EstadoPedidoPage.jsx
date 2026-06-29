import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Package, RefreshCw } from "lucide-react";
import { takeawayService } from "@/services/takeawayService";
import { getErrorMessage } from "@/services/api";
import { ESTADOS_PEDIDO } from "@/utils/constants";
import { formatearPrecio, formatearDateTime } from "@/utils/formatters";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage, Alert } from "@/components/ui/Spinner";

const PASOS = ["recibido", "en_preparacion", "listo", "entregado"];

export default function EstadoPedidoPage() {
  const { codigo } = useParams();
  const [pedido, setPedido] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const cargar = () => {
    setLoading(true);
    takeawayService
      .consultarEstado(codigo)
      .then(setPedido)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
    const interval = setInterval(cargar, 30000);
    return () => clearInterval(interval);
  }, [codigo]);

  if (loading && !pedido) return <LoadingPage message="Consultando pedido..." />;

  if (error && !pedido) {
    return (
      <div className="page-container max-w-lg mx-auto">
        <Alert variant="error">{error}</Alert>
        <Link to="/takeaway" className="block text-center mt-4 text-brand-orange">
          ← Volver al menú
        </Link>
      </div>
    );
  }

  const estadoInfo = ESTADOS_PEDIDO[pedido.estado] || {};
  const pasoActual = PASOS.indexOf(pedido.estado);

  return (
    <div className="page-container max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-brand-brick flex items-center gap-2">
          <Package className="h-7 w-7 text-brand-orange" />
          Seguimiento de pedido
        </h1>
        <Button variant="outline" size="sm" onClick={cargar}>
          <RefreshCw className="h-4 w-4" />
          Actualizar
        </Button>
      </div>

      <Card className="shadow-elevated mb-6">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>{pedido.codigo_seguimiento}</CardTitle>
            <Badge className={estadoInfo.color}>{estadoInfo.label}</Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-gray-600">
            Cliente: <strong>{pedido.cliente_nombre}</strong> ·{" "}
            {formatearDateTime(pedido.created_at)}
          </p>

          {pedido.estado !== "cancelado" && (
            <div className="flex items-center justify-between px-2">
              {PASOS.map((paso, i) => {
                const info = ESTADOS_PEDIDO[paso];
                const activo = i <= pasoActual;
                return (
                  <div key={paso} className="flex flex-col items-center flex-1">
                    <div
                      className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold ${
                        activo ? "bg-brand-orange text-white" : "bg-gray-200 text-gray-500"
                      }`}
                    >
                      {i + 1}
                    </div>
                    <span className="text-xs text-gray-500 mt-1 text-center hidden sm:block">
                      {info.label}
                    </span>
                    {i < PASOS.length - 1 && (
                      <div
                        className={`hidden sm:block absolute h-0.5 w-full ${
                          activo ? "bg-brand-orange" : "bg-gray-200"
                        }`}
                      />
                    )}
                  </div>
                );
              })}
            </div>
          )}

          <div className="border-t border-orange-100 pt-4">
            <h3 className="font-semibold text-brand-brick mb-2">Detalle del pedido</h3>
            {(pedido.items || []).map((item) => (
              <div key={item.id} className="flex justify-between text-sm py-1">
                <span>
                  {item.cantidad}x {item.platillo || item.platillo_nombre}
                </span>
                <span>{formatearPrecio(item.subtotal || item.precio_unitario * item.cantidad)}</span>
              </div>
            ))}
            <div className="flex justify-between font-bold text-brand-orange mt-2 pt-2 border-t">
              <span>Total</span>
              <span>{formatearPrecio(pedido.total)}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="text-center">
        <Link to="/takeaway">
          <Button variant="outline">Hacer otro pedido</Button>
        </Link>
      </div>
    </div>
  );
}
