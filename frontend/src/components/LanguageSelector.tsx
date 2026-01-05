"use client";

import { useState, useEffect } from "react";
import { Languages } from "lucide-react";
import { Language, getCurrentLanguage, setCurrentLanguage } from "@/lib/i18n";

interface LanguageSelectorProps {
  onLanguageChange?: (lang: Language) => void;
}

export function LanguageSelector({ onLanguageChange }: LanguageSelectorProps) {
  const [currentLang, setCurrentLang] = useState<Language>('es');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const lang = getCurrentLanguage();
    setCurrentLang(lang);
  }, []);

  const toggleLanguage = () => {
    const newLang: Language = currentLang === 'es' ? 'en' : 'es';
    setCurrentLang(newLang);
    setCurrentLanguage(newLang);
    onLanguageChange?.(newLang);
    
    // Reload page to apply language changes
    window.location.reload();
  };

  if (!mounted) return null;

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-2 rounded-lg bg-card border border-border hover:bg-muted transition-colors"
      title={currentLang === 'es' ? 'Cambiar a Inglés' : 'Switch to Spanish'}
    >
      <Languages className="h-4 w-4 text-primary" />
      <span className="text-sm font-medium">{currentLang.toUpperCase()}</span>
    </button>
  );
}
