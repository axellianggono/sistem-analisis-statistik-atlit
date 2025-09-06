// Search logic for players page
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("playerSearch");
  const searchBtn   = document.getElementById("searchBtn");
  const cards       = Array.from(document.querySelectorAll(".player-card"));

  function filterPlayers() {
    const q = (searchInput.value || "").toLowerCase().trim();
    if (!q) {
      cards.forEach(c => c.style.display = "block");
      return;
    }
    cards.forEach(card => {
      const name = (card.dataset.name || "");
      const team = (card.dataset.team || "");
      const match = name.startsWith(q) || team.startsWith(q);
      card.style.display = match ? "block" : "none";
    });
  }

  searchInput.addEventListener("input", filterPlayers);
  searchBtn.addEventListener("click", filterPlayers);

  // click card → go to detail
  cards.forEach(card => {
    card.addEventListener("click", () => {
      const href = card.dataset.href;
      if (href) window.location.href = href;
    });
  });
});

// plugin ring konsentris
const radarBands = {
  id: "radarBands",
  beforeDatasetsDraw(chart, args, opt) {
    const r = chart.scales.r; if (!r) return;
    const ctx = chart.ctx;
    const steps = opt?.steps ?? 5;
    const colors = opt?.colors ?? [
      "rgba(239,68,68,0.45)",
      "rgba(245,158,11,0.35)",
      "rgba(234,179,8,0.28)",
      "rgba(163,230,201,0.22)",
      "rgba(34,197,94,0.18)",
    ];
    const count = r._pointLabels?.length || chart.data.labels.length;
    const min = r.min ?? 0, max = r.max ?? 100, step = (max - min) / steps;
    for (let s = steps; s >= 1; s--) {
      const v = min + step * s;
      ctx.beginPath();
      for (let i = 0; i < count; i++) {
        const p = r.getPointPositionForValue(i, v);
        i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y);
      }
      ctx.closePath();
      ctx.fillStyle = colors[Math.min(colors.length - 1, s - 1)];
      ctx.fill();
    }
  },
};

// helpers
const toNum = v => {
  if (v === null || v === undefined) return null;
  const n = Number(String(v).replace(",", ".").trim());
  return Number.isFinite(n) ? n : null;
};
const avgOf = (obj, keys) => {
  const vals = keys.map(k => toNum(obj?.[k])).filter(v => v !== null);
  return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : 0;
};

// ambil player dari <script type="application/json">
function getPlayer() {
  const el = document.getElementById("playersData");
  if (!el) return null;
  try { return JSON.parse(el.textContent || "{}"); }
  catch(e){ console.error("parse playersData gagal:", e); return null; }
}

// definisi kategori (pakai key Kapital sesuai data CSV/dataclass)
const categories = [
  { label: "Physical",  agg: "Physical",  attrs: ["Acceleration","Agility","Balance","JumpingReach","NaturalFitness","Pace","Stamina","Strength","Condition"] },
  { label: "Speed",     agg: "Speed",     attrs: ["Acceleration","Pace"] },
  { label: "Vision",    agg: "Vision",    attrs: ["Vision","Passing","Composure","Decisions","FirstTouch"] },
  { label: "Attacking", agg: "Attacking", attrs: ["Dribbling","Finishing","LongShots","OffTheBall","Technique"] },
  { label: "Technical", agg: "Technical", attrs: ["FirstTouch","Technique","Passing","Crossing"] },
  { label: "Aerial",    agg: "Aerial",    attrs: ["Heading","JumpingReach"] },
  { label: "Defending", agg: "Defending", attrs: ["Tackling","Marking","Positioning","Aggression"] },
  { label: "Mental",    agg: "Mental",    attrs: ["Determination","WorkRate","Teamwork","Anticipation","Concentration","Leadership","Bravery","Flair"] },
];

let radarChart = null;

document.addEventListener("DOMContentLoaded", () => {
  if (typeof Chart !== "undefined") Chart.register(radarBands);

  const P = getPlayer();
  const canvas = document.getElementById("perfRadar");
  if (!P || !canvas) return;

  const labels = categories.map(c => c.label);
  const data = categories.map(c => {
    const preset = toNum(P[c.agg]);               // pakai agregat kalau ada (e.g. P.Physical)
    return preset !== null ? preset : Math.round(avgOf(P, c.attrs));
  });

  if (radarChart) radarChart.destroy();
  radarChart = new Chart(canvas.getContext("2d"), {
    type: "radar",
    plugins: [radarBands],
    data: {
      labels,
      datasets: [{
        label: P.Name || "Player",
        data,
        backgroundColor: "rgba(16,185,129,0.18)",
        borderColor: "rgba(16,185,129,1)",
        borderWidth: 2,
        pointBackgroundColor: "rgba(16,185,129,1)",
        pointRadius: 2,
        pointHoverRadius: 4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        radarBands: { steps: 5 },
        legend: { labels: { color: "#d1d5db", font: { size: 14, weight: "bold" } } },
        tooltip: { enabled: true },
      },
      scales: {
        r: {
          beginAtZero: true,
          suggestedMax: 100,
          grid: { color: "rgba(148,163,184,0.2)" },
          angleLines: { color: "rgba(148,163,184,0.2)" },
          pointLabels: { color: "#e5e7eb", font: { size: 12, weight: "bold" } },
          ticks: { display: false, backdropColor: "transparent" },
        },
      },
      elements: { line: { tension: 0.2 } },
    },
  });
});

