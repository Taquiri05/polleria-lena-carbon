import { z } from "zod";

export const takeawaySchema = z.object({
  cliente_nombre: z.string().min(2, "Mínimo 2 caracteres").max(100),
  cliente_contacto: z.string().min(7, "Teléfono inválido").max(20),
});

export const platilloSchema = z.object({
  nombre: z.string().min(2, "Mínimo 2 caracteres"),
  descripcion: z.string().optional(),
  precio: z.coerce.number().min(0.01, "Precio debe ser mayor a 0"),
  imagen_url: z.string().optional().or(z.literal("")),
  categoria_id: z.coerce.number().min(1, "Selecciona una categoría"),
});

export const mesaSchema = z.object({
  numero: z.coerce.number().min(1, "Número inválido"),
  capacidad: z.coerce.number().min(1).max(30),
  tipo_ocasion: z.enum(["familiar", "romantica", "reunion"]),
});
