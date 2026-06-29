import { Link, useLocation, useNavigate } from "react-router-dom";
import { Flame, ShoppingBag, Calendar, LogIn, LogOut, LayoutDashboard, Menu, X } from "lucide-react";
import { useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { useCartStore } from "@/store/cartStore";
import { Button } from "@/components/ui/Button";
import { authService } from "@/services/authService";

const navLinks = [
  { to: "/", label: "Carta", icon: Flame },
  { to: "/reservas", label: "Reservas", icon: Calendar },
  { to: "/takeaway", label: "Takeaway", icon: ShoppingBag },
];

export function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, usuario, logout, isStaff } = useAuthStore();
  const totalItems = useCartStore((s) => s.totalItems());
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await authService.logout();
    } catch {
      /* token ya inválido */
    }
    logout();
    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-50 bg-brand-brick text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 font-display text-xl font-bold">
            <Flame className="h-7 w-7 text-brand-orange" />
            <span>Leña y Carbón</span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map(({ to, label, icon: Icon }) => (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === to
                    ? "bg-white/20 text-white"
                    : "text-white/80 hover:bg-white/10 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
                {to === "/takeaway" && totalItems > 0 && (
                  <span className="ml-1 bg-brand-orange text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {totalItems}
                  </span>
                )}
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-3">
            {isStaff() && (
              <Link to="/admin">
                <Button variant="orange" size="sm">
                  <LayoutDashboard className="h-4 w-4" />
                  Panel
                </Button>
              </Link>
            )}
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <span className="text-sm text-white/80">{usuario?.nombre}</span>
                <Button variant="ghost" size="sm" onClick={handleLogout} className="text-white hover:bg-white/10">
                  <LogOut className="h-4 w-4" />
                  Salir
                </Button>
              </div>
            ) : (
              <Link to="/login">
                <Button variant="orange" size="sm">
                  <LogIn className="h-4 w-4" />
                  Ingresar
                </Button>
              </Link>
            )}
          </div>

          <button
            className="md:hidden p-2 rounded-lg hover:bg-white/10"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {menuOpen && (
          <nav className="md:hidden pb-4 space-y-1">
            {navLinks.map(({ to, label, icon: Icon }) => (
              <Link
                key={to}
                to={to}
                onClick={() => setMenuOpen(false)}
                className="flex items-center gap-2 px-4 py-3 rounded-lg hover:bg-white/10"
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
            {isStaff() && (
              <Link to="/admin" onClick={() => setMenuOpen(false)} className="block px-4 py-3 rounded-lg hover:bg-white/10">
                Panel de administración
              </Link>
            )}
            {isAuthenticated ? (
              <button onClick={handleLogout} className="w-full text-left px-4 py-3 rounded-lg hover:bg-white/10">
                Cerrar sesión
              </button>
            ) : (
              <Link to="/login" onClick={() => setMenuOpen(false)} className="block px-4 py-3 rounded-lg hover:bg-white/10">
                Ingresar
              </Link>
            )}
          </nav>
        )}
      </div>
    </header>
  );
}
