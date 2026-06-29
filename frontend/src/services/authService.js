import api from "./api";

export const authService = {
  login: (email, password) =>
    api.post("/auth/login", { email, password }).then((r) => r.data),

  logout: () => api.post("/auth/logout").then((r) => r.data),

  getPerfil: () => api.get("/auth/perfil").then((r) => r.data),

  cambiarPassword: (password_actual, password_nueva) =>
    api.put("/auth/cambiar-password", { password_actual, password_nueva }).then((r) => r.data),
};
