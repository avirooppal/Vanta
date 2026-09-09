import { useState, useEffect } from "react";
import { Check, Copy, Download, Loader2, Sparkles, AlertCircle } from "lucide-react";

interface ModeOption {
  id: string;
  name: string;
  badge: string;
  desc: string;
  defaultRounds: number;
}

const MODES: ModeOption[] = [
  {
    id: "research",
    name: "🔬 Standard Research",
    badge: "3 Rounds",
    desc: "Comprehensive analytical research. Evidence gathering, contradiction analysis, and structured citations.",
    defaultRounds: 3,
  },
  {
    id: "study",
    name: "🎓 Study & Learn",
    badge: "2 Rounds",
    desc: "Educational mastery. First-principles Feynman explanations, practice quiz, and glossary.",
    defaultRounds: 2,
  },
  {
    id: "brief",
    name: "⚡ Executive Brief",
    badge: "1 Round",
    desc: "Rapid executive briefing. Bottom Line Up Front (BLUF), top takeaways, and action items.",
    defaultRounds: 1,
  },
  {
    id: "deep",
    name: "🏛️ Deep Academic",
    badge: "4 Rounds",
    desc: "Exhaustive academic deep dive. Rigorous literature review, whitepapers, and contradiction matrix.",
    defaultRounds: 4,
  },
];

export function ResearchConsole() {
  const [mode, setMode] = useState("research");
  const [rounds, setRounds] = useState(3);
  const [query, setQuery] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [provider, setProvider] = useState("");
  const [showSettings, setShowSettings] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState("");
  const [progress, setProgress] = useState(0);
  const [jobId, setJobId] = useState<string | null>(null);
  const [report, setReport] = useState<{ summary?: string; body_md?: string; citations?: any[] } | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("vanta_key");
    if (saved) setApiKey(saved);
  }, []);

  const handleModeSelect = (m: ModeOption) => {
    setMode(m.id);
    setRounds(m.defaultRounds);
  };

  const handleLaunch = async () => {
    if (!query.trim()) {
      alert("Please enter a research topic or inquiry.");
      return;
    }
    if (!apiKey.trim()) {
      setShowSettings(true);
      alert("Please provide an LLM API key (OpenAI, Anthropic, Gemini, or OpenRouter).");
      return;
    }

    localStorage.setItem("vanta_key", apiKey.trim());
    setLoading(true);
    setReport(null);
    setProgress(10);
    setStatusText("Dispatching multi-agent fleet...");

    try {
      const res = await fetch("http://localhost:8000/v1/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey.trim()}`,
        },
        body: JSON.stringify({
          query: query.trim(),
          mode: mode,
          max_rounds: rounds,
          provider: provider || undefined,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || err.detail || `Server returned ${res.status}`);
      }

      const data = await res.json();
      setJobId(data.id);
      startPolling(data.id);
    } catch (err: any) {
      alert(`Launch error: ${err.message}`);
      setLoading(false);
    }
  };

  const startPolling = (id: string) => {
    let elapsed = 0;
    const interval = setInterval(async () => {
      elapsed += 2;
      try {
        const res = await fetch(`http://localhost:8000/v1/research/${id}`, {
          headers: { Authorization: `Bearer ${apiKey.trim()}` },
        });
        if (!res.ok) return;
        const job = await res.json();

        if (job.status === "running") {
          const currentPct = Math.min(90, Math.max(20, elapsed * 6));
          setProgress(currentPct);
          if (currentPct < 35) setStatusText("SearchAgent generating queries & scraping sources...");
          else if (currentPct < 60) setStatusText("ValidatorAgent evaluating domain trust & extracting facts...");
          else setStatusText("SynthesizerAgent building final monograph report...");
        } else if (job.status === "completed") {
          clearInterval(interval);
          setProgress(100);
          setStatusText("Research completed.");
          setReport(job.report || { body_md: "No report generated." });
          setLoading(false);
        } else if (job.status === "failed") {
          clearInterval(interval);
          setLoading(false);
          alert(`Research failed: ${job.error}`);
        }
      } catch (e) {
        console.error("Polling error", e);
      }
    }, 2000);
  };

  const copyMarkdown = () => {
    if (!report?.body_md) return;
    navigator.clipboard.writeText(report.body_md);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadMarkdown = () => {
    if (!report?.body_md) return;
    const blob = new Blob([report.body_md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `vanta-${mode}-report.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section id="console" className="relative z-10 mx-auto max-w-7xl px-6 pb-28">
      <div className="liquid-glass rounded-[12px] p-6 sm:p-10">
        <div className="flex flex-col gap-4 border-b border-white/10 pb-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.32em] text-muted-foreground">
              Interactive Console
            </p>
            <h2
              className="mt-4 text-4xl font-normal leading-tight tracking-[-1.4px] sm:text-5xl"
              style={{ fontFamily: "'Instrument Serif', serif" }}
            >
              Launch Deep Research Fleet
            </h2>
          </div>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="inline-flex h-9 items-center gap-2 rounded-full border border-white/15 bg-white/5 px-4 text-xs font-medium text-foreground transition-colors hover:bg-white/10"
          >
            ⚙️ {showSettings ? "Hide API Settings" : "Configure API Keys"}
          </button>
        </div>

        {/* Collapsible API Settings */}
        {showSettings && (
          <div className="mt-6 grid gap-4 rounded-lg border border-white/10 bg-black/40 p-4 sm:grid-cols-2">
            <div>
              <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-muted-foreground">
                LLM Provider
              </label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full rounded-md border border-white/15 bg-black/60 px-3 py-2 text-sm text-foreground outline-none focus:border-white/50"
              >
                <option value="">Auto-detect from key prefix</option>
                <option value="openai">OpenAI (GPT-4o, o3-mini)</option>
                <option value="anthropic">Anthropic (Claude 3.5 Sonnet)</option>
                <option value="openai_compatible">Gemini / Custom OpenAI Base</option>
                <option value="openrouter">OpenRouter</option>
              </select>
            </div>
            <div>
              <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-muted-foreground">
                API Key (Bearer Token)
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-ant-... / sk-... / AIza..."
                className="w-full rounded-md border border-white/15 bg-black/60 px-3 py-2 text-sm text-foreground outline-none focus:border-white/50"
              />
            </div>
          </div>
        )}

        {/* Mode Selector Tiles */}
        <div className="mt-8">
          <p className="mb-3 text-xs font-medium uppercase tracking-widest text-muted-foreground">
            1. Select Research Mode
          </p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {MODES.map((m) => {
              const active = mode === m.id;
              return (
                <div
                  key={m.id}
                  onClick={() => handleModeSelect(m)}
                  className={`cursor-pointer rounded-lg border p-4 transition-all ${
                    active
                      ? "border-white/60 bg-white/10 shadow-[0_0_20px_rgba(255,255,255,0.1)]"
                      : "border-white/10 bg-white/[0.02] hover:border-white/25 hover:bg-white/[0.05]"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-foreground">{m.name}</span>
                    <span
                      className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                        active ? "bg-white text-black" : "bg-white/10 text-muted-foreground"
                      }`}
                    >
                      {m.badge}
                    </span>
                  </div>
                  <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{m.desc}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Query Input */}
        <div className="mt-8">
          <p className="mb-3 text-xs font-medium uppercase tracking-widest text-muted-foreground">
            2. Research Question
          </p>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            placeholder="e.g. What are the key breakthroughs in solid-state lithium-metal batteries in 2026?"
            className="w-full rounded-lg border border-white/15 bg-black/50 p-4 text-sm leading-relaxed text-foreground placeholder:text-muted-foreground/60 outline-none transition-colors focus:border-white/50"
          />
          <div className="mt-2 flex flex-wrap gap-2">
            <span className="text-xs text-muted-foreground/80">Try:</span>
            {[
              "Quantum computing and superposition from first principles",
              "Solid-state battery breakthroughs in 2026",
              "State space models (Mamba) vs Transformers trade-offs",
            ].map((s) => (
              <button
                key={s}
                onClick={() => setQuery(s)}
                className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs text-muted-foreground transition-colors hover:border-white/30 hover:text-foreground"
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Action Bar */}
        <div className="mt-8 flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
              Search Rounds:
            </span>
            <select
              value={rounds}
              onChange={(e) => setRounds(Number(e.target.value))}
              className="rounded-md border border-white/15 bg-black/60 px-3 py-1.5 text-xs text-foreground outline-none"
            >
              {[1, 2, 3, 4, 5].map((r) => (
                <option key={r} value={r}>
                  {r} Round{r > 1 ? "s" : ""}
                </option>
              ))}
            </select>
          </div>

          <button
            disabled={loading}
            onClick={handleLaunch}
            className="inline-flex h-11 items-center gap-2 rounded-full bg-white px-8 text-sm font-medium text-black transition-all hover:bg-white/90 disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                <span>Running Pipeline...</span>
              </>
            ) : (
              <>
                <Sparkles className="size-4" />
                <span>Launch Research Fleet</span>
              </>
            )}
          </button>
        </div>

        {/* Progress Tracker */}
        {loading && (
          <div className="mt-8 rounded-lg border border-white/15 bg-black/40 p-6">
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span className="font-mono text-white">{statusText}</span>
              <span>{progress}%</span>
            </div>
            <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full bg-gradient-to-r from-indigo-400 to-purple-400 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Report Output */}
        {report && (
          <div className="mt-10 rounded-lg border border-white/15 bg-black/50 p-6 sm:p-8">
            <div className="mb-6 flex flex-col justify-between gap-4 border-b border-white/10 pb-6 sm:flex-row sm:items-center">
              <div>
                <span className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                  {mode.toUpperCase()} REPORT
                </span>
                <h3
                  className="mt-1 text-3xl font-normal tracking-tight text-foreground"
                  style={{ fontFamily: "'Instrument Serif', serif" }}
                >
                  {query}
                </h3>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={copyMarkdown}
                  className="inline-flex h-8 items-center gap-1.5 rounded-full border border-white/15 bg-white/5 px-3 text-xs text-muted-foreground hover:text-foreground"
                >
                  {copied ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}
                  {copied ? "Copied" : "Copy"}
                </button>
                <button
                  onClick={downloadMarkdown}
                  className="inline-flex h-8 items-center gap-1.5 rounded-full border border-white/15 bg-white/5 px-3 text-xs text-muted-foreground hover:text-foreground"
                >
                  <Download className="size-3.5" />
                  Download
                </button>
              </div>
            </div>

            <div className="prose prose-invert max-w-none text-sm leading-relaxed text-white/90">
              <pre className="whitespace-pre-wrap font-sans text-[14px] leading-7">
                {report.body_md}
              </pre>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
