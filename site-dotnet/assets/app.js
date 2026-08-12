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

(function () {
  'use strict';

  var root = document.documentElement;

  // ---- theme (the inline head script already picked it; this only toggles) --
  var themeBtn = document.querySelector('.theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('llmcourse-theme', next); } catch (e) {}
    });
  }

  // ---- contents drawer -----------------------------------------------------
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () { document.body.classList.toggle('nav-open'); });
  }
  document.addEventListener('click', function (ev) {
    if (!document.body.classList.contains('nav-open')) return;
    if (ev.target.closest('.sidebar') || ev.target.closest('.nav-toggle')) return;
    document.body.classList.remove('nav-open');
  });
  var active = document.querySelector('.sidebar a.active');
  if (active) active.scrollIntoView({ block: 'center' });

  // ---- copy buttons --------------------------------------------------------
  var COPY = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 012-2h9"/></svg>';
  var DONE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.5 5.5L20 6.5"/></svg>';

  Array.prototype.forEach.call(document.querySelectorAll('.codeblock'), function (block) {
    var pre = block.querySelector('pre');
    if (!pre) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy';
    btn.title = 'Copy code';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = COPY;
    block.appendChild(btn);
    btn.addEventListener('click', function () {
      var text = pre.innerText;
      var done = function () {
        btn.innerHTML = DONE;
        btn.classList.add('done');
        setTimeout(function () { btn.innerHTML = COPY; btn.classList.remove('done'); }, 1300);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, done); return; }
      var ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta); done();
    });
  });

  // ---- quizzes -------------------------------------------------------------
  Array.prototype.forEach.call(document.querySelectorAll('.quiz'), function (quiz) {
    var btn = quiz.querySelector('.btn-check');
    var verdict = quiz.querySelector('.verdict');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var picked = 0, wrong = 0, missed = 0;
      Array.prototype.forEach.call(quiz.querySelectorAll('.choice'), function (choice) {
        var input = choice.querySelector('input');
        var isCorrect = input.getAttribute('data-correct') === 'true';
        choice.classList.remove('right', 'wrong-picked');
        if (isCorrect) choice.classList.add('right');
        if (input.checked) {
          picked++;
          if (!isCorrect) { wrong++; choice.classList.add('wrong-picked'); }
        } else if (isCorrect) { missed++; }
      });
      quiz.classList.add('revealed');
      if (!picked) { verdict.textContent = 'Pick an answer'; verdict.className = 'verdict bad'; return; }
      if (!wrong && !missed) { verdict.textContent = 'Correct'; verdict.className = 'verdict ok'; }
      else { verdict.textContent = 'Not quite'; verdict.className = 'verdict bad'; }
    });
  });

  // ---- reading ruler: progress ticks plus a hover outline of the sections ---
  var ruler = document.querySelector('.ruler');
  if (ruler) {
    var ticks = ruler.querySelector('.ticks');
    var lane = ruler.querySelector('.marks');
    var pct = ruler.querySelector('.pct');

    var COUNT = 46, bars = [];
    for (var i = 0; i < COUNT; i++) {
      var tick = document.createElement('i');
      ticks.appendChild(tick);
      bars.push(tick);
    }

    // one labelled mark per top-level section, parked at its place in the page
    var heads = [].slice.call(document.querySelectorAll('.lesson h2[id], .lesson h2 > a.anchor'));
    var seen = {}, marks = [];
    heads.forEach(function (node) {
      var head = node.tagName === 'A' ? node.parentNode : node;
      var anchor = node.id || (head.querySelector('a.anchor') || {}).id;
      if (!anchor || seen[anchor]) return;
      seen[anchor] = 1;
      var label = head.textContent.replace(/#\s*$/, '').trim();
      var mark = document.createElement('a');
      mark.className = 'mark';
      mark.href = '#' + anchor;
      mark.innerHTML = '<span class="lbl"></span><i></i>';
      mark.querySelector('.lbl').textContent = label;
      lane.appendChild(mark);
      marks.push({ el: mark, head: head });
    });

    // Sections that sit close together in the page would stack their labels on top of
    // each other, so nudge them apart: push down, then push the tail back up.
    var place = function () {
      var docH = document.documentElement.scrollHeight;
      var laneH = lane.clientHeight;
      if (!laneH || !marks.length) return;
      var GAP = 17;
      var items = marks.map(function (m) {
        var top = m.head.getBoundingClientRect().top + window.scrollY;
        return { m: m, y: Math.max(0, Math.min(laneH, (top / docH) * laneH)) };
      });
      items.sort(function (a, b) { return a.y - b.y; });
      for (var i = 1; i < items.length; i++) {
        if (items[i].y - items[i - 1].y < GAP) items[i].y = items[i - 1].y + GAP;
      }
      var lastItem = items[items.length - 1];
      if (lastItem.y > laneH) lastItem.y = laneH;
      for (var j = items.length - 1; j > 0; j--) {
        if (items[j].y - items[j - 1].y < GAP) items[j - 1].y = items[j].y - GAP;
      }
      items.forEach(function (it) { it.m.el.style.top = Math.max(0, it.y) + 'px'; });
    };

    var last = -1, current = null;
    var update = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      pct.textContent = (ratio * 100).toFixed(2);
      pct.style.top = (ratio * 100) + '%';
      var idx = Math.round(ratio * (COUNT - 1));
      if (idx !== last) {
        if (last >= 0) bars[last].classList.remove('on');
        bars[idx].classList.add('on');
        last = idx;
      }
      var here = null, edge = window.innerHeight * 0.28;
      marks.forEach(function (m) {
        if (m.head.getBoundingClientRect().top <= edge) here = m;
      });
      if (here !== current) {
        if (current) current.el.classList.remove('here');
        if (here) here.el.classList.add('here');
        current = here;
      }
    };

    place();
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', function () { place(); update(); });
    window.addEventListener('load', function () { place(); update(); });
    // images settle late and shift every offset with them
    setTimeout(function () { place(); update(); }, 900);
  }

  // ---- Ctrl+K search -------------------------------------------------------
  var palette = document.querySelector('.palette');
  if (palette) {
    var field = palette.querySelector('input');
    var list = palette.querySelector('.palette-results');
    var hits = palette.querySelector('.hits');
    var base = palette.getAttribute('data-base') || '';
    var loading = false, index = null, rows = [], cursor = -1;

    var esc = function (s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    };
    var terms = function (q) {
      return q.toLowerCase().split(/[^a-z0-9_.+#]+/).filter(function (t) { return t.length > 1; });
    };
    var highlight = function (text, ts) {
      var low = text.toLowerCase(), spans = [];
      ts.forEach(function (t) {
        var from = 0, at;
        while ((at = low.indexOf(t, from)) >= 0) { spans.push([at, at + t.length]); from = at + t.length; }
      });
      if (!spans.length) return esc(text);
      spans.sort(function (a, b) { return a[0] - b[0]; });
      var merged = [], cur = spans[0].slice();
      for (var i = 1; i < spans.length; i++) {
        if (spans[i][0] <= cur[1]) cur[1] = Math.max(cur[1], spans[i][1]);
        else { merged.push(cur); cur = spans[i].slice(); }
      }
      merged.push(cur);
      var out = '', pos = 0;
      merged.forEach(function (span) {
        out += esc(text.slice(pos, span[0])) + '<mark>' + esc(text.slice(span[0], span[1])) + '</mark>';
        pos = span[1];
      });
      return out + esc(text.slice(pos));
    };

    // pull a readable window of body text around the first match
    var snippet = function (body, ts) {
      var low = body.toLowerCase(), at = -1;
      for (var i = 0; i < ts.length && at < 0; i++) at = low.indexOf(ts[i]);
      if (at < 0) return body.slice(0, 150) + '...';
      var from = Math.max(0, at - 70), to = Math.min(body.length, at + 130);
      return (from ? '...' : '') + body.slice(from, to).trim() + (to < body.length ? '...' : '');
    };

    var score = function (entry, ts) {
      var title = entry.t.toLowerCase(), chapter = entry.c.toLowerCase();
      var body = entry.b.toLowerCase(), total = 0, hit;
      for (var i = 0; i < ts.length; i++) {
        var t = ts[i], any = 0;
        if (title.indexOf(t) >= 0) { total += 30; any = 1; }
        if (chapter.indexOf(t) >= 0) { total += 6; any = 1; }
        for (var h = 0; h < entry.h.length; h++) {
          if (entry.h[h].t.toLowerCase().indexOf(t) >= 0) { total += 10; any = 1; break; }
        }
        var n = 0, from = 0;
        while ((from = body.indexOf(t, from)) >= 0) { n++; from += t.length; if (n > 12) break; }
        if (n) { total += Math.min(n, 12); any = 1; }
        if (!any) return 0;                       // every term has to appear somewhere
      }
      if (ts.length > 1 && (title + ' ' + body).indexOf(ts.join(' ')) >= 0) total += 25;
      return total;
    };

    var render = function () {
      var q = field.value.trim();
      var ts = terms(q);
      list.innerHTML = '';
      rows = [];
      cursor = -1;
      if (!index) { list.innerHTML = '<p class="palette-empty">Loading the index...</p>'; return; }
      if (!ts.length) {
        list.innerHTML = '<p class="palette-empty">Type to search titles, headings and body text.</p>';
        hits.textContent = index.length + ' sections';
        return;
      }
      var found = [];
      index.forEach(function (entry) {
        var s = score(entry, ts);
        if (s > 0) found.push({ e: entry, s: s });
      });
      found.sort(function (a, b) { return b.s - a.s; });
      hits.textContent = found.length + (found.length === 1 ? ' match' : ' matches');
      if (!found.length) {
        list.innerHTML = '<p class="palette-empty">Nothing matches ' + esc(q) + '.</p>';
        return;
      }
      found.slice(0, 30).forEach(function (found_one) {
        var entry = found_one.e;
        // deep-link to the matching heading when one of them matches
        var anchor = '';
        for (var h = 0; h < entry.h.length; h++) {
          var head = entry.h[h].t.toLowerCase();
          if (ts.some(function (t) { return head.indexOf(t) >= 0; })) { anchor = '#' + entry.h[h].a; break; }
        }
        var row = document.createElement('a');
        row.className = 'hit';
        row.href = base + entry.u + anchor;
        row.innerHTML =
          '<div class="hit-where">' + esc(entry.c) + '</div>' +
          '<div class="hit-title">' + highlight(entry.t, ts) + '</div>' +
          '<div class="hit-snip">' + highlight(snippet(entry.b, ts), ts) + '</div>';
        list.appendChild(row);
        rows.push(row);
      });
      move(0);
    };

    var move = function (to) {
      if (!rows.length) return;
      if (cursor >= 0) rows[cursor].classList.remove('on');
      cursor = (to + rows.length) % rows.length;
      rows[cursor].classList.add('on');
      rows[cursor].scrollIntoView({ block: 'nearest' });
    };

    // the index is a plain script, so it also loads from file:// where fetch cannot
    var load = function () {
      if (index || loading) return;
      loading = true;
      var tag = document.createElement('script');
      tag.src = base + 'assets/search-data.js?v=' + (palette.getAttribute('data-v') || '1');
      tag.onload = function () { index = window.COURSE_INDEX || []; render(); };
      tag.onerror = function () {
        list.innerHTML = '<p class="palette-empty">Could not load the search index.</p>';
      };
      document.head.appendChild(tag);
    };

    var open = function () {
      palette.hidden = false;
      document.body.style.overflow = 'hidden';
      field.value = '';
      load();
      render();
      field.focus();
    };
    var close = function () {
      palette.hidden = true;
      document.body.style.overflow = '';
    };

    var findBtn = document.querySelector('.find');
    if (findBtn) findBtn.addEventListener('click', open);
    palette.addEventListener('click', function (ev) {
      if (!ev.target.closest('.palette-box')) close();
    });
    field.addEventListener('input', render);
    field.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); move(cursor + 1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); move(cursor - 1); }
      else if (ev.key === 'Enter' && cursor >= 0) { ev.preventDefault(); rows[cursor].click(); }
      else if (ev.key === 'Escape') { ev.preventDefault(); close(); }
    });
    document.addEventListener('keydown', function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'k' || ev.key === 'K')) {
        ev.preventDefault();
        palette.hidden ? open() : close();
        return;
      }
      if (ev.key === 'Escape' && !palette.hidden) close();
      if (ev.key === '/' && palette.hidden && !/^(input|textarea|select)$/i.test(ev.target.tagName)) {
        ev.preventDefault();
        open();
      }
    });
  }

  // ---- Ask panel: reuse the search index for retrieval ---------------------
  installAsk({
    getIndex: function (done) {
      if (index) { done(index); return; }
      var tag = document.createElement('script');
      tag.src = base + 'assets/search-data.js?v=' + (palette.getAttribute('data-v') || '1');
      tag.onload = function () { index = window.COURSE_INDEX || []; done(index); };
      document.head.appendChild(tag);
    },
    hrefFor: function (entry) { return base + entry.u; },
    // the section this page is showing, keyed the same way the index is
    currentKey: function () {
      return location.pathname.split('/').slice(-2).join('/');
    }
  });

  // ---- keep the reading position, and [ / ] paging ------------------------
  var key = 'llmcourse-pos:' + location.pathname;
  var saved = null;
  try { saved = sessionStorage.getItem(key); } catch (e) {}
  // jump, never animate: a smooth restore reads as the page sliding on arrival
  if (saved && !location.hash) window.scrollTo({ top: parseInt(saved, 10) || 0, behavior: 'instant' });
  window.addEventListener('beforeunload', function () {
    try { sessionStorage.setItem(key, String(window.scrollY)); } catch (e) {}
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    var tag = (ev.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;
    var sel = ev.key === '[' ? '.topbar a.prev' : ev.key === ']' ? '.topbar a.next' : null;
    if (!sel) return;
    var link = document.querySelector(sel);
    if (link) location.href = link.getAttribute('href');
  });
})();
