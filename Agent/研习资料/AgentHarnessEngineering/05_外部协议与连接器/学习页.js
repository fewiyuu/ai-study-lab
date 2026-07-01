(() => {
const lessonTitle = "外部协议与连接器";
    const courseTitle = "智能体运行承载工程";

    function updateProgress() {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const pct = height > 0 ? (scrollTop / height) * 100 : 0;
      document.getElementById("progress").style.width = pct + "%";
    }

    window.addEventListener("scroll", updateProgress);
    updateProgress();

    const sections = Array.from(document.querySelectorAll("main section, main header"));
    const navLinks = Array.from(document.querySelectorAll("nav a"));

    function updateActiveNav() {
      const current = sections
        .filter((section) => section.id && section.getBoundingClientRect().top < 140)
        .pop();
      navLinks.forEach((link) => {
        const isActive = current && link.getAttribute("href") === "#" + current.id;
        link.classList.toggle("active", Boolean(isActive));
      });
    }

    window.addEventListener("scroll", updateActiveNav);
    updateActiveNav();

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
      const checked = Array.from(document.querySelectorAll(`input[name="${name}"]:checked`));
      if (checked.length) return checked.map((item) => item.value).join(", ");
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

      let out = `# ${courseTitle}｜${lessonTitle}｜练习记录\n\n`;
      out += `> 核心复盘上下文：外部协议、MCP、连接器、授权、资源暴露与副作用边界。\n\n`;

      groups.forEach((items, group) => {
        out += `## ${group}\n\n`;
        items.forEach((item) => {
          out += `### ${item.title}\n\n`;
          out += `${item.answer || "（未填写）"}\n\n`;
        });
      });

      out += "## 自检清单\n\n";
      out += "- 我是否区分了 tool、resource、prompt？\n";
      out += "- 我是否说明了主体、权限范围、有效期和审批？\n";
      out += "- 我是否区分了过滤和审批？\n";
      out += "- 我是否写清楚错误是否可重试、是否已经产生副作用？\n";
      out += "- 我是否把 SDK 或协议更新转成了回归测试？\n";

      document.getElementById("record").textContent = out;
      const quality = document.getElementById("quality");
      quality.style.display = "block";
      quality.textContent = missing.length
        ? `还有 ${missing.length} 题未填写：\n` + missing.join("\n")
        : "练习记录完整，可以继续复盘。";
      return out;
    }

    function copyRecord() {
      const text = document.getElementById("record").textContent;
      navigator.clipboard.writeText(text).then(() => {
        const quality = document.getElementById("quality");
        quality.style.display = "block";
        quality.textContent = "已复制 Markdown 练习记录。";
      }).catch(() => {
        alert("复制失败，请手动复制。");
      });
    }

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
