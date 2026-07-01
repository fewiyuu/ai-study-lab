(() => {
const lessonTitle = "07 版本更新与迁移策略";

    const cases = {
      model: {
        title: "案例一：默认模型变化",
        risk: "应用没有显式设置模型。升级后默认模型和默认推理设置改变，同一任务的回答风格、工具调用、成本和延迟都可能变化。",
        action: "把生产 Agent 的模型写成显式配置；为旧行为保留固定模型；对关键任务做 golden run；把 token、延迟、拒绝率和工具调用数纳入对比。",
        check: "如果升级后输出质量提高但成本超预算，不能简单判定升级成功。迁移验收要同时看质量、成本、延迟和安全场景。"
      },
      refusal: {
        title: "案例二：拒绝处理显式化",
        risk: "拒绝从空输出或结构化输出重试，变成显式错误。旧代码如果只检查 final_output，可能把安全拒绝误判为普通失败。",
        action: "定义拒绝的业务语义；添加 model_refusal 处理路径；把拒绝结果写入 trace；为结构化输出准备合法的拒绝结果或人工处理分支。",
        check: "回归用例至少包含一个应该拒绝的输入、一个不应该拒绝的边界输入、一个结构化输出拒绝场景。"
      },
      sandbox: {
        title: "案例三：沙箱路径授权",
        risk: "旧应用把 base_dir 外的主机目录复制进 sandbox workspace。升级后未授权路径被拒绝，任务无法读取资料。",
        action: "审计 LocalFile、LocalDir 和 mount；把可信 host 根目录写入 manifest 级别的只读授权；禁止从模型输出直接生成授权路径；补充路径拒绝测试。",
        check: "迁移成功不是“所有路径都放开”，而是“只有业务允许的路径可见，并且拒绝路径能被清晰记录”。"
      },
      checkpoint: {
        title: "案例四：旧 checkpoint 用新代码恢复",
        risk: "LangGraph thread 中已有旧状态。升级后节点代码、状态字段或工具结果格式变化，恢复时可能走错分支或重复副作用。",
        action: "为状态加 schema_version；写旧状态迁移函数；对副作用节点加幂等键；用旧 thread_id 做恢复演练；比较恢复前后 trace。",
        check: "重点不是从头跑一遍能成功，而是从旧 checkpoint 中间恢复也能成功，并且不会重复已经发生的外部动作。"
      }
    };

    function updateProgress() {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const pct = height > 0 ? (scrollTop / height) * 100 : 0;
      document.getElementById("progress").style.width = pct + "%";
    }

    function setActiveNav() {
      const links = Array.from(document.querySelectorAll("nav a"));
      const sections = links
        .map((link) => link.getAttribute("href"))
        .filter((href) => href && href.startsWith("#"))
        .map((href) => document.querySelector(href))
        .filter(Boolean);
      let current = sections[0]?.id;
      sections.forEach((section) => {
        if (section.getBoundingClientRect().top <= 120) current = section.id;
      });
      links.forEach((link) => {
        const href = link.getAttribute("href");
        link.classList.toggle("active", href === "#" + current);
      });
    }

    function renderCase(name) {
      const item = cases[name] || cases.model;
      document.querySelectorAll("[data-case]").forEach((button) => {
        button.classList.toggle("active", button.dataset.case === name);
      });
      document.getElementById("casePanel").innerHTML = `
        <h3>${item.title}</h3>
        <p><strong>风险：</strong>${item.risk}</p>
        <p><strong>迁移动作：</strong>${item.action}</p>
        <p><strong>验收重点：</strong>${item.check}</p>
      `;
    }

    document.querySelectorAll("[data-case]").forEach((button) => {
      button.addEventListener("click", () => renderCase(button.dataset.case));
    });

    window.addEventListener("scroll", () => {
      updateProgress();
      setActiveNav();
    });

    document.querySelectorAll(".codebar").forEach((bar) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-code";
      btn.textContent = "复制";
      btn.addEventListener("click", () => {
        const code = bar.nextElementSibling?.innerText || "";
        navigator.clipboard.writeText(code).then(() => {
          btn.textContent = "已复制";
          setTimeout(() => { btn.textContent = "复制"; }, 1200);
        }).catch(() => {
          btn.textContent = "失败";
          setTimeout(() => { btn.textContent = "复制"; }, 1200);
        });
      });
      bar.appendChild(btn);
    });

    function valueFor(name) {
      const checked = document.querySelector(`input[name="${name}"]:checked`);
      if (checked) return checked.value;
      const field = document.querySelector(`[name="${name}"]`);
      return field ? field.value.trim() : "";
    }

    function collectQuestions() {
      return Array.from(document.querySelectorAll("[data-question]")).map((node) => ({
        id: node.dataset.question,
        group: node.dataset.group || "练习",
        title: node.dataset.title || node.querySelector("h3")?.textContent || node.dataset.question,
        answer: valueFor(node.dataset.question)
      }));
    }

    function generateRecord() {
      const questions = collectQuestions();
      const groups = new Map();
      const missing = [];

      questions.forEach((q) => {
        if (!q.answer) missing.push(q.title);
        if (!groups.has(q.group)) groups.set(q.group, []);
        groups.get(q.group).push(q);
      });

      let out = `# ${lessonTitle}｜练习记录\n\n`;
      out += "## 核心复盘上下文\n\n";
      out += "- OpenAI Agents SDK 更新\n";
      out += "- OpenAI Agents SDK 文档\n";
      out += "- LangGraph Durable Execution\n";
      out += "- 资料边界：访问日期 2026-06-21\n\n";
      groups.forEach((items, group) => {
        out += `## ${group}\n\n`;
        items.forEach((item) => {
          out += `### ${item.title}\n${item.answer || "（未填写）"}\n\n`;
        });
      });

      document.getElementById("record").textContent = out;
      const quality = document.getElementById("quality");
      quality.style.display = "block";
      quality.textContent = missing.length
        ? `还有 ${missing.length} 题未填写：\n` + missing.join("\n")
        : "练习记录完整，可以继续复盘。";
      return out;
    }

    function copyRecord() {
      const text = document.getElementById("record").textContent === "还没有生成练习记录。"
        ? generateRecord()
        : document.getElementById("record").textContent;
      navigator.clipboard.writeText(text).then(() => {
        const quality = document.getElementById("quality");
        quality.style.display = "block";
        quality.textContent = "Markdown 已复制。";
      }).catch(() => {
        alert("复制失败，请手动复制。");
      });
    }

    function downloadRecord() {
      const text = document.getElementById("record").textContent === "还没有生成练习记录。"
        ? generateRecord()
        : document.getElementById("record").textContent;
      const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "07-version-migration-practice.md";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }

    renderCase("model");
    updateProgress();
    setActiveNav();

(function () {
  var progress = document.getElementById("progress");
  if (!progress) return;
  function updateProgress() {
    var doc = document.documentElement;
    var scrollable = Math.max(1, doc.scrollHeight - doc.clientHeight);
    var ratio = Math.max(0, Math.min(1, (window.scrollY || doc.scrollTop) / scrollable));
    progress.style.width = (ratio * 100).toFixed(2) + "%";
  }
  updateProgress();
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);
})();

  if (typeof window !== 'undefined') {
    window.generateRecord = typeof generateRecord === 'function' ? generateRecord : window.generateRecord;
    window.copyRecord = typeof copyRecord === 'function' ? copyRecord : window.copyRecord;
  }
})();
