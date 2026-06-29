import api from "./api";

export const takeawayService = {
  crear: (data) => api.post("/takeaway", data).then((r) => r.data),

  consultarEstado: (codigo) =>
    api.get(`/takeaway/estado/${codigo}`).then((r) => r.data),

  listar: (params = {}) =>
    api.get("/takeaway", { params }).then((r) => r.data),

  obtener: (id) => api.get(`/takeaway/${id}`).then((r) => r.data),

  actualizarEstado: (id, estado) =>
    api.patch(`/takeaway/${id}/estado`, { estado }).then((r) => r.data),
};
