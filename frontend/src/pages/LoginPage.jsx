import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Flame } from "lucide-react";
import { loginSchema } from "@/schemas/authSchema";
import { authService } from "@/services/authService";
import { getErrorMessage } from "@/services/api";
import { useAuthStore } from "@/store/authStore";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { FormField } from "@/components/ui/Label";
import { Alert, Spinner } from "@/components/ui/Spinner";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated, isAdmin } = useAuthStore();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(loginSchema) });

  useEffect(() => {
    if (isAuthenticated) {
      navigate(isAdmin() ? "/admin" : "/admin/reservas", { replace: true });
    }
  }, [isAuthenticated, isAdmin, navigate]);

  const onSubmit = async (data) => {
    setLoading(true);
    setError("");
    try {
      const result = await authService.login(data.email, data.password);
      login(result.usuario, result.access_token);
      navigate(result.usuario.rol === "ADMIN" ? "/admin" : "/admin/reservas");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-8rem)] flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md shadow-elevated">
        <CardHeader className="text-center">
          <div className="mx-auto h-14 w-14 rounded-full bg-brand-brick flex items-center justify-center mb-2">
            <Flame className="h-8 w-8 text-brand-orange" />
          </div>
          <CardTitle>Iniciar sesión</CardTitle>
          <CardDescription>
            Acceso para recepcionistas y administradores
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="error" className="mb-4">
              {error}
            </Alert>
          )}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <FormField label="Correo electrónico" required error={errors.email?.message}>
              <Input
                type="email"
                placeholder="admin@lenacarbon.com"
                {...register("email")}
                error={errors.email}
              />
            </FormField>
            <FormField label="Contraseña" required error={errors.password?.message}>
              <Input
                type="password"
                placeholder="••••••••"
                {...register("password")}
                error={errors.password}
              />
            </FormField>
            <Button type="submit" variant="orange" className="w-full" disabled={loading}>
              {loading ? <Spinner size="sm" /> : "Ingresar"}
            </Button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-6">
            <a href="/" className="text-brand-orange hover:underline">
              ← Volver a la carta
            </a>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
