"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  Briefcase,
  Gamepad2,
  Minus,
  Cpu,
  Heart,
  Terminal,
  Search,
  Crown,
  Sparkles,
  Ruler,
  Palette,
  ChevronDown,
} from "lucide-react";

export type ThemeId = 
  | "corporate"
  | "gamer"
  | "minimalist"
  | "cyborg"
  | "feminine"
  | "hacker"
  | "criminalist"
  | "executive"
  | "anime"
  | "architect";

interface Theme {
  id: ThemeId;
  name: string;
  description: string;
  icon: React.ReactNode;
  preview: {
    bg: string;
    primary: string;
    accent: string;
  };
}

const themes: Theme[] = [
  {
    id: "corporate",
    name: "Corporate",
    description: "Directivo azul grafito",
    icon: <Briefcase className="h-4 w-4" />,
    preview: { bg: "#0b1a2a", primary: "#1e86ff", accent: "#3dd5ff" },
  },
  {
    id: "gamer",
    name: "Gamer",
    description: "RGB gaming oscuro",
    icon: <Gamepad2 className="h-4 w-4" />,
    preview: { bg: "#0a0e1a", primary: "#00ff88", accent: "#ff0080" },
  },
  {
    id: "minimalist",
    name: "Minimalist",
    description: "Monocromático elegante",
    icon: <Minus className="h-4 w-4" />,
    preview: { bg: "#fafafa", primary: "#2d2d2d", accent: "#666666" },
  },
  {
    id: "cyborg",
    name: "Cyborg",
    description: "Cyberpunk cyan/magenta",
    icon: <Cpu className="h-4 w-4" />,
    preview: { bg: "#0d0221", primary: "#00f0ff", accent: "#ff00ff" },
  },
  {
    id: "feminine",
    name: "Feminine",
    description: "Rosa/lavanda suave",
    icon: <Heart className="h-4 w-4" />,
    preview: { bg: "#fff5f7", primary: "#ec4899", accent: "#f472b6" },
  },
  {
    id: "hacker",
    name: "Hacker",
    description: "Terminal CRT verde",
    icon: <Terminal className="h-4 w-4" />,
    preview: { bg: "#0d0208", primary: "#00ff41", accent: "#39ff14" },
  },
  {
    id: "criminalist",
    name: "Criminalist",
    description: "Forense sepia/rojo",
    icon: <Search className="h-4 w-4" />,
    preview: { bg: "#1a1410", primary: "#d4a574", accent: "#dc143c" },
  },
  {
    id: "executive",
    name: "Executive",
    description: "Lujo oro/negro premium",
    icon: <Crown className="h-4 w-4" />,
    preview: { bg: "#0a0a0a", primary: "#d4af37", accent: "#ffd700" },
  },
  {
    id: "anime",
    name: "Anime",
    description: "Manga vibrante rosa/azul",
    icon: <Sparkles className="h-4 w-4" />,
    preview: { bg: "#fff0f5", primary: "#ff1493", accent: "#00bfff" },
  },
  {
    id: "architect",
    name: "Architect",
    description: "Blueprint azul técnico",
    icon: <Ruler className="h-4 w-4" />,
    preview: { bg: "#0a1628", primary: "#5eb3f6", accent: "#90caf9" },
  },
];

interface ThemeSelectorProps {
  onThemeChange?: (theme: ThemeId) => void;
}

export function ThemeSelector({ onThemeChange }: ThemeSelectorProps) {
  const [currentTheme, setCurrentTheme] = useState<ThemeId>("hacker");
  const [isOpen, setIsOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load saved theme
    const saved = localStorage.getItem("atp-theme") as ThemeId;
    if (saved && themes.find(t => t.id === saved)) {
      setCurrentTheme(saved);
      applyTheme(saved);
    } else {
      applyTheme("hacker");
    }
  }, []);

  const applyTheme = (themeId: ThemeId) => {
    document.documentElement.setAttribute("data-theme", themeId);
    // Force re-render of CSS variables
    document.body.style.backgroundColor = "";
    document.body.offsetHeight; // Trigger reflow
  };

  const handleThemeChange = (themeId: ThemeId) => {
    setCurrentTheme(themeId);
    applyTheme(themeId);
    localStorage.setItem("atp-theme", themeId);
    setIsOpen(false);
    onThemeChange?.(themeId);
  };

  const currentThemeData = themes.find(t => t.id === currentTheme);

  if (!mounted) return null;

  return (
    <div className="relative">
      <Button
        variant="ghost"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 h-auto"
      >
        <Palette className="h-4 w-4" />
        <span className="hidden sm:inline text-sm">{currentThemeData?.name}</span>
        <ChevronDown className={cn("h-4 w-4 transition-transform", isOpen && "rotate-180")} />
      </Button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 top-full mt-2 z-50 w-80 max-h-96 overflow-y-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] shadow-2xl">
            <div className="p-3 border-b border-[var(--color-border)]">
              <h3 className="font-bold text-sm" style={{ color: "var(--color-text)" }}>
                Seleccionar Tema
              </h3>
              <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>
                10 temas disponibles
              </p>
            </div>
            
            <div className="p-2 grid grid-cols-2 gap-2">
              {themes.map((theme) => (
                <button
                  key={theme.id}
                  onClick={() => handleThemeChange(theme.id)}
                  className={cn(
                    "flex flex-col items-start p-3 rounded-lg border-2 transition-all duration-200 text-left",
                    currentTheme === theme.id
                      ? "border-[var(--color-primary)] bg-[var(--color-primary)]/10"
                      : "border-transparent hover:border-[var(--color-border)] hover:bg-[var(--color-background)]"
                  )}
                >
                  {/* Preview Colors */}
                  <div className="flex gap-1 mb-2">
                    <div
                      className="w-4 h-4 rounded-full border border-white/20"
                      style={{ backgroundColor: theme.preview.bg }}
                    />
                    <div
                      className="w-4 h-4 rounded-full border border-white/20"
                      style={{ backgroundColor: theme.preview.primary }}
                    />
                    <div
                      className="w-4 h-4 rounded-full border border-white/20"
                      style={{ backgroundColor: theme.preview.accent }}
                    />
                  </div>
                  
                  {/* Theme Info */}
                  <div className="flex items-center gap-2">
                    <span style={{ color: theme.preview.primary }}>
                      {theme.icon}
                    </span>
                    <span 
                      className="font-medium text-sm"
                      style={{ color: "var(--color-text)" }}
                    >
                      {theme.name}
                    </span>
                  </div>
                  <span 
                    className="text-xs mt-1"
                    style={{ color: "var(--color-text-muted)" }}
                  >
                    {theme.description}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
