import api from "./api";

export const adminService = {
  getDashboard: () => api.get("/admin/dashboard").then((r) => r.data),

  getConfiguracion: () => api.get("/admin/configuracion").then((r) => r.data),

  actualizarConfiguracion: (data) =>
    api.put("/admin/configuracion", data).then((r) => r.data),
};
