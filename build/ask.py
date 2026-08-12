"""The Ask panel: retrieval-augmented answers over the book's own content.

Shared by both books. The page keeps no key of its own: the reader pastes their own
Google credentials, they are stored only in that browser's localStorage, and requests
go straight from the browser to Google. Retrieval runs locally against the same index
the search palette uses, so the model only ever sees excerpts we sent it, and every
answer is asked to cite the sections it used.
"""

ASK_CSS = r"""
/* ---------------- ask panel ---------------- */
.ask-open{display:flex;align-items:center;gap:6px;height:28px;margin-right:2px;padding:0 6px;
  cursor:pointer;border:0;background:none;color:var(--faint);
  font:700 9px/1 var(--mono);letter-spacing:.07em;text-transform:uppercase}
.ask-open:hover{color:var(--blue)}
/* a docked right-hand panel, not a dialog: the page makes room for it */
.ask{position:fixed;right:0;top:0;bottom:0;z-index:40;width:var(--askw,420px);
  display:flex;background:var(--paper);border-left:1px solid var(--line)}
.ask[hidden]{display:none}
.ask-box{position:relative;display:flex;flex-direction:column;width:100%;min-width:0}
.ask-main{flex:1;display:flex;flex-direction:column;min-width:0;min-height:0}

/* ---- chat history, an overlay inside the panel ---- */
.ask-side{position:absolute;inset:0;z-index:3;display:none;flex-direction:column;
  background:var(--side);border-right:0}
.ask.side-open .ask-side{display:flex}
.ask-side-head{display:flex;align-items:center;gap:8px;padding:13px 12px 13px 14px;
  border-bottom:1px solid var(--hair);font:700 9.5px/1 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted)}
.ask-side-head span{flex:1}
.ask-new{display:flex;align-items:center;gap:5px;padding:5px 8px;cursor:pointer;
  border:1px solid var(--hair);border-radius:2px;background:var(--paper);color:var(--ink);
  font:700 9px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.ask-new:hover{border-color:var(--blue);color:var(--blue)}
.ask-list{flex:1;min-height:0;overflow-y:auto;padding:6px}
.chat{position:relative;display:block;width:100%;padding:8px 26px 8px 9px;cursor:pointer;
  border:0;border-left:2px solid transparent;background:none;color:var(--ink);text-align:left;
  font:400 13px/1.45 var(--serif)}
.chat:hover{background:var(--paper)}
.chat.on{background:var(--paper);border-left-color:var(--blue)}
.chat b{display:block;font-weight:400;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap}
.chat span{display:block;margin-top:2px;font:700 8.5px/1.6 var(--mono);letter-spacing:.06em;
  text-transform:uppercase;color:var(--faint)}
.chat-del{position:absolute;right:3px;top:7px;display:grid;place-items:center;width:20px;
  height:20px;padding:0;cursor:pointer;border:0;background:none;color:var(--faint);opacity:0}
.chat:hover .chat-del{opacity:.75}
.chat-del:hover{color:var(--bad);opacity:1}
.ask-none{padding:12px 10px;font:400 12.5px/1.6 var(--serif);color:var(--faint)}
.ask-side-toggle{display:grid;place-items:center;width:26px;height:26px;padding:0;
  cursor:pointer;border:1px solid var(--hair);border-radius:3px;background:none;
  color:var(--muted)}
.ask-side-toggle:hover{color:var(--blue);border-color:var(--line)}
.ask-head{display:flex;align-items:center;gap:9px;padding:13px 16px;
  border-bottom:1px solid var(--hair);font:700 9.5px/1 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted)}
.ask-head .grow{flex:1}
.ask-head button{display:grid;place-items:center;width:26px;height:26px;padding:0;
  cursor:pointer;border:1px solid var(--hair);border-radius:3px;background:none;color:var(--muted)}
.ask-head button:hover{color:var(--blue);border-color:var(--line)}
/* min-height:0 or this flex child grows to fit its content and never scrolls */
.ask-body{flex:1;min-height:0;overflow-y:auto;padding:18px 20px}
/* settings are an overlay, not a block at the top of the transcript: at the bottom of
   a long chat an inline panel would be scrolled out of sight */
.ask-form{position:absolute;inset:0;z-index:4;display:none;flex-direction:column;
  background:var(--paper)}
.ask.configuring .ask-form{display:flex}
.ask-form-body{flex:1;min-height:0;overflow-y:auto;padding:16px 16px 20px}
.ask-form-done{padding:5px 10px;cursor:pointer;border:1px solid var(--hair);border-radius:2px;
  background:var(--side);color:var(--ink);font:700 9px/1 var(--mono);letter-spacing:.06em;
  text-transform:uppercase}
.ask-form-done:hover{border-color:var(--blue);color:var(--blue)}
.ask-row{display:flex;gap:10px;align-items:center;margin:0 0 9px;flex-wrap:wrap}
.ask-row label{flex:0 0 110px;font:700 10px/1.4 var(--mono);letter-spacing:.05em;
  text-transform:uppercase;color:var(--faint)}
.ask-row input,.ask-row select{flex:1;min-width:180px;padding:7px 9px;border:1px solid var(--line);
  background:var(--paper);color:var(--ink);font:400 13px/1.4 var(--mono);border-radius:2px}
.ask-note{margin:10px 0 0;font:400 12px/1.6 var(--serif);color:var(--faint)}
.ask-note code{font-size:.9em}
.ask-ask{display:flex;gap:10px;align-items:flex-end;padding:14px 16px;
  border-top:1px solid var(--hair)}
/* no scrollbar while the box is still growing to fit what you typed */
.ask-ask textarea{flex:1;resize:none;min-height:44px;max-height:160px;padding:10px 12px;
  overflow-y:hidden;border:1px solid var(--line);background:var(--paper);color:var(--ink);
  font:400 15px/1.5 var(--serif);border-radius:2px;outline:none}
.ask-ask textarea:focus{border-color:var(--blue)}
.ask-send{display:grid;place-items:center;width:42px;height:42px;padding:0;cursor:pointer;
  border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:2px}
.ask-send:hover{border-color:var(--blue);color:var(--blue)}
.ask-send[disabled]{opacity:.4;cursor:default}
.turn{margin:0 0 22px}
/* the question needs to read as a question, not as more answer prose */
.turn-q{margin:0 0 14px;padding:10px 13px;font:700 15.5px/1.5 var(--serif);
  background:color-mix(in srgb,var(--blue) 7%,var(--sink));
  border:1px dashed color-mix(in srgb,var(--blue) 55%,transparent);border-radius:2px}
.turn-a{font:400 15.5px/1.72 var(--serif)}
.turn-a p{margin:.7em 0}
.turn-a h4{margin:1.5em 0 .4em;font:700 17.5px/1.35 var(--serif)}
.turn-a h4:first-child{margin-top:0}
.turn-a h5{margin:1.3em 0 .35em;font:700 15.5px/1.4 var(--serif)}
.turn-a blockquote{margin:1.1em 0;padding:2px 14px}
.turn-a blockquote p{font-size:15px}
.turn-a hr{margin:1.4em 0;border:0;border-top:1px solid var(--hair)}
.turn-a ul,.turn-a ol{margin:.7em 0;padding-left:1.3em}
.turn-a li{margin:.25em 0}
.turn-a pre{background:var(--side);border:1px solid var(--hair);padding:12px 14px;
  overflow-x:auto;font:400 13px/1.6 var(--mono)}
.turn-a code{font-size:.87em}
.cite{display:inline-block;min-width:17px;height:17px;margin:0 1px;padding:0 4px;
  border:1px solid var(--line);border-radius:2px;text-align:center;text-decoration:none;
  font:700 10px/16px var(--mono);color:var(--blue);vertical-align:1px}
.cite:hover{border-color:var(--blue);background:var(--side)}
.turn-src{margin:12px 0 0;padding-top:10px;border-top:1px solid var(--hair)}
.turn-src h4{margin:0 0 6px;font:700 9px/1 var(--mono);letter-spacing:.09em;
  text-transform:uppercase;color:var(--faint)}
.turn-src ol{margin:0;padding-left:1.4em;font-size:13.5px}
.turn-src li{margin:.2em 0}
.turn-src a{color:var(--ink);text-decoration:none}
.turn-src a:hover{color:var(--blue)}
.ask-status{font:400 14px/1.6 var(--serif);color:var(--muted)}
.ask-status.bad{color:var(--bad)}
.turn-a.streaming > :last-child::after{content:"";display:inline-block;width:7px;height:14px;
  margin-left:3px;vertical-align:-2px;background:var(--blue);animation:askcaret 1s steps(2) infinite}
@keyframes askcaret{0%,49%{opacity:1}50%,100%{opacity:0}}
@media (max-width:1100px){
  /* no room to dock beside the text, so cover it instead */
  .ask{width:min(460px,100%);box-shadow:-14px 0 44px rgba(0,0,0,.14)}
  html[data-theme=dark] .ask{box-shadow:-14px 0 44px rgba(0,0,0,.5)}
  .ask-row label{flex-basis:100%}
}
"""


# The panel markup is identical in both books and in both layouts. `book` scopes the
# stored chat history, so the two books keep separate histories in the same browser.
def ask_markup(icon, book="book"):
    return f"""<div class="ask" hidden data-book="{book}">
  <div class="ask-box" role="dialog" aria-label="Ask about this book" aria-modal="true">
    <aside class="ask-side">
      <div class="ask-side-head"><span>Chats</span>
        <button class="ask-new" type="button" title="Start a new chat">
          {icon("plus", 12)}<span>New</span></button>
      </div>
      <div class="ask-list"></div>
    </aside>
    <div class="ask-main">
      <div class="ask-head">
        <button class="ask-side-toggle" type="button" title="Chats"
          aria-label="Chat history">{icon("menu", 14)}</button>
        {icon("spark", 15)}<span class="grow">Ask about this book</span>
        <button class="ask-config" type="button" title="Model settings"
          aria-label="Model settings">{icon("gear", 14)}</button>
        <button class="ask-close" type="button" title="Close" aria-label="Close">
          {icon("close", 14)}</button>
      </div>
      <div class="ask-form">
        <div class="ask-side-head"><span>Google model</span>
          <button class="ask-form-done" type="button" title="Done">Done</button>
        </div>
        <div class="ask-form-body">
          <div class="ask-row"><label for="ask-provider">Provider</label>
            <select id="ask-provider">
              <option value="aistudio">AI Studio (Gemini API)</option>
              <option value="vertex">Vertex AI</option>
            </select></div>
          <div class="ask-row"><label for="ask-key">API key</label>
            <input id="ask-key" type="password" placeholder="AIza..." autocomplete="off"></div>
          <div class="ask-row"><label for="ask-model">Model</label>
            <input id="ask-model" type="text" placeholder="gemini-2.5-flash"></div>
          <p class="ask-note">Both providers take a plain API key &mdash; no project, no
          location, no access token. Get an AI Studio key from
          <code>aistudio.google.com</code>, or a Vertex AI key from the Google Cloud
          console. If the key is not valid for the provider you picked, the other one is
          tried automatically. The key stays in this browser's <code>localStorage</code>
          and is sent only to Google; nothing is stored in the page itself.</p>
        </div>
      </div>
      <div class="ask-body">
        <div class="ask-turns"></div>
      </div>
      <div class="ask-ask">
        <textarea rows="1" placeholder="Ask a question about the material..."
          aria-label="Your question"></textarea>
        <button class="ask-send" type="button" title="Send" aria-label="Send">
          {icon("send", 17)}</button>
      </div>
    </div>
  </div>
</div>"""


ASK_JS = r"""
// ---- Ask: retrieval-augmented answers over this book --------------------------
// installAsk({getIndex, hrefFor}) - getIndex(cb) hands over [{u,t,c,h,b}],
// hrefFor(entry) returns the link to that section in this layout.
// A tiny per-book chat store. IndexedDB when it is available (Firefox refuses it on
// file://), localStorage otherwise, so history survives either way.
function chatStore(book) {
  var DB = 'llmcourse-chats', STORE = 'chats', KEY = 'llmcourse-chats:' + book;
  var open = function () {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) { reject(new Error('no indexeddb')); return; }
      var req = indexedDB.open(DB, 1);
      req.onupgradeneeded = function () {
        var db = req.result;
        if (!db.objectStoreNames.contains(STORE)) {
          db.createObjectStore(STORE, { keyPath: 'id' }).createIndex('book', 'book');
        }
      };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error || new Error('indexeddb failed')); };
      req.onblocked = function () { reject(new Error('indexeddb blocked')); };
    });
  };

  // indexedDB.open() can hang without firing success or error - a blocked or
  // partitioned origin does exactly that - so never wait on it indefinitely.
  var guard = function (promise, ms) {
    return new Promise(function (resolve, reject) {
      var settled = false;
      var timer = setTimeout(function () {
        if (!settled) { settled = true; reject(new Error('storage unavailable')); }
      }, ms || 600);
      promise.then(function (value) {
        if (!settled) { settled = true; clearTimeout(timer); resolve(value); }
      }, function (err) {
        if (!settled) { settled = true; clearTimeout(timer); reject(err); }
      });
    });
  };

  var local = {
    all: function () {
      try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
    },
    put: function (chat) {
      var rows = local.all().filter(function (c) { return c.id !== chat.id; });
      rows.push(chat);
      try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch (e) {}
    },
    drop: function (id) {
      var rows = local.all().filter(function (c) { return c.id !== id; });
      try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch (e) {}
    }
  };

  var byNewest = function (rows) {
    return rows.sort(function (a, b) { return b.updated - a.updated; });
  };

  // Whichever backend answers on a given page load has the full history: every write
  // goes to both, and a read merges them, keeping the newer copy of each chat.
  var merge = function (a, b) {
    var seen = {};
    a.concat(b).forEach(function (row) {
      if (!row || !row.id) return;
      if (!seen[row.id] || row.updated > seen[row.id].updated) seen[row.id] = row;
    });
    return byNewest(Object.keys(seen).map(function (id) { return seen[id]; }));
  };

  // the whole round trip is guarded, not just the open: a transaction on a
  // partitioned origin can stall without ever firing an event
  var fromDb = function () {
    return guard(open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var req = db.transaction(STORE, 'readonly').objectStore(STORE).getAll();
        req.onsuccess = function () {
          resolve((req.result || []).filter(function (c) { return c.book === book; }));
        };
        req.onerror = function () { reject(req.error); };
      });
    }), 1500).catch(function () { return []; });
  };

  var toDb = function (run) {
    return guard(open().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(STORE, 'readwrite');
        run(tx.objectStore(STORE));
        tx.oncomplete = resolve;
        tx.onerror = function () { reject(tx.error); };
      });
    }), 1500).catch(function () {});
  };

  return {
    list: function () {
      return fromDb().then(function (rows) { return merge(rows, local.all()); });
    },
    save: function (chat) {
      chat.book = book;
      local.put(chat);
      return toDb(function (store) { store.put(chat); });
    },
    remove: function (id) {
      local.drop(id);
      return toDb(function (store) { store.delete(id); });
    }
  };
}


function installAsk(adapter) {
  var panel = document.querySelector('.ask');
  if (!panel) return;

  var store = chatStore(panel.getAttribute('data-book') || 'book');
  var side = panel.querySelector('.ask-list');
  var chat = null;          // {id, title, turns:[{q, text, sources}], created, updated}
  var chats = [];

  var body = panel.querySelector('.ask-body');
  var turns = panel.querySelector('.ask-turns');
  var box = panel.querySelector('textarea');
  var send = panel.querySelector('.ask-send');
  var STORE = 'llmcourse-ask';
  var index = null, busy = false;

  var fields = {
    provider: panel.querySelector('#ask-provider'),
    model: panel.querySelector('#ask-model'),
    key: panel.querySelector('#ask-key')
  };

  var readConfig = function () {
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) {}
    return {
      provider: saved.provider || 'aistudio',
      model: saved.model || 'gemini-2.5-flash',
      key: saved.key || '',
      host: saved.host || ''          // whichever endpoint actually answered last time
    };
  };
  var writeConfig = function (extra) {
    var cfg = readConfig();
    if (fields.provider.value !== cfg.provider) cfg.host = '';   // honour the new choice
    cfg.provider = fields.provider.value;
    cfg.model = fields.model.value.trim() || 'gemini-2.5-flash';
    cfg.key = fields.key.value.trim();
    if (extra && extra.host) cfg.host = extra.host;
    try { localStorage.setItem(STORE, JSON.stringify(cfg)); } catch (e) {}
    return cfg;
  };
  var rememberHost = function (host) {
    var cfg = readConfig();
    cfg.host = host;
    try { localStorage.setItem(STORE, JSON.stringify(cfg)); } catch (e) {}
  };
  var fillConfig = function () {
    var cfg = readConfig();
    fields.provider.value = cfg.provider;
    fields.model.value = cfg.model;
    fields.key.value = cfg.key;
  };
  var ready = function (cfg) { return !!cfg.key; };

  var esc = function (s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };

  // ---- local retrieval: the same scoring the search palette uses --------------
  var terms = function (q) {
    return q.toLowerCase().split(/[^a-z0-9_.+#]+/).filter(function (t) {
      return t.length > 2 && STOP.indexOf(t) < 0;
    });
  };
  var STOP = ['the', 'and', 'for', 'you', 'your', 'what', 'when', 'how', 'why', 'does',
    'can', 'with', 'this', 'that', 'from', 'are', 'was', 'its', 'use', 'used', 'using',
    'into', 'about', 'between', 'difference', 'explain', 'tell'];

  var passages = function (entry, ts) {
    // slice the article into paragraphs and keep the ones that mention the question
    var parts = entry.b.split(/(?<=\.)\s+(?=[A-Z])/);
    var chunks = [], buf = '';
    parts.forEach(function (part) {
      buf += (buf ? ' ' : '') + part;
      if (buf.length > 420) { chunks.push(buf); buf = ''; }
    });
    if (buf) chunks.push(buf);
    var scored = chunks.map(function (chunk) {
      var low = chunk.toLowerCase(), hit = 0;
      ts.forEach(function (t) { if (low.indexOf(t) >= 0) hit++; });
      return { chunk: chunk, hit: hit };
    }).filter(function (c) { return c.hit > 0; });
    scored.sort(function (a, b) { return b.hit - a.hit; });
    return scored.slice(0, 3).map(function (c) { return c.chunk; }).join(' ... ');
  };

  // Score a section against a list of terms at a given weight. Pulled out so the
  // current question and the carried-over context terms can be scored together.
  var scoreEntry = function (entry, list, weight) {
    if (!list.length) return 0;
    var title = entry.t.toLowerCase(), low = entry.b.toLowerCase(), chap = entry.c.toLowerCase();
    var s = 0;
    list.forEach(function (t) {
      if (title.indexOf(t) >= 0) s += 24 * weight;
      if (chap.indexOf(t) >= 0) s += 4 * weight;
      for (var h = 0; h < entry.h.length; h++) {
        if (entry.h[h].t.toLowerCase().indexOf(t) >= 0) { s += 9 * weight; break; }
      }
      var n = 0, from = 0;
      while ((from = low.indexOf(t, from)) >= 0) { n++; from += t.length; if (n > 8) break; }
      s += Math.min(n, 8) * weight;
    });
    return s;
  };

  // A follow-up like "what about the C#" carries no useful terms on its own, and
  // retrieval never sees the chat history the model gets. So fold the previous
  // question's terms in at reduced weight - history-aware retrieval - which keeps a
  // thin follow-up anchored to what the thread is actually about.
  var retrieve = function (question, want, context) {
    var ts = terms(question);
    var cts = (context ? terms(context) : []).filter(function (t) { return ts.indexOf(t) < 0; });
    var here = adapter.currentKey && adapter.currentKey();
    var pinned = here && index.filter(function (e) { return e.u === here; })[0];
    if (!ts.length && !cts.length) {
      return pinned ? [{ entry: pinned, text: pinned.b.slice(0, 1800) }] : [];
    }
    var ranked = [];
    index.forEach(function (entry) {
      var score = scoreEntry(entry, ts, 1) + scoreEntry(entry, cts, 0.4);
      if (score > 0) ranked.push({ e: entry, s: score });
    });
    ranked.sort(function (a, b) { return b.s - a.s; });
    var picked = ranked.slice(0, want).map(function (r) { return r.e; });
    if (pinned && picked.indexOf(pinned) < 0) picked.unshift(pinned);
    var allTs = ts.concat(cts);
    return picked.map(function (entry) {
      var text = passages(entry, allTs) || entry.b.slice(0, 900);
      return { entry: entry, text: text.slice(0, 1800) };
    });
  };

  // ---- answer rendering ------------------------------------------------------

// ---- a small highlighter for answer code ------------------------------------
// Emits the same class names Pygments uses in the book, so answers pick up the
// existing palette in both themes instead of arriving as flat text.
var WORDS = {
  csharp: 'abstract as async await base bool break byte case catch char checked class const continue decimal default delegate do double dynamic else enum event explicit extern false finally fixed float for foreach get goto if implicit in init int interface internal is lock long namespace new null object operator out override params private protected public readonly record ref required return sbyte sealed set short sizeof stackalloc static string struct switch this throw true try typeof uint ulong unchecked unsafe ushort using var virtual void volatile when where while with yield',
  python: 'and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield match case',
  javascript: 'async await break case catch class const continue debugger default delete do else export extends false finally for function if import in instanceof let new null of return static super switch this throw true try typeof var void while yield',
  bash: 'if then else elif fi for while do done case esac function return export local source echo cd exit set unset',
  json: 'true false null',
  sql: 'select from where group by having order insert update delete create table alter drop join left right inner outer on as and or not null values set distinct limit'
};
var ALIAS = {
  cs: 'csharp', 'c#': 'csharp', py: 'python', js: 'javascript', ts: 'javascript',
  typescript: 'javascript', sh: 'bash', shell: 'bash', console: 'bash',
  dotnetcli: 'bash', powershell: 'bash', yaml: 'json', jsonc: 'json'
};

var hl = function (code, lang) {
  var key = ALIAS[(lang || '').toLowerCase()] || (lang || '').toLowerCase();
  var words = WORDS[key];
  if (!words) return esc(code);
  var keywords = {};
  words.split(' ').forEach(function (w) { keywords[w] = 1; });
  var comment = key === 'python' || key === 'bash' ? /#[^\n]*/ : /\/\/[^\n]*|\/\*[\s\S]*?\*\//;
  var pattern = new RegExp([
    comment.source,
    '@?"(?:[^"\\\\\\n]|\\\\.|"")*"',      // strings, including C# verbatim
    "'(?:[^'\\\\\\n]|\\\\.)*'",
    '`(?:[^`\\\\]|\\\\.)*`',
    '\\b\\d[\\d_]*(?:\\.\\d+)?(?:[eE][-+]?\\d+)?[fFdDmMlLuU]?\\b',
    '#[A-Za-z]+',                          // preprocessor / attributes
    '[A-Za-z_$][A-Za-z0-9_$]*',
    '[{}()\\[\\].,;:=+\\-*/%<>!&|^~?]+'
  ].join('|'), 'g');

  var out = '', last = 0, match;
  var wrap = function (cls, text) { return '<span class="' + cls + '">' + esc(text) + '</span>'; };
  while ((match = pattern.exec(code)) !== null) {
    var piece = match[0];
    out += esc(code.slice(last, match.index));
    last = match.index + piece.length;
    var first = piece.charAt(0);
    if (piece.indexOf('//') === 0 || piece.indexOf('/*') === 0 || (first === '#' && /^#[^A-Za-z]/.test(piece)) ||
        (first === '#' && (key === 'python' || key === 'bash'))) {
      out += wrap('c1', piece);
    } else if (first === '"' || first === "'" || first === '`' || piece.indexOf('@"') === 0) {
      out += wrap('s', piece);
    } else if (/^\d/.test(piece)) {
      out += wrap('mi', piece);
    } else if (first === '#') {
      out += wrap('cp', piece);
    } else if (/^[A-Za-z_$]/.test(piece)) {
      if (keywords[piece]) out += wrap('k', piece);
      else if (code.charAt(last) === '(') out += wrap('nf', piece);
      else if (/^[A-Z]/.test(piece)) out += wrap('nc', piece);
      else out += esc(piece);
    } else {
      out += wrap('p', piece);
    }
  }
  return out + esc(code.slice(last));
};

  // Model output is Markdown, so it needs a real block pass: headings, list items and
  // quotes arrive on their own line without a blank line before them, which a
  // paragraph-splitting renderer runs together into prose.
  var SLOT = '\u0000PRE';

  var inlineBits = function (text, sources) {
    var out = esc(text);
    out = out.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    out = out.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/(^|[\s(])\*([^*\n]+)\*(?=$|[\s.,;:)])/g, '$1<em>$2</em>');
    out = out.replace(/\[([^\]\n]+)\]\((https?:\/\/[^)\s]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>');
    out = out.replace(/\[(\d+)\]/g, function (m, n) {
      var src = sources[parseInt(n, 10) - 1];
      if (!src) return m;
      var entry = src.entry || src;
      return '<a class="cite" href="' + adapter.hrefFor(entry) + '" title="' +
        esc(entry.t) + '">' + n + '</a>';
    });
    return out;
  };

  var codeBlock = function (block) {
    var label = /^(c#|cs|csharp)$/i.test(block.lang) ? 'c#' : (block.lang || 'code');
    return '<div class="codeblock"><span class="lang">' + esc(label) + '</span>' +
      '<div class="hl"><pre><code>' + hl(block.code, block.lang) + '</code></pre></div></div>';
  };

  var lite = function (text, sources) {
    var blocks = [];
    // an unclosed fence is normal mid-stream, so treat end-of-text as a closer
    var body = String(text).replace(/```([\w#+-]*)\n([\s\S]*?)(?:```|$)/g, function (m, lang, code) {
      blocks.push({ lang: lang || '', code: code.replace(/\n$/, '') });
      return '\n' + SLOT + (blocks.length - 1) + '\n';
    });

    var out = [], para = [], list = null;
    var flushPara = function () {
      if (!para.length) return;
      out.push('<p>' + inlineBits(para.join(' '), sources) + '</p>');
      para = [];
    };
    var flushList = function () {
      if (!list) return;
      out.push('<' + list.tag + '>' + list.items.map(function (item) {
        return '<li>' + inlineBits(item, sources) + '</li>';
      }).join('') + '</' + list.tag + '>');
      list = null;
    };
    var flush = function () { flushPara(); flushList(); };

    body.split('\n').forEach(function (line) {
      var slot = line.indexOf(SLOT) === 0 ? line.slice(SLOT.length) : null;
      if (slot !== null && /^\d+$/.test(slot)) {
        flush();
        out.push(codeBlock(blocks[parseInt(slot, 10)]));
        return;
      }
      if (!line.trim()) { flush(); return; }

      var heading = line.match(/^\s{0,3}(#{1,6})\s+(.*)$/);
      if (heading) {
        flush();
        // only two heading levels are useful here, and both must be styled: a bare
        // h5/h6 falls back to the browser default, which is smaller than body text
        var level = heading[1].length <= 3 ? 4 : 5;
        out.push('<h' + level + '>' +
          inlineBits(heading[2].replace(/\s*#+\s*$/, ''), sources) + '</h' + level + '>');
        return;
      }
      if (/^\s{0,3}(?:[-*_]\s*){3,}$/.test(line)) { flush(); out.push('<hr>'); return; }

      var bullet = line.match(/^\s{0,6}([-*+]|\d+[.)])\s+(.*)$/);
      if (bullet) {
        flushPara();
        var tag = /\d/.test(bullet[1]) ? 'ol' : 'ul';
        if (!list || list.tag !== tag) { flushList(); list = { tag: tag, items: [] }; }
        list.items.push(bullet[2]);
        return;
      }
      if (list) {                       // a wrapped continuation of the last item
        list.items[list.items.length - 1] += ' ' + line.trim();
        return;
      }

      var quote = line.match(/^\s{0,3}>\s?(.*)$/);
      if (quote) {
        flush();
        out.push('<blockquote><p>' + inlineBits(quote[1], sources) + '</p></blockquote>');
        return;
      }
      para.push(line.trim());
    });
    flush();
    return out.join('');
  };

  var sourceList = function (sources, text) {
    // list only the sections the answer actually cited, keeping their [n] numbers -
    // retrieval hands over more candidates than the answer ends up drawing on
    var nums = [], re = /\[(\d+)\]/g, m;
    while ((m = re.exec(String(text || ''))) !== null) {
      var n = parseInt(m[1], 10);
      if (n >= 1 && n <= sources.length && nums.indexOf(n) < 0) nums.push(n);
    }
    if (!nums.length) return '';
    nums.sort(function (a, b) { return a - b; });
    var rows = nums.map(function (n) {
      var e = sources[n - 1].entry || sources[n - 1];
      return '<li value="' + n + '"><a href="' + adapter.hrefFor(e) + '">' + esc(e.t) + '</a> ' +
        '<span style="color:var(--faint)">' + esc(e.c) + '</span></li>';
    }).join('');
    return '<div class="turn-src"><h4>Sections used</h4><ol>' + rows + '</ol></div>';
  };

  // Follow the stream only while the reader is already at the bottom, and start each
  // answer with its own question at the top of the view - otherwise a long answer
  // scrolls its own beginning off the screen while it is still being written.
  var atBottom = function () {
    return body.scrollHeight - body.scrollTop - body.clientHeight < 90;
  };

  var addTurn = function (question) {
    var turn = document.createElement('div');
    turn.className = 'turn';
    turn.innerHTML = '<p class="turn-q"></p><div class="turn-a">' +
      '<p class="ask-status">Searching the book...</p></div>';
    turn.querySelector('.turn-q').textContent = question;
    turns.appendChild(turn);
    turn.scrollIntoView({ block: 'start' });
    return turn;
  };

  // ---- chat history --------------------------------------------------------
  var ago = function (ms) {
    var mins = Math.round((nowMs() - ms) / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + 'm ago';
    var hours = Math.round(mins / 60);
    if (hours < 24) return hours + 'h ago';
    var days = Math.round(hours / 24);
    return days < 8 ? days + 'd ago' : new Date(ms).toISOString().slice(0, 10);
  };
  var nowMs = function () { return new Date().getTime(); };

  var TRASH = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9.5 7V5h5v2M6.5 7l1 13h9l1-13"/></svg>';

  var paintList = function () {
    side.innerHTML = '';
    if (!chats.length) {
      side.innerHTML = '<p class="ask-none">No chats yet. Ask something and it is kept here.</p>';
      return;
    }
    chats.forEach(function (row) {
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'chat' + (chat && row.id === chat.id ? ' on' : '');
      item.innerHTML = '<b></b><span>' + esc(ago(row.updated)) + ' &middot; ' +
        row.turns.length + (row.turns.length === 1 ? ' question' : ' questions') +
        '</span><button class="chat-del" type="button" title="Delete chat" ' +
        'aria-label="Delete chat">' + TRASH + '</button>';
      item.querySelector('b').textContent = row.title;
      item.addEventListener('click', function (ev) {
        if (ev.target.closest('.chat-del')) {
          ev.stopPropagation();
          store.remove(row.id).then(function () {
            chats = chats.filter(function (c) { return c.id !== row.id; });
            if (chat && chat.id === row.id) startChat();
            paintList();
          });
          return;
        }
        openChat(row);
      });
      side.appendChild(item);
    });
  };

  var refreshList = function () {
    return store.list().then(function (rows) {
      // the store can answer slower than the chat we just started, so never let a
      // late read drop it off the list
      if (chat && !rows.some(function (row) { return row.id === chat.id; })) {
        rows.unshift(chat);
      }
      chats = rows;
      paintList();
    });
  };

  var paintTurns = function () {
    turns.innerHTML = '';
    if (!chat) return;
    chat.turns.forEach(function (turn) {
      var node = document.createElement('div');
      node.className = 'turn';
      node.innerHTML = '<p class="turn-q"></p><div class="turn-a">' +
        lite(turn.text, turn.sources) + sourceList(turn.sources, turn.text) + '</div>';
      node.querySelector('.turn-q').textContent = turn.q;
      turns.appendChild(node);
    });
    body.scrollTop = body.scrollHeight;
  };

  var startChat = function () {
    chat = null;
    try { sessionStorage.removeItem('llmcourse-ask-chat'); } catch (e) {}
    turns.innerHTML = '';
    paintList();
    panel.classList.remove('side-open');   // the list covers the panel; get out of the way
    box.focus();
  };

  var openChat = function (row) {
    chat = row;
    try { sessionStorage.setItem('llmcourse-ask-chat', row.id); } catch (e) {}
    paintTurns();
    paintList();
    panel.classList.remove('side-open');
  };

  var keep = function (question, text, sources) {
    var slim = sources.map(function (src) {
      return { u: src.entry.u, t: src.entry.t, c: src.entry.c };
    });
    if (!chat) {
      chat = {
        id: 'c' + nowMs() + Math.floor(Math.random() * 1000),
        title: question.length > 68 ? question.slice(0, 68) + '...' : question,
        turns: [], created: nowMs(), updated: nowMs()
      };
      chats.unshift(chat);
    }
    try { sessionStorage.setItem('llmcourse-ask-chat', chat.id); } catch (e) {}
    chat.turns.push({ q: question, text: text, sources: slim });
    chat.updated = nowMs();
    store.save(chat).then(refreshList);
  };

  // ---- the model call --------------------------------------------------------
  // Both endpoints authenticate with a plain API key. A key minted for one is rejected
  // by the other, so the chosen provider is tried first and the other is the fallback.
  var HOSTS = [{ id: 'vertex' }, { id: 'gemini' }];

  var endpointUrl = function (host, cfg, method) {
    var base = host.id === 'vertex'
      ? 'https://aiplatform.googleapis.com/v1/publishers/google/models/'
      : 'https://generativelanguage.googleapis.com/v1beta/models/';
    var url = base + cfg.model + ':' + method + '?key=' + encodeURIComponent(cfg.key);
    return method === 'streamGenerateContent' ? url + '&alt=sse' : url;
  };

  var hostsFor = function (cfg) {
    var wanted = cfg.host || (cfg.provider === 'vertex' ? 'vertex' : 'gemini');
    var first = HOSTS.filter(function (h) { return h.id === wanted; });
    return first.concat(HOSTS.filter(function (h) { return h.id !== wanted; }));
  };

  var textOf = function (data) {
    var cand = (data.candidates || [])[0] || {};
    var parts = (cand.content && cand.content.parts) || [];
    return parts.map(function (part) { return part.text || ''; }).join('');
  };
  var worthRetrying = function (status) { return [400, 401, 403, 404].indexOf(status) >= 0; };

  // Read Server-Sent Events as they arrive and hand each delta straight to the page.
  var readStream = function (res, onDelta) {
    var reader = res.body.getReader();
    var decoder = new TextDecoder();
    var buffer = '', whole = '';
    var pump = function () {
      return reader.read().then(function (chunk) {
        if (chunk.done) return whole;
        buffer += decoder.decode(chunk.value, { stream: true });
        var lines = buffer.split('\n');
        buffer = lines.pop();                   // hold the partial line for the next chunk
        lines.forEach(function (line) {
          line = line.replace(/\r$/, '');
          if (line.indexOf('data:') !== 0) return;
          var body = line.slice(5).trim();
          if (!body || body === '[DONE]') return;
          var delta;
          try { delta = textOf(JSON.parse(body)); } catch (e) { return; }
          if (delta) { whole += delta; onDelta(whole, delta); }
        });
        return pump();
      });
    };
    return pump();
  };

  var callModel = function (cfg, payload, hosts, onDelta, lastError) {
    if (!hosts.length) return Promise.reject(lastError || new Error('No endpoint answered.'));
    var host = hosts[0];
    var stream = !!(onDelta && window.TextDecoder);
    var method = stream ? 'streamGenerateContent' : 'generateContent';

    return fetch(endpointUrl(host, cfg, method), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (res) {
      if (!res.ok) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          var err = new Error((data && data.error && data.error.message) || ('HTTP ' + res.status));
          // a key or model the other host may still accept
          if (worthRetrying(res.status)) {
            return callModel(cfg, payload, hosts.slice(1), onDelta, err);
          }
          throw err;
        });
      }
      rememberHost(host.id);
      if (stream && res.body && res.body.getReader) return readStream(res, onDelta);
      // answered, but cannot stream here: take the whole thing in one go
      return res.json().then(function (data) {
        var all = textOf(data);
        if (all && onDelta) onDelta(all, all);
        return all;
      });
    }, function (netErr) {
      return callModel(cfg, payload, hosts.slice(1), onDelta, netErr);
    });
  };

  var ask = function (question) {
    var cfg = readConfig();
    var turn = addTurn(question);
    var answer = turn.querySelector('.turn-a');

    // carry the previous question so a short follow-up still retrieves on-thread
    var priorQ = (chat && chat.turns.length) ? chat.turns[chat.turns.length - 1].q : '';
    var sources = retrieve(question, 6, priorQ);
    if (!sources.length) {
      answer.innerHTML = '<p class="ask-status bad">Nothing in this book looks related to that.</p>';
      return Promise.resolve();
    }

    var context = sources.map(function (src, i) {
      return '[' + (i + 1) + '] ' + src.entry.c + ' > ' + src.entry.t + '\n' + src.text;
    }).join('\n\n');

    // Grounded, but not stiff: the old wording asked the model to report on its own
    // excerpts, which made every answer open with what the excerpts do or do not say.
    var prompt =
      'You are helping someone read a technical book. Answer their question.\n\n' +
      'The numbered sections below are from the book they are reading. Ground your\n' +
      'answer in them and cite them inline as [1], [2] where you draw on them.\n\n' +
      'How to answer:\n' +
      '- Lead with the answer. Never open by describing the excerpts or what they do\n' +
      '  or do not contain, and never mention "excerpts", "context" or "sections" as\n' +
      '  things the reader can see.\n' +
      '- Write plainly and directly, the way a good teacher explains something.\n' +
      '- Answer exactly what was asked and match the size of the answer to the size\n' +
      '  of the question. A short or simple question gets a short answer, a sentence\n' +
      '  or two, with no headings or lists. Do not pad, do not add sections the reader\n' +
      '  did not ask for, and do not volunteer tangents or alternatives unless asked.\n' +
      '- Add background only when it is needed to make the direct answer make sense,\n' +
      '  and keep it to the minimum. Never invent specifics that the book does not\n' +
      '  state.\n' +
      '- Do not invent specifics: no APIs, flags, numbers, versions or behaviour that\n' +
      '  the book does not state. If a specific is not covered, say what is true in\n' +
      '  general and leave it there.\n' +
      '- If the message is a greeting or small talk rather than a question about the\n' +
      '  book (for example "hi", "hello", "thanks"), do not answer from the sections\n' +
      '  and do not cite them. Reply with one short, friendly line and invite them to\n' +
      '  ask about the book.\n' +
      '- Only if the book genuinely says nothing on the topic, say so in one short\n' +
      '  sentence and point to the nearest thing it does cover.\n' +
      '- Use Markdown: short paragraphs, `code` for identifiers, fenced blocks for code,\n' +
      '  a list only when the content really is a list.\n\n' +
      'BOOK SECTIONS\n' + context + '\n\nQUESTION\n' + question;

    answer.innerHTML = '<p class="ask-status">Asking ' + esc(cfg.model) + '...</p>';

    // carry the last few turns so follow-ups ("and why is that?") make sense
    var history = [];
    if (chat && chat.turns.length) {
      chat.turns.slice(-3).forEach(function (turn) {
        history.push({ role: 'user', parts: [{ text: turn.q }] });
        history.push({ role: 'model', parts: [{ text: turn.text }] });
      });
    }

    var payload = {
      contents: history.concat([{ role: 'user', parts: [{ text: prompt }] }]),
      generationConfig: { temperature: 0.4, maxOutputTokens: 2048 }
    };

    // repaint on a frame boundary: repainting per token would thrash the layout
    var pending = null, painting = false, settled = false;
    var draw = function () {
      painting = false;
      // a frame queued mid-stream must not land after the final answer, or it
      // would repaint without the sources list
      if (settled || pending === null) return;
      var follow = atBottom();
      answer.innerHTML = lite(pending, sources);
      if (follow) body.scrollTop = body.scrollHeight;
    };
    var onDelta = function (whole) {
      pending = whole;
      answer.classList.add('streaming');
      if (painting) return;
      painting = true;
      requestAnimationFrame(draw);
    };
    var finish = function (markup) {
      settled = true;
      answer.classList.remove('streaming');
      answer.innerHTML = markup;
    };

    return callModel(cfg, payload, hostsFor(cfg), onDelta).then(function (text) {
      text = (text || '').trim();
      if (!text) throw new Error('The model returned nothing.');
      finish(lite(text, sources) + sourceList(sources, text));
      keep(question, text, sources);
    }).catch(function (err) {
      finish('<p class="ask-status bad">' + esc(err.message) + '</p>');
    }).then(function () {
      if (atBottom()) body.scrollTop = body.scrollHeight;
    });
  };

  // ---- wiring ----------------------------------------------------------------
  var SEEN = 'llmcourse-ask-open';
  var open = function (quiet) {
    panel.hidden = false;
    document.documentElement.classList.add('with-ask');
    try { sessionStorage.setItem(SEEN, '1'); } catch (e) {}
    fillConfig();
    if (!ready(readConfig())) panel.classList.add('configuring');
    adapter.getIndex(function (data) { index = data; });
    refreshList();
    relayout();
    if (!quiet) box.focus();
  };
  var close = function () {
    panel.hidden = true;
    panel.classList.remove('side-open');
    panel.classList.remove('configuring');
    document.documentElement.classList.remove('with-ask');
    try { sessionStorage.removeItem(SEEN); } catch (e) {}
    relayout();
  };

  // The page reflows around the docked panel, and the reading ruler is hidden while it
  // is open. Anything that measures the layout has to measure it again afterwards, or
  // the ruler keeps the positions it computed while it had no height.
  function relayout() {
    requestAnimationFrame(function () {
      window.dispatchEvent(new Event('resize'));
    });
  }

  var submit = function () {
    var question = box.value.trim();
    if (!question || busy) return;
    var cfg = readConfig();
    if (!ready(cfg)) {
      panel.classList.add('configuring');
      addTurn(question).querySelector('.turn-a').innerHTML =
        '<p class="ask-status bad">Add your Google API key above first.</p>';
      return;
    }
    if (!index) {
      adapter.getIndex(function (data) { index = data; submit(); });
      return;
    }
    box.value = '';
    sizeBox();
    busy = true;
    send.disabled = true;
    ask(question).then(function () { busy = false; send.disabled = false; box.focus(); });
  };

  Array.prototype.forEach.call(panel.querySelectorAll('.ask-form input,.ask-form select'), function (el) {
    el.addEventListener('change', function () { writeConfig(); });
    el.addEventListener('blur', function () { writeConfig(); });
  });
  panel.querySelector('.ask-new').addEventListener('click', startChat);
  panel.querySelector('.ask-side-toggle').addEventListener('click', function () {
    panel.classList.toggle('side-open');
  });
  panel.querySelector('.ask-config').addEventListener('click', function () {
    panel.classList.toggle('configuring');
    if (panel.classList.contains('configuring')) fields.key.focus();
  });
  panel.querySelector('.ask-form-done').addEventListener('click', function () {
    writeConfig();
    panel.classList.remove('configuring');
    box.focus();
  });
  panel.querySelector('.ask-close').addEventListener('click', close);
  // a citation opens the section behind the panel; the panel stays where it is
  panel.addEventListener('click', function (ev) {
    var jump = ev.target.closest('.cite, .turn-src a');
    if (!jump) return;
    var href = jump.getAttribute('href') || '';
    if (href.charAt(0) !== '#') return;          // page-per-section build: let it navigate
    ev.preventDefault();
    if (location.hash === href) {
      var here = document.getElementById(href.slice(1).split('--').pop());
      if (here) here.scrollIntoView({ behavior: 'smooth' });
    } else {
      location.hash = href;
    }
  });
  send.addEventListener('click', submit);
  var sizeBox = function () {
    box.style.height = 'auto';
    var wanted = box.scrollHeight;
    box.style.height = Math.min(160, wanted) + 'px';
    box.style.overflowY = wanted > 160 ? 'auto' : 'hidden';
  };
  box.addEventListener('input', sizeBox);
  box.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); submit(); }
    if (ev.key === 'Escape') close();
  });
  document.addEventListener('click', function (ev) {
    if (ev.target.closest('.ask-open')) panel.hidden ? open() : close();
  });

  // in the page-per-section build a citation loads another page, so bring the panel
  // and its open chat back with it
  var wasOpen = null;
  try { wasOpen = sessionStorage.getItem(SEEN); } catch (e) {}
  if (wasOpen) {
    open(true);
    var lastId = null;
    try { lastId = sessionStorage.getItem('llmcourse-ask-chat'); } catch (e) {}
    if (lastId) {
      store.list().then(function (rows) {
        chats = rows;
        var found = rows.filter(function (row) { return row.id === lastId; })[0];
        if (found) openChat(found); else paintList();
      });
    }
  }
  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'i' || ev.key === 'I')) {
      ev.preventDefault();
      panel.hidden ? open() : close();
    } else if (ev.key === 'Escape' && !panel.hidden) {
      if (panel.classList.contains('configuring')) panel.classList.remove('configuring');
      else if (panel.classList.contains('side-open')) panel.classList.remove('side-open');
      else close();
    }
  });
}
"""
