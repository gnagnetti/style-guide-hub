import { Link } from "@tanstack/react-router";
import { useLanguage } from "@/lib/language";
import { cn } from "@/lib/utils";

export function Header() {
  const { lang, setLang, t } = useLanguage();

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-2xl items-center justify-between gap-3 px-4 py-3">
        <Link to="/" className="min-w-0">
          <p className="font-display text-base leading-none font-semibold tracking-[0.22em] text-foreground uppercase">
            Luisa Spagnoli
          </p>
          <p className="mt-1 truncate text-[11px] tracking-wide text-muted-foreground">{t("brandSub")}</p>
        </Link>
        <div className="flex shrink-0 items-center rounded-full border border-gold/40 p-0.5">
          {(["en", "ru"] as const).map((l) => (
            <button
              key={l}
              type="button"
              onClick={() => setLang(l)}
              aria-pressed={lang === l}
              className={cn(
                "rounded-full px-3 py-1 text-xs font-semibold tracking-widest uppercase transition-colors",
                lang === l ? "bg-gold text-gold-foreground" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {l}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
