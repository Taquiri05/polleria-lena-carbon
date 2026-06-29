import { Flame } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-brand-brick text-white/80 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Flame className="h-5 w-5 text-brand-orange" />
            <span className="font-display font-semibold text-white">
              Pollería Leña y Carbón
            </span>
          </div>
          <p className="text-sm text-center">
            Pollos a la brasa con receta tradicional · Ayacucho, Perú
          </p>
          <p className="text-xs text-white/60">
            © {new Date().getFullYear()} — IS-489 UNSCH
          </p>
        </div>
      </div>
    </footer>
  );
}
