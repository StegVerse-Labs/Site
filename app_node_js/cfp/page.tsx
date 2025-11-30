// app/cfp/page.tsx

type TeamRow = {
  rank: number;
  team: string;
  record: string;
  conf: string;
};

const SAMPLE_TEAMS: TeamRow[] = [
  { rank: 1, team: "Georgia", record: "12–0", conf: "SEC", },
  { rank: 2, team: "Ohio State", record: "11–1", conf: "Big Ten", },
  // ...fill in or edit as needed each week
];

export default function CFPPage() {
  const lastUpdated = "Manual placeholder – edit in code";

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold mb-1">Today&apos;s CFP Picture</h1>
        <p className="text-sm text-slate-300">
          Lightweight, manual snapshot of the current playoff rankings.
        </p>
        <p className="mt-1 text-xs text-slate-400">
          Last updated: {lastUpdated}
        </p>
      </header>

      <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-950/70">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-900/80 text-slate-300">
            <tr>
              <th className="px-3 py-2 text-left">Rank</th>
              <th className="px-3 py-2 text-left">Team</th>
              <th className="px-3 py-2 text-left">Record</th>
              <th className="px-3 py-2 text-left">Conf</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TEAMS.map((row) => (
              <tr key={row.rank} className="border-t border-slate-800">
                <td className="px-3 py-2">#{row.rank}</td>
                <td className="px-3 py-2">{row.team}</td>
                <td className="px-3 py-2">{row.record}</td>
                <td className="px-3 py-2">{row.conf}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
