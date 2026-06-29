import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useAuthStore = create(
  persist(
    (set, get) => ({
      usuario: null,
      token: null,
      isAuthenticated: false,

      login: (usuario, token) => {
        localStorage.setItem("token", token);
        set({ usuario, token, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem("token");
        set({ usuario: null, token: null, isAuthenticated: false });
      },

      setUsuario: (usuario) => set({ usuario }),

      isAdmin: () => get().usuario?.rol === "ADMIN",

      isStaff: () =>
        ["ADMIN", "RECEPCIONISTA"].includes(get().usuario?.rol),
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        usuario: state.usuario,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
