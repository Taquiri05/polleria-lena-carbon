import api from "./api";

export const cartaService = {
  getCategorias: () => api.get("/categorias").then((r) => r.data),

  getPlatillos: (params = {}) =>
    api.get("/platillos", { params }).then((r) => r.data),

  crearCategoria: (data) => api.post("/categorias", data).then((r) => r.data),

  actualizarCategoria: (id, data) =>
    api.put(`/categorias/${id}`, data).then((r) => r.data),

  eliminarCategoria: (id) =>
    api.delete(`/categorias/${id}`).then((r) => r.data),

  crearPlatillo: (data) => api.post("/platillos", data).then((r) => r.data),

  actualizarPlatillo: (id, data) =>
    api.put(`/platillos/${id}`, data).then((r) => r.data),

  cambiarEstadoPlatillo: (id, activo) =>
    api.patch(`/platillos/${id}/estado`, { activo }).then((r) => r.data),
};
