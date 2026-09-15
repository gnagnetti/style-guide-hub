import index from "@/data/index.json";

export type Lang = "en" | "ru" | "ar" | "hy" | "ka" | "uk" | "lv" | "lt" | "pl";

export interface ColorVariant {
  name: string;
  code: string;
  imageUrl: string | null;
}

export interface OutfitItem {
  name: string;
  code: string;
  imageUrl: string | null;
  modelId?: number;
}

export interface Look {
  title: Record<string, string | null> | string | null;
  text: Record<string, string> | string;
  items: OutfitItem[];
}

export function getLookTitle(look: Look, lang: string): string | null {
  if (!look.title) return null;
  if (typeof look.title === "string") return look.title;
  return look.title[lang] || look.title.en || look.title.ru || null;
}

export function getLookText(look: Look, lang: string): string {
  if (!look.text) return "";
  if (typeof look.text === "string") return look.text;
  return look.text[lang] || look.text.en || look.text.ru || "";
}

export interface Objection {
  q: string;
  a: string;
}

export interface Model {
  id: number;
  name: string;
  description: Record<string, string>;
  colors: ColorVariant[];
  looks: Look[];
  advice: Record<string, string[]>;
  objections: Record<string, Objection[]>;
}

export const modelIndex: { id: number; name: string }[] = index;

const files = import.meta.glob<{ default: Model }>("../data/models/*.json");

export async function loadModel(id: number): Promise<Model | null> {
  const loader = files[`../data/models/${id}.json`];
  if (!loader) return null;
  const mod = await loader();
  return mod.default;
}

export function heroImage(model: Model): string | null {
  return model.colors.find((c) => c.imageUrl)?.imageUrl ?? null;
}
