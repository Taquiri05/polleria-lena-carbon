import api from "./api";

export const reservaService = {
  crear: (data) => api.post("/reservas", data).then((r) => r.data),

  getDisponibilidad: (params) =>
    api.get("/reservas/disponibilidad", { params }).then((r) => r.data),

  listar: (params = {}) =>
    api.get("/reservas", { params }).then((r) => r.data),

  obtener: (id) => api.get(`/reservas/${id}`).then((r) => r.data),

  actualizarEstado: (id, estado) =>
    api.patch(`/reservas/${id}/estado`, { estado }).then((r) => r.data),

  cancelar: (codigo_confirmacion) =>
    api.post("/reservas/cancelar", { codigo_confirmacion }).then((r) => r.data),
};
