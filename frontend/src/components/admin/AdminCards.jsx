import { ESTADOS_PEDIDO, ESTADOS_RESERVA } from "@/utils/constants";
import { formatearPrecio, formatearDateTime, formatearFechaCorta } from "@/utils/formatters";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { Select } from "@/components/ui/Select";

export function TarjetaReserva({ reserva, onCambiarEstado, transiciones }) {
  const estadoInfo = ESTADOS_RESERVA[reserva.estado] || {};

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-brand-brick">{reserva.cliente_nombre}</h3>
              <Badge className={estadoInfo.color}>{estadoInfo.label || reserva.estado}</Badge>
            </div>
            <p className="text-sm text-gray-600">
              {formatearFechaCorta(reserva.fecha)} · {reserva.hora?.slice(0, 5)} · Mesa{" "}
              {reserva.mesa?.numero}
            </p>
            <p className="text-xs text-gray-400 font-mono">{reserva.codigo_confirmacion}</p>
          </div>
          {transiciones?.length > 0 && onCambiarEstado && (
            <EstadoSelector
              valor={reserva.estado}
              transiciones={transiciones}
              onChange={(estado) => onCambiarEstado(reserva.id, estado)}
            />
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export function TarjetaPedido({ pedido, onCambiarEstado, transiciones }) {
  const estadoInfo = ESTADOS_PEDIDO[pedido.estado] || {};

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-brand-brick">{pedido.cliente_nombre}</h3>
              <Badge className={estadoInfo.color}>{estadoInfo.label || pedido.estado}</Badge>
            </div>
            <p className="text-sm text-gray-600">
              {formatearPrecio(pedido.total)} · {formatearDateTime(pedido.created_at)}
            </p>
            <p className="text-xs text-gray-400 font-mono">{pedido.codigo_seguimiento}</p>
          </div>
          {transiciones?.length > 0 && onCambiarEstado && (
            <EstadoSelector
              valor={pedido.estado}
              transiciones={transiciones}
              onChange={(estado) => onCambiarEstado(pedido.id, estado)}
            />
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function EstadoSelector({ valor, transiciones, onChange }) {
  return (
    <div className="flex items-center gap-2">
      <Select
        defaultValue=""
        onChange={(e) => e.target.value && onChange(e.target.value)}
        className="w-44"
      >
        <option value="" disabled>
          Cambiar estado
        </option>
        {transiciones.map((t) => (
          <option key={t} value={t}>
            → {t.replace("_", " ")}
          </option>
        ))}
      </Select>
    </div>
  );
}

export function StatCard({ title, value, icon: Icon, subtitle }) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500">{title}</p>
            <p className="text-3xl font-bold text-brand-brick mt-1">{value}</p>
            {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
          </div>
          {Icon && (
            <div className="h-12 w-12 rounded-full bg-brand-orange/10 flex items-center justify-center">
              <Icon className="h-6 w-6 text-brand-orange" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export function Modal({ open, onClose, title, children }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-white rounded-xl shadow-elevated max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-orange-100">
          <h2 className="text-lg font-semibold text-brand-brick">{title}</h2>
          <Button variant="ghost" size="icon" onClick={onClose}>✕</Button>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  );
}
