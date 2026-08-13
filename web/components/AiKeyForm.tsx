"use client";

import { useState } from "react";
import { saveConfig, type AiConfig, type Provider } from "@/lib/ai-browser";

/**
 * Where a key and the models to use with it are entered.
 *
 * Shared by the reader's Ask panel and the editor's diagram generator, because both run
 * on the same credentials — and because an error telling someone to "try another model"
 * is useless if the only place to change it is a screen they are not on.
 */
export default function AiKeyForm({
  config,
  onDone,
  onCancel,
}: {
  config: AiConfig | null;
  onDone: (cfg: AiConfig) => void;
  onCancel?: () => void;
}) {
  // Vertex by default: it is the host this project's own tools use, and keys issued for
  // it are commonly blocked on the Gemini API.
  const [provider, setProvider] = useState<Provider>(config?.provider ?? "vertex");
  const [credential, setCredential] = useState(config?.credential ?? "");
  const [textModel, setTextModel] = useState(config?.textModel ?? "");
  const [imageModel, setImageModel] = useState(config?.imageModel ?? "");

  return (
    <form
      className="ask-key"
      onSubmit={(e) => {
        e.preventDefault();
        if (!credential.trim()) return;
        const next: AiConfig = {
          provider,
          credential: credential.trim(),
          ...(textModel.trim() ? { textModel: textModel.trim() } : {}),
          ...(imageModel.trim() ? { imageModel: imageModel.trim() } : {}),
        };
        // Saved here rather than by the caller: the editor forgot to, so a model typed
        // there was gone by the next request while the same form worked in the panel.
        saveConfig(next);
        onDone(next);
      }}
    >
      <p className="ask-none">
        Answers use your own Google API key. It is stored only in this browser and sent
        only to Google — this site never receives it, and no question or answer is saved
        anywhere.
      </p>

      <label className="field">
        <span>Host — the same key works on either</span>
        <select value={provider} onChange={(e) => setProvider(e.target.value as Provider)}>
          <option value="gemini">Gemini API</option>
          <option value="vertex">Vertex AI</option>
        </select>
      </label>

      <label className="field mono">
        <span>API key</span>
        <input
          value={credential}
          onChange={(e) => setCredential(e.target.value)}
          placeholder="AIza…"
          autoFocus
          type="password"
        />
      </label>

      <label className="field mono">
        <span>Text model</span>
        <input
          value={textModel}
          onChange={(e) => setTextModel(e.target.value)}
          placeholder="Model id"
        />
      </label>

      <label className="field mono">
        <span>Image model</span>
        <input
          value={imageModel}
          onChange={(e) => setImageModel(e.target.value)}
          placeholder="Model id"
        />
      </label>

      <div className="btn-row">
        <button className="btn primary" type="submit">
          Use this key
        </button>
        {onCancel ? (
          <button className="btn" type="button" onClick={onCancel}>
            Cancel
          </button>
        ) : null}
        {config ? (
          <button
            className="btn danger"
            type="button"
            onClick={() => {
              saveConfig(null);
              location.reload();
            }}
          >
            Forget
          </button>
        ) : null}
      </div>
    </form>
  );
}
