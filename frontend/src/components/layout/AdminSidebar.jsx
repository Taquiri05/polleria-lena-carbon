import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Calendar,
  ShoppingBag,
  UtensilsCrossed,
  Grid3X3,
} from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { cn } from "@/lib/utils";

const links = [
  { to: "/admin", label: "Dashboard", icon: LayoutDashboard, adminOnly: true },
  { to: "/admin/reservas", label: "Reservas", icon: Calendar },
  { to: "/admin/takeaway", label: "Takeaway", icon: ShoppingBag },
  { to: "/admin/platillos", label: "Platillos", icon: UtensilsCrossed, adminOnly: true },
  { to: "/admin/mesas", label: "Mesas", icon: Grid3X3, adminOnly: true },
];

export function AdminSidebar() {
  const usuario = useAuthStore((s) => s.usuario);

  const visibleLinks = links.filter((l) => !l.adminOnly || usuario?.rol === 'ADMIN');

  return (
    <aside className="w-64 bg-white border-r border-orange-100 hidden lg:block shrink-0">
      <div className="p-6 border-b border-orange-100">
        <h2 className="font-display text-lg font-bold text-brand-brick">
          {usuario?.rol === 'ADMIN' ? 'Panel Admin' : 'Panel Recepcionista'}
        </h2>
        <p className="text-xs text-gray-500 mt-1">
          {usuario?.rol === 'ADMIN' ? 'Gestión del restaurante' : 'Operaciones del día'}
        </p>
      </div>
      <nav className="p-4 space-y-1">
        {visibleLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/admin"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-brand-brick text-white"
                  : "text-gray-600 hover:bg-brand-cream hover:text-brand-brick"
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export function AdminMobileNav() {
  const usuario = useAuthStore((s) => s.usuario);
  const visibleLinks = links.filter((l) => !l.adminOnly || usuario?.rol === 'ADMIN');

  return (
    <nav className="lg:hidden flex gap-2 overflow-x-auto pb-4 px-4 -mx-4">
      {visibleLinks.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/admin"}
          className={({ isActive }) =>
            cn(
              "flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium whitespace-nowrap shrink-0",
              isActive
                ? "bg-brand-brick text-white"
                : "bg-white text-gray-600 border border-orange-100"
            )
          }
        >
          <Icon className="h-3.5 w-3.5" />
          {label}
        </NavLink>
      ))}
    </nav>
  );
}
