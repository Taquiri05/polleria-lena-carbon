import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, Pencil } from "lucide-react";
import { mesaService } from "@/services/mesaService";
import { getErrorMessage } from "@/services/api";
import { mesaSchema } from "@/schemas/takeawaySchema";
import { TIPOS_OCASION } from "@/utils/constants";
import { AdminMobileNav } from "@/components/layout/AdminSidebar";
import { Modal } from "@/components/admin/AdminCards";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { FormField } from "@/components/ui/Label";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent } from "@/components/ui/Card";
import { LoadingPage, Alert, Spinner } from "@/components/ui/Spinner";

export default function AdminMesasPage() {
  const [mesas, setMesas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const form = useForm({ resolver: zodResolver(mesaSchema) });

  const cargar = () => {
    setLoading(true);
    mesaService
      .listar()
      .then(setMesas)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
  }, []);

  const abrirCrear = () => {
    setEditando(null);
    form.reset({ tipo_ocasion: "familiar", capacidad: 4 });
    setModalOpen(true);
  };

  const abrirEditar = (mesa) => {
    setEditando(mesa);
    form.reset({
      numero: mesa.numero,
      capacidad: mesa.capacidad,
      tipo_ocasion: mesa.tipo_ocasion,
    });
    setModalOpen(true);
  };

  const onSubmit = async (data) => {
    setSubmitting(true);
    try {
      if (editando) {
        await mesaService.actualizar(editando.id, data);
      } else {
        await mesaService.crear(data);
      }
      setModalOpen(false);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const toggleActivo = async (mesa) => {
    try {
      await mesaService.cambiarEstado(mesa.id, !mesa.activo);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  if (loading) return <LoadingPage message="Cargando mesas..." />;

  return (
    <div className="p-6 lg:p-8">
      <AdminMobileNav />
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-brand-brick">
          Gestión de Mesas
        </h1>
        <Button variant="orange" onClick={abrirCrear}>
          <Plus className="h-4 w-4" />
          Nueva mesa
        </Button>
      </div>

      {error && <Alert variant="error" className="mb-4">{error}</Alert>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mesas.map((mesa) => (
          <Card key={mesa.id}>
            <CardContent className="pt-6">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-2xl font-bold text-brand-brick">
                      #{mesa.numero}
                    </span>
                    <Badge variant={mesa.activo ? "success" : "danger"}>
                      {mesa.activo ? "Activa" : "Inactiva"}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">
                    Capacidad: {mesa.capacidad} personas
                  </p>
                  <p className="text-sm text-gray-500 capitalize">
                    {mesa.tipo_ocasion}
                  </p>
                </div>
                <div className="flex flex-col gap-1">
                  <Button variant="outline" size="sm" onClick={() => abrirEditar(mesa)}>
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => toggleActivo(mesa)}>
                    {mesa.activo ? "Desactivar" : "Activar"}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editando ? "Editar mesa" : "Nueva mesa"}
      >
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField label="Número de mesa" required error={form.formState.errors.numero?.message}>
            <Input type="number" {...form.register("numero")} />
          </FormField>
          <FormField label="Capacidad" required error={form.formState.errors.capacidad?.message}>
            <Input type="number" min={1} max={30} {...form.register("capacidad")} />
          </FormField>
          <FormField label="Tipo de ocasión" required error={form.formState.errors.tipo_ocasion?.message}>
            <Select {...form.register("tipo_ocasion")}>
              {TIPOS_OCASION.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </Select>
          </FormField>
          <Button type="submit" variant="orange" className="w-full" disabled={submitting}>
            {submitting ? <Spinner size="sm" /> : editando ? "Guardar" : "Crear mesa"}
          </Button>
        </form>
      </Modal>
    </div>
  );
}
