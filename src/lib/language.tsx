import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import type { Lang } from "./models";

const KEY = "ls-training-lang";

interface Ctx {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (k: keyof typeof strings) => string;
}

const strings = {
  brandSub: { en: "Training Material FW 2026/2027", ru: "Учебные материалы Осень-Зима 2026/2027" },
  pageTitle: { en: "Training Material Fall Winter 2026/2027", ru: "Учебные материалы Осень-Зима 2026/2027" },
  selectModel: { en: "Select a model", ru: "Выберите модель" },
  searchPlaceholder: { en: "Search model…", ru: "Поиск модели…" },
  search: { en: "SEARCH", ru: "ПОИСК" },
  noResults: { en: "No model found", ru: "Модель не найдена" },
  analysis: { en: "ANALYSIS", ru: "АНАЛИЗ" },
  description: { en: "Description", ru: "Описание" },
  colors: { en: "Color Variants", ru: "Варианты цвета" },
  styling: { en: "Styling & Combinations", ru: "Стайлинг и сочетания" },
  advice: { en: "Sales Advice", ru: "Советы по продажам" },
  objections: { en: "Objection Handling", ru: "Управление возражениями" },
  back: { en: "All models", ru: "Все модели" },
  noImage: { en: "No image", ru: "Нет изображения" },
  intro: {
    en: "Choose a model to open its full training sheet: description, colours, total looks, sales advice and objection handling.",
    ru: "Выберите модель, чтобы открыть полную карточку: описание, цвета, образы, советы по продажам и работа с возражениями.",
  },
  models: { en: "models", ru: "моделей" },
} as const;

const LanguageContext = createContext<Ctx>({ lang: "en", setLang: () => {}, t: (k) => strings[k].en });

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");

  useEffect(() => {
    const stored = localStorage.getItem(KEY);
    if (stored === "ru" || stored === "en") setLangState(stored);
  }, []);

  const setLang = useCallback((l: Lang) => {
    setLangState(l);
    localStorage.setItem(KEY, l);
  }, []);

  const t = useCallback((k: keyof typeof strings) => strings[k][lang], [lang]);

  return <LanguageContext.Provider value={{ lang, setLang, t }}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  return useContext(LanguageContext);
}
