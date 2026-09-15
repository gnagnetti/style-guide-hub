import index from "@/data/index.json";

export type Lang = "en" | "ru";

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
  title: string | null;
  text: string;
  items: OutfitItem[];
}

export interface Objection {
  q: string;
  a: string;
}

export interface Model {
  id: number;
  name: string;
  description: Record<Lang, string>;
  colors: ColorVariant[];
  looks: Look[];
  advice: Record<Lang, string[]>;
  objections: Record<Lang, Objection[]>;
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
