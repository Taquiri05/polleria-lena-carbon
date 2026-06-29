import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { reservaService } from "@/services/reservaService";
import { getErrorMessage } from "@/services/api";
import { FormularioReserva } from "@/components/reservas/FormularioReserva";
import { Alert } from "@/components/ui/Spinner";
import { Card, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function ReservasPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [disponibilidad, setDisponibilidad] = useState(null);
  const [confirmacion, setConfirmacion] = useState(null);

  const handleConsultar = async (params) => {
    try {
      const result = await reservaService.getDisponibilidad(params);
      setDisponibilidad(result);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const handleSubmit = async (data) => {
    setLoading(true);
    setError("");
    try {
      const result = await reservaService.crear(data);
      setConfirmacion(result);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  if (confirmacion) {
    return (
      <div className="page-container max-w-lg mx-auto">
        <Card className="text-center shadow-elevated">
          <CardContent className="pt-8 pb-8">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-brand-brick mb-2">
              ¡Reserva confirmada!
            </h2>
            <p className="text-gray-600 mb-6">
              Tu mesa ha sido asignada. Guarda tu código de confirmación.
            </p>
            <div className="bg-brand-cream rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-500">Código de confirmación</p>
              <p className="text-2xl font-mono font-bold text-brand-orange">
                {confirmacion.codigo_confirmacion}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Mesa #{confirmacion.mesa?.numero} · {confirmacion.fecha} ·{" "}
                {confirmacion.hora?.slice(0, 5)}
              </p>
            </div>
            <Button variant="orange" onClick={() => setConfirmacion(null)}>
              Hacer otra reserva
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="page-container max-w-3xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="font-display text-3xl font-bold text-brand-brick">
          Reserva tu mesa
        </h1>
        <p className="text-gray-600 mt-2">
          Completa el formulario y te asignaremos la mesa ideal automáticamente.
        </p>
      </div>

      {error && (
        <Alert variant="error" className="mb-6">
          {error}
        </Alert>
      )}

      <FormularioReserva
        onSubmit={handleSubmit}
        loading={loading}
        disponibilidad={disponibilidad}
        onConsultar={handleConsultar}
      />
    </div>
  );
}
