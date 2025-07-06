window.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("sectorTreemap");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const stockMapData = [
    { label: "기술주", ticker: "AAPL", logo: "AAPL.png", v: 800, color: "#4caf50" },
    { label: "기술주", ticker: "TSLA", logo: "TSLA.png", v: 700, color: "#ff9800" },
    { label: "기술주", ticker: "NVDA", logo: "NVDA.png", v: 900, color: "#2196f3" },
    { label: "금융", ticker: "JPM", logo: "JPM.png", v: 600, color: "#9c27b0" },
    { label: "금융", ticker: "GS", logo: "GS.png", v: 400, color: "#e91e63" },
    { label: "헬스케어", ticker: "PFE", logo: "PFE.png", v: 550, color: "#3f51b5" },
    { label: "헬스케어", ticker: "JNJ", logo: "JNJ.png", v: 520, color: "#009688" },
    { label: "헬스케어", ticker: "UNH", logo: "UNH.png", v: 500, color: "#00bcd4" },
    { label: "소비재", ticker: "PG", logo: "PG.png", v: 480, color: "#795548" },
    { label: "소비재", ticker: "KO", logo: "KO.png", v: 470, color: "#8e44ad" },
    { label: "소비재", ticker: "PEP", logo: "PEP.png", v: 450, color: "#607d8b" },
    { label: "에너지", ticker: "XOM", logo: "XOM.png", v: 610, color: "#c0392b" },
    { label: "에너지", ticker: "CVX", logo: "CVX.png", v: 590, color: "#d35400" },
    { label: "에너지", ticker: "COP", logo: "COP.png", v: 580, color: "#2c3e50" }
  ];

  const logoPlugin = {
    id: "logoPlugin",
    afterDatasetDraw(chart) {
      const ctx = chart.ctx;
      const dataset = chart.getDatasetMeta(0);
      dataset.data.forEach((rect) => {
        const raw = rect?.$context?.raw;
        if (!raw || !raw.logo || !raw.ticker) return;
        const { x, y } = rect;
        // (이미지 경로 반드시 맞춰주세요)
        const img = new window.Image();
        img.src = "/static/assets/img/logos/" + raw.logo;
        img.onload = () => {
          ctx.drawImage(img, x + 5, y + 5, 24, 24);
          ctx.fillStyle = "#fff";
          ctx.font = "10px sans-serif";
          ctx.fillText(raw.ticker, x + 5, y + 37);
        };
      });
    }
  };

  new Chart(ctx, {
    type: "treemap",
    data: {
      datasets: [{
        tree: stockMapData,
        key: "v",
        groups: ["label"],
        borderColor: "#fff",
        borderWidth: 1,
        backgroundColor: ctx => ctx?.raw?.color || "#ccc"
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      onClick: (e, elements) => {
        const el = elements[0];
        const raw = el?.element?.$context?.raw;
        if (!raw || !raw.ticker) return;
        alert(`${raw.ticker} 선택됨`);
      },
      layout: { padding: 20 }
    },
    plugins: [logoPlugin]
  });
});
