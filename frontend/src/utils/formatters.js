export function formatearPrecio(valor) {
  return new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
  }).format(valor ?? 0);
}

export function formatearFecha(fecha) {
  if (!fecha) return "";
  return new Intl.DateTimeFormat("es-PE", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date(fecha + "T12:00:00"));
}

export function formatearFechaCorta(fecha) {
  if (!fecha) return "";
  return new Intl.DateTimeFormat("es-PE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(new Date(fecha + "T12:00:00"));
}

export function formatearHora(hora) {
  if (!hora) return "";
  const [h, m] = hora.split(":");
  return `${h}:${m}`;
}

export function formatearDateTime(iso) {
  if (!iso) return "";
  return new Intl.DateTimeFormat("es-PE", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(iso));
}
