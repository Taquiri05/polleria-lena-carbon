import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { reservaSchema } from "@/schemas/reservaSchema";
import { TIPOS_OCASION } from "@/utils/constants";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { FormField } from "@/components/ui/Label";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";

export function FormularioReserva({ onSubmit, loading, disponibilidad, onConsultar }) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(reservaSchema),
    defaultValues: {
      num_personas: 2,
      tipo_ocasion: "familiar",
    },
  });

  const fecha = watch("fecha");
  const hora = watch("hora");
  const tipo_ocasion = watch("tipo_ocasion");
  const num_personas = watch("num_personas");

  const handleConsultar = () => {
    if (fecha && tipo_ocasion && num_personas) {
      onConsultar?.({ fecha, hora, tipo_ocasion, num_personas });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Datos de la reserva</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Nombre completo" required error={errors.cliente_nombre?.message}>
              <Input
                {...register("cliente_nombre")}
                placeholder="Ej: Juan Pérez"
                error={errors.cliente_nombre}
              />
            </FormField>

            <FormField label="Teléfono de contacto" required error={errors.cliente_contacto?.message}>
              <Input
                {...register("cliente_contacto")}
                placeholder="Ej: 987654321"
                error={errors.cliente_contacto}
              />
            </FormField>

            <FormField label="Fecha" required error={errors.fecha?.message}>
              <Input type="date" {...register("fecha")} error={errors.fecha} />
            </FormField>

            <FormField label="Hora" required error={errors.hora?.message}>
              <Input type="time" {...register("hora")} error={errors.hora} />
            </FormField>

            <FormField label="Número de personas" required error={errors.num_personas?.message}>
              <Input
                type="number"
                min={1}
                max={30}
                {...register("num_personas", { valueAsNumber: true })}
                error={errors.num_personas}
              />
            </FormField>

            <FormField label="Tipo de ocasión" required error={errors.tipo_ocasion?.message}>
              <Select {...register("tipo_ocasion")} error={errors.tipo_ocasion}>
                {TIPOS_OCASION.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label} — {t.descripcion}
                  </option>
                ))}
              </Select>
            </FormField>
          </div>

          {disponibilidad && (
            <div
              className={`rounded-lg p-4 text-sm ${
                disponibilidad.disponible
                  ? "bg-green-50 text-green-800 border border-green-200"
                  : "bg-red-50 text-red-800 border border-red-200"
              }`}
            >
              {disponibilidad.disponible ? (
                <>
                  ✓ Hay mesas disponibles para tu reserva.
                  {disponibilidad.horarios_sugeridos?.length > 0 && (
                    <p className="mt-1 text-xs">
                      Horarios sugeridos: {disponibilidad.horarios_sugeridos.join(", ")}
                    </p>
                  )}
                </>
              ) : (
                "No hay mesas disponibles para el horario seleccionado. Prueba otra fecha u hora."
              )}
            </div>
          )}

          <div className="flex flex-wrap gap-3 pt-2">
            <Button type="button" variant="outline" onClick={handleConsultar}>
              Consultar disponibilidad
            </Button>
            <Button type="submit" variant="orange" disabled={loading}>
              {loading ? <Spinner size="sm" /> : "Confirmar reserva"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
