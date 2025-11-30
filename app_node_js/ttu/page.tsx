// app/ttu/page.tsx

const scenarios = [
  {
    slug: "best-case",
    title: "Best-case TTU bracket",
    blurb: "Everything breaks just right and TTU surges into a clean, believable playoff slot.",
  },
  {
    slug: "max-chaos",
    title: "Maximum chaos (TTU ~40% shot)",
    blurb: "Top seeds stumble, weird upsets stack, and the committee has to squint hard at Lubbock.",
  },
  {
    slug: "nightmare",
    title: "Nightmare bracket",
    blurb: "Everyone TTU needs to lose keeps winning. We map out what that looks like anyway.",
  },
];

export default function TTUPage() {
  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold mb-1">TTU Paths to the Playoff</h1>
        <p className="text-sm text-slate-300 max-w-2xl">
          These are scenario sketches, not predictions. Each one corresponds to a
          bracket we can refine over time.
        </p>
      </header>

      <div className="grid gap-5 md:grid-cols-3">
        {scenarios.map((s) => (
          <a
            key={s.slug}
            href={`/bracket/${s.slug}`}
            className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 hover:border-emerald-300 hover:bg-slate-900 transition flex flex-col justify-between"
          >
            <div>
              <h2 className="text-lg font-semibold mb-1">{s.title}</h2>
              <p className="text-xs text-slate-300">{s.blurb}</p>
            </div>
            <span className="mt-3 text-xs text-emerald-300/90">
              View bracket →
            </span>
          </a>
        ))}
      </div>
    </section>
  );
}
