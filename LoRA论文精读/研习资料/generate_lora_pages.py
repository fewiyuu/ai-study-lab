from __future__ import annotations

import html
from pathlib import Path


BASE = Path(__file__).resolve().parent


STYLE = r"""
:root{
  --report-bg:#f4f6f9;--report-paper:#fff;--report-line:#d8dee8;--navy:#1b2a4a;--dark-navy:#151f35;--cyan:#00a9f4;
  --ink:#1a1a1a;--muted:#5f6b7a;--soft:#f8fafc;--warn:#fff8e1;--bad:#fff1f2;--ok:#ecfdf3;
  --code:#1e1e1e;--codeText:#d4d4d4;--mono:"Cascadia Code","Cascadia Mono","Consolas","SFMono-Regular",monospace;
  --sans:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",Arial,sans-serif;--serif:"Songti SC","Noto Serif CJK SC","STSong","SimSun",serif;
}
*{box-sizing:border-box}html{scroll-behavior:smooth}.progress{position:fixed;left:0;top:0;height:4px;width:0;background:linear-gradient(90deg,var(--cyan),var(--navy));z-index:20}
body{margin:0;background:linear-gradient(90deg,rgba(27,42,74,.045) 1px,transparent 1px) 0 0/60px 60px,linear-gradient(rgba(27,42,74,.035) 1px,transparent 1px) 0 0/60px 60px,var(--report-bg);color:var(--ink);font-family:var(--sans);line-height:1.72;-webkit-font-smoothing:antialiased}
.layout{display:grid;grid-template-columns:308px minmax(0,1fr);min-height:100vh}aside{position:sticky;top:0;height:100vh;overflow:auto;background:var(--navy);color:#fff;padding:30px 22px;background-image:repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,.045) 59px,rgba(255,255,255,.045) 60px),repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,.035) 59px,rgba(255,255,255,.035) 60px)}
.brand{border-bottom:1px solid rgba(255,255,255,.36);padding-bottom:22px;margin-bottom:20px}.brand strong{display:block;color:#fff;font-family:var(--serif);font-size:27px;line-height:1.18;font-weight:700}.brand span{display:block;color:rgba(255,255,255,.68);font-size:13px;line-height:1.7;margin-top:8px}
nav{display:grid;gap:0}nav a{display:flex;gap:10px;align-items:center;color:rgba(255,255,255,.82);text-decoration:none;border-bottom:1px solid rgba(255,255,255,.13);padding:10px 0;font-size:13px;letter-spacing:.04em}nav a:hover,nav a.active{color:#fff;border-color:rgba(255,255,255,.42);font-weight:700}.dot{width:5px;height:5px;background:var(--cyan);opacity:.55;flex:0 0 auto}.side-note{margin-top:24px;padding:13px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.08);color:rgba(255,255,255,.72);font-size:13px;line-height:1.8}
main{max-width:1420px;padding:34px 44px}.hero,section{background:var(--report-paper);border:1px solid var(--report-line);box-shadow:0 14px 28px rgba(27,42,74,.08);position:relative}.hero{display:grid;grid-template-columns:minmax(0,1fr) 392px;gap:24px;padding:38px 42px;border-top:6px solid var(--navy)}section{padding:28px 34px;margin-top:18px}.kicker{font-family:var(--mono);font-size:11px;color:#8a96a8;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}h1{margin:0;font-family:var(--serif);font-size:46px;line-height:1.16;color:#000;font-weight:700;max-width:18ch}h2{margin:0 0 12px;font-family:var(--serif);font-size:28px;font-weight:700;color:#000}h3{margin:12px 0 8px;font-size:17px;color:#000}p{margin:9px 0}.muted,.hero p{color:var(--muted)}ul,ol{padding-left:22px}li{margin:5px 0}.head{display:flex;justify-content:space-between;gap:16px;align-items:start;border-bottom:2px solid #000;padding-bottom:12px;margin-bottom:18px}.tag{color:#8a96a8;font-family:var(--mono);letter-spacing:.12em;font-size:11px;text-transform:uppercase;white-space:nowrap}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.9fr);gap:1px;background:var(--report-line);border:1px solid var(--report-line)}.grid3,.terms{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--report-line);border:1px solid var(--report-line)}.terms{grid-template-columns:repeat(2,minmax(0,1fr))}.box,.term,.example-card,.q,.review-card,.check-item,.route{background:#fff;border:0;padding:16px}.soft{border-top:4px solid #4caf50}.warn{border-top:4px solid #ffc107}.blue,.info{border-top:4px solid var(--cyan)}.bad{border-top:4px solid #e53935}.ok{border-top:4px solid #4caf50}.term strong{display:block;margin-bottom:5px}.map{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0;border:1px solid var(--report-line);margin:18px 0}.node{background:#f8fafc;border-right:1px solid var(--report-line);padding:14px 10px;text-align:center;font-weight:800}.node:last-child{border-right:0}
code{background:#e8edf2;color:#182331;padding:2px 5px;border-radius:3px;font-family:var(--mono);font-size:.92em}.codebar{margin-top:14px;background:#252526;color:#cbd5e1;border:1px solid #3c3c3c;border-bottom:0;padding:8px 12px;display:flex;justify-content:space-between;gap:12px;align-items:center;font-family:var(--mono);font-size:13px}.codebar:before{content:"";width:34px;height:10px;flex:0 0 auto;background:radial-gradient(circle at 5px 5px,#f87171 0 4px,transparent 4.5px),radial-gradient(circle at 17px 5px,#fbbf24 0 4px,transparent 4.5px),radial-gradient(circle at 29px 5px,#34d399 0 4px,transparent 4.5px)}pre{margin:0 0 12px;background:var(--code);color:var(--codeText);border:1px solid #3c3c3c;padding:15px 16px;overflow:auto;font-family:var(--mono);font-size:14.5px;line-height:1.65;white-space:pre;tab-size:2}pre code{background:transparent;color:inherit;padding:0}.copy,.copy-code{border:1px solid #3c3c3c;background:#2d2d30;color:#dbeafe;padding:4px 8px;font-family:var(--mono);font-size:12px;cursor:pointer}.badge,.pill{display:inline-flex;align-items:center;background:#eef5fb;color:var(--navy);border:1px solid #cfe3f5;padding:2px 8px;font-size:12px;font-weight:700}.badge.err{background:#4a1d1d;color:#fecaca}.badge.ok{background:#123d2f;color:#b8f7d4}.badge.walk{background:#23324d;color:#bfdbfe}.codebar.error{background:#2a1517;border-color:#7f1d1d}.codebar.error+pre{border-color:#7f1d1d;box-shadow:inset 4px 0 0 #7f1d1d}.codebar.good{background:#12251d;border-color:#166534}.codebar.good+pre{border-color:#166534}.codebar.walk{background:#172033;border-color:#1d4ed8}.codebar.walk+pre{border-color:#1d4ed8}
.formula{background:#fffdfa;color:#111;border:1px solid var(--report-line);border-left:8px solid var(--navy);padding:16px 18px;overflow:auto;font-family:"Cambria Math","Latin Modern Math","Times New Roman",var(--serif);font-size:18px;line-height:1.75;margin:12px 0}.formula .big{font-size:24px;font-weight:700}.frac{display:inline-grid;grid-template-rows:auto auto;vertical-align:middle;text-align:center;margin:0 3px}.frac span:first-child{border-bottom:1px solid currentColor;padding:0 4px}.frac span:last-child{padding:0 4px}.sub{font-size:.78em;vertical-align:sub}.sup{font-size:.78em;vertical-align:super}
.viz-panel{margin:16px 0;border:1px solid var(--report-line);background:#fff}.viz-title{display:flex;justify-content:space-between;gap:18px;align-items:start;padding:16px 18px;border-bottom:1px solid var(--report-line);background:#f8fafc}.viz-grid{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(300px,.92fr);gap:1px;background:var(--report-line)}.viz-cell{background:#fff;padding:16px;min-width:0}.viz-flow{display:grid;gap:8px}.viz-btn{border:1px solid #cfe3f5;background:#fff;color:var(--navy);padding:8px 10px;text-align:left;cursor:pointer}.viz-btn.active{background:var(--navy);color:#fff;border-color:var(--navy)}.viz-output{min-height:130px;border:1px solid var(--report-line);background:#fbfdff;padding:12px;white-space:pre-wrap}.viz-output b{display:block;margin-bottom:6px;color:var(--navy)}.viz-note{border-left:4px solid var(--cyan);background:#eef8fe;padding:12px 13px;margin-top:12px;color:#27364a;font-size:13.5px}.metric-table{width:100%;border-collapse:collapse;margin-top:14px;background:#fff;font-size:13.5px}.metric-table th,.metric-table td{border:1px solid var(--report-line);padding:9px 10px;text-align:left;vertical-align:top}.metric-table th{background:#f3f7fb;color:var(--navy);font-weight:800}
.bar-row{display:grid;grid-template-columns:130px minmax(0,1fr) 92px;gap:10px;align-items:center;margin:9px 0}.bar{height:16px;background:#e7edf5;border:1px solid #d3dde9;position:relative}.bar span{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,var(--cyan),var(--navy));min-width:2px}.svg-wrap{border:1px solid var(--report-line);background:#fbfdff;padding:10px;overflow:auto}.svg-wrap svg{max-width:100%;height:auto;display:block}
.practice-intro{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--report-line);border:1px solid var(--report-line);margin-bottom:14px}.practice-check{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--report-line);border:1px solid var(--report-line);margin:12px 0}.check-item{min-height:104px}.practice-group{border:1px solid var(--report-line);background:#fff;margin-top:20px}.group-head{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:14px;align-items:start;background:#f8fafc;border-bottom:1px solid var(--report-line);padding:20px 22px}.group-head h3{font-family:var(--serif);font-size:24px;font-weight:700;margin:0}.group-head p{color:var(--muted);margin:6px 0 0}.quick-review{border-left:4px solid var(--cyan);background:#fff;padding:12px;font-size:13.5px}.quick-review b{display:block;color:var(--navy);font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:5px}.drill-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--report-line)}.q{padding:16px}.q.full{grid-column:1/-1}.q h3{font-size:15.5px;line-height:1.55;margin-top:0}.q-meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.hint,.solve-note{font-size:13.5px;color:var(--muted)}label{display:block;margin:8px 0}input[type=radio],input[type=checkbox]{accent-color:var(--navy);margin-right:7px}textarea,input[type=text],select{width:100%;border:1px solid var(--report-line);background:#fff;color:var(--ink);padding:10px;font:inherit;resize:vertical}textarea{min-height:78px}.answer{white-space:pre-wrap;background:#fff;border:1px dashed #9aa8b6;padding:14px;max-height:380px;overflow:auto}.quality{white-space:pre-wrap;background:#fff8e1;border:1px solid #ffc107;color:#5f4b12;padding:12px;margin-top:12px;display:none}.actions{position:sticky;bottom:0;display:flex;gap:10px;justify-content:flex-end;padding:14px 0 0;margin-top:18px;background:linear-gradient(transparent,var(--report-bg) 40%)}button{border:0;padding:9px 12px;background:var(--navy);color:#fff;font:inherit;cursor:pointer}.ghost{background:#fff;color:var(--navy);border:1px solid var(--navy)}
@media(max-width:940px){.layout{grid-template-columns:1fr}aside{position:static;height:auto}main{padding:18px}.hero,.grid2,.grid3,.terms,.viz-grid,.practice-intro,.practice-check,.group-head,.drill-grid{grid-template-columns:1fr}h1{font-size:30px}.map{grid-template-columns:1fr}.node{border-right:0;border-bottom:1px solid var(--report-line)}}
"""


SCRIPT = r"""
function copyCode(id){const el=document.getElementById(id);if(!el)return;navigator.clipboard.writeText(el.innerText).then(()=>{},()=>alert("复制失败，请手动选择代码复制。"))}
function valueOf(q){const checks=[...q.querySelectorAll('input[type=checkbox]:checked')].map(x=>x.value);if(checks.length)return checks.join(", ");const radio=q.querySelector('input[type=radio]:checked');if(radio)return radio.value;const text=q.querySelector('textarea,input[type=text],select');return text?text.value.trim():""}
function generateAnswer(){const qs=[...document.querySelectorAll('[data-role="homework"]')],warnings=[],lines=["# "+document.body.dataset.course+" 练习记录","","主题："+document.body.dataset.course,""];qs.forEach((q,i)=>{const title=q.dataset.title||q.querySelector('h3')?.innerText||`第 ${i+1} 题`,ans=valueOf(q);if(!ans)warnings.push(`第 ${i+1} 题未答：${title}`);if(q.dataset.type==="diagnostic"&&ans&&!(/错因|原因/.test(ans)&&/后果|影响|导致/.test(ans)&&/修法|修正|解决|改/.test(ans)))warnings.push(`第 ${i+1} 题建议补全错因、后果和修法。`);if(q.dataset.type==="feynman"){const keys=(q.dataset.keys||"").split(",").filter(Boolean),miss=keys.filter(k=>!ans.includes(k));if(ans.length<140)warnings.push("费曼题偏短，建议不少于 140 个中文字符。");if(miss.length)warnings.push(`费曼题关键词可能缺失：${miss.join("、")}`)}lines.push(`## ${i+1}. ${title}`,"",ans||"（未作答）","")});const q=document.getElementById("quality");q.style.display=warnings.length?"block":"none";q.innerText=warnings.length?("检查提醒：\n- "+warnings.join("\n- ")):"";document.getElementById("answer").innerText=lines.join("\n")}
function copyAnswer(){navigator.clipboard.writeText(document.getElementById("answer").innerText).then(()=>{},()=>alert("复制失败，请手动选择练习记录复制。"))}
(function(){const progress=document.querySelector('.progress');function updateProgress(){const h=document.documentElement,max=h.scrollHeight-innerHeight;progress.style.width=(max>0?scrollY/max*100:0)+"%"}addEventListener("scroll",updateProgress,{passive:true});addEventListener("resize",updateProgress);updateProgress();document.querySelectorAll(".viz-panel").forEach(panel=>{const title=panel.querySelector(".viz-state-title"),note=panel.querySelector(".viz-note-text"),body=panel.querySelector(".metric-body"),buttons=[...panel.querySelectorAll(".viz-btn")];function activate(btn){buttons.forEach(b=>b.classList.toggle("active",b===btn));if(title)title.textContent=btn.dataset.title||btn.textContent.trim();if(note)note.textContent=btn.dataset.note||"";if(body){body.innerHTML=(btn.dataset.rows||"").split("|").filter(Boolean).map(row=>{const parts=row.split("=");return `<tr><td>${parts[0]||""}</td><td>${parts.slice(1).join("=")||""}</td></tr>`}).join("")}}buttons.forEach(btn=>btn.addEventListener("click",()=>activate(btn)));if(buttons[0])activate(buttons[0])});document.querySelectorAll("[data-param-demo]").forEach(panel=>{const rank=panel.querySelector("[data-rank]"),targets=panel.querySelector("[data-targets]"),layers=panel.querySelector("[data-layers]"),dim=panel.querySelector("[data-dim]"),out=panel.querySelector("[data-param-out]");function calc(){const r=Number(rank.value),t=Number(targets.value),l=Number(layers.value),d=Number(dim.value),params=2*t*l*d*r;out.textContent=`${params.toLocaleString()} 个可训练参数，约 ${(params*2/1024/1024).toFixed(2)} MB（FP16）`;panel.querySelector("[data-rank-out]").textContent=r;panel.querySelector("[data-targets-out]").textContent=t} [rank,targets,layers,dim].forEach(x=>x.addEventListener("input",calc));calc()})})();
"""


def tag(text: str) -> str:
    return html.escape(text, quote=True)


def terms(items: list[tuple[str, str]]) -> str:
    return '<div class="terms">' + "\n".join(
        f'<div class="term"><strong>{tag(k)}</strong>{v}</div>' for k, v in items
    ) + "</div>"


def grid(items: list[tuple[str, str, str]], columns: int = 3) -> str:
    cls = "grid3" if columns == 3 else "grid2"
    return f'<div class="{cls}">' + "\n".join(
        f'<div class="box {kind}"><h3>{tag(title)}</h3><p>{body}</p></div>' for title, body, kind in items
    ) + "</div>"


def code_block(code_id: str, label: str, code: str, kind: str = "walk", badge: str = "逐行拆解") -> str:
    return (
        f'<div class="codebar {kind}"><span><span class="badge {"err" if kind == "error" else "ok" if kind == "good" else "walk"}">{tag(badge)}</span> {tag(label)}</span>'
        f'<button class="copy" onclick="copyCode(\'{code_id}\')">复制</button></div>'
        f'<pre><code id="{code_id}">{html.escape(code)}</code></pre>'
    )


def formula(body: str) -> str:
    return f'<div class="formula">{body}</div>'


def viz(buttons: list[tuple[str, str, str, str]], note: str) -> str:
    btns = "\n".join(
        f'<button class="viz-btn" data-title="{tag(title)}" data-note="{tag(note_text)}" data-rows="{tag(rows)}">{tag(label)}</button>'
        for label, title, note_text, rows in buttons
    )
    return f"""
<div class="viz-panel">
  <div class="viz-title"><span>交互观察</span><span class="tag">interactive</span></div>
  <div class="viz-grid">
    <div class="viz-cell"><div class="viz-flow">{btns}</div></div>
    <div class="viz-cell">
      <div class="viz-output"><b class="viz-state-title">选择一个场景</b><span class="viz-note-text">这里会显示判断结果。</span></div>
      <table class="metric-table"><thead><tr><th>项目</th><th>观察</th></tr></thead><tbody class="metric-body"></tbody></table>
      <div class="viz-note">{note}</div>
    </div>
  </div>
</div>
"""


def bars(rows: list[tuple[str, int, str]]) -> str:
    return '<div class="viz-panel"><div class="viz-title"><span>数值对比</span><span class="tag">scale</span></div><div class="viz-cell">' + "\n".join(
        f'<div class="bar-row"><b>{tag(label)}</b><div class="bar"><span style="width:{pct}%"></span></div><span>{tag(value)}</span></div>'
        for label, pct, value in rows
    ) + "</div></div>"


def param_demo() -> str:
    return """
<div class="viz-panel" data-param-demo>
  <div class="viz-title"><span>LoRA 参数量计算器</span><span class="tag">2 x modules x layers x d x r</span></div>
  <div class="viz-grid">
    <div class="viz-cell">
      <label>rank r：<span data-rank-out>8</span><input data-rank type="range" min="1" max="64" value="8"></label>
      <label>每层 LoRA 矩阵数：<span data-targets-out>2</span><input data-targets type="range" min="1" max="6" value="2"></label>
      <label>层数 L<input data-layers type="text" value="96"></label>
      <label>隐藏维度 d_model<input data-dim type="text" value="12288"></label>
    </div>
    <div class="viz-cell">
      <div class="viz-output"><b>估算结果</b><span data-param-out></span></div>
      <div class="viz-note">判断提示：对一个方阵投影，LoRA 每个目标矩阵训练 A 和 B 两个矩阵，所以参数量约为 2 x d_model x r。再乘以层数和目标矩阵数。</div>
    </div>
  </div>
</div>
"""


def practice(groups: list[dict], keys: str) -> str:
    body = """
<section id="practice">
  <div class="head"><h2>综合练习</h2><span class="tag">mixed drills</span></div>
  <div class="practice-intro">
    <div class="review-card"><strong>作答方式</strong><p>前面的例题用于即时检查；这里的综合练习会整理成记录。短答题尽量写出判断依据，不只写一个结论。</p></div>
    <div class="review-card"><strong>自查重点</strong><ul><li>诊断题是否写了错因、后果、修法。</li><li>概念题是否区分相邻概念。</li><li>费曼题是否串起本块主线。</li></ul></div>
  </div>
  <div class="practice-check">
    <div class="check-item"><b>概念</b>能说清术语含义。</div>
    <div class="check-item"><b>公式</b>能解释符号和形状。</div>
    <div class="check-item"><b>诊断</b>能指出错误后果。</div>
    <div class="check-item"><b>表达</b>能用自己的话复述。</div>
  </div>
"""
    index = 1
    for group in groups:
        body += f"""
  <div class="practice-group">
    <div class="group-head"><div><h3>{tag(group['title'])}</h3><p>{group['intro']}</p></div><div class="quick-review"><b>检查点</b><span>{group['review']}</span></div></div>
    <div class="drill-grid">
"""
        for q in group["questions"]:
            qtype = q.get("type", "short")
            full = " full" if q.get("full") else ""
            body += f'<div class="q{full}" data-role="homework" data-type="{tag(qtype)}" data-title="{tag(q["title"])}"'
            if qtype == "feynman":
                body += f' data-keys="{tag(keys)}"'
            body += ">"
            body += f'<div class="q-meta"><span class="pill">{tag(q.get("kind", "短答"))}</span><span class="pill">{tag(q.get("topic", group["title"]))}</span></div>'
            body += f'<h3>{index}. {q["prompt"]}</h3>'
            if q.get("hint"):
                body += f'<p class="hint">{q["hint"]}</p>'
            if q.get("options"):
                input_type = "checkbox" if qtype == "multi" else "radio"
                for option in q["options"]:
                    body += f'<label><input type="{input_type}" name="q{index}" value="{tag(option)}"> {tag(option)}</label>'
            elif qtype == "fill":
                body += '<input type="text">'
            else:
                ph = q.get("placeholder", "")
                body += f'<textarea placeholder="{tag(ph)}"></textarea>'
            body += "</div>\n"
            index += 1
        body += "    </div>\n  </div>\n"
    body += """
</section>
<section id="final">
  <div class="head"><h2>导出练习记录</h2><span class="tag">record</span></div>
  <p class="muted">完成综合练习后生成一份记录，便于回看哪些判断还不稳。</p>
  <div class="actions"><button onclick="generateAnswer()">生成记录</button><button class="ghost" onclick="copyAnswer()">复制记录</button></div>
  <div id="quality" class="quality"></div>
  <div id="answer" class="answer">尚未生成。</div>
</section>
"""
    return body


PAGES = [
    {
        "dir": "01_为什么大模型微调需要PEFT",
        "title": "为什么大模型微调需要 PEFT",
        "subtitle": "从全量微调的代价读懂 LoRA 的问题意识",
        "kicker": "第 1 块 · 论文动机",
        "side": "先把问题讲清楚，再谈方法。LoRA 不是为了显得参数少，而是为了让大模型能服务多个下游任务。",
        "goals": [
            "解释全量微调在大模型时代的存储、显存和部署代价。",
            "区分 full fine-tuning、BitFit、adapter、prefix tuning、LoRA。",
            "判断一个 PEFT 方法到底解决了参数量、延迟、上下文长度还是任务切换问题。",
            "用论文中的 GPT-3 175B 例子说明为什么任务参数不能按任务复制一整份模型。",
        ],
        "sections": [
            ("problem", "1. 全量微调贵在哪里", "problem", """
<p>直觉先说清楚：全量微调不是只在训练时贵，它还会把每个下游任务都变成一份新的大模型。模型越大，这件事越不像“多存几个文件”，更像给每个任务都准备一套完整机器。GPT-3 175B 这种规模下，复制一个任务 checkpoint 就已经是几百 GB 级别；如果一个服务要支持上百个任务，存储和切换都会变成实际系统问题。</p>
<p>术语上，full fine-tuning 是从预训练参数 <code>Phi_0</code> 出发，更新所有参数，得到 <code>Phi_0 + Delta Phi</code>。它的好处是表达能力强，模型所有层都能为新任务调整。代价也来自这里：每个任务学到的 <code>Delta Phi</code> 和原模型一样大，训练时还要为绝大多数参数保存梯度和 Adam 优化器状态。</p>
<p>论文的问题意识不是“全量微调不行”，而是“当一个大模型要服务很多下游任务时，全量微调难以部署”。这点很重要。LoRA 要保住全量微调的任务质量，同时把任务相关的可训练参数压到很小，并且不要像一些 adapter 那样增加推理延迟。</p>
<p>判断句：如果一个方法让每个任务都要保存一整份 175B 参数，它就没有解决多任务部署的主要成本。你现在应该能把“训练成本”和“部署成本”分开说。</p>
""" + formula('<span class="big">full fine-tuning:</span> &nbsp; Phi = Phi<span class="sub">0</span> + Delta Phi, &nbsp; |Delta Phi| = |Phi<span class="sub">0</span>|') + bars([
    ("单个 GPT-3 任务全量权重", 100, "约 350GB FP16"),
    ("100 个任务全量微调", 100, "约 35TB"),
    ("共享底座 + 100 个 LoRA", 2, "约 354GB"),
]) + "<p>上面的数字来自论文的工程估算：底座模型仍然需要存在，但每个任务不再复制整份模型，只增加很小的 LoRA 权重。你现在应该能解释为什么“每任务参数量”比“总模型参数量”更适合作为 PEFT 的核心指标。</p>"),
            ("objective", "2. 论文里的问题定义", "objective", """
<p>论文把任务写成条件文本生成：给定输入 <code>x</code>，模型生成目标序列 <code>y</code>。训练目标是在下游数据集上最大化每个 token 的条件概率。这个公式看起来像语言模型常规训练，但这里的重点不是损失函数本身，而是参数从哪里来、更新到哪里去。</p>
<p>全量微调直接优化 <code>Phi</code>。PEFT 改成优化一个更小的参数集合 <code>Theta</code>，再由 <code>Theta</code> 间接决定模型更新 <code>Delta Phi(Theta)</code>。换句话说，模型最终仍然要适配任务，但我们不允许每个任务自由改动所有权重，而是给它一个受控、低成本的更新通道。</p>
<p>这个写法帮你看清各类方法的共同点：adapter 学的是额外模块参数，prefix 学的是特殊 token 或层激活，BitFit 学的是 bias，LoRA 学的是低秩矩阵。它们都把“更新整个模型”改写为“学习小型任务参数”。</p>
""" + formula('<span class="big">PEFT:</span> &nbsp; max<span class="sub">Theta</span> Σ log p<span class="sub">Phi0 + Delta Phi(Theta)</span>(y<span class="sub">t</span> | x, y<span class="sub">&lt;t</span>), &nbsp; |Theta| << |Phi<span class="sub">0</span>|') + """
<p>判断句：只要能指出 <code>Theta</code> 是什么、它如何影响模型输出，你就能读懂一个 PEFT 方法的核心设计。你现在应该能从公式里分出“底座参数”和“任务参数”。</p>
"""),
            ("baselines", "3. 已有方法解决了什么，又留下什么问题", "baselines", """
<p>Adapter 的想法很直接：在模型内部插入小的瓶颈层，只训练这些新层。它确实减少了可训练参数，但新层通常沿着网络深度顺序执行。在线推理时，特别是 batch size 小、序列短的时候，这些额外顺序计算会带来明显延迟。论文在 GPT-2 medium 上测到，adapter 可能带来 20% 到 30% 以上的延迟增加。</p>
<p>Prefix tuning 走另一条路：不改模型权重，训练一组连续提示向量。它的代价不是额外深度，而是占用可用序列长度，并且优化可能不稳定。特殊 token 多了以后，下游任务真正能使用的上下文变短，输入分布也可能偏离预训练时见过的形式。</p>
<p>BitFit 只训练 bias，参数更少，但表达能力有限。Top-k fine-tuning 只训练最后几层，比全量微调省一些，但仍然不是极小任务模块。LoRA 的位置就在这里：它想像 adapter 一样参数少，但推理时能并回原权重；想像 prefix 一样不复制整模型，但不占上下文长度。</p>
""" + grid([
    ("Adapter", "优点是模块小、直观；问题是插入顺序计算，可能增加推理延迟。", "warn"),
    ("Prefix tuning", "优点是不直接改权重；问题是占用上下文长度，训练和参数规模不一定单调变好。", "warn"),
    ("LoRA", "训练低秩更新，部署时可 merge 进原线性层，目标是参数少且零额外推理延迟。", "ok"),
], 3) + "<p>判断句：参数少只是 PEFT 的一个维度；还要问是否增加推理延迟、是否占上下文长度、是否方便切换任务。你现在应该能用这四个维度比较方法。</p>"),
            ("map", "4. PEFT 方法的对照地图", "map", """
<div class="map"><span class="node">全量微调</span><span class="node">只训少量参数</span><span class="node">保持质量</span><span class="node">控制延迟</span><span class="node">方便切换任务</span></div>
<p>LoRA 的论文贡献要放在这个地图里读。它不是第一个参数高效方法，也不是唯一能微调大模型的方法。它的关键组合是：冻结预训练权重、用低秩矩阵表达权重更新、推理时把更新并回原权重、在多个模型和任务上达到接近或超过全量微调的效果。</p>
<p>学习论文时最容易犯的错，是只记“LoRA 把参数量减少 10000 倍”。这句话本身没错，但它不是完整理解。你还要知道这个数来自 GPT-3 175B、Adam 优化器、只适配部分 attention 权重、每任务 checkpoint 等具体语境。没有语境的数量级会变成宣传口径。</p>
""" + viz([
    ("全量微调", "全量微调", "每个任务复制或保存一整份更新后的模型，质量强但部署重。", "训练参数=全部权重|推理延迟=无额外层|任务切换=重|主要成本=存储/显存/优化器状态"),
    ("Adapter", "Adapter", "只训练小模块，但模块顺序插入网络，在线短序列推理可能变慢。", "训练参数=adapter 层|推理延迟=可能增加|任务切换=换模块|主要成本=额外深度"),
    ("Prefix", "Prefix tuning", "训练特殊提示向量，不复制模型，但会占用可用序列长度。", "训练参数=prefix token/层激活|推理延迟=不一定大|任务切换=换 prefix|主要成本=上下文长度/优化稳定性"),
    ("LoRA", "LoRA", "训练低秩矩阵，部署时可以 merge 成普通线性层。", "训练参数=A 和 B|推理延迟=merge 后无额外延迟|任务切换=换 LoRA 权重|主要成本=不能轻易混批不同任务"),
], "判断提示：读 PEFT 方法时，不要只看参数量。把训练参数、推理延迟、上下文长度、任务切换放到同一张表里。") ),
            ("pitfalls", "5. 常见误区和修正", "pitfalls", grid([
                ("误区：PEFT 一定比全量微调弱", "参数少不等于表达力完全不足。论文实验显示 LoRA 在多组任务上可达到或超过全量微调，但这不是所有任务的保证。", "bad"),
                ("误区：adapter 参数少所以零延迟", "adapter 的小矩阵仍然在网络里顺序执行。延迟取决于硬件、batch size、序列长度和实现。", "bad"),
                ("误区：prefix 不改权重就没有代价", "prefix 会占用位置和序列长度，特殊 token 太多还可能让输入分布变怪。", "bad"),
                ("误区：LoRA 不需要底座模型", "LoRA 只保存任务更新。推理时仍然需要完整预训练模型。", "bad"),
                ("误区：10000 倍是所有场景通用数字", "这是论文在特定 GPT-3 配置下的数量级。换模型、rank、target modules 后要重新算。", "warn"),
                ("误区：只看平均指标就够了", "PEFT 还要看训练吞吐、显存、部署延迟、任务切换和可维护性。", "warn"),
            ], 3) ),
            ("examples", "6. 试一试：把问题说成工程判断", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p>一个 7B 模型要为 30 个客户做定制分类器。全量微调的主要部署问题是什么？</p><p class="hint">参考思路：每个客户一份大 checkpoint，存储和加载切换成本高，训练时优化器状态也重。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>adapter 和 LoRA 都有小矩阵，为什么推理延迟不同？</p><p class="hint">adapter 是顺序新层；LoRA 的线性更新可提前并回原权重。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>prefix tuning 为什么可能影响长上下文任务？</p><p class="hint">特殊 token 占用序列位置，任务 token 可用长度减少。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、基础概念", "intro": "先检查你是否能把论文动机说清楚。", "review": "问自己：这个方法到底训练什么，部署时付出什么？", "questions": [
                {"title": "PEFT 目的", "kind": "单选", "type": "choice", "prompt": "LoRA 论文中 PEFT 最直接要缓解的问题是哪一个？", "options": ["每个下游任务复制和训练整套大模型太贵", "让模型完全不需要下游数据", "让所有推理都不用底座模型"]},
                {"title": "全量微调", "kind": "判断", "type": "choice", "prompt": "全量微调的任务参数增量 Delta Phi 通常和原模型参数规模相同。", "options": ["正确", "错误"]},
                {"title": "LoRA 是否需要底座", "kind": "判断", "type": "choice", "prompt": "只保存 LoRA 权重就可以脱离预训练底座模型单独推理。", "options": ["正确", "错误"]},
                {"title": "Theta", "kind": "填空", "type": "fill", "prompt": "PEFT 公式里，小型可训练任务参数通常记作 ____。"},
                {"title": "任务参数", "kind": "填空", "type": "fill", "prompt": "全量微调中，每个任务学到的参数增量通常记作 ____。"},
                {"title": "部署代价", "kind": "短答", "prompt": "为什么“训练完以后保存一个新模型”在 GPT-3 175B 级别会变成部署问题？", "hint": "从每任务 checkpoint、存储、加载切换和多任务服务说。"},
            ]},
            {"title": "二、方法对照", "intro": "这一组检查你是否能把相邻方法分开。", "review": "比较时至少说训练对象和推理影响。", "questions": [
                {"title": "方法匹配", "kind": "匹配", "prompt": "把 full fine-tuning、adapter、prefix tuning、LoRA 分别匹配到它们训练的对象。"},
                {"title": "adapter 延迟", "kind": "短答", "prompt": "为什么 adapter 参数很少，仍然可能增加在线推理延迟？"},
                {"title": "prefix 代价", "kind": "短答", "prompt": "prefix tuning 可能牺牲什么资源？为什么？"},
                {"title": "BitFit", "kind": "单选", "type": "choice", "prompt": "BitFit 主要训练什么？", "options": ["bias 参数", "全部 attention 权重", "额外 prefix token 的文本内容"]},
                {"title": "多选比较维度", "kind": "多选", "type": "multi", "prompt": "评估 PEFT 方法时应该看哪些维度？", "options": ["可训练参数量", "推理延迟", "是否占用上下文长度", "任务切换成本"]},
                {"title": "序列长度", "kind": "短答", "prompt": "为什么“占用上下文长度”在长文档、摘要或代码任务里会变成真实成本？"},
            ]},
            {"title": "三、错误诊断与表达", "intro": "这一组要求你把概念放回真实判断。", "review": "诊断题按错因、后果、修法写。", "questions": [
                {"title": "错误诊断：只看参数量", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：“adapter 参数不到 1%，所以它一定不会影响推理速度。”按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：LoRA 不要底座", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：“我训练了 LoRA，所以部署时只上传 35MB LoRA 权重就够了。”按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "场景应用", "kind": "场景", "prompt": "你要给一个共享大模型接 50 个客户任务，会优先关注 PEFT 的哪 4 个工程指标？"},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话解释 LoRA 相对 adapter 的推理延迟优势。"},
                {"title": "面试追问：质量和效率", "kind": "面试追问", "prompt": "为什么论文不能只证明 LoRA 参数少，还必须证明它在任务指标上接近或超过全量微调？"},
                {"title": "场景：低数据任务", "kind": "场景", "prompt": "如果下游任务只有几百条样本，你会如何看待全量微调和 PEFT 的风险？"},
                {"title": "论文主张边界", "kind": "短答", "prompt": "“LoRA 没有额外推理延迟”这句话默认依赖什么部署动作？"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 6-9 句话向刚学大模型的人解释：为什么 LoRA 论文要从 PEFT 问题讲起。", "hint": "请串联：全量微调、任务参数、adapter、prefix、LoRA、推理延迟。"},
            ]},
        ],
        "keys": "全量微调,任务参数,adapter,prefix,LoRA,推理延迟",
    },
    {
        "dir": "02_LoRA低秩更新公式",
        "title": "LoRA 低秩更新公式",
        "subtitle": "把 Delta W 写成 BA，读懂形状、参数量、初始化和 merge",
        "kicker": "第 2 块 · 方法核心",
        "side": "这一块只盯住一个公式：h = W0x + BAx。公式看懂了，LoRA 的大半机制就不会飘。",
        "goals": [
            "写出 LoRA 的核心前向公式，并解释每个矩阵的形状。",
            "根据 d、k、r 计算一个 LoRA 模块的可训练参数量。",
            "说明为什么 A 随机初始化、B 初始化为 0。",
            "解释 alpha/r 的缩放作用，以及 merge 为什么能消除额外推理延迟。",
        ],
        "sections": [
            ("intuition", "1. 直觉：不直接改 W，而是学 W 的改变量", "low-rank", """
<p>LoRA 的核心不是“加一个小网络”，而是把原来要学习的权重改变量拆成两个小矩阵。预训练权重 <code>W0</code> 保持不动，下游任务只学习 <code>Delta W</code>。但 <code>Delta W</code> 仍然可能和 <code>W0</code> 一样大，于是 LoRA 进一步约束：让 <code>Delta W = BA</code>，其中中间维度 <code>r</code> 很小。</p>
<p>用形状看会更清楚。假设原线性层权重 <code>W0</code> 的形状是 <code>d x k</code>，输入 <code>x</code> 是 <code>k</code> 维，输出是 <code>d</code> 维。LoRA 让 <code>A</code> 先把输入从 <code>k</code> 维压到 <code>r</code> 维，再让 <code>B</code> 从 <code>r</code> 维还原到 <code>d</code> 维。这样 <code>BA</code> 的形状仍然是 <code>d x k</code>，可以和 <code>W0</code> 相加。</p>
<p>术语上，这叫低秩参数化更新。它不是说原模型权重 <code>W0</code> 必须低秩，而是说下游任务需要的改变量可能只占少数方向。LoRA 把可训练自由度限制在这些低维方向里。限制得太小可能表达不够，限制得合适就能省大量参数。</p>
<p>判断句：看到一个 LoRA 公式时，先检查 <code>BA</code> 是否和 <code>W0</code> 同形状。如果形状对不上，后面讲得再漂亮也不能加到原线性层上。你现在应该能用形状判断一个 LoRA 实现是否写反。</p>
""" + formula('<span class="big">h = W<span class="sub">0</span>x + Delta W x = W<span class="sub">0</span>x + BAx</span><br>W<span class="sub">0</span> in R<span class="sup">d x k</span>, &nbsp; B in R<span class="sup">d x r</span>, &nbsp; A in R<span class="sup">r x k</span>, &nbsp; r << min(d,k)') + """
<div class="svg-wrap">
<svg viewBox="0 0 760 230" role="img" aria-label="LoRA 矩阵形状图">
  <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#1b2a4a"/></marker></defs>
  <rect x="30" y="70" width="90" height="70" fill="#eef8fe" stroke="#1b2a4a"/><text x="75" y="110" text-anchor="middle" font-size="18">x</text><text x="75" y="132" text-anchor="middle" font-size="12">k 维</text>
  <line x1="125" y1="105" x2="205" y2="105" stroke="#1b2a4a" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="210" y="35" width="120" height="70" fill="#fff8e1" stroke="#a66b00"/><text x="270" y="74" text-anchor="middle" font-size="18">W0</text><text x="270" y="95" text-anchor="middle" font-size="12">d x k 冻结</text>
  <rect x="210" y="130" width="120" height="70" fill="#ecfdf3" stroke="#166534"/><text x="270" y="160" text-anchor="middle" font-size="18">A 再 B</text><text x="270" y="181" text-anchor="middle" font-size="12">r x k, d x r</text>
  <line x1="335" y1="70" x2="455" y2="105" stroke="#1b2a4a" stroke-width="2" marker-end="url(#arrow)"/><line x1="335" y1="165" x2="455" y2="115" stroke="#1b2a4a" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="460" y="78" width="90" height="70" fill="#f8fafc" stroke="#1b2a4a"/><text x="505" y="110" text-anchor="middle" font-size="18">相加</text><text x="505" y="132" text-anchor="middle" font-size="12">d 维</text>
  <line x1="555" y1="113" x2="645" y2="113" stroke="#1b2a4a" stroke-width="2" marker-end="url(#arrow)"/><rect x="650" y="78" width="90" height="70" fill="#eef8fe" stroke="#1b2a4a"/><text x="695" y="110" text-anchor="middle" font-size="18">h</text><text x="695" y="132" text-anchor="middle" font-size="12">输出</text>
</svg>
</div>
"""),
            ("shape", "2. 参数量：为什么两个小矩阵会省这么多", "parameters", """
<p>一个普通 <code>d x k</code> 权重矩阵有 <code>d*k</code> 个参数。如果全量微调这个矩阵，任务更新也可以覆盖这 <code>d*k</code> 个自由度。LoRA 只训练 <code>A</code> 和 <code>B</code>，参数量变成 <code>r*k + d*r = r(d+k)</code>。如果是 Transformer 里常见的方阵 <code>d_model x d_model</code>，每个目标矩阵就是 <code>2*d_model*r</code>。</p>
<p>这不是魔法，而是明确牺牲了一部分表达自由度。LoRA 只能表示 rank 不超过 <code>r</code> 的更新矩阵。论文的经验发现是：语言模型下游适配常常不需要满秩更新，小 <code>r</code> 就能捕捉主要任务方向。你要记住的是“低秩假设”，不是“免费变强”。</p>
<p>当 LoRA 应用于多层 Transformer 时，还要乘以层数和每层选中的目标矩阵数。论文里常用 <code>W_q</code> 和 <code>W_v</code>，也就是每层两个目标矩阵。GPT-3 175B 有 96 层，<code>d_model=12288</code>，如果 <code>r=8</code> 且每层两个矩阵，参数量大约 3770 万个，FP16 约 72MB。论文也展示了更小预算，比如 4.7M 参数配置。</p>
""" + formula('<span class="big">|Theta| = r*k + d*r = r(d+k)</span><br>若 W 是 d<span class="sub">model</span> x d<span class="sub">model</span>：每个目标矩阵约 2 x d<span class="sub">model</span> x r') + param_demo() + """
<p>判断句：当你看到“LoRA 参数量很小”，应该马上问：rank 是多少，作用了多少层，作用了几个目标矩阵，隐藏维度是多少。你现在应该能手算一个 LoRA 配置的大致参数量。</p>
"""),
            ("init", "3. 初始化：为什么 B 从 0 开始", "initialization", """
<p>论文使用的初始化很朴素：<code>A</code> 随机高斯初始化，<code>B</code> 初始化为 0。这样训练刚开始时 <code>BA=0</code>，LoRA 分支不会改变预训练模型的输出。模型一开始等同于原模型，然后训练逐步学出任务更新。</p>
<p>如果 <code>A</code> 和 <code>B</code> 都随机，刚开始就会给原模型加上一段随机扰动。预训练模型本来已经有可用行为，随机扰动可能让训练初期不稳定。反过来，如果两者都初始化为 0，梯度会出现对称性问题：其中一个矩阵可能拿不到有效方向，训练启动会受影响。随机 A、零 B 是一种常用折中。</p>
<p>这里的判断不要停在“论文这么做”。你要能解释删改后果：B 不为 0 会扰动底座输出；A 和 B 都为 0 会让低秩分支起步困难；忘记冻结 <code>W0</code> 则会变成“LoRA + 部分全量微调”，参数和显存收益都会跑偏。</p>
""" + code_block("c2_init_good", "正确示例：LoRA 初始化思路", """# A: r x in_features，随机初始化
A = normal(mean=0, std=small_value, shape=(r, in_features))

# B: out_features x r，初始化为 0
B = zeros(shape=(out_features, r))

# 初始时 Delta W = B @ A = 0
delta = B @ A""", "good", "正确示例") + code_block("c2_init_bad", "错误示例：两个矩阵都随机扰动底座", """A = normal(shape=(r, in_features))
B = normal(shape=(out_features, r))

# 问题：刚开始 Delta W != 0
# 预训练模型输出被随机分支改写，训练初期可能更不稳。""", "error", "错误示例") + "<p>判断句：初始化是否合理，要看训练第 0 步 LoRA 分支有没有改变原模型输出。你现在应该能诊断 LoRA 初始化错误。</p>"),
            ("scale", "4. alpha/r：控制 LoRA 分支的尺度", "scaling", """
<p>LoRA 前向通常不是直接加 <code>BAx</code>，而是加上 <code>(alpha/r) * BAx</code>。这里 <code>alpha</code> 是缩放常数，<code>r</code> 是 rank。缩放的目的，是让改变 rank 时，LoRA 分支输出的量级不至于失控，也减少每次改 rank 后大幅重调学习率的负担。</p>
<p>直觉上，rank 变大代表分支里有更多方向。如果不做缩放，不同 rank 的输出尺度可能差很多。论文提到，在 Adam 下调 <code>alpha</code> 和调学习率有相近味道，但它不是学习率本身。学习率控制优化步长，<code>alpha/r</code> 控制 LoRA 分支进入主干输出的幅度。</p>
<p>实际项目里常见错误是只记公式但忘记配置语义。<code>alpha</code> 太小，LoRA 分支影响弱；太大，训练可能不稳或覆盖预训练行为。不同库还会把 <code>lora_alpha</code>、<code>scaling</code>、<code>rank</code> 写成不同字段，验收时要确认最终乘到输出上的系数。</p>
""" + formula('<span class="big">h = W<span class="sub">0</span>x + <span class="frac"><span>alpha</span><span>r</span></span> BAx</span>') + """
<div class="viz-panel">
  <div class="viz-title"><span>缩放直觉</span><span class="tag">alpha / r</span></div>
  <div class="viz-cell">
    <div class="bar-row"><b>r=4, alpha=8</b><div class="bar"><span style="width:50%"></span></div><span>scale=2</span></div>
    <div class="bar-row"><b>r=8, alpha=8</b><div class="bar"><span style="width:25%"></span></div><span>scale=1</span></div>
    <div class="bar-row"><b>r=16, alpha=8</b><div class="bar"><span style="width:12.5%"></span></div><span>scale=0.5</span></div>
    <div class="viz-note">判断提示：rank 改了，LoRA 分支的表达方向数变了；缩放项用于控制它进入主分支的量级。</div>
  </div>
</div>
<p>你现在应该能区分：rank 控制低秩空间大小，alpha 控制分支强度，学习率控制参数更新步长。</p>
"""),
            ("merge", "5. merge：为什么部署时可以零额外延迟", "merge", """
<p>LoRA 在训练时有两条路径：原始线性层 <code>W0x</code> 和低秩分支 <code>BAx</code>。但 <code>BA</code> 的结果本身就是一个和 <code>W0</code> 同形状的矩阵。部署时可以先算出 <code>W = W0 + BA</code>，以后推理仍然只跑一个普通线性层。这就是论文说“不引入额外推理延迟”的关键。</p>
<p>merge 不是把 LoRA 扔掉，而是把任务更新吸收到原权重里。切换任务时，可以从 <code>W0</code> 出发，加载另一个任务的 <code>B'A'</code>。工程上要小心重复 merge：如果同一个 LoRA 权重被加了两次，输出就错了。也要记住，merge 后如果还想继续训练 LoRA，需要知道当前权重是否已经包含 LoRA 更新。</p>
<p>这里还有一个边界：如果一个 batch 里混合不同任务，并且每个样本要用不同 LoRA，提前 merge 成单一权重就不方便。可以选择不 merge，动态按样本选择 LoRA 分支，但这样会牺牲一部分延迟优势。论文也提到这个限制。</p>
""" + code_block("c2_merge", "逐行拆解：merge 和 unmerge 的状态", """# 训练时
y = x @ W0.T + scaling * (x @ A.T @ B.T)

# 部署前 merge
W_merged = W0 + scaling * (B @ A)
y = x @ W_merged.T

# 切换任务时，从干净 W0 加另一个 LoRA
W_task_b = W0 + scaling_b * (B_b @ A_b)""") + grid([
                ("merge 前", "便于训练 LoRA、切换不同低秩分支；推理要额外算低秩路径。", "blue"),
                ("merge 后", "推理就是普通线性层；适合单任务部署或服务当前任务。", "ok"),
                ("重复 merge", "同一份 Delta W 被加两次，模型输出偏移。要记录 merge 状态。", "bad"),
            ], 3) + "<p>判断句：“LoRA 零额外推理延迟”默认指已经 merge 到权重后的推理路径。你现在应该能说明这句话的前提。</p>"),
            ("pitfalls", "6. 常见错法：公式看似会了，代码却写坏了", "diagnosis", grid([
                ("A/B 形状写反", "如果 B@A 不能得到 d x k，就无法和 W0 相加。先用形状验收。", "bad"),
                ("忘记冻结 W0", "底座参数继续训练，显存、优化器状态和任务 checkpoint 都会变重。", "bad"),
                ("B 不为 0", "初始输出被随机 LoRA 分支扰动，训练起点不再是预训练模型。", "warn"),
                ("alpha 当学习率", "alpha 控制 LoRA 输出尺度，不等同于优化器步长。两者都会影响训练，但位置不同。", "warn"),
                ("重复 merge", "多次把同一 LoRA 加到 W0，会让更新翻倍。需要 merge 状态标记。", "bad"),
                ("rank 盲目越大越好", "rank 越大参数越多，不保证指标单调提升。论文实验里小 r 已经很强。", "warn"),
            ], 3)),
            ("examples", "7. 试一试：用形状检查公式", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p><code>W0</code> 是 4096 x 4096，<code>r=8</code>。一个 LoRA 目标矩阵有多少可训练参数？</p><p class="hint">参考：2 x 4096 x 8 = 65536。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>如果 <code>A</code> 是 4096 x 8，<code>B</code> 是 8 x 4096，哪里不对？</p><p class="hint">按论文约定，B@A 应得到 d x k。这个写法乘出来是 8 x 8 或需要换转置语义。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>为什么刚开始 <code>Delta W=0</code> 是好事？</p><p class="hint">训练第 0 步保留预训练模型行为，LoRA 分支从不扰动开始学习。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、公式和形状", "intro": "先检查你是否真的能读懂 h = W0x + BAx。", "review": "任何 LoRA 实现先验形状，再谈效果。", "questions": [
                {"title": "核心公式", "kind": "填空", "type": "fill", "prompt": "LoRA 把权重更新写成 Delta W = ____。"},
                {"title": "冻结对象", "kind": "单选", "type": "choice", "prompt": "LoRA 训练时通常冻结哪个对象？", "options": ["预训练权重 W0", "低秩矩阵 A 和 B", "下游数据集"]},
                {"title": "形状判断", "kind": "填空", "type": "fill", "prompt": "若 W0 是 d x k，A 是 r x k，则 B 应该是 ____。"},
                {"title": "输出维度", "kind": "短答", "prompt": "为什么 BAx 的输出维度必须和 W0x 一样？"},
                {"title": "低秩含义", "kind": "短答", "prompt": "LoRA 中“低秩”限制的是 W0 还是 Delta W？请说明。"},
                {"title": "判断 rank", "kind": "判断", "type": "choice", "prompt": "rank r 越大，LoRA 的可训练参数越多。", "options": ["正确", "错误"]},
            ]},
            {"title": "二、参数量和缩放", "intro": "这一组把公式落到可计算数量。", "review": "先写参数量公式，再代数。", "questions": [
                {"title": "参数量公式", "kind": "填空", "type": "fill", "prompt": "一个 d x k 权重矩阵的 LoRA 参数量是 ____。"},
                {"title": "方阵计算", "kind": "计算", "prompt": "W0 是 4096 x 4096，r=16。一个目标矩阵的 LoRA 参数量是多少？"},
                {"title": "多层计算", "kind": "计算", "prompt": "一个 32 层模型，每层对 Wq 和 Wv 加 LoRA，d_model=4096，r=8。可训练参数量约是多少？"},
                {"title": "alpha/r", "kind": "短答", "prompt": "alpha/r 缩放控制的是什么？它和学习率有什么区别？"},
                {"title": "rank 越大越好", "kind": "判断", "type": "choice", "prompt": "只要显存允许，rank 越大验证集指标一定越好。", "options": ["正确", "错误"]},
                {"title": "参数少的代价", "kind": "短答", "prompt": "为什么说 LoRA 参数少不是免费午餐？"},
            ]},
            {"title": "三、初始化、merge 和诊断", "intro": "这一组检查你能不能发现实现错误。", "review": "诊断题按错因、后果、修法写。", "questions": [
                {"title": "初始化理由", "kind": "短答", "prompt": "为什么论文让 A 随机初始化、B 初始化为 0？"},
                {"title": "错误诊断：两个都随机", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：A 和 B 都随机初始化，训练第 0 步模型输出已经改变。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：忘记冻结", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：训练 LoRA 时 W0 也在更新。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "merge 前提", "kind": "短答", "prompt": "为什么 LoRA merge 后可以没有额外推理延迟？"},
                {"title": "重复 merge", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：同一个 LoRA 权重被 merge 两次。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "混批边界", "kind": "场景", "prompt": "如果一个 batch 里每个样本要用不同 LoRA，merge 策略会遇到什么问题？"},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话解释 LoRA 为什么能省参数。"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 6-9 句话解释 LoRA 的低秩更新公式，从 W0、A、B、r、alpha/r 一直讲到 merge。", "hint": "请串联：W0、Delta W、A、B、rank、alpha/r、merge。"},
            ]},
        ],
        "keys": "W0,Delta W,A,B,rank,alpha/r,merge",
    },
    {
        "dir": "03_LoRA放进Transformer",
        "title": "LoRA 放进 Transformer",
        "subtitle": "从 Wq/Wv 的落点理解显存、checkpoint、吞吐和任务切换",
        "kicker": "第 3 块 · Transformer 应用",
        "side": "公式能跑只是第一步。真正用 LoRA，要知道它放在哪些权重上，以及这些选择带来什么工程后果。",
        "goals": [
            "说清 Transformer attention 中 Wq、Wk、Wv、Wo 的角色。",
            "解释论文为什么主要把 LoRA 放在 attention 权重，而不是默认改所有层。",
            "根据 target modules 判断参数量、显存、checkpoint 和任务切换影响。",
            "诊断 target module 选错、MLP 是否冻结、merge 与多任务混批等工程问题。",
        ],
        "sections": [
            ("attention", "1. Transformer 里哪些矩阵可以放 LoRA", "attention", """
<p>论文说 LoRA 原则上可以应用到神经网络里的任意 dense layer。放到 Transformer 里，最自然的候选包括 self-attention 的四类投影矩阵 <code>Wq</code>、<code>Wk</code>、<code>Wv</code>、<code>Wo</code>，以及 MLP 里的两个线性层。论文实验为了简化和控制参数量，主要研究 attention 权重，并在多数实验中只适配 <code>Wq</code> 和 <code>Wv</code>。</p>
<p>先给直觉：attention 需要把 token 表示投影成 query、key、value，再把注意力结果投影回模型维度。<code>Wq</code> 影响“我用什么问题去看上下文”，<code>Wk</code> 影响“别人提供什么索引被我匹配”，<code>Wv</code> 影响“被取回的信息内容是什么”，<code>Wo</code> 影响“注意力结果如何写回残差流”。这些说法不是严格语义解释，但能帮助你理解不同 target module 的作用位置。</p>
<p>论文把每个投影看成 <code>d_model x d_model</code> 的矩阵，即使实现里会按 attention heads 切分输出维度。LoRA 不需要每个 head 单独理解，它通常作用在完整线性投影上。你现在应该能在模型模块名里识别 <code>q_proj</code>、<code>v_proj</code>、<code>query</code>、<code>value</code> 这类目标。</p>
""" + """
<div class="svg-wrap">
<svg viewBox="0 0 820 280" role="img" aria-label="Transformer attention LoRA 落点">
  <defs><marker id="a3" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#1b2a4a"/></marker></defs>
  <rect x="30" y="105" width="90" height="60" fill="#eef8fe" stroke="#1b2a4a"/><text x="75" y="140" text-anchor="middle">hidden</text>
  <line x1="125" y1="135" x2="185" y2="70" stroke="#1b2a4a" marker-end="url(#a3)"/><line x1="125" y1="135" x2="185" y2="135" stroke="#1b2a4a" marker-end="url(#a3)"/><line x1="125" y1="135" x2="185" y2="200" stroke="#1b2a4a" marker-end="url(#a3)"/>
  <rect x="190" y="40" width="110" height="48" fill="#ecfdf3" stroke="#166534"/><text x="245" y="69" text-anchor="middle">Wq + LoRA</text>
  <rect x="190" y="111" width="110" height="48" fill="#fff" stroke="#9aa8b6"/><text x="245" y="140" text-anchor="middle">Wk</text>
  <rect x="190" y="182" width="110" height="48" fill="#ecfdf3" stroke="#166534"/><text x="245" y="211" text-anchor="middle">Wv + LoRA</text>
  <rect x="370" y="103" width="150" height="66" fill="#f8fafc" stroke="#1b2a4a"/><text x="445" y="132" text-anchor="middle">attention</text><text x="445" y="154" text-anchor="middle" font-size="12">softmax(QK^T)V</text>
  <line x1="305" y1="64" x2="365" y2="118" stroke="#1b2a4a" marker-end="url(#a3)"/><line x1="305" y1="135" x2="365" y2="135" stroke="#1b2a4a" marker-end="url(#a3)"/><line x1="305" y1="206" x2="365" y2="154" stroke="#1b2a4a" marker-end="url(#a3)"/>
  <line x1="525" y1="136" x2="595" y2="136" stroke="#1b2a4a" marker-end="url(#a3)"/><rect x="600" y="112" width="110" height="48" fill="#fff" stroke="#9aa8b6"/><text x="655" y="141" text-anchor="middle">Wo</text>
  <line x1="715" y1="136" x2="780" y2="136" stroke="#1b2a4a" marker-end="url(#a3)"/><text x="790" y="141" font-size="13">output</text>
</svg>
</div>
<p>判断句：target module 不是随便填字符串。你要知道它对应 attention 的哪类投影，以及该选择会影响多少参数。你现在应该能把论文里的 <code>Wq/Wv</code> 映射到常见代码里的 <code>q_proj/v_proj</code>。</p>
"""),
            ("why-qv", "2. 为什么论文常选 Wq 和 Wv", "target modules", """
<p>论文在 GPT-3 175B 上做了一个固定参数预算的实验：给相同的可训练参数量，比较 LoRA 放到不同 attention 权重上的效果。结果显示，只放 <code>Wq</code> 或只放 <code>Wk</code> 往往不如把预算分给 <code>Wq</code> 和 <code>Wv</code>；适配 <code>Wq,Wv</code> 在 WikiSQL 和 MultiNLI 上整体表现强，适配四个投影也有竞争力。</p>
<p>这给出一个实践直觉：与其把 rank 全堆到一个矩阵上，不如在关键投影上分散一些低秩方向。论文的解释不是“Wq/Wv 永远最优”，而是在它们的实验预算和任务里，query 与 value 的组合更划算。现代实现里也常把 LoRA 默认加到 <code>q_proj</code> 和 <code>v_proj</code>，有些模型会加上 <code>k_proj</code>、<code>o_proj</code>，甚至 MLP 投影。</p>
<p>你要学到的是选择逻辑：target modules 越多，每个 rank 带来的参数越多；固定参数预算下，增加模块数可能需要降低 rank。选少了可能表达不够，选多了可能训练成本上升，也可能对具体任务没有额外收益。</p>
""" + grid([
                ("只放 Wq", "改查询方向，参数集中但覆盖面窄。论文表中 WikiSQL 表现弱于 Wq+Wv。", "warn"),
                ("放 Wq + Wv", "同时改注意力读取方式和被读取内容，是论文多数实验的简洁选择。", "ok"),
                ("放四个投影", "覆盖更广，但固定预算下 rank 更低。是否更好要看任务和模型。", "blue"),
            ], 3) + viz([
                ("Wq", "只适配 Wq", "预算集中在 query 投影。可能改了“看什么”，但 value 内容通道不变。", "target=Wq|rank=8|WikiSQL=70.4|MultiNLI=91.0"),
                ("Wv", "只适配 Wv", "预算集中在 value 投影。论文表中比只适配 Wq/Wk 更强。", "target=Wv|rank=8|WikiSQL=73.0|MultiNLI=91.0"),
                ("Wq+Wv", "适配 Wq 和 Wv", "固定预算下 rank 降到 4，但整体表现很强。", "target=Wq,Wv|rank=4|WikiSQL=73.7|MultiNLI=91.3"),
                ("all-attn", "适配 Wq,Wk,Wv,Wo", "覆盖四类投影，rank 降到 2。MultiNLI 表现最好，WikiSQL 与 Wq+Wv 接近。", "target=四个 attention 投影|rank=2|WikiSQL=73.7|MultiNLI=91.7"),
], "判断提示：固定预算下，target modules 和 rank 是一对 trade-off。不要只看 rank，也不要只看模块数。") ),
            ("memory", "3. 工程收益：显存、checkpoint 和吞吐", "engineering", """
<p>LoRA 的训练显存收益来自冻结大部分参数。使用 Adam 这类自适应优化器时，训练一个参数不仅要保存参数本身，还要保存梯度、一阶/二阶动量等优化器状态。冻结底座权重后，绝大多数参数不需要梯度和优化器状态，显存压力明显下降。论文给出的 GPT-3 175B 例子里，训练显存从约 1.2TB 降到约 350GB。</p>
<p>checkpoint 收益也很直接。全量微调保存的是整套任务模型；LoRA 保存的是每个任务的 A/B 矩阵。论文中 <code>r=4</code> 且只适配 query/value 时，任务 checkpoint 从 350GB 量级降到 35MB 量级。底座模型仍然要保存和加载，但上百个任务只需要共享一份底座，外加很多小 LoRA。</p>
<p>吞吐提升来自少算很多梯度。论文报告 GPT-3 175B 上 LoRA 训练吞吐比全量微调高约 25%。这个数字不是所有训练都固定成立，但机制清楚：冻结参数不反传梯度，不维护优化器状态，I/O 和内存压力也更低。</p>
""" + bars([
    ("训练显存：全量微调", 100, "约 1.2TB"),
    ("训练显存：LoRA", 29, "约 350GB"),
    ("单任务 checkpoint：全量", 100, "约 350GB"),
    ("单任务 checkpoint：LoRA", 1, "约 35MB"),
]) + """
<p>判断句：LoRA 的收益不是来自模型本体变小，而是来自“训练和保存的任务参数”变小。你现在应该能解释为什么部署时仍然需要底座模型。</p>
"""),
            ("switch", "4. 任务切换和推理路径", "deployment", """
<p>共享底座模型后，不同任务只需要切换 LoRA 权重。对于一个在线服务，如果当前机器已经把底座模型放进显存，任务切换可以变成加载或替换小型 A/B 矩阵，而不是替换几百 GB 的全量权重。论文把这看成 LoRA 的重要部署优势。</p>
<p>但任务切换也有边界。为了零额外推理延迟，通常要把 LoRA merge 到原权重。merge 以后当前权重对应某个任务；如果下一个请求来自另一个任务，就要 unmerge 或从干净底座重新加另一个 LoRA。对于高并发、多任务混合请求，这会影响批处理策略。可以不 merge 动态计算 LoRA 分支，但这样又回到额外计算路径。</p>
<p>所以工程判断不是“LoRA 一定最适合所有服务”，而是看你的请求形态：如果一个服务一段时间主要服务同一任务，merge 很划算；如果一个 batch 内混合很多任务，需要设计 adapter 路由、LoRA 分组或不 merge 的推理路径。</p>
""" + code_block("c3_switch", "逐行拆解：切换任务的权重状态", """# 干净底座
W = W0

# 切到客服摘要任务
W = W0 + scale_summary * (B_summary @ A_summary)

# 切到 SQL 生成任务
W = W0 + scale_sql * (B_sql @ A_sql)

# 不要从已经 merge 的 W 再叠加另一个任务
W_wrong = W + scale_sql * (B_sql @ A_sql)""") + grid([
                ("适合 merge", "长时间服务同一任务、单任务部署、离线批处理。", "ok"),
                ("谨慎 merge", "batch 内混合多个任务，频繁切换 LoRA，或需要按样本选择模块。", "warn"),
                ("不要忘记底座", "LoRA 权重只是增量。没有 W0，A/B 无法单独完成推理。", "bad"),
            ], 3) ),
            ("limits", "5. 论文明确留下的边界", "limitations", """
<p>论文没有声称 LoRA 只能放 attention，也没有证明所有任务都应该用同一组 target modules。它为了简化和参数效率，主要冻结 MLP、LayerNorm 和 bias，把注意力权重作为研究对象。对后续项目来说，这是一条强基线，不是不可更改的规则。</p>
<p>另一个边界是混合任务 batch。LoRA merge 后是单套权重，天然对应某个任务。不同任务用不同 A/B 时，想在一个 forward pass 里混合样本并不简单。你可以不 merge，动态选择 LoRA；也可以按任务分 batch；还可以复制计算路径。每个方案都在延迟、吞吐、显存和实现复杂度之间取舍。</p>
<p>最后，论文的实验主要集中在语言模型和 NLP 任务。LoRA 原理可用于 dense layer，但“放哪里、rank 多大、是否只训 attention”到了视觉、多模态、扩散模型或现代 MoE 模型里，都需要重新验证。你现在应该能把论文结论和实践迁移分开。</p>
""" + grid([
                ("不是所有层都必须加", "论文选择 attention 是实验设计和效率选择，不是数学限制。", "blue"),
                ("不是所有任务都 r 很小", "任务分布差异大、需要新知识或新语言时，小 rank 可能不够。", "warn"),
                ("不是所有服务都适合频繁 merge", "混合任务请求会让 merge 状态管理变复杂。", "warn"),
            ], 3)),
            ("examples", "6. 试一试：从配置看工程后果", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p>一个配置写 <code>target_modules=[q_proj,v_proj]</code>。它对应论文里的哪些矩阵？</p><p class="hint">Wq 和 Wv。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>为什么冻结 MLP 后训练显存会下降？</p><p class="hint">冻结参数不需要梯度和 Adam 优化器状态。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>一个服务每个请求都可能用不同 LoRA，要不要一律 merge？</p><p class="hint">要谨慎。merge 对单任务推理好，但混合任务需要考虑切换和分 batch。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、attention 落点", "intro": "先检查你是否能识别 LoRA 在 Transformer 里的位置。", "review": "把模块名映射到 Wq/Wk/Wv/Wo。", "questions": [
                {"title": "Wq", "kind": "单选", "type": "choice", "prompt": "常见实现里的 q_proj 通常对应论文里的哪个矩阵？", "options": ["Wq", "Wv", "MLP down projection"]},
                {"title": "Wv", "kind": "单选", "type": "choice", "prompt": "常见实现里的 v_proj 通常对应论文里的哪个矩阵？", "options": ["Wv", "Wk", "LayerNorm"]},
                {"title": "目标矩阵", "kind": "判断", "type": "choice", "prompt": "LoRA 原理上只能用于 attention 权重，不能用于 MLP 线性层。", "options": ["正确", "错误"]},
                {"title": "论文默认选择", "kind": "填空", "type": "fill", "prompt": "论文多数实验为了简化，常把 LoRA 加到 ____ 和 ____。"},
                {"title": "head 切分", "kind": "短答", "prompt": "为什么论文仍把 Wq 看成 d_model x d_model，即使实现里有多头 attention？"},
                {"title": "模块识别", "kind": "匹配", "prompt": "把 q_proj、k_proj、v_proj、o_proj 分别对应到 Wq、Wk、Wv、Wo。"},
            ]},
            {"title": "二、工程收益", "intro": "这一组检查你是否能把模块选择和资源联系起来。", "review": "target modules 越多，参数量和保存成本越高。", "questions": [
                {"title": "显存来源", "kind": "短答", "prompt": "为什么冻结底座权重会降低 Adam 训练显存？"},
                {"title": "checkpoint", "kind": "短答", "prompt": "为什么 LoRA checkpoint 小，但部署仍然需要完整底座模型？"},
                {"title": "吞吐", "kind": "判断", "type": "choice", "prompt": "LoRA 训练吞吐可能提升，是因为大部分参数不需要反向传播梯度。", "options": ["正确", "错误"]},
                {"title": "参数预算", "kind": "计算", "prompt": "固定总参数预算时，target modules 从 2 个变成 4 个，rank 通常需要怎样调整？为什么？"},
                {"title": "任务切换", "kind": "短答", "prompt": "为什么 LoRA 适合共享底座、多任务切换的部署方式？"},
                {"title": "merge 场景", "kind": "场景", "prompt": "举一个适合 merge 的服务场景，再举一个需要谨慎 merge 的场景。"},
            ]},
            {"title": "三、错误诊断和边界", "intro": "这一组要求你把配置错误讲清楚。", "review": "诊断题按错因、后果、修法写。", "questions": [
                {"title": "错误诊断：target 选错", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：配置里写了不存在的 target module，训练日志显示可训练参数为 0。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：混批 merge", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：一个 batch 混合多个任务，但服务端只 merge 了其中一个任务的 LoRA。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：过度扩展", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：为了“更强”，把 LoRA 加到所有线性层但没有重新评估显存和过拟合。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "论文边界", "kind": "短答", "prompt": "为什么不能把论文的 Wq/Wv 结论直接当成所有模型、所有任务的最优配置？"},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话解释 LoRA 在 Transformer 里的典型落点。"},
                {"title": "实践清单", "kind": "清单", "prompt": "准备训练 LoRA 前，你会检查 target modules 的哪 5 件事？"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 6-9 句话解释 LoRA 如何放进 Transformer，以及为什么它能带来工程收益。", "hint": "请串联：Wq、Wv、attention、冻结、checkpoint、merge、任务切换。"},
            ]},
        ],
        "keys": "Wq,Wv,attention,冻结,checkpoint,merge,任务切换",
    },
    {
        "dir": "04_实验设计与结果解读",
        "title": "实验设计与结果解读",
        "subtitle": "读懂 LoRA 论文里的基线、指标、参数量和结论边界",
        "kicker": "第 4 块 · 实验读表",
        "side": "实验表不是为了背数字。读表时要问：谁和谁比、参数量多少、任务是什么、结论能推到哪里。",
        "goals": [
            "区分论文中的 FT、BitFit、PreEmbed、PreLayer、Adapter 和 LoRA 基线。",
            "读懂 RoBERTa/DeBERTa、GPT-2、GPT-3 三组实验各自想回答的问题。",
            "根据参数量和指标判断 LoRA 的优势是否成立。",
            "说明实验结论的边界：任务、模型、指标和统计波动。",
        ],
        "sections": [
            ("baselines", "1. 先认清基线：每个方法到底训练什么", "baselines", """
<p>论文的实验表里名字很多，先别急着看谁加粗。第一步是认清每个 baseline 的训练对象。Fine-tuning 更新全部参数；BitFit 只训练 bias；PreEmbed 训练输入端特殊 token 的 embedding；PreLayer 训练每层里的特殊 token 激活；Adapter 在模型内部插入小层；LoRA 训练并联到已有权重上的低秩矩阵。</p>
<p>这一步很重要，因为参数量接近不代表机制接近。Adapter 和 LoRA 都可能只有几十万或几百万参数，但 adapter 是顺序插入模块，LoRA 是并联低秩更新。PreEmbed 参数少，但它用的是上下文位置。BitFit 便宜，但表达能力受限。读表时要把“训练对象”和“推理路径”放在一起看。</p>
<p>论文有些数字来自作者复现实验，有些带星号的是引用前人结果，有些带 dagger 的是为了公平比较而采用受限设置。表里这些符号不只是脚注，它们影响可比性。你现在应该能先看实验设置，再看指标高低。</p>
""" + terms([
                ("FT", "更新全部预训练参数，表达强，但每任务参数和原模型同量级。"),
                ("BitFit", "只训练 bias，参数很少，通常作为极轻量基线。"),
                ("PreEmbed", "训练特殊 prefix/infix token 的 embedding，占用序列长度。"),
                ("PreLayer", "训练每层特殊 token 激活，参数比 PreEmbed 多。"),
                ("Adapter", "插入瓶颈模块，参数少但推理可能增加顺序计算。"),
                ("LoRA", "训练低秩矩阵 A/B，merge 后推理走原线性层。"),
            ]) + "<p>判断句：表格里的方法名如果不能翻译成“训练什么”，就还没开始读实验。你现在应该能把每个 baseline 放回训练路径里。</p>"),
            ("nlu", "2. RoBERTa / DeBERTa：自然语言理解任务", "glue", """
<p>第一组主要看 NLU，也就是自然语言理解任务。RoBERTa base/large 和 DeBERTa XXL 在 GLUE benchmark 上测试，指标包括 MNLI、SST-2、MRPC、CoLA、QNLI、QQP、RTE、STS-B 等。这里的核心问题是：LoRA 用远少于全量微调的参数，能否接近或超过全量微调和 adapter 类方法。</p>
<p>论文表格显示，RoBERTa base 的 LoRA 只训练约 0.3M 参数，平均分 87.2，高于全量微调表中 86.4；RoBERTa large 的 LoRA 约 0.8M 参数，平均分 89.0，和全量微调 88.9 接近并略高；DeBERTa XXL 的 LoRA 约 4.7M 参数，平均分 91.3，也达到全量微调水平。这里不是说 LoRA 永远更准，而是说在这些任务上，它没有因为参数少而明显牺牲质量。</p>
<p>读这组实验要注意公平性。论文为了和 adapter 更公平比较，还做了受限设置，例如相同 batch size、序列长度 128，并避免某些任务从已经适配 MNLI 的模型起步。带 dagger 的行就是这种设置下的结果。你现在应该能解释为什么实验设置会影响基线比较。</p>
""" + bars([
                ("RoBERTa base FT 参数", 100, "125.0M"),
                ("RoBERTa base LoRA 参数", 1, "0.3M"),
                ("RoBERTa large FT 参数", 100, "355.0M"),
                ("RoBERTa large LoRA 参数", 1, "0.8M"),
                ("DeBERTa XXL FT 参数", 100, "1500M"),
                ("DeBERTa XXL LoRA 参数", 1, "4.7M"),
            ]) + "<p>判断句：当参数量相差几百到几千倍而指标接近，实验才真正支持“参数高效”。你现在应该能用参数量和指标一起读结论。</p>"),
            ("nlg", "3. GPT-2：生成任务不是只看准确率", "generation", """
<p>GPT-2 实验看的是 E2E NLG Challenge，属于生成任务。生成任务常用 BLEU、NIST、METEOR、ROUGE-L、CIDEr 这类指标，不像分类任务只有 accuracy。论文把 GPT-2 medium 和 large 都拿来比较，重点看 LoRA 在 NLG 模型上是否仍然有优势。</p>
<p>表中 GPT-2 medium 的 LoRA 只训练 0.35M 参数，但 BLEU、NIST、METEOR、ROUGE-L、CIDEr 都达到或超过列出的基线。GPT-2 large 的 LoRA 训练 0.77M 参数，也在多数指标上表现很强。这里说明 LoRA 不只在理解任务有效，在生成任务上也能作为强基线。</p>
<p>不过生成指标本身有噪声和局限。BLEU 高不一定代表所有生成质量都好，ROUGE 更偏重重叠，CIDEr 来自图像描述评估传统。读这组实验时，重点不是背每个指标，而是看到作者覆盖了不同任务类型，并用多个指标避免单一评价偏差。</p>
""" + grid([
                ("BLEU / NIST", "偏 n-gram 重叠和信息量，常用于生成质量比较。", "blue"),
                ("METEOR / ROUGE-L", "关注匹配、召回或最长公共子序列，能补充 BLEU。", "blue"),
                ("CIDEr", "衡量候选文本和参考文本的相似性，E2E 表中也作为一个生成指标。", "blue"),
            ], 3) + "<p>判断句：生成任务不能只说“准确率提升”。你现在应该能识别论文在不同任务类型上用了不同指标。</p>"),
            ("gpt3", "4. GPT-3：大模型压力测试", "gpt-3", """
<p>GPT-3 175B 是论文最有代表性的压力测试。这里比较 WikiSQL、MultiNLI-matched 和 SAMSum 三类任务：自然语言到 SQL、自然语言推理、对话摘要。全量微调要训练约 175,255.8M 参数；LoRA 有 4.7M 和 37.7M 两个参数预算。这个对比直接服务论文动机：大模型多任务适配不能每次都复制完整模型。</p>
<p>表格显示，LoRA 在 WikiSQL、MNLI-m、SAMSum 上达到或超过全量微调与其他 PEFT 基线。比如 4.7M 参数的 LoRA 在 MNLI-m 上是 91.7，在 SAMSum 的 ROUGE-1/2/L 是 53.8/29.8/45.9；37.7M 参数的 LoRA 在 WikiSQL 上达到 74.0。论文还标注了任务上的典型波动：WikiSQL 约 ±0.5%，MNLI-m 约 ±0.1%，SAMSum 约 ±0.2/±0.2/±0.1。</p>
<p>这里有一个读表细节：更多可训练参数不总是更好。prefix 方法在参数变多时可能反而下降，论文怀疑特殊 token 太多会让输入分布远离预训练分布。LoRA 的结果相对稳定，但也不能推出“参数越多越强”。</p>
""" + viz([
                ("FT", "GPT-3 全量微调", "参数最多，是质量基线，但每任务保存和训练成本极高。", "训练参数=175,255.8M|WikiSQL=73.8|MNLI-m=89.5|SAMSum=52.0/28.0/44.5"),
                ("Adapter", "GPT-3 AdapterH", "参数远少于 FT，部分任务表现接近，但仍有 adapter 推理路径问题。", "训练参数=40.1M|WikiSQL=73.2|MNLI-m=91.5|SAMSum=53.2/29.0/45.1"),
                ("LoRA small", "GPT-3 LoRA 4.7M", "极小参数预算下，在 MNLI 和 SAMSum 上很强。", "训练参数=4.7M|WikiSQL=73.4|MNLI-m=91.7|SAMSum=53.8/29.8/45.9"),
                ("LoRA large", "GPT-3 LoRA 37.7M", "更高参数预算下 WikiSQL 更好，但不是所有指标都单调增加。", "训练参数=37.7M|WikiSQL=74.0|MNLI-m=91.6|SAMSum=53.4/29.2/45.1"),
], "判断提示：把参数量和任务指标一起看。LoRA 的论点是“少很多参数仍能保持质量”，不是“每个指标都无条件第一”。") ),
            ("fairness", "5. 读实验的四个检查问题", "fairness", """
<p>第一，比较对象是否合理？如果一个方法训练 0.3M 参数，另一个训练 355M 参数，你要同时看质量和成本。只说“谁分高”是不完整的。</p>
<p>第二，设置是否公平？序列长度、batch size、初始化、是否引用前人结果、是否调参充分，都会影响表格。论文用星号和 dagger 标注部分设置，这些脚注要读。</p>
<p>第三，指标是否支持主张？LoRA 的主张有几部分：任务质量、可训练参数量、训练吞吐、显存、推理延迟、checkpoint 大小。单个 GLUE 平均分不能支持所有主张，必须结合方法设计和工程数字。</p>
<p>第四，结论能否外推？论文覆盖了 RoBERTa、DeBERTa、GPT-2、GPT-3 和多个 NLP 任务，但没有覆盖所有模型和所有领域。你可以把 LoRA 当强基线，不能把表格数字当成新任务的保证。</p>
""" + grid([
                ("只看加粗", "会忽略参数量、方差和设置差异。读表不能只追最高分。", "bad"),
                ("忽略脚注", "星号和 dagger 影响可比性。脚注常常比表头更关键。", "warn"),
                ("过度外推", "论文实验支持论文范围内结论，不自动覆盖所有现代模型和任务。", "warn"),
            ], 3)),
            ("examples", "6. 试一试：把表格读成结论", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p>RoBERTa large 上 LoRA 0.8M 参数、FT 355M 参数且平均分接近，这支持什么结论？</p><p class="hint">支持“少量任务参数也能达到相近质量”，不是证明 LoRA 永远更准。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>GPT-3 表里 LoRA 4.7M 在某些指标超过 37.7M，说明什么？</p><p class="hint">更多参数不保证单调提升，任务和配置会影响结果。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>为什么要同时看 adapter latency 实验和任务指标表？</p><p class="hint">任务指标说明质量，latency 实验说明部署路径。两者回答不同问题。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、基线识别", "intro": "先确认你能读懂实验表里的方法名。", "review": "每个方法都要说出训练对象。", "questions": [
                {"title": "FT", "kind": "单选", "type": "choice", "prompt": "Full fine-tuning 训练什么？", "options": ["全部模型参数", "只训练 bias", "只训练 prefix token"]},
                {"title": "BitFit", "kind": "单选", "type": "choice", "prompt": "BitFit 训练什么？", "options": ["bias", "Wq 和 Wv", "adapter bottleneck"]},
                {"title": "PreEmbed", "kind": "短答", "prompt": "PreEmbed 和 PreLayer 的训练对象有什么不同？"},
                {"title": "Adapter", "kind": "短答", "prompt": "Adapter 和 LoRA 都参数少，为什么推理路径不同？"},
                {"title": "星号含义", "kind": "短答", "prompt": "实验表里有些结果来自前人报告。读结论时为什么要注意这一点？"},
                {"title": "dagger 设置", "kind": "短答", "prompt": "为什么论文要用受限设置和 adapter 做公平比较？"},
            ]},
            {"title": "二、读表判断", "intro": "这一组要求你从参数量和指标得出稳妥结论。", "review": "不要只看分数最高，也不要只看参数最少。", "questions": [
                {"title": "RoBERTa 结论", "kind": "短答", "prompt": "RoBERTa large 中 LoRA 0.8M 参数达到接近 FT 的平均分，这能说明什么？"},
                {"title": "DeBERTa 结论", "kind": "短答", "prompt": "DeBERTa XXL 上 LoRA 4.7M 与 FT 1500M 参数对比，重点应该看什么？"},
                {"title": "GPT-2 指标", "kind": "多选", "type": "multi", "prompt": "GPT-2 生成任务表里出现了哪些指标？", "options": ["BLEU", "ROUGE-L", "CIDEr", "GPU 温度"]},
                {"title": "GPT-3 任务", "kind": "多选", "type": "multi", "prompt": "GPT-3 实验覆盖了哪些任务？", "options": ["WikiSQL", "MultiNLI-m", "SAMSum", "ImageNet"]},
                {"title": "波动范围", "kind": "短答", "prompt": "为什么论文要说明 WikiSQL、MNLI、SAMSum 的典型波动？"},
                {"title": "更多参数", "kind": "判断", "type": "choice", "prompt": "论文实验说明所有 PEFT 方法参数越多指标一定越高。", "options": ["正确", "错误"]},
            ]},
            {"title": "三、诊断和表达", "intro": "这一组练习把实验读法转成批判性表达。", "review": "诊断题按错因、后果、修法写。", "questions": [
                {"title": "错误诊断：只看加粗", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：有人只看表格加粗项就说 LoRA 全面碾压所有方法。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：忽略成本", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：有人只比较分数，不比较可训练参数量和推理延迟。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：过度外推", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：有人把 2021 年论文表格直接当作所有 2026 年模型的默认结论。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话解释 LoRA 论文的实验为什么有说服力。"},
                {"title": "复现实验", "kind": "场景", "prompt": "如果你要在自己任务上验证 LoRA，至少要记录哪 6 个实验条件？"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 6-9 句话解释 LoRA 论文的实验设计和主要结论。", "hint": "请串联：基线、参数量、RoBERTa、GPT-2、GPT-3、任务指标、边界。"},
            ]},
        ],
        "keys": "基线,参数量,RoBERTa,GPT-2,GPT-3,任务指标,边界",
    },
    {
        "dir": "05_rank与低秩解释",
        "title": "rank 与低秩解释",
        "subtitle": "从 rank 扫描、子空间相似度和 Delta W 读懂 LoRA 为什么有效",
        "kicker": "第 5 块 · 机制解释",
        "side": "这一块不背玄学：rank 小为什么还行，要靠实验现象、子空间重合和 W/Delta W 的关系来解释。",
        "goals": [
            "解释论文中 intrinsic rank 的含义和证据。",
            "读懂 rank 扫描实验为什么支持小 r 可行。",
            "说明 normalized subspace similarity 在比较什么。",
            "解释 Delta W 与 W 的关系：不是复制 W 的最大方向，而是放大任务相关方向。",
        ],
        "sections": [
            ("questions", "1. 论文想回答的三个机制问题", "science", """
<p>LoRA 的实验结果说明它好用，但论文还想解释为什么低秩更新能工作。作者在 GPT-3 175B 上做了一组分析，围绕三个问题：固定参数预算时应该适配哪些权重；LoRA 学到的 <code>Delta W</code> 是否真的 rank-deficient；<code>Delta W</code> 和原始权重 <code>W</code> 到底是什么关系。</p>
<p>这里的新概念是 intrinsic rank。直觉上，它不是矩阵代数课里的“这个矩阵实际 rank 等于几”那么简单，而是问下游任务真正需要多少有效方向来改变模型行为。如果任务更新主要集中在少数方向上，小 rank LoRA 就可能够用。</p>
<p>术语上，论文用 rank 扫描、不同 rank 的子空间重合、不同随机种子的子空间重合，以及 <code>Delta W</code> 投影到 <code>W</code> 方向上的范数来支持这个说法。你现在应该能把“低秩有效”理解成实证假设，而不是数学定理。</p>
""" + grid([
                ("放哪些权重", "固定参数预算下，Wq/Wv 或四个 attention 投影往往比只放一个投影更好。", "blue"),
                ("rank 多大", "在 GPT-3 的 WikiSQL/MNLI 实验中，小到 r=1 仍有竞争力。", "ok"),
                ("Delta W 与 W", "Delta W 倾向放大 W 中已有但不突出的任务相关方向。", "blue"),
            ], 3)),
            ("rank-scan", "2. rank 扫描：小 r 已经很强", "rank", """
<p>论文把 LoRA 加到不同 attention 权重上，并扫描 <code>r=1,2,4,8,64</code>。让人意外的是，在 GPT-3 的 WikiSQL 和 MultiNLI 上，只要适配 <code>Wq,Wv</code> 或四个 attention 投影，<code>r=1</code> 就已经很有竞争力。比如 <code>Wq,Wv</code> 在 WikiSQL 上 <code>r=1</code> 为 73.4，<code>r=8</code> 为 73.8，差距很小。</p>
<p>这不表示 rank 1 永远够用。论文自己也提醒，如果下游任务和预训练分布差异很大，比如不同语言或需要大量新知识，小 rank 可能不够。rank 扫描支持的是“这些任务上的有效更新方向很少”，不是“所有任务都低秩到 rank 1”。</p>
<p>一个更细的观察是：只适配 <code>Wq</code> 时，rank 变大更有帮助；适配 <code>Wq,Wv</code> 时，小 rank 已经够强。这说明 target module 选择和 rank 不是独立超参。你现在应该能解释为什么“多放几个关键矩阵、每个矩阵小 rank”有时比“只放一个矩阵、大 rank”更划算。</p>
""" + viz([
                ("Wq r=1", "只适配 Wq，r=1", "WikiSQL 表现明显低于 Wq/Wv，说明只改一个投影可能覆盖不够。", "target=Wq|rank=1|WikiSQL=68.8|MNLI=90.7"),
                ("Wq/Wv r=1", "适配 Wq/Wv，r=1", "参数很少，但已经接近更高 rank 的表现。", "target=Wq,Wv|rank=1|WikiSQL=73.4|MNLI=91.3"),
                ("Wq/Wv r=8", "适配 Wq/Wv，r=8", "比 r=1 略高，但不是数量级差距。", "target=Wq,Wv|rank=8|WikiSQL=73.8|MNLI=91.6"),
                ("all r=2", "四个 attention 投影，r=2", "固定预算下覆盖更多投影，也很有竞争力。", "target=Wq,Wk,Wv,Wo|rank=2|WikiSQL=73.7|MNLI=91.7"),
], "判断提示：rank 和 target modules 要一起看。小 r 有效是实验现象，不是所有任务的保证。") ),
            ("subspace", "3. 子空间相似度：比较学到的方向是否重合", "subspace", """
<p>rank 扫描只能告诉你指标差不多，还不能说明学到的方向是否相似。论文进一步比较 <code>r=8</code> 和 <code>r=64</code> 学到的 <code>A</code> 矩阵子空间。做法是对 <code>A</code> 做 SVD，取右奇异向量，再看 top-i 方向和另一个矩阵 top-j 方向的重合程度。</p>
<p>normalized subspace similarity 的值在 0 到 1 之间。1 表示两个子空间完全重合，0 表示几乎分离。论文发现，<code>r=8</code> 和 <code>r=64</code> 的顶部奇异方向有明显重合，尤其是最重要的方向；后面很多方向重合少，可能包含更多训练噪声。这解释了为什么小 rank 也能抓住主要任务方向。</p>
<p>这段最容易误解成“r=64 没用”。更稳的说法是：在这些实验中，r=64 的额外方向没有带来同等重要的有效信号，顶部方向才是主要贡献。对于更难任务或不同模型，额外方向可能有用，需要实验确认。</p>
""" + formula('<span class="big">phi(A<span class="sub">8</span>, A<span class="sub">64</span>, i, j) = ||U<span class="sub">8,i</span><sup>T</sup> U<span class="sub">64,j</span>||<span class="sub">F</span><sup>2</sup> / min(i,j)</span><br>范围：[0,1]。越接近 1，两个子空间越重合。') + """
<div class="svg-wrap">
<svg viewBox="0 0 680 230" role="img" aria-label="子空间相似度直觉图">
  <rect x="40" y="40" width="220" height="140" fill="#eef8fe" stroke="#1b2a4a"/><text x="150" y="70" text-anchor="middle" font-size="16">A(r=8) 的 top 方向</text>
  <line x1="80" y1="150" x2="220" y2="80" stroke="#00a9f4" stroke-width="5"/><line x1="90" y1="90" x2="210" y2="155" stroke="#9aa8b6" stroke-width="2"/>
  <rect x="420" y="40" width="220" height="140" fill="#fff8e1" stroke="#a66b00"/><text x="530" y="70" text-anchor="middle" font-size="16">A(r=64) 的 top 方向</text>
  <line x1="455" y1="148" x2="600" y2="78" stroke="#00a9f4" stroke-width="5"/><line x1="455" y1="95" x2="610" y2="132" stroke="#9aa8b6" stroke-width="2"/><line x1="470" y1="165" x2="620" y2="160" stroke="#d8dee8" stroke-width="2"/>
  <text x="340" y="113" text-anchor="middle" font-size="14">比较方向重合</text><text x="340" y="137" text-anchor="middle" font-size="12">顶部方向重合高，后续方向可能更噪</text>
</svg>
</div>
<p>判断句：子空间相似度比较的是“学到的方向”，不是直接比较最终分数。你现在应该能用它解释 rank 实验背后的机制。</p>
"""),
            ("seeds", "4. 不同随机种子：不是偶然撞上的方向", "random seeds", """
<p>为了排除“同一个模型、同一训练设置下偶然相似”的解释，论文还比较了两个不同随机种子训练出的 <code>r=64</code> LoRA 子空间。结果显示，<code>Delta Wq</code> 似乎有更多共同奇异方向，<code>Delta Wv</code> 的共同方向更少一些；随机高斯矩阵之间则没有这种结构性重合。</p>
<p>这说明训练不是随便找到一堆等价噪声方向。不同随机种子仍会学到一些共同方向，表明任务确实在模型中牵引出稳定的适配子空间。稳定方向越靠前，越说明小 rank 可能抓住关键部分。</p>
<p>不过，这类分析仍是经验性的。它依赖具体模型层、任务和训练过程。你不能只凭“论文说有共同方向”就跳过自己任务上的 rank sweep。正确用法是：把它当作为什么 LoRA 值得先试小 rank 的理由。</p>
""" + grid([
                ("同 rank 不同种子", "若顶部方向仍重合，说明任务牵引出稳定子空间。", "ok"),
                ("随机矩阵对照", "随机矩阵没有共同方向，用来排除纯随机重合。", "blue"),
                ("实践含义", "先用小 rank 做强基线，再按任务验证是否需要更高 rank。", "warn"),
            ], 3)),
            ("delta", "5. Delta W 和 W：放大已有但不突出的方向", "delta-w", """
<p>论文最后问：LoRA 学到的 <code>Delta W</code> 和原始权重 <code>W</code> 是什么关系？如果 <code>Delta W</code> 只是复制 <code>W</code> 的最大奇异方向，那它可能只是强化原模型已经最强的通道。作者用投影范数比较发现，<code>Delta W</code> 和 <code>W</code> 比随机方向相关，但并不主要落在 <code>W</code> 的 top singular directions 上。</p>
<p>他们的解释是：<code>Delta W</code> 放大了预训练模型已经学到、但在原始权重里没有被强烈强调的任务相关方向。用论文表中的一个数值看，<code>r=4</code> 时，某层 <code>Delta Wq</code> 的范数是 6.91，而 <code>Wq</code> 投影到这些方向上的范数只有 0.32，放大因子约 21.5。也就是说，LoRA 不是从零造出所有能力，而是在已有表示里把对任务有用的方向推高。</p>
<p>这也是 LoRA 适合预训练大模型的原因之一。大模型已经在预训练中学到许多潜在特征，下游任务往往需要重新组合或强调其中一部分。低秩更新能以较小参数量完成这种“方向放大”。边界也在这里：如果任务需要模型没有学过的新能力，小 rank LoRA 可能不够。</p>
""" + bars([
                ("W 在 DeltaW 方向上的范数", 5, "0.32"),
                ("DeltaW 自身范数", 100, "6.91"),
                ("放大因子", 100, "约 21.5x"),
            ]) + "<p>判断句：LoRA 更像放大和重排预训练模型里的任务相关方向，不是用 35MB 权重凭空替代 350GB 模型。你现在应该能解释 LoRA 为什么仍然依赖底座模型。</p>"),
            ("pitfalls", "6. 常见误区：把低秩解释讲过头", "pitfalls", grid([
                ("误区：r=1 永远够", "论文只在部分任务上观察到小 r 很强。分布差异大时可能需要更高 rank。", "bad"),
                ("误区：rank 越大越稳", "更大 rank 会增加参数，也可能引入噪声或过拟合，不保证指标单调提升。", "warn"),
                ("误区：低秩等于低质量", "低秩限制表达空间，但预训练模型的任务更新可能本来就集中在少数方向。", "bad"),
                ("误区：Delta W 和 W 无关", "论文发现 Delta W 比随机方向更相关，但不是简单复制 W 的最大方向。", "warn"),
                ("误区：机制分析等于理论证明", "这些是实证分析，能提供解释和启发，不是覆盖所有任务的定理。", "warn"),
                ("误区：只看 rank 不看 target", "rank 和 target modules 联动。只谈 r 大小会漏掉预算分配。", "bad"),
            ], 3)),
            ("examples", "7. 试一试：把机制说成判断", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p>为什么 r=1 表现强，能支持 intrinsic rank 低的说法？</p><p class="hint">说明任务更新的关键方向可能很少，但不能推到所有任务。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>子空间相似度高说明什么？</p><p class="hint">不同 rank 或种子学到的顶部方向有重合，可能是稳定任务方向。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>Delta W 放大 W 中“不突出但有用”的方向，这句话如何理解？</p><p class="hint">底座已有相关特征，但下游任务需要把这些方向权重调高。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、rank 和 target", "intro": "先检查你是否能把 rank 实验读稳。", "review": "rank 不单独决定效果，要和 target modules 一起看。", "questions": [
                {"title": "intrinsic rank", "kind": "短答", "prompt": "用自己的话解释 LoRA 论文里的 intrinsic rank。"},
                {"title": "rank 扫描", "kind": "判断", "type": "choice", "prompt": "论文中某些任务 r=1 表现强，说明所有任务都应该用 r=1。", "options": ["正确", "错误"]},
                {"title": "target 联动", "kind": "短答", "prompt": "为什么只适配 Wq 时可能需要更大 rank，而适配 Wq/Wv 时小 rank 已经很强？"},
                {"title": "参数预算", "kind": "短答", "prompt": "固定参数预算下，为什么适配更多矩阵通常要降低 rank？"},
                {"title": "边界任务", "kind": "场景", "prompt": "举一个小 rank 可能不够的下游任务场景，并说明原因。"},
                {"title": "rank 选择", "kind": "清单", "prompt": "在自己项目里选择 rank 时，你会看哪 4 个信号？"},
            ]},
            {"title": "二、子空间解释", "intro": "这一组检查你是否能说清相似度分析。", "review": "相似度比较方向，不是直接比较指标。", "questions": [
                {"title": "相似度范围", "kind": "填空", "type": "fill", "prompt": "normalized subspace similarity 的范围是 ____ 到 ____。"},
                {"title": "SVD 作用", "kind": "短答", "prompt": "为什么论文要对 A 做 SVD 后比较奇异方向？"},
                {"title": "r=8 vs r=64", "kind": "短答", "prompt": "r=8 和 r=64 顶部方向重合，能解释什么？"},
                {"title": "随机种子", "kind": "短答", "prompt": "比较不同随机种子的 LoRA 子空间，想排除什么误解？"},
                {"title": "随机矩阵对照", "kind": "短答", "prompt": "为什么要和随机高斯矩阵做对照？"},
                {"title": "噪声方向", "kind": "判断", "type": "choice", "prompt": "后续奇异方向重合低，可能意味着额外方向里有更多训练噪声。", "options": ["正确", "错误"]},
            ]},
            {"title": "三、Delta W 与 W", "intro": "这一组要求你把机制解释说准确。", "review": "不要把放大方向讲成凭空创造能力。", "questions": [
                {"title": "Delta W 关系", "kind": "短答", "prompt": "论文认为 Delta W 和 W 的关系是什么？"},
                {"title": "投影范数", "kind": "短答", "prompt": "比较 W 在 Delta W 方向上的投影范数，有什么意义？"},
                {"title": "放大因子", "kind": "短答", "prompt": "r=4 中 6.91/0.32 这个放大因子想说明什么？"},
                {"title": "错误诊断：机制过度", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：“LoRA 证明大模型所有任务只需要 rank 1 更新。”按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "错误诊断：低秩低质", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：“低秩就是表达能力差，所以 LoRA 不可能接近全量微调。”按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话解释为什么 LoRA 小 rank 可能有效。"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 6-9 句话解释论文如何分析 LoRA 的低秩更新。", "hint": "请串联：rank、target modules、子空间相似度、随机种子、Delta W、W、任务方向。"},
            ]},
        ],
        "keys": "rank,target modules,子空间相似度,随机种子,Delta W,W,任务方向",
    },
    {
        "dir": "06_实践验收与论文复述",
        "title": "实践验收与论文复述",
        "subtitle": "把 LoRA 用到项目里：配置、排错、边界和论文表达",
        "kicker": "第 6 块 · 实战收束",
        "side": "最后一块把论文变成可执行清单：怎么配、怎么验、怎么排错，以及如何完整复述 LoRA。",
        "goals": [
            "设计一个 LoRA 微调实验的最小验收清单。",
            "排查冻结失败、target module 错误、merge 状态、rank/alpha 设置等常见问题。",
            "说清 LoRA 的适用边界，以及和后续 PEFT 方法的关系。",
            "用一段完整表达复述论文贡献、证据和限制。",
        ],
        "sections": [
            ("checklist", "1. 从论文到项目：先写验收清单", "checklist", """
<p>真正做 LoRA 微调时，不要只把配置复制进训练脚本。先写一个最小验收清单：底座模型是什么，任务数据是什么，target modules 是哪些，rank 和 alpha 是多少，哪些参数可训练，保存的 adapter 文件多大，merge 前后输出是否一致，和哪些 baseline 比较。</p>
<p>这份清单的作用是防止“以为在训练 LoRA，其实什么都没训”或“以为只训 LoRA，其实底座也被更新”。最常见的两个检查是：打印 trainable parameters，并列出可训练参数名。只看 loss 下降不够，因为底座误更新也会让 loss 下降，但你已经失去 PEFT 的工程收益。</p>
<p>实验设计也要有 baseline。至少要有原始底座零样本/少样本表现、一个合理 LoRA 配置，以及如果资源允许的全量微调或小样本全量微调对照。没有 baseline，就无法判断 LoRA 的质量和成本是否值得。</p>
""" + grid([
                ("参数检查", "确认只有 LoRA A/B 或允许的 bias 可训练。", "ok"),
                ("配置检查", "记录 rank、alpha、target modules、dropout、学习率。", "blue"),
                ("部署检查", "验证 merge 前后输出接近，避免重复 merge。", "warn"),
            ], 3) + code_block("c6_trainable", "正确示例：检查可训练参数名", """trainable = []
total = 0
for name, param in model.named_parameters():
    if param.requires_grad:
        trainable.append(name)
        total += param.numel()

print("trainable params:", total)
print("\\n".join(trainable[:50]))

# 期望看到类似：
# ...q_proj.lora_A...
# ...q_proj.lora_B...
# ...v_proj.lora_A...
# ...v_proj.lora_B...""", "good", "正确示例") + "<p>判断句：LoRA 训练开始前，必须能说出“哪些参数在训练”。你现在应该能用参数名验收配置是否生效。</p>"),
            ("config", "2. rank、alpha、target modules 怎么选", "configuration", """
<p>初始配置可以保守：先从常见的 <code>q_proj/v_proj</code> 和中等 rank 开始，例如 <code>r=8</code> 或 <code>r=16</code>，再根据验证集、显存和过拟合情况调整。论文告诉你小 rank 可能很强，但不是让你跳过验证。rank 是容量，alpha 是分支尺度，target modules 是更新位置，它们会一起影响训练。</p>
<p>如果 loss 降不动，先别马上把 rank 拉满。先检查 target module 是否命中、学习率是否合理、数据格式是否正确、标签是否参与 loss、LoRA 参数是否真的 requires_grad。很多“rank 不够”的问题其实是配置没生效。确认训练正常后，再做 rank sweep。</p>
<p>如果过拟合明显，可以降低 rank、加 LoRA dropout、减少训练 epoch、调低学习率，或者扩大数据。LoRA 参数少不代表不会过拟合，尤其是小数据任务。你现在应该能把“容量不够”和“训练配置错误”分开排查。</p>
""" + viz([
                ("loss 不降", "loss 不降", "先查训练链路，再调 rank。target module 没命中或标签没进 loss 更常见。", "先查=可训练参数/数据/学习率|再试=rank/target modules|避免=盲目加大 r"),
                ("显存不够", "显存不够", "降低 rank 或 target modules，使用量化/梯度检查点等，但别忘记质量验证。", "先查=batch/序列长度|LoRA侧=rank/模块数|权衡=速度和质量"),
                ("过拟合", "过拟合", "小数据下 LoRA 也会记忆。减少容量或训练强度。", "信号=训练好验证差|调整=rank/dropout/epoch/LR|补救=更多数据"),
                ("推理变慢", "推理变慢", "确认是否 merge，是否每次动态加载，是否混合任务导致无法批处理。", "先查=merge状态|服务形态=单任务/多任务|修法=分组或预merge"),
], "判断提示：调参前先验收训练链路。LoRA 配置错误比“论文方法失效”更常见。") ),
            ("merge", "3. 保存、加载和 merge 的状态管理", "state", """
<p>LoRA 产物通常只保存 adapter 权重和配置，不保存完整底座。加载时要用同一个或兼容的底座模型，再把 LoRA 权重挂上去。部署可以选择保留动态 LoRA 分支，也可以 merge 到原权重后保存合并模型。两种方式各有用途。</p>
<p>状态管理的核心是避免混乱：当前模型是干净底座、挂载未 merge LoRA、已经 merge 的模型，还是 merge 后又卸载过？很多线上错误来自重复合并、加载错底座、把 adapter 当完整模型发布、或者量化模型 merge 后精度路径没测。</p>
<p>验收时要做一个小测试：同一批输入，未 merge 的 LoRA 模型和 merge 后模型输出应当非常接近。允许有极小浮点误差，但不能语义大变。如果差异大，先查 scaling、dtype、是否重复 merge、target module 命名和加载顺序。</p>
""" + code_block("c6_merge_check", "逐行拆解：merge 前后输出验收", """# 伪代码：实际 API 随框架不同会变化
model_lora = load_base_with_lora(base_path, lora_path)
logits_before = model_lora(input_ids).logits

model_merged = merge_lora(model_lora)
logits_after = model_merged(input_ids).logits

max_diff = (logits_before - logits_after).abs().max()
print("max diff:", max_diff)

# 若差异很大，先查 scaling、dtype、是否重复 merge。""") + grid([
                ("adapter 权重", "小、便于分发，但加载时必须指定兼容底座。", "blue"),
                ("合并模型", "部署简单，推理路径普通，但文件变大，不便于频繁切换任务。", "ok"),
                ("状态错误", "重复 merge 或加载错底座，会让输出异常且难排查。", "bad"),
            ], 3)),
            ("limits", "4. LoRA 的适用边界", "boundaries", """
<p>LoRA 适合的典型场景是：底座模型已经具备相关能力，下游任务主要需要风格、格式、领域偏好或特定输出映射；你希望低成本保存多个任务版本；部署希望少增加延迟。分类、抽取、指令风格、结构化输出、领域问答、摘要和轻量对齐都常见。</p>
<p>LoRA 不一定适合所有场景。如果任务需要大量新知识、预训练模型完全没有相关能力、下游数据分布差异极大，或你需要从底层表示到高层行为都大幅改变，小 rank LoRA 可能不够。此时可以提高 rank、扩展 target modules、结合继续预训练，或者考虑全量/部分微调。</p>
<p>还有一个现代语境：LoRA 之后出现了很多变体和组合，例如量化底座上训练 LoRA 的 QLoRA，调整方向和幅度的 DoRA，自适应 rank 的方法等。这些不改变论文的基本理解。先学会 LoRA 的 <code>Delta W=BA</code>，再看后续方法才不会迷路。</p>
""" + grid([
                ("适合", "底座已有能力，任务更新像重排、强调或格式适配。", "ok"),
                ("谨慎", "任务需要大量新能力、新语言、新知识或强分布迁移。", "warn"),
                ("替代方案", "更高 rank、更多 target modules、继续预训练、部分或全量微调。", "blue"),
            ], 3)),
            ("paper", "5. 如何完整复述 LoRA 论文", "feynman", """
<p>复述论文可以按四步走。第一步讲问题：大模型全量微调在多任务部署中太贵，每个任务保存完整模型不现实。第二步讲方法：冻结预训练权重，对部分线性层学习低秩更新 <code>Delta W=BA</code>，训练 A/B，部署时可 merge。第三步讲证据：在 RoBERTa、DeBERTa、GPT-2、GPT-3 上，LoRA 用远少的可训练参数达到接近或超过全量微调和其他 PEFT 基线的指标，并且没有 adapter 那类额外推理延迟。第四步讲解释和边界：rank 扫描和子空间分析显示下游更新可能有低 intrinsic rank，但这不是所有任务的定理。</p>
<p>表达时不要把论文讲成“LoRA 是最好的微调方法”。更准确的是：LoRA 提供了一种简单、可 merge、参数高效的低秩适配方法，在论文覆盖的模型和任务上表现强，并给出了低秩更新的实证解释。它的优势来自任务参数少、显存和 checkpoint 低、推理路径可合并；限制包括混合任务 batch、target/rank 选择依赖经验，以及小 rank 对分布差异大的任务未必足够。</p>
<p>你现在应该能把 LoRA 从公式、工程和实验三个角度讲清楚。真正会用论文，不是背结论，而是能在新任务上设计验证，发现配置错误，并知道什么时候该扩大 LoRA 或换别的方法。</p>
""" + formula('<span class="big">一段稳妥复述：</span><br>问题 → 方法 → 实验证据 → 机制解释 → 边界') + """
<div class="map"><span class="node">全量微调太贵</span><span class="node">Delta W=BA</span><span class="node">Wq/Wv 等落点</span><span class="node">实验接近 FT</span><span class="node">小 rank 有边界</span></div>
"""),
            ("pitfalls", "6. 常见工程错误、后果和修法", "diagnosis", grid([
                ("可训练参数为 0", "target module 没命中或冻结逻辑错误。修法：打印参数名和 requires_grad。", "bad"),
                ("底座也在训练", "PEFT 变成部分全量微调。修法：冻结底座并检查 optimizer 参数组。", "bad"),
                ("adapter 当完整模型", "部署缺少底座无法推理。修法：明确保存 adapter 和 base 版本。", "bad"),
                ("merge 前后差异大", "可能 scaling、dtype、重复 merge 或加载顺序错误。修法：做 logits diff 测试。", "warn"),
                ("rank 盲调", "未排除数据和配置问题就加容量。修法：先验收链路，再 sweep。", "warn"),
                ("论文表达夸大", "把局部实验说成普适定理。修法：补上任务范围和边界。", "warn"),
            ], 3)),
            ("examples", "7. 试一试：项目里怎么验收", "examples", """
<div class="grid3">
  <div class="example-card"><h3>例题 1</h3><p>训练日志显示 trainable params = 0，第一步查什么？</p><p class="hint">查 target module 名称是否命中，参数 requires_grad 是否打开。</p></div>
  <div class="example-card"><h3>例题 2</h3><p>merge 后输出和 merge 前差异很大，可能有哪些原因？</p><p class="hint">scaling、dtype、重复 merge、加载错底座、target module 不一致。</p></div>
  <div class="example-card"><h3>例题 3</h3><p>如何一句话稳妥描述 LoRA 的贡献？</p><p class="hint">冻结底座，用低秩矩阵学习任务更新，merge 后不增加推理路径，在多组 NLP 实验中保持质量。</p></div>
</div>
"""),
        ],
        "practice": [
            {"title": "一、实践配置", "intro": "先检查你能否把 LoRA 训练配置验收清楚。", "review": "先验收参数和数据，再调超参。", "questions": [
                {"title": "参数名检查", "kind": "短答", "prompt": "训练前为什么要打印可训练参数名？"},
                {"title": "target modules", "kind": "短答", "prompt": "target module 没命中会出现什么现象？"},
                {"title": "rank 选择", "kind": "短答", "prompt": "为什么不应该一开始就把 rank 拉到很大？"},
                {"title": "alpha", "kind": "短答", "prompt": "alpha 调整的是 LoRA 分支的什么？"},
                {"title": "baseline", "kind": "多选", "type": "multi", "prompt": "LoRA 实验至少应该记录哪些 baseline 或对照？", "options": ["原始底座表现", "LoRA 配置表现", "可训练参数量", "今天的天气"]},
                {"title": "过拟合", "kind": "场景", "prompt": "LoRA 小数据训练过拟合，你会尝试哪些调整？"},
            ]},
            {"title": "二、保存、加载、merge", "intro": "这一组检查部署路径。", "review": "确认当前模型状态：干净底座、挂载 LoRA，还是已 merge。", "questions": [
                {"title": "adapter 与底座", "kind": "判断", "type": "choice", "prompt": "LoRA adapter 文件通常可以脱离底座模型单独推理。", "options": ["正确", "错误"]},
                {"title": "merge 验收", "kind": "短答", "prompt": "如何验证 merge 前后模型输出是否一致？"},
                {"title": "重复 merge", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：线上模型重复 merge 同一份 LoRA，输出明显变差。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "加载错底座", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：LoRA adapter 加载到不兼容底座上。按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "动态 LoRA", "kind": "场景", "prompt": "一个服务要频繁切换多个 LoRA，保存合并模型和动态加载各有什么取舍？"},
                {"title": "dtype", "kind": "短答", "prompt": "为什么量化或半精度场景下更要测试 merge 前后差异？"},
            ]},
            {"title": "三、边界和论文复述", "intro": "最后检查你能否讲清贡献而不夸大。", "review": "好表达包含问题、方法、证据和边界。", "questions": [
                {"title": "适合场景", "kind": "短答", "prompt": "列出 3 类适合优先尝试 LoRA 的任务。"},
                {"title": "不适合场景", "kind": "短答", "prompt": "列出 2 类小 rank LoRA 可能不够的任务。"},
                {"title": "错误诊断：论文夸大", "kind": "诊断", "type": "diagnostic", "prompt": "诊断：“LoRA 已经证明全量微调没有必要。”按错因、后果、修法回答。", "placeholder": "错因：\n后果：\n修法："},
                {"title": "后续方法", "kind": "短答", "prompt": "学习 QLoRA、DoRA 等后续方法前，为什么要先懂 Delta W=BA？"},
                {"title": "面试追问", "kind": "面试追问", "prompt": "用 1-3 句话说明 LoRA 的核心贡献。"},
                {"title": "项目验收清单", "kind": "清单", "prompt": "写一份 8 项 LoRA 训练验收清单。"},
                {"title": "费曼解释", "kind": "费曼解释", "type": "feynman", "full": True, "prompt": "用 8-10 句话完整复述 LoRA 论文：问题、方法、实验、机制解释和边界都要出现。", "hint": "请串联：全量微调、低秩更新、A/B、merge、实验、rank、工程收益、限制。"},
            ]},
        ],
        "keys": "全量微调,低秩更新,A/B,merge,实验,rank,工程收益,限制",
    },
]


def page_html(page: dict) -> str:
    nav = [
        ("goal", "目标与地图"),
        *[(sid, title.split(". ", 1)[-1]) for sid, title, _tag, _body in page["sections"]],
        ("practice", "综合练习"),
        ("final", "导出记录"),
    ]
    nav_html = "\n".join(f'<a href="#{sid}"><span class="dot"></span>{tag(label)}</a>' for sid, label in nav)
    goals = "".join(f"<li>{tag(g)}</li>" for g in page["goals"])
    sections = ""
    for sid, title, st, body in page["sections"]:
        sections += f'<section id="{sid}"><div class="head"><h2>{tag(title)}</h2><span class="tag">{tag(st)}</span></div>{body}</section>\n'
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{tag(page["title"])}｜学习页</title>
  <style>{STYLE}</style>
</head>
<body data-course="{tag(page["title"])}">
<div class="progress"></div>
<div class="layout">
<aside>
  <div class="brand"><strong>{tag(page["title"])}</strong><span>{tag(page["subtitle"])}</span></div>
  <nav>{nav_html}</nav>
  <div class="side-note">{tag(page["side"])}</div>
</aside>
<main>
<header class="hero" id="goal">
  <div>
    <div class="kicker">{tag(page["kicker"])}</div>
    <h1>{tag(page["title"])}</h1>
    <p>{tag(page["subtitle"])}</p>
  </div>
  <div class="route">
    <h3>学完你应该能做什么</h3>
    <ol>{goals}</ol>
  </div>
</header>
{sections}
{practice(page["practice"], page["keys"])}
</main>
</div>
<script>{SCRIPT}</script>
</body>
</html>
"""


def add_page(page: dict) -> None:
    target_dir = BASE / page["dir"]
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "学习页.html").write_text(page_html(page), encoding="utf-8")


def main() -> None:
    for page in PAGES:
        add_page(page)


if __name__ == "__main__":
    main()
