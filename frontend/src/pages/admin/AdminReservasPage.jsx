import { useState, useEffect } from "react";
import { reservaService } from "@/services/reservaService";
import { getErrorMessage } from "@/services/api";
import { TRANSICIONES_RESERVA } from "@/utils/constants";
import { AdminMobileNav } from "@/components/layout/AdminSidebar";
import { TarjetaReserva } from "@/components/admin/AdminCards";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Label } from "@/components/ui/Label";
import { LoadingPage, Alert } from "@/components/ui/Spinner";

export default function AdminReservasPage() {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [fecha, setFecha] = useState(new Date().toISOString().split("T")[0]);
  const [estado, setEstado] = useState("");

  const cargar = () => {
    setLoading(true);
    const params = { fecha };
    if (estado) params.estado = estado;
    reservaService
      .listar(params)
      .then(setReservas)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
  }, [fecha, estado]);

  const handleCambiarEstado = async (id, nuevoEstado) => {
    try {
      await reservaService.actualizarEstado(id, nuevoEstado);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  return (
    <div className="p-6 lg:p-8">
      <AdminMobileNav />
      <h1 className="font-display text-2xl font-bold text-brand-brick mb-6">
        Reservas del día
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
            <option value="pendiente">Pendiente</option>
            <option value="confirmada">Confirmada</option>
            <option value="completada">Completada</option>
            <option value="cancelada">Cancelada</option>
          </Select>
        </div>
      </div>

      {error && <Alert variant="error" className="mb-4">{error}</Alert>}

      {loading ? (
        <LoadingPage message="Cargando reservas..." />
      ) : reservas.length === 0 ? (
        <p className="text-gray-500 text-center py-12">No hay reservas para esta fecha.</p>
      ) : (
        <div className="space-y-4">
          {reservas.map((r) => (
            <TarjetaReserva
              key={r.id}
              reserva={r}
              transiciones={TRANSICIONES_RESERVA[r.estado] || []}
              onCambiarEstado={handleCambiarEstado}
            />
          ))}
        </div>
      )}
    </div>
  );
}
