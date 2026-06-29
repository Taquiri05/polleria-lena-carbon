import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import { AdminSidebar } from "./AdminSidebar";

export function ProtectedRoute({ requireAdmin = false, requireStaff = false }) {
  const location = useLocation();
  const { isAuthenticated, isAdmin, isStaff } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (requireAdmin && !isAdmin()) {
    return <Navigate to="/admin/reservas" replace />;
  }

  if (requireStaff && !isStaff()) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <AdminSidebar />
      <main className="flex-1 bg-brand-cream overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
