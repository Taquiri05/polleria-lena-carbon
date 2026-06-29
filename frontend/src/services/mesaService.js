import api from "./api";

export const mesaService = {
  listar: () => api.get("/mesas").then((r) => r.data),

  crear: (data) => api.post("/mesas", data).then((r) => r.data),

  actualizar: (id, data) => api.put(`/mesas/${id}`, data).then((r) => r.data),

  cambiarEstado: (id, activo) =>
    api.patch(`/mesas/${id}/estado`, { activo }).then((r) => r.data),
};
