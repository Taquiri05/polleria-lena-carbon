import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],

      agregarItem: (platillo) => {
        const items = get().items;
        const existente = items.find((i) => i.platillo_id === platillo.id);

        if (existente) {
          set({
            items: items.map((i) =>
              i.platillo_id === platillo.id
                ? { ...i, cantidad: i.cantidad + 1 }
                : i
            ),
          });
        } else {
          set({
            items: [
              ...items,
              {
                platillo_id: platillo.id,
                nombre: platillo.nombre,
                precio: platillo.precio,
                imagen_url: platillo.imagen_url,
                cantidad: 1,
              },
            ],
          });
        }
      },

      quitarItem: (platilloId) => {
        set({ items: get().items.filter((i) => i.platillo_id !== platilloId) });
      },

      actualizarCantidad: (platilloId, cantidad) => {
        if (cantidad <= 0) {
          get().quitarItem(platilloId);
          return;
        }
        set({
          items: get().items.map((i) =>
            i.platillo_id === platilloId ? { ...i, cantidad } : i
          ),
        });
      },

      limpiarCarrito: () => set({ items: [] }),

      totalItems: () =>
        get().items.reduce((sum, i) => sum + i.cantidad, 0),

      totalPrecio: () =>
        get().items.reduce((sum, i) => sum + i.precio * i.cantidad, 0),

      getItemsParaPedido: () =>
        get().items.map(({ platillo_id, cantidad }) => ({
          platillo_id,
          cantidad,
        })),
    }),
    {
      name: "cart-storage",
      partialize: (state) => ({ items: state.items }),
    }
  )
);
