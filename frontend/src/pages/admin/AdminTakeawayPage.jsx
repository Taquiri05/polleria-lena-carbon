import { useState, useEffect } from "react";
import { takeawayService } from "@/services/takeawayService";
import { getErrorMessage } from "@/services/api";
import { TRANSICIONES_PEDIDO } from "@/utils/constants";
import { AdminMobileNav } from "@/components/layout/AdminSidebar";
import { TarjetaPedido } from "@/components/admin/AdminCards";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Label } from "@/components/ui/Label";
import { LoadingPage, Alert } from "@/components/ui/Spinner";

export default function AdminTakeawayPage() {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [fecha, setFecha] = useState(new Date().toISOString().split("T")[0]);
  const [estado, setEstado] = useState("");

  const cargar = () => {
    setLoading(true);
    const params = { fecha };
    if (estado) params.estado = estado;
    takeawayService
      .listar(params)
      .then(setPedidos)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
  }, [fecha, estado]);

  const handleCambiarEstado = async (id, nuevoEstado) => {
    try {
      await takeawayService.actualizarEstado(id, nuevoEstado);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  return (
    <div className="p-6 lg:p-8">
      <AdminMobileNav />
      <h1 className="font-display text-2xl font-bold text-brand-brick mb-6">
        Pedidos Takeaway
      </h1>

      <div className="flex flex-wrap gap-4 mb-6">
        <div>
          <Label>Fecha</Label>
          <Input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} className="w-44" />
        </div>
        <div>
          <Label>Estado</Label>
          <Select value={estado} onChange={(e) => setEstado(e.target.value)} className="w-44">
            <option value="">Todos</option>
            <option value="recibido">Recibido</option>
            <option value="en_preparacion">En preparación</option>
            <option value="listo">Listo</option>
            <option value="entregado">Entregado</option>
            <option value="cancelado">Cancelado</option>
          </Select>
        </div>
      </div>

      {error && <Alert variant="error" className="mb-4">{error}</Alert>}

      {loading ? (
        <LoadingPage message="Cargando pedidos..." />
      ) : pedidos.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No hay pedidos para esta fecha.</p>
      ) : (
        <div className="space-y-4">
          {pedidos.map((p) => (
            <TarjetaPedido
              key={p.id}
              pedido={p}
              transiciones={TRANSICIONES_PEDIDO[p.estado] || []}
              onCambiarEstado={handleCambiarEstado}
            />
          ))}
        </div>
      )}
    </div>
  );
}
