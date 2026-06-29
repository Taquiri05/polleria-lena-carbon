export const TIPOS_OCASION = [
  { value: "familiar", label: "Familiar", descripcion: "Mesas para 4+ personas" },
  { value: "romantica", label: "Romántica", descripcion: "Ambiente íntimo para 2" },
  { value: "reunion", label: "Reunión", descripcion: "Mesas amplias para 6+ personas" },
];

export const ESTADOS_RESERVA = {
  pendiente: { label: "Pendiente", color: "bg-yellow-100 text-yellow-800" },
  confirmada: { label: "Confirmada", color: "bg-green-100 text-green-800" },
  completada: { label: "Completada", color: "bg-blue-100 text-blue-800" },
  cancelada: { label: "Cancelada", color: "bg-red-100 text-red-800" },
};

export const ESTADOS_PEDIDO = {
  recibido: { label: "Recibido", color: "bg-yellow-100 text-yellow-800" },
  en_preparacion: { label: "En preparación", color: "bg-orange-100 text-orange-800" },
  listo: { label: "Listo", color: "bg-green-100 text-green-800" },
  entregado: { label: "Entregado", color: "bg-blue-100 text-blue-800" },
  cancelado: { label: "Cancelado", color: "bg-red-100 text-red-800" },
};

export const TRANSICIONES_RESERVA = {
  pendiente: ["confirmada", "cancelada"],
  confirmada: ["completada", "cancelada"],
};

export const TRANSICIONES_PEDIDO = {
  recibido: ["en_preparacion", "cancelado"],
  en_preparacion: ["listo"],
  listo: ["entregado"],
};

export const ROLES = {
  ADMIN: "ADMIN",
  RECEPCIONISTA: "RECEPCIONISTA",
};
