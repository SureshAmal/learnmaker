import { ChevronUp, ChevronDown } from "lucide-react";
import { move } from "@/app/admin/actions";

/** Up/down reordering for a book, chapter or section row. */
export default function MoveButtons({
  kind,
  id,
  first,
  last,
}: {
  kind: "book" | "chapter" | "section";
  id: number;
  first: boolean;
  last: boolean;
}) {
  return (
    <span style={{ display: "flex", gap: 2 }}>
      <form action={move}>
        <input type="hidden" name="kind" value={kind} />
        <input type="hidden" name="id" value={id} />
        <input type="hidden" name="dir" value="up" />
        <button className="nudge" type="submit" aria-label="Move up" disabled={first}>
          <ChevronUp size={14} strokeWidth={1.7} />
        </button>
      </form>
      <form action={move}>
        <input type="hidden" name="kind" value={kind} />
        <input type="hidden" name="id" value={id} />
        <input type="hidden" name="dir" value="down" />
        <button className="nudge" type="submit" aria-label="Move down" disabled={last}>
          <ChevronDown size={14} strokeWidth={1.7} />
        </button>
      </form>
    </span>
  );
}
