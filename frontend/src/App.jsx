import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { ProtectedRoute } from "@/components/layout/ProtectedRoute";

import LoginPage from "@/pages/LoginPage";
import CartaDigitalPage from "@/pages/CartaDigitalPage";
import ReservasPage from "@/pages/ReservasPage";
import TakeawayPage from "@/pages/TakeawayPage";
import EstadoPedidoPage from "@/pages/EstadoPedidoPage";

import AdminDashboardPage from "@/pages/admin/AdminDashboardPage";
import AdminReservasPage from "@/pages/admin/AdminReservasPage";
import AdminTakeawayPage from "@/pages/admin/AdminTakeawayPage";
import AdminPlatillosPage from "@/pages/admin/AdminPlatillosPage";
import AdminMesasPage from "@/pages/admin/AdminMesasPage";

function PublicLayout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas */}
        <Route
          path="/"
          element={
            <PublicLayout>
              <CartaDigitalPage />
            </PublicLayout>
          }
        />
        <Route
          path="/reservas"
          element={
            <PublicLayout>
              <ReservasPage />
            </PublicLayout>
          }
        />
        <Route
          path="/takeaway"
          element={
            <PublicLayout>
              <TakeawayPage />
            </PublicLayout>
          }
        />
        <Route
          path="/takeaway/estado/:codigo"
          element={
            <PublicLayout>
              <EstadoPedidoPage />
            </PublicLayout>
          }
        />
        <Route path="/login" element={<LoginPage />} />

        {/* Rutas admin protegidas con JWT */}
        <Route element={<ProtectedRoute requireStaff />}>
          <Route path="/admin/reservas" element={<AdminReservasPage />} />
          <Route path="/admin/takeaway" element={<AdminTakeawayPage />} />
        </Route>

        <Route element={<ProtectedRoute requireStaff requireAdmin />}>
          <Route path="/admin" element={<AdminDashboardPage />} />
          <Route path="/admin/platillos" element={<AdminPlatillosPage />} />
          <Route path="/admin/mesas" element={<AdminMesasPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
