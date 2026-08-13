"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { UploadCloud } from "lucide-react";

export default function Uploader() {
  const [hot, setHot] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const input = useRef<HTMLInputElement>(null);
  const router = useRouter();

  async function send(files: FileList | null) {
    if (!files?.length) return;
    setMessage(`Uploading ${files.length} file${files.length > 1 ? "s" : ""}…`);
    for (const file of Array.from(files)) {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("/api/upload", { method: "POST", body: form });
      const data = (await res.json()) as { error?: string };
      if (data.error) {
        setMessage(`${file.name}: ${data.error}`);
        return;
      }
    }
    setMessage(null);
    router.refresh();
  }

  return (
    <>
      {message ? <p className="notice">{message}</p> : null}
      <div
        className={`drop${hot ? " hot" : ""}`}
        onClick={() => input.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setHot(true);
        }}
        onDragLeave={() => setHot(false)}
        onDrop={(e) => {
          e.preventDefault();
          setHot(false);
          send(e.dataTransfer.files);
        }}
      >
        <UploadCloud size={20} strokeWidth={1.6} style={{ margin: "0 auto 8px" }} />
        Drop images here, or click to choose. PNG, JPEG, GIF, WebP, AVIF, SVG — up to 8 MB.
      </div>
      <input
        ref={input}
        type="file"
        accept="image/*"
        multiple
        hidden
        onChange={(e) => {
          send(e.target.files);
          e.target.value = "";
        }}
      />
    </>
  );
}
