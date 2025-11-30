// app/page.tsx
export default function HomePage() {
  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">
          StegVerse CFP Lab
        </h1>
        <p className="text-slate-300 max-w-2xl">
          A tiny playoff war-room for running through chaos brackets, TTU
          scenarios, and “what if?” storylines as the season unfolds.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <a
          href="/cfp"
          className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 hover:border-emerald-300 hover:bg-slate-900 transition"
        >
          <h2 className="text-xl font-semibold mb-1">Today&apos;s CFP picture</h2>
          <p className="text-sm text-slate-300">
            Current top-12 snapshot, records, and quick notes in one place.
          </p>
        </a>

        <a
          href="/ttu"
          className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 hover:border-emerald-300 hover:bg-slate-900 transition"
        >
          <h2 className="text-xl font-semibold mb-1">TTU paths to the playoff</h2>
          <p className="text-sm text-slate-300">
            Best-case, maximum-chaos, and nightmare brackets,
            all tuned around the Red Raiders.
          </p>
        </a>
      </div>

      <div className="text-xs text-slate-400 max-w-2xl">
        Note: Rankings and scenarios here are manually curated and speculative.
        This is an experiment inside the StegVerse universe, not gambling advice
        and not official CFP modeling.
      </div>
    </section>
  );
}
