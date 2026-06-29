import { z } from "zod";

export const reservaSchema = z.object({
  cliente_nombre: z.string().min(2, "Mínimo 2 caracteres").max(100),
  cliente_contacto: z.string().min(7, "Teléfono inválido").max(20),
  fecha: z.string().min(1, "La fecha es obligatoria"),
  hora: z.string().min(1, "La hora es obligatoria"),
  num_personas: z.coerce.number().min(1, "Mínimo 1 persona").max(30, "Máximo 30 personas"),
  tipo_ocasion: z.enum(["familiar", "romantica", "reunion"], {
    errorMap: () => ({ message: "Selecciona un tipo de ocasión" }),
  }),
});
