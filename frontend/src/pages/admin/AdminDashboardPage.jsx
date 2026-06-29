import { useState, useEffect } from "react";
import { Calendar, ShoppingBag, DollarSign, TrendingUp } from "lucide-react";
import { adminService } from "@/services/adminService";
import { getErrorMessage } from "@/services/api";
import { formatearPrecio } from "@/utils/formatters";
import { AdminMobileNav } from "@/components/layout/AdminSidebar";
import { StatCard } from "@/components/admin/AdminCards";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { LoadingPage, Alert } from "@/components/ui/Spinner";

export default function AdminDashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    adminService
      .getDashboard()
      .then(setData)
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingPage message="Cargando dashboard..." />;

  return (
    <div className="p-6 lg:p-8">
      <AdminMobileNav />
      <h1 className="font-display text-2xl font-bold text-brand-brick mb-6">
        Dashboard del día
      </h1>

      {error && <Alert variant="error" className="mb-6">{error}</Alert>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Reservas hoy"
          value={data?.reservas_hoy ?? 0}
          icon={Calendar}
        />
        <StatCard
          title="Pedidos takeaway"
          value={data?.pedidos_hoy ?? 0}
          icon={ShoppingBag}
        />
        <StatCard
          title="Ingresos estimados"
          value={formatearPrecio(data?.ingresos_estimados ?? 0)}
          icon={DollarSign}
          subtitle="Pedidos en preparación o entregados"
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-brand-orange" />
            Platillos más pedidos hoy
          </CardTitle>
        </CardHeader>
        <CardContent>
          {(data?.platillos_top || []).length === 0 ? (
            <p className="text-gray-500 text-sm">Sin pedidos registrados hoy.</p>
          ) : (
            <ul className="space-y-3">
              {data.platillos_top.map((p, i) => (
                <li key={p.nombre} className="flex items-center justify-between">
                  <span className="flex items-center gap-3">
                    <span className="h-7 w-7 rounded-full bg-brand-orange/10 text-brand-orange text-sm font-bold flex items-center justify-center">
                      {i + 1}
                    </span>
                    {p.nombre}
                  </span>
                  <span className="text-sm text-gray-600">{p.total_pedido} unidades</span>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
