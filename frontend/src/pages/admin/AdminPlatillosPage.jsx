import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, Pencil, Eye, EyeOff } from "lucide-react";
import { cartaService } from "@/services/cartaService";
import { getErrorMessage } from "@/services/api";
import { platilloSchema } from "@/schemas/takeawaySchema";
import { formatearPrecio } from "@/utils/formatters";
import { AdminMobileNav } from "@/components/layout/AdminSidebar";
import { Modal } from "@/components/admin/AdminCards";
import { Button } from "@/components/ui/Button";
import { Input, Textarea } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { FormField } from "@/components/ui/Label";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent } from "@/components/ui/Card";
import { LoadingPage, Alert, Spinner } from "@/components/ui/Spinner";

export default function AdminPlatillosPage() {
  const [platillos, setPlatillos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const form = useForm({ resolver: zodResolver(platilloSchema) });

  const cargar = async () => {
    setLoading(true);
    try {
      const [cats, activos, inactivos] = await Promise.all([
        cartaService.getCategorias(),
        cartaService.getPlatillos({ activo: true }),
        cartaService.getPlatillos({ activo: false }),
      ]);
      setCategorias(cats);
      setPlatillos([...activos, ...inactivos]);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargar();
  }, []);

  const abrirCrear = () => {
    setEditando(null);
    form.reset({ categoria_id: categorias[0]?.id, precio: 0 });
    setModalOpen(true);
  };

  const abrirEditar = (platillo) => {
    setEditando(platillo);
    form.reset({
      nombre: platillo.nombre,
      descripcion: platillo.descripcion || "",
      precio: platillo.precio,
      imagen_url: platillo.imagen_url || "",
      categoria_id: platillo.categoria_id,
    });
    setModalOpen(true);
  };

  const onSubmit = async (data) => {
    setSubmitting(true);
    try {
      if (editando) {
        await cartaService.actualizarPlatillo(editando.id, data);
      } else {
        await cartaService.crearPlatillo(data);
      }
      setModalOpen(false);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const toggleActivo = async (platillo) => {
    try {
      await cartaService.cambiarEstadoPlatillo(platillo.id, !platillo.activo);
      cargar();
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  if (loading) return <LoadingPage message="Cargando platillos..." />;

  return (
    <div className="p-6 lg:p-8">
      <AdminMobileNav />
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-2xl font-bold text-brand-brick">
          Gestión de Platillos
        </h1>
        <Button variant="orange" onClick={abrirCrear}>
          <Plus className="h-4 w-4" />
          Nuevo platillo
        </Button>
      </div>

      {error && <Alert variant="error" className="mb-4">{error}</Alert>}

      <div className="grid gap-4">
        {platillos.map((p) => (
          <Card key={p.id}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-brand-brick">{p.nombre}</h3>
                    <Badge variant={p.activo ? "success" : "danger"}>
                      {p.activo ? "Activo" : "Inactivo"}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">
                    {formatearPrecio(p.precio)} · {p.categoria}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => abrirEditar(p)}>
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => toggleActivo(p)}>
                    {p.activo ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
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
        title={editando ? "Editar platillo" : "Nuevo platillo"}
      >
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField label="Nombre" required error={form.formState.errors.nombre?.message}>
            <Input {...form.register("nombre")} />
          </FormField>
          <FormField label="Descripción" error={form.formState.errors.descripcion?.message}>
            <Textarea {...form.register("descripcion")} />
          </FormField>
          <FormField label="Precio (S/)" required error={form.formState.errors.precio?.message}>
            <Input type="number" step="0.01" {...form.register("precio")} />
          </FormField>
          <FormField label="URL de imagen" error={form.formState.errors.imagen_url?.message}>
            <Input {...form.register("imagen_url")} placeholder="https://..." />
          </FormField>
          <FormField label="Categoría" required error={form.formState.errors.categoria_id?.message}>
            <Select {...form.register("categoria_id")}>
              {categorias.map((c) => (
                <option key={c.id} value={c.id}>{c.nombre}</option>
              ))}
            </Select>
          </FormField>
          <Button type="submit" variant="orange" className="w-full" disabled={submitting}>
            {submitting ? <Spinner size="sm" /> : editando ? "Guardar cambios" : "Crear platillo"}
          </Button>
        </form>
      </Modal>
    </div>
  );
}
