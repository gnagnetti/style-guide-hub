import { useMemo, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { Check, ChevronsUpDown, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { modelIndex } from "@/lib/models";
import { useLanguage } from "@/lib/language";
import { cn } from "@/lib/utils";

export function ModelPicker() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);

  const options = useMemo(
    () => [...modelIndex].sort((a, b) => a.name.localeCompare(b.name)),
    [],
  );
  const current = options.find((o) => o.id === selected);

  const go = () => {
    if (selected != null) navigate({ to: "/model/$id", params: { id: String(selected) } });
  };

  return (
    <div className="space-y-3">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="h-12 w-full justify-between border-border bg-card px-4 text-left font-normal"
          >
            <span className={cn("truncate", !current && "text-muted-foreground")}>
              {current ? current.name : t("selectModel")}
            </span>
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 text-gold" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0" align="start">
          <Command>
            <CommandInput placeholder={t("searchPlaceholder")} />
            <CommandList>
              <CommandEmpty>{t("noResults")}</CommandEmpty>
              <CommandGroup>
                {options.map((o) => (
                  <CommandItem
                    key={o.id}
                    value={o.name}
                    onSelect={() => {
                      setSelected(o.id);
                      setOpen(false);
                      navigate({ to: "/model/$id", params: { id: String(o.id) } });
                    }}
                  >
                    <Check className={cn("mr-2 h-4 w-4", selected === o.id ? "opacity-100" : "opacity-0")} />
                    {o.name}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>

      <Button
        onClick={go}
        disabled={selected == null}
        className="h-12 w-full bg-gold text-gold-foreground tracking-[0.2em] uppercase hover:bg-gold/90"
      >
        <Search className="mr-2 h-4 w-4" />
        {t("search")}
      </Button>
    </div>
  );
}
