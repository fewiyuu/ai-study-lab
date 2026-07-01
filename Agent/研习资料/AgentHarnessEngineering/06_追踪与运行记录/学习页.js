(() => {
const fields = [
      ["answerTrace", "根 trace 设计"],
      ["answerSpan", "span 动作清单"],
      ["answerPrivacy", "记录与脱敏策略"],
      ["answerCheckpoint", "checkpoint 与恢复判断"],
      ["answerIdempotency", "副作用幂等策略"],
      ["answerDebug", "失败排查步骤"]
    ];

    const checks = [
      ["checkTrace", "trace 标识清晰"],
      ["checkSpan", "span 边界清晰"],
      ["checkSensitive", "敏感数据策略清晰"],
      ["checkCheckpoint", "trace 与 checkpoint 可关联"],
      ["checkReplay", "副作用具备幂等或任务边界"]
    ];

    function valueOf(id) {
      const el = document.getElementById(id);
      return el && el.value.trim() ? el.value.trim() : "未填写";
    }

    function checkedText(id) {
      const el = document.getElementById(id);
      return el && el.checked ? "完成" : "未完成";
    }

    function buildMarkdown() {
      const date = new Date().toISOString().slice(0, 10);
      const sections = fields.map(([id, title]) => `## ${title}\n\n${valueOf(id)}`).join("\n\n");
      const checklist = checks.map(([id, title]) => `- [${checkedText(id) === "完成" ? "x" : " "}] ${title}`).join("\n");
      return `# 06 追踪与运行记录｜练习记录\n\n- 日期：${date}\n- 核心复盘上下文：OpenAI Agents SDK tracing；LangGraph Durable Execution / Persistence（访问日期：2026-06-21）\n\n${sections}\n\n## 自检清单\n\n${checklist}\n\n## 下一步\n\n- 选择一个真实任务，补齐 trace_id、group_id、thread_id、checkpoint_id 的关联字段。\n- 为一个外部写入动作补充 custom span 和幂等键。\n`;
    }

    function generateRecord() {
      const markdown = buildMarkdown();
      refreshPreview();
      return markdown;
    }

    function refreshPreview() {
      document.getElementById("recordPreview").textContent = buildMarkdown();
    }

    function showToast(message) {
      const toast = document.getElementById("toast");
      toast.textContent = message;
      window.setTimeout(() => {
        if (toast.textContent === message) {
          toast.textContent = "";
        }
      }, 2200);
    }

    async function copyRecord() {
      const markdown = buildMarkdown();
      try {
        await navigator.clipboard.writeText(markdown);
        showToast("已复制 Markdown 记录");
      } catch (error) {
        const preview = document.getElementById("recordPreview");
        preview.textContent = markdown;
        const range = document.createRange();
        range.selectNodeContents(preview);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        showToast("浏览器阻止自动复制，已选中预览文本");
      }
    }

    function downloadRecord() {
      const blob = new Blob([buildMarkdown()], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "06-tracing-run-record.md";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      showToast("已生成 Markdown 下载");
    }

    function generateRecord() {
      const markdown = buildMarkdown();
      refreshPreview();
      return markdown;
    }

    document.getElementById("copyRecord").addEventListener("click", copyRecord);
    document.getElementById("downloadRecord").addEventListener("click", downloadRecord);
    document.getElementById("refreshRecord").addEventListener("click", refreshPreview);
    [...fields, ...checks].forEach(([id]) => {
      const el = document.getElementById(id);
      const eventName = el.type === "checkbox" ? "change" : "input";
      el.addEventListener(eventName, refreshPreview);
    });
    refreshPreview();

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
