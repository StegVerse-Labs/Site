(() => {
  'use strict';
  const panels = [...document.querySelectorAll('.panel')];
  const first = panels[0];
  if (!first || document.getElementById('guidedPathExamples')) return;
  const section = document.createElement('section');
  section.id = 'guidedPathExamples';
  section.className = 'panel';
  section.innerHTML = `
    <h2 class="sv-h2">How the guided pages narrow the search</h2>
    <p>The workspace does not show every possible field at once. Your earlier answer determines which later page is useful.</p>
    <div class="example"><strong>Example 1 — very little is known:</strong><br>Enter the candidate ID, choose UNKNOWN lineage, UNASSESSED grade, and ASSUMPTION_ONLY. Skip the file import when no authorized record is available. Leave project numbers missing. The expected posture is discovery first, not a commercial commitment.</div>
    <div class="example warning"><strong>Example 2 — uncertain but potentially workable:</strong><br>Choose Grade B, import an inspection or maintenance export when available, and enter only the project numbers supported by current quotes or records. The likely path is cost-plus protection or re-scoping.</div>
    <div class="example stop"><strong>Example 3 — a hard stop is already known:</strong><br>Choose Grade C or enter a stop-work condition such as an identity conflict or structural crack. The workspace skips unnecessary economics and threshold pages and moves directly to review. A hard stop is not repaired by adding a better margin.</div>
    <div class="mini-table">
      <div class="mini-row"><span class="term">No evidence file</span><span>The import fields stay hidden. Continue without inventing a source.</span></div>
      <div class="mini-row"><span class="term">No project numbers</span><span>The economics fields stay hidden and the missing values remain explicit.</span></div>
      <div class="mini-row"><span class="term">No approved threshold</span><span>The threshold fields stay hidden. Do not create a profile merely to complete the form.</span></div>
      <div class="mini-row"><span class="term">Hard stop present</span><span>Commercial-detail pages are skipped because they cannot override the stop.</span></div>
    </div>
    <h3>Safe practice files</h3>
    <p>These files are synthetic and exist only to test the import and conflict workflow.</p>
    <div class="actions">
      <a class="sv-btn sv-btn-secondary" href="examples/gp10-clean-record.json" download>Download clean JSON sample</a>
      <a class="sv-btn sv-btn-secondary" href="examples/gp10-conflict-record.csv" download>Download conflicting CSV sample</a>
    </div>
    <div class="example warning"><strong>Practice sequence:</strong> Use candidate ID <code>CAND-DEMO-001</code>. Import the clean JSON first, then import the CSV. Both describe unit 1201, but they disagree about donor lineage. The second import should create an identity-conflict review item.</div>`;
  first.parentNode.insertBefore(section, first.nextSibling);
})();