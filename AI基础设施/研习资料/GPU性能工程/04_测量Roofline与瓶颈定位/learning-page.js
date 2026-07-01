const controls = ["peak", "bandwidth", "flops", "bytes", "time"];
const scenarioValues = {
  elementwise: { peak: 300, bandwidth: 3, flops: 0.25, bytes: 3, time: 1.1 },
  matmul: { peak: 300, bandwidth: 3, flops: 140, bytes: 0.11, time: 0.62 },
  softmax: { peak: 300, bandwidth: 3, flops: 4, bytes: 16, time: 6 },
  bad: { peak: 300, bandwidth: 3, flops: 120, bytes: 4, time: 9 }
};

function n(id) {
  return Number(document.getElementById(id)?.value) || 0;
}

function fmt(value, unit, digits = 2) {
  if (!Number.isFinite(value)) return "-";
  if (Math.abs(value) >= 100) return `${value.toFixed(0)} ${unit}`;
  if (Math.abs(value) >= 10) return `${value.toFixed(1)} ${unit}`;
  return `${value.toFixed(digits)} ${unit}`;
}

function log10(x) {
  return Math.log(x) / Math.LN10;
}

function drawRoofline() {
  const canvas = document.getElementById("roofCanvas");
  if (!canvas) return;

  const peak = n("peak");
  const bandwidth = n("bandwidth");
  const flops = n("flops");
  const bytes = n("bytes");
  const time = n("time");

  const ai = bytes > 0 ? flops / bytes : 0;
  const actual = time > 0 ? flops / time : 0;
  const roof = Math.min(peak, bandwidth * ai);
  const ridge = bandwidth > 0 ? peak / bandwidth : 0;
  const efficiency = roof > 0 ? actual / roof : 0;

  let diagnosis = "检查输入";
  if (ai > 0 && actual > 0) {
    if (efficiency < 0.2) diagnosis = "远低于屋顶";
    else if (bandwidth * ai < peak) diagnosis = "偏带宽";
    else diagnosis = "偏计算";
  }

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };

  setText("aiResult", fmt(ai, "F/B"));
  setText("perfResult", fmt(actual, "TF/s"));
  setText("roofResult", fmt(roof, "TF/s"));
  setText("diagResult", diagnosis);

  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  const padL = 70, padR = 28, padT = 32, padB = 58;
  const xMin = -2, xMax = 4;
  const yMin = -2, yMax = Math.max(3, Math.ceil(log10(Math.max(peak, roof, actual, 1))) + 0.2);

  const xScale = (v) => padL + ((log10(v) - xMin) / (xMax - xMin)) * (w - padL - padR);
  const yScale = (v) => h - padB - ((log10(v) - yMin) / (yMax - yMin)) * (h - padT - padB);

  ctx.strokeStyle = "rgba(36,34,31,.16)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "#67645d";
  ctx.font = "24px Cascadia Code, Consolas, monospace";
  for (let p = -2; p <= 4; p++) {
    const x = padL + ((p - xMin) / (xMax - xMin)) * (w - padL - padR);
    ctx.beginPath();
    ctx.moveTo(x, padT);
    ctx.lineTo(x, h - padB);
    ctx.stroke();
    ctx.fillText(`1e${p}`, x - 18, h - 22);
  }
  for (let p = -2; p <= Math.floor(yMax); p++) {
    const y = h - padB - ((p - yMin) / (yMax - yMin)) * (h - padT - padB);
    ctx.beginPath();
    ctx.moveTo(padL, y);
    ctx.lineTo(w - padR, y);
    ctx.stroke();
    ctx.fillText(`1e${p}`, 12, y + 8);
  }

  ctx.strokeStyle = "#24221f";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(padL, padT);
  ctx.lineTo(padL, h - padB);
  ctx.lineTo(w - padR, h - padB);
  ctx.stroke();

  ctx.fillStyle = "#24221f";
  ctx.font = "26px Microsoft YaHei, sans-serif";
  ctx.fillText("算术强度 FLOP/byte", w / 2 - 110, h - 8);
  ctx.save();
  ctx.translate(22, h / 2 + 88);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("性能 TFLOP/s", 0, 0);
  ctx.restore();

  const xs = [];
  for (let i = 0; i <= 180; i++) {
    const lx = xMin + (i / 180) * (xMax - xMin);
    xs.push(Math.pow(10, lx));
  }

  ctx.strokeStyle = "#216d5d";
  ctx.lineWidth = 4;
  ctx.beginPath();
  xs.forEach((xv, i) => {
    const yv = Math.max(0.01, Math.min(peak, bandwidth * xv));
    const x = xScale(xv);
    const y = yScale(yv);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.strokeStyle = "#ad3e33";
  ctx.lineWidth = 3;
  ctx.setLineDash([9, 6]);
  ctx.beginPath();
  ctx.moveTo(xScale(Math.max(0.01, ridge)), yScale(peak));
  ctx.lineTo(xScale(10000), yScale(peak));
  ctx.stroke();
  ctx.setLineDash([]);

  if (ai > 0 && actual > 0) {
    const pointX = xScale(Math.min(Math.max(ai, 0.01), 10000));
    const pointY = yScale(Math.min(Math.max(actual, 0.01), Math.pow(10, yMax)));
    ctx.fillStyle = "#0969da";
    ctx.beginPath();
    ctx.arc(pointX, pointY, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fillStyle = "#0969da";
    ctx.font = "24px Microsoft YaHei, sans-serif";
    ctx.fillText("实测点", Math.min(pointX + 12, w - 110), Math.max(pointY - 12, 28));
  }

  ctx.fillStyle = "#216d5d";
  ctx.font = "23px Microsoft YaHei, sans-serif";
  ctx.fillText("带宽 × AI", xScale(0.18), yScale(Math.max(0.02, bandwidth * 0.18)) - 10);
  ctx.fillStyle = "#ad3e33";
  ctx.fillText("计算峰值", xScale(Math.max(ridge * 1.15, 0.1)), yScale(peak) - 10);
}

function bindRoofline() {
  const controlsPresent = controls.filter((id) => document.getElementById(id));
  controlsPresent.forEach((id) => {
    document.getElementById(id).addEventListener("input", () => {
      const scenario = document.getElementById("scenario");
      if (scenario) scenario.value = "custom";
      drawRoofline();
    });
  });

  const scenario = document.getElementById("scenario");
  if (scenario) {
    scenario.addEventListener("change", (event) => {
      const preset = scenarioValues[event.target.value];
      if (!preset) {
        drawRoofline();
        return;
      }
      Object.entries(preset).forEach(([key, value]) => {
        const field = document.getElementById(key);
        if (field) field.value = value;
      });
      drawRoofline();
    });
  }

  window.addEventListener("resize", drawRoofline);
  drawRoofline();
}

document.addEventListener("DOMContentLoaded", bindRoofline);
