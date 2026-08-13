"use client";

/**
 * Google's models, called straight from the browser with the reader's own credentials —
 * the same arrangement the repository's Python build uses for its Ask panel.
 *
 * The site holds no key and sees no question: the request goes from the reader's browser
 * to Google. The key is kept in this browser's localStorage and nowhere else; questions
 * and answers are never written to the database, to localStorage, or to any log.
 */

export type Provider = "gemini" | "vertex";

export type AiConfig = {
  /** Which host answers: the Gemini API, or the same models through Vertex AI. */
  provider: Provider;
  /** A Google API key. Both hosts take one; neither needs a project or a token. */
  credential: string;
  textModel?: string;
  imageModel?: string;
};

const STORE = "learn-ai-config";

export const TEXT_MODEL = "gemini-2.5-flash";
export const IMAGE_MODEL = "gemini-2.5-flash-image-preview";

/** The credentials this browser has been given, if any. */
export function loadConfig(): AiConfig | null {
  try {
    const raw = localStorage.getItem(STORE);
    if (!raw) return null;
    const cfg = JSON.parse(raw) as AiConfig;
    return cfg.credential ? cfg : null;
  } catch {
    return null;
  }
}

export function saveConfig(cfg: AiConfig | null) {
  try {
    if (cfg) localStorage.setItem(STORE, JSON.stringify(cfg));
    else localStorage.removeItem(STORE);
  } catch {
    /* private mode: the key simply does not persist */
  }
}

/**
 * The two hosts differ only in their base URL — the same API key works on both, exactly
 * as `genai.Client(api_key=…, vertexai=True)` does in this repository's Python tools.
 * Vertex needs no project and no access token when it is reached this way.
 */
function endpoint(cfg: AiConfig, model: string, stream: boolean) {
  const method = stream ? "streamGenerateContent?alt=sse" : "generateContent";
  const base =
    cfg.provider === "vertex"
      ? "https://aiplatform.googleapis.com/v1/publishers/google/models"
      : "https://generativelanguage.googleapis.com/v1beta/models";
  return `${base}/${model}:${method}`;
}

function headers(cfg: AiConfig): Record<string, string> {
  return { "content-type": "application/json", "x-goog-api-key": cfg.credential };
}

function explain(status: number, body: string) {
  if (status === 403 && /generativelanguage/.test(body)) {
    // A very common case: a key issued for Vertex, pointed at the Gemini API host.
    return "This key is not allowed on the Gemini API. Switch the host to Vertex AI.";
  }
  if (status === 401 || status === 403) {
    return "That key was refused. Check it is valid and that the API is enabled for it.";
  }
  if (status === 404) {
    return "That model is not available to this key. Try another model name in the key settings.";
  }
  if (status === 429) return "Your key is rate limited right now. Try again in a moment.";
  return `The model returned ${status}. ${body.slice(0, 160)}`;
}

async function post(cfg: AiConfig, model: string, body: unknown, stream: boolean) {
  const res = await fetch(endpoint(cfg, model, stream), {
    method: "POST",
    headers: headers(cfg),
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(explain(res.status, await res.text()));
  return res;
}

/** The book, offered to the model as two things it may do. */
export const BOOK_TOOLS = [
  {
    functionDeclarations: [
      {
        name: "search_book",
        description:
          "Search this book and return the most relevant passages. Call this whenever " +
          "the answer depends on what the book says. Prefer specific technical terms " +
          "over whole sentences as the query.",
        parameters: {
          type: "OBJECT",
          properties: {
            query: { type: "STRING", description: "Search terms." },
            limit: { type: "INTEGER", description: "How many passages, 1 to 8. Default 4." },
          },
          required: ["query"],
        },
      },
      {
        name: "read_section",
        description:
          "Read one section of the book in full. Use only when a passage from " +
          "search_book was not enough, passing the path it returned.",
        parameters: {
          type: "OBJECT",
          properties: {
            path: { type: "STRING", description: "A path like /ml-course/unit2/cost-function." },
          },
          required: ["path"],
        },
      },
    ],
  },
];

export type Turn = {
  role: "user" | "model";
  parts: Record<string, unknown>[];
};

type StreamEvent =
  | { type: "text"; text: string }
  | { type: "call"; id: string; name: string; args: Record<string, unknown> };

/**
 * One streamed turn. Yields text as it arrives, and any tool calls the model asks for —
 * the caller runs those and comes back with the results.
 */
async function* streamTurn(
  cfg: AiConfig,
  contents: Turn[],
  system: string | undefined,
  tools: unknown[] | undefined,
): AsyncGenerator<StreamEvent> {
  const res = await post(
    cfg,
    cfg.textModel || TEXT_MODEL,
    {
      contents,
      ...(system ? { systemInstruction: { parts: [{ text: system }] } } : {}),
      ...(tools ? { tools } : {}),
      // The model is answering from passages in front of it, not reasoning its way to
      // something new, so its thinking budget is spent latency for no gain.
      generationConfig: { thinkingConfig: { thinkingBudget: 0 } },
    },
    true,
  );

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let calls = 0;

  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split(/\r?\n\r?\n/);
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const line = frame.split(/\r?\n/).find((l) => l.startsWith("data:"));
      if (!line) continue;
      const payload = line.slice(5).trim();
      if (!payload || payload === "[DONE]") continue;
      try {
        const data = JSON.parse(payload) as {
          candidates?: {
            content?: {
              parts?: {
                text?: string;
                functionCall?: { name: string; args?: Record<string, unknown> };
              }[];
            };
          }[];
        };
        for (const part of data.candidates?.[0]?.content?.parts ?? []) {
          if (part.functionCall) {
            yield {
              type: "call",
              id: `c${calls++}`,
              name: part.functionCall.name,
              args: part.functionCall.args ?? {},
            };
          } else if (part.text) {
            yield { type: "text", text: part.text };
          }
        }
      } catch {
        /* not a JSON frame */
      }
    }
  }
}

/**
 * A full answer, grounded in the book.
 *
 * The passages most likely to bear on the question are fetched first and handed over
 * with it — a few hundred characters each, not whole sections — and the search tools stay
 * available for anything they miss. One round trip answers most questions; the model
 * spends another only when it decides it needs to.
 */
export async function* ask(
  cfg: AiConfig,
  question: string,
  system: string,
  run: (name: string, args: Record<string, unknown>) => Promise<unknown>,
  onLookup?: (name: string, args: Record<string, unknown>) => void,
  primed?: string,
): AsyncGenerator<string> {
  // Retrieval is local and takes a fraction of what a model round trip does, so the
  // first passages are fetched before asking rather than after being asked for. That
  // removes a whole round trip from the common case; the tools remain for the model to
  // dig further when the excerpts are not enough.
  const contents: Turn[] = [
    { role: "user", parts: [{ text: primed ? `${question}\n\n${primed}` : question }] },
  ];

  // A handful of rounds is plenty; the cap stops a confused model looping forever.
  for (let round = 0; round < 4; round++) {
    const calls: { name: string; args: Record<string, unknown> }[] = [];
    let spoke = false;

    for await (const event of streamTurn(cfg, contents, system, BOOK_TOOLS)) {
      if (event.type === "text") {
        spoke = true;
        yield event.text;
      } else {
        calls.push({ name: event.name, args: event.args });
        onLookup?.(event.name, event.args);
      }
    }

    if (!calls.length) return;

    // Record what was asked for and what came back, then let the model continue.
    contents.push({ role: "model", parts: calls.map((c) => ({ functionCall: { name: c.name, args: c.args } })) });
    const results = await Promise.all(calls.map((c) => run(c.name, c.args)));
    contents.push({
      role: "user",
      parts: calls.map((c, i) => ({
        functionResponse: { name: c.name, response: { result: results[i] } },
      })),
    });

    if (spoke) yield "\n\n";
  }
}

/** Streams an answer with no tools, for callers that supply their own context. */
export async function* streamText(
  cfg: AiConfig,
  prompt: string,
  system?: string,
): AsyncGenerator<string> {
  const res = await post(
    cfg,
    cfg.textModel || TEXT_MODEL,
    {
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      ...(system ? { systemInstruction: { parts: [{ text: system }] } } : {}),
    },
    true,
  );

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // Frames are separated by a blank line; a trailing partial frame waits for more.
    const frames = buffer.split(/\r?\n\r?\n/);
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const line = frame.split(/\r?\n/).find((l) => l.startsWith("data:"));
      if (!line) continue;
      const payload = line.slice(5).trim();
      if (!payload || payload === "[DONE]") continue;
      try {
        const data = JSON.parse(payload) as {
          candidates?: { content?: { parts?: { text?: string }[] } }[];
        };
        const text = (data.candidates?.[0]?.content?.parts ?? [])
          .map((p) => p.text ?? "")
          .join("");
        if (text) yield text;
      } catch {
        /* not a JSON frame */
      }
    }
  }
}

/** Asks for a picture, returned as base64 with its mime type. */
export async function generateImage(
  cfg: AiConfig,
  prompt: string,
): Promise<{ data: string; mimeType: string } | null> {
  const res = await post(
    cfg,
    cfg.imageModel || IMAGE_MODEL,
    {
      contents: [
        {
          role: "user",
          parts: [
            { text: `${prompt}\n\nReturn one final generated image. Include image output, not text only.` },
          ],
        },
      ],
      generationConfig: { responseModalities: ["IMAGE"] },
    },
    false,
  );

  const data = (await res.json()) as {
    candidates?: { content?: { parts?: { inlineData?: { mimeType?: string; data?: string } }[] } }[];
  };
  for (const part of data.candidates?.[0]?.content?.parts ?? []) {
    if (part.inlineData?.data) {
      return { data: part.inlineData.data, mimeType: part.inlineData.mimeType ?? "image/png" };
    }
  }
  return null;
}
