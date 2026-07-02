function initMathAndCode(){
  // 先处理 .formula 元素（直接 katex.render，不需要定界符扫描）
  if(window.katex){
    document.querySelectorAll('.formula').forEach(el => {
      let tex = el.textContent.trim();
      if(tex.startsWith('$$') && tex.endsWith('$$')){
        tex = tex.slice(2, -2).trim();
      }
      if(tex){
        katex.render(tex, el, { throwOnError: false, displayMode: true });
      }
    });
  }
  // 再处理 body 中其他 $...$ / $$...$$
  if(window.renderMathInElement){
    renderMathInElement(document.body,{
      delimiters:[
        {left:'$$',right:'$$',display:true},
        {left:'\\[',right:'\\]',display:true},
        {left:'$',right:'$',display:false},
        {left:'\\(',right:'\\)',display:false}
      ],
      throwOnError:false
    });
  }
  // Prism 代码高亮
  document.querySelectorAll('pre code').forEach(code=>{
    const pre=code.closest('pre'); if(!pre) return;
    const lang=(code.className.match(/language-([\w-]+)/)||[])[1]||code.dataset.exportLang||'text';
    if(lang && !code.classList.contains('language-'+lang)) code.classList.add('language-'+lang);
    pre.classList.add('language-'+lang);
    if(!pre.classList.contains('line-numbers')) pre.classList.add('line-numbers');
    const bar=pre.previousElementSibling;
    if(bar && bar.classList.contains('codebar') && !bar.querySelector('.code-lang')){
      const badge=document.createElement('span');
      badge.className='code-lang'; badge.textContent=lang;
      bar.insertBefore(badge, bar.querySelector('button.copy'));
    }
  });
  if(window.Prism) Prism.highlightAll();
}

function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  }
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  const ok = document.execCommand('copy');
  document.body.removeChild(ta);
  return ok ? Promise.resolve() : Promise.reject(new Error('copy failed'));
}

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, ch => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[ch]));
}

// ── Copy code ──
document.querySelectorAll('.copy').forEach(btn => {
  btn.addEventListener('click', () => {
    const code = btn.closest('.code-example').querySelector('pre code').textContent;
    copyText(code).then(() => {
      const orig = btn.textContent; btn.textContent = '已复制'; btn.style.color = '#10b981';
      setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 1500);
    });
  });
});

// ── Practice ──
const userAnswers = {};      // 记录用户实际作答
const answeredSet = new Set(); // 记录已作答的题目
const resultState = {};      // objective | open, correct | false

function normalizeAnswer(text) {
  let value = String(text || '').trim();
  value = value.replace(/^[\s.。:：、-]+/, '').trim();
  value = value.replace(/\s+/g, ' ').toLowerCase();
  const truthy = new Set(['true', 't', 'yes', 'y', '对', '正确', '是']);
  const falsy = new Set(['false', 'f', 'no', 'n', '错', '错误', '否', '不对']);
  if (truthy.has(value)) return 'true';
  if (falsy.has(value)) return 'false';
  return value;
}

function getCheckedValues(q) {
  return Array.from(q.querySelectorAll('.choices input:checked')).map(input => {
    return (input.value || input.closest('label')?.textContent || '').trim();
  });
}

document.querySelectorAll('.q').forEach(q => {
  const qid = q.dataset.question;
  const answer = (q.dataset.answer || '').trim();

  const btn = q.querySelector('.check');
  const choices = q.querySelectorAll('.choices input');
  const textarea = q.querySelector('textarea');
  const fb = q.querySelector('.feedback');
  const details = q.querySelector('details');
  if (!btn || !fb) return;

  // 记录选择题答案
  choices.forEach(input => {
    input.addEventListener('change', () => {
      const values = getCheckedValues(q);
      userAnswers[qid] = values.join('；');
      q.querySelectorAll('.choices label').forEach(l => {
        l.style.borderColor = 'var(--border)';
        l.style.background = 'var(--bg)';
      });
      q.querySelectorAll('.choices input:checked').forEach(checked => {
        checked.closest('label').style.borderColor = 'var(--text-accent)';
        checked.closest('label').style.background = '#f8fafc';
      });
    });
  });

  // 记录文本框答案
  if (textarea) {
    textarea.addEventListener('input', () => {
      userAnswers[qid] = textarea.value.trim();
    });
  }

  btn.addEventListener('click', () => {
    let correct = false, user = '';

    if (choices.length > 0) {
      const values = getCheckedValues(q);
      if (values.length === 0) {
        fb.style.cssText = 'background:#fffbeb;border:1px solid #fcd34d;color:#92400e;';
        fb.textContent = '请先选择选项';
        return;
      }
      user = values.join('；');
      correct = Boolean(answer) && normalizeAnswer(user) === normalizeAnswer(answer);
    } else if (textarea) {
      user = textarea.value.trim();
      if (!user) {
        fb.style.cssText = 'background:#fffbeb;border:1px solid #fcd34d;color:#92400e;';
        fb.textContent = '请先输入答案';
        return;
      }
      if (answer) {
        const normalizedUser = normalizeAnswer(user);
        const normalizedAnswer = normalizeAnswer(answer);
        correct = normalizedUser === normalizedAnswer ||
                  normalizedUser.includes(normalizedAnswer) ||
                  normalizedAnswer.includes(normalizedUser);
      }
    }

    userAnswers[qid] = user;
    answeredSet.add(qid);

    if (!answer) {
      resultState[qid] = { type: 'open', correct: null };
      fb.style.cssText = 'background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;';
      fb.textContent = '已记录。展开下方参考答案 / 评分要点自查。';
      if (details) details.open = true;
      return;
    }

    if (correct) {
      resultState[qid] = { type: 'objective', correct: true };
      fb.style.cssText = 'background:#f0fdf4;border:1px solid #86efac;color:#166534;';
      fb.innerHTML = '<b>✓ 正确</b>';
      if (details) details.open = true;
    } else {
      resultState[qid] = { type: 'objective', correct: false };
      fb.style.cssText = 'background:#fef2f2;border:1px solid #fecaca;color:#991b1b;';
      fb.innerHTML = '<b>✗ 不正确</b><br>正确答案是：<b>' + escapeHtml(answer) + '</b>';
      if (details) details.open = true;
    }
  });
});

function generateRecord() {
  const record = document.getElementById('record');
  const quality = document.getElementById('quality');
  let md = '## 练习记录\n\n';
  let correctCount = 0;
  let scoredCount = 0;

  document.querySelectorAll('.q').forEach((q, i) => {
    const qid = q.dataset.question;
    const num = String(i + 1).padStart(2, '0');
    const userAns = userAnswers[qid] || '（未作答）';
    const correctAns = (q.dataset.answer || '').trim();
    const hasAnswer = Boolean(correctAns);
    let isCorrect = false;
    if (hasAnswer) {
      scoredCount++;
      const normalizedUser = normalizeAnswer(userAns);
      const normalizedAnswer = normalizeAnswer(correctAns);
      isCorrect = userAns !== '（未作答）' && (
        normalizedUser === normalizedAnswer ||
        normalizedUser.includes(normalizedAnswer) ||
        normalizedAnswer.includes(normalizedUser)
      );
    }
    if (isCorrect) correctCount++;
    const status = hasAnswer ? (isCorrect ? '✓' : (userAns === '（未作答）' ? '○' : '✗')) : '自查';
    md += `- Q${num}: ${q.querySelector('h3').textContent}\n  - 你的答案: ${userAns}\n  - 参考答案: ${correctAns || '见评分要点'} ${status}\n\n`;
  });

  md += '---\n生成时间: ' + new Date().toLocaleString() +
        '\n客观题正确: ' + correctCount + ' / ' + scoredCount;

  record.textContent = md;
  record.style.color = 'var(--text-secondary)';
  quality.textContent = '完成 ' + answeredSet.size + ' 题，客观题正确 ' + correctCount + ' / ' + scoredCount;
}

function copyRecord() {
  const text = document.getElementById('record').textContent;
  if (text.includes('还没有')) return;
  copyText(text).then(() => {
    const btn = document.querySelector('#export .ghost');
    const orig = btn.textContent;
    btn.textContent = '已复制';
    setTimeout(() => btn.textContent = orig, 1500);
  });
}

initMathAndCode();
