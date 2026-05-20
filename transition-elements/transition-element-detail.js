async function loadDiscovery() {
  const response = await fetch("../data/formalism-tests/transition-discovery-map.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load transition-discovery-map.json");
  return response.json();
}
function q(name) {
  return new URLSearchParams(window.location.search).get(name);
}
function levelName(data, level) {
  const match = (data.scale.levels || []).find((item) => item.level === level);
  return match ? match.name : "Unknown";
}
function pill(level, name) {
  return `<span class="level-pill level-${level}">L${level} · ${name}</span>`;
}
function render(data, elementId) {
  const element = (data.elements || []).find((item) => item.element_id === elementId);
  if (!element) throw new Error(`Unknown transition element: ${elementId}`);
  const level = element.completion_level;
  document.title = `${element.name} | Transition Element`;
  document.getElementById("name").textContent = element.name;
  document.getElementById("summary").textContent = element.summary;
  document.getElementById("level").innerHTML = pill(level, levelName(data, level));
  document.getElementById("identity").textContent = element.element_id;
  document.getElementById("family").textContent = element.family;
  document.getElementById("status").textContent = element.status;
  document.getElementById("authority").textContent = data.authority_boundary || "";
  document.getElementById("details").innerHTML = (element.details || []).map((item) => `<li>${item}</li>`).join("");
  document.getElementById("families").innerHTML = (element.linked_transition_families || []).map((item) => `<li><code>${item}</code></li>`).join("");
  document.getElementById("raw").textContent = JSON.stringify(element, null, 2);
  document.getElementById("shell").className = `card element-card level-border-${level}`;
}
loadDiscovery()
  .then((data) => render(data, window.TRANSITION_ELEMENT_ID))
  .catch((error) => {
    document.getElementById("name").textContent = "Transition element unavailable";
    document.getElementById("summary").textContent = error.message;
  });
