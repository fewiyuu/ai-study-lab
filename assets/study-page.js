const progress=document.getElementById('progress');
const navLinks=Array.from(document.querySelectorAll('nav a[href^="#"]'));
const navSections=navLinks.map(link=>document.querySelector(link.getAttribute('href'))).filter(Boolean);

function initMathAndCode(){
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
  document.querySelectorAll('pre code').forEach(code=>{
    const pre=code.closest('pre');
    if(!pre)return;
    const lang=(code.className.match(/language-([\w-]+)/)||[])[1]||code.dataset.exportLang||'text';
    if(lang&&!code.classList.contains('language-'+lang))code.classList.add('language-'+lang);
    pre.classList.add('language-'+lang);
    if(!pre.classList.contains('line-numbers'))pre.classList.add('line-numbers');
    const bar=pre.previousElementSibling;
    if(bar&&bar.classList.contains('codebar')&&!bar.querySelector('.code-lang')){
      const badge=document.createElement('span');
      badge.className='code-lang';
      badge.textContent=lang;
      bar.insertBefore(badge,bar.querySelector('button.copy'));
    }
    if(!pre.parentElement.classList.contains('code-wrap')){
      const wrap=document.createElement('div');
      wrap.className='code-wrap';
      pre.parentNode.insertBefore(wrap,pre);
      wrap.appendChild(pre);
      if((code.textContent||'').split('\n').length>16){
        wrap.classList.add('collapsed');
        const tools=document.createElement('div');
        tools.className='code-tools';
        const toggle=document.createElement('button');
        toggle.type='button';
        toggle.textContent='展开代码';
        toggle.addEventListener('click',()=>{
          wrap.classList.toggle('collapsed');
          toggle.textContent=wrap.classList.contains('collapsed')?'展开代码':'收起代码';
        });
        tools.appendChild(toggle);
        wrap.appendChild(tools);
      }
    }
  });
  if(window.Prism)Prism.highlightAll();
}

function updateProgress(){
  if(!progress)return;
  const max=document.documentElement.scrollHeight-document.documentElement.clientHeight;
  const top=document.documentElement.scrollTop||document.body.scrollTop;
  progress.style.width=max>0?Math.min(100,Math.max(0,top/max*100))+'%':'0%';
}

function updateActiveSection(){
  if(!navSections.length)return;
  const top=(window.scrollY||document.documentElement.scrollTop)+150;
  let current=navSections[0];
  navSections.forEach(section=>{if(section.offsetTop<=top)current=section});
  navLinks.forEach(link=>link.classList.toggle('active',current&&link.getAttribute('href')==='#'+current.id));
}

function updateScrollState(){updateProgress();updateActiveSection()}
addEventListener('scroll',updateScrollState,{passive:true});
updateScrollState();
initMathAndCode();

document.querySelectorAll('[data-copy]').forEach(btn=>btn.addEventListener('click',async()=>{
  const text=document.getElementById(btn.dataset.copy)?.textContent||'';
  try{await navigator.clipboard.writeText(text);btn.textContent='已复制'}catch{btn.textContent='复制失败'}
  setTimeout(()=>btn.textContent='复制',1200);
}));

function normalizeAnswer(text){return (text||'').toLowerCase().replace(/\s+/g,' ').trim()}

function textMatches(field){
  const answer=normalizeAnswer(field.value);
  if(!answer)return false;
  return field.dataset.answer.split(';').every(group=>group.split(',').some(term=>answer.includes(normalizeAnswer(term))));
}

function questionNode(name){return document.querySelector(`[data-question="${name}"]`)}

function miniFieldValues(node){
  const fields=Array.from(node.querySelectorAll('.mini-fields input'));
  if(!fields.length)return null;
  return fields.map(field=>{
    const label=field.closest('label')?.textContent.replace(field.value,'').trim()||field.name||'字段';
    return {label,value:field.value.trim()};
  });
}

function valueFor(name){
  const node=questionNode(name);
  const mini=node&&miniFieldValues(node);
  if(mini){
    if(mini.every(item=>!item.value))return '';
    return mini.map(item=>`${item.label}=${item.value}`).join('; ');
  }
  const checkedBoxes=Array.from(document.querySelectorAll(`input[name="${name}"][type="checkbox"]:checked`));
  if(checkedBoxes.length)return checkedBoxes.map(item=>item.value).join('; ');
  const checked=document.querySelector(`input[name="${name}"]:checked`);
  if(checked)return checked.value;
  const field=document.querySelector(`[name="${name}"]`);
  return field?field.value.trim():'';
}

function checkMiniFields(node){
  const fields=Array.from(node.querySelectorAll('.mini-fields input[data-answer]'));
  if(!fields.length)return null;
  const missing=fields.filter(f=>!f.value.trim());
  const wrong=fields.filter(f=>f.value.trim()&&!textMatches(f));
  if(missing.length)return {ok:false,text:'还有空着的字段。先把每个对象分别写清楚。'};
  if(wrong.length)return {ok:false,text:'有字段还不稳。对照提示重新区分对象、形状或术语。'};
  return {ok:true,text:'回答正确。'};
}

function checkQuestion(node){
  const feedback=node.querySelector('.feedback');
  if(!feedback)return;
  const mini=checkMiniFields(node);
  if(mini){
    feedback.className='feedback '+(mini.ok?'ok':'bad');
    feedback.textContent=mini.text;
    return;
  }
  const textField=node.querySelector('input[type="text"][data-answer]');
  const selected=node.querySelector('input[type="radio"]:checked');
  let ok=false;
  let explanation='';
  if(textField){
    ok=textMatches(textField);
    explanation=textField.dataset.explain||node.dataset.explain||'';
  }else if(node.dataset.answer){
    ok=selected&&selected.value===node.dataset.answer;
    explanation=node.dataset.explain||'';
  }
  feedback.className='feedback '+(ok?'ok':'bad');
  feedback.textContent=ok?'回答正确。'+(explanation?' '+explanation:''):'再检查一下。'+(explanation?' '+explanation:'');
}

document.querySelectorAll('.check').forEach(btn=>btn.addEventListener('click',()=>checkQuestion(btn.closest('.q'))));

document.querySelectorAll('.reveal').forEach(btn=>btn.addEventListener('click',()=>{
  const detail=btn.closest('.q')?.querySelector('details');
  if(detail){
    detail.open=!detail.open;
    btn.textContent=detail.open?'收起反馈':'展开反馈';
    if(detail.open)detail.scrollIntoView({block:'nearest'});
  }
}));

document.querySelectorAll('[data-shape-tracer]').forEach(tracer=>{
  const lines=Array.from(tracer.querySelectorAll('[data-trace-step]'));
  const cards=Array.from(tracer.querySelectorAll('[data-trace-target]'));
  function setStep(step){
    lines.forEach(line=>line.classList.toggle('active',line.dataset.traceStep===step));
    cards.forEach(card=>card.classList.toggle('active',card.dataset.traceTarget===step));
  }
  lines.forEach(line=>{
    line.addEventListener('mouseenter',()=>setStep(line.dataset.traceStep));
    line.addEventListener('focus',()=>setStep(line.dataset.traceStep));
    line.addEventListener('click',()=>setStep(line.dataset.traceStep));
  });
});

function parseTokenInput(value){
  return (value||'')
    .replace(/[\[\](){}]/g,' ')
    .split(/[,\s]+/)
    .map(item=>item.trim())
    .filter(Boolean)
    .slice(0,12);
}

function renderShiftDemo(demo){
  const input=demo.querySelector('input');
  const rows=demo.querySelector('.shift-rows');
  const tokens=parseTokenInput(input.value);
  if(tokens.length<2){
    rows.innerHTML='<p class="hint">至少输入两个 token，才能构造 x/y。</p>';
    return;
  }
  const x=tokens.slice(0,-1);
  const y=tokens.slice(1);
  const cells=items=>items.map(item=>`<span class="shift-cell">${item.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))}</span>`).join('');
  rows.innerHTML=`<div class="shift-row x"><b>x 输入</b><div class="shift-cells">${cells(x)}</div></div><div class="shift-row y"><b>y 目标</b><div class="shift-cells">${cells(y)}</div></div>`;
}

document.querySelectorAll('[data-shift-demo]').forEach(demo=>{
  const input=demo.querySelector('input');
  renderShiftDemo(demo);
  input.addEventListener('input',()=>renderShiftDemo(demo));
});

document.querySelectorAll('[data-terminal-lab]').forEach(lab=>{
  const buttons=Array.from(lab.querySelectorAll('[data-terminal-case]'));
  const output=lab.querySelector('.terminal-output');
  const templates=new Map(Array.from(lab.querySelectorAll('template[data-terminal-output]')).map(template=>[
    template.dataset.terminalOutput,
    template.innerHTML.trim()
  ]));
  function render(which){
    buttons.forEach(btn=>btn.classList.toggle('active',btn.dataset.terminalCase===which));
    output.innerHTML=templates.get(which)||templates.values().next().value||output.innerHTML;
  }
  buttons.forEach(btn=>btn.addEventListener('click',()=>render(btn.dataset.terminalCase)));
  if(buttons.length)render(buttons[0].dataset.terminalCase);
});

function answeredFor(node,answer){
  const mini=Array.from(node.querySelectorAll('.mini-fields input'));
  if(mini.length)return mini.every(field=>field.value.trim());
  if(node.querySelector('input[type="checkbox"]'))return Boolean(node.querySelector('input[type="checkbox"]:checked'));
  if(node.querySelector('input[type="radio"]'))return Boolean(node.querySelector('input[type="radio"]:checked'));
  return Boolean(answer);
}

function statusFor(node){
  const miniFields=Array.from(node.querySelectorAll('.mini-fields input[data-answer]'));
  if(miniFields.length){
    if(miniFields.every(field=>!field.value.trim()))return '未作答';
    return checkMiniFields(node).ok?'✅ 正确':'❌ 待修正';
  }
  if(node.dataset.answer){
    const selected=node.querySelector('input[type="radio"]:checked');
    if(!selected)return '未作答';
    return selected.value===node.dataset.answer?'✅ 正确':'❌ 待修正';
  }
  if(node.querySelector('input[type="checkbox"]')){
    return node.querySelector('input[type="checkbox"]:checked')?'已选择，展开反馈自查':'未作答';
  }
  const field=node.querySelector('input[type="text"][data-answer]');
  if(field){
    if(!field.value.trim())return '未作答';
    return textMatches(field)?'✅ 正确':'❌ 待修正';
  }
  return '';
}

function groupReview(node){
  const review=node.closest('.practice-group')?.querySelector('.quick-review');
  return review?review.textContent.replace(/\s+/g,' ').trim():'';
}

function questionTags(node){
  return Array.from(node.querySelectorAll('.q-meta .pill')).map(pill=>pill.textContent.trim()).filter(Boolean).join(' / ');
}

function tableToMarkdown(table){
  const rows=Array.from(table.querySelectorAll('tr')).map(row=>
    Array.from(row.children).map(cell=>
      (cell.textContent||'').replace(/\s+/g,' ').trim().replace(/\|/g,'\\|')
    )
  ).filter(row=>row.length);
  if(!rows.length)return '';
  const width=Math.max(...rows.map(row=>row.length));
  const normalized=rows.map(row=>Array.from({length:width},(_,index)=>row[index]||''));
  const header=normalized[0];
  const divider=header.map(()=>'---');
  const body=normalized.slice(1);
  return [header,divider,...body].map(row=>'| '+row.join(' | ')+' |').join('\n');
}

function exportContexts(){
  return Array.from(document.querySelectorAll('[data-export-context]')).map(node=>{
    const table=node.matches('table')?node:node.querySelector('table');
    const lang=node.dataset.exportLang||'text';
    const text=lang==='table'&&table
      ? tableToMarkdown(table)
      : (node.textContent||'').replace(/\n{3,}/g,'\n\n').trim();
    return {
      title:node.dataset.exportContext||node.closest('section')?.querySelector('h2')?.textContent||'核心上下文',
      lang,
      text
    };
  }).filter(item=>item.text);
}

function collectQuestions(){
  const dataQ = Array.from(document.querySelectorAll('[data-question]')).map(node=>{
    const answer=valueFor(node.dataset.question);
    return {
      id:node.dataset.question,
      group:node.dataset.group||'练习',
      groupReview:groupReview(node),
      title:node.dataset.title||node.querySelector('h3')?.textContent||node.dataset.question,
      tags:questionTags(node),
      answer,
      answered:answeredFor(node,answer),
      status:statusFor(node)
    };
  });
  
  const seen=new Set(dataQ.map(q=>q.id));
  const nameQ=[];
  document.querySelectorAll('input[name], textarea[name]').forEach(el=>{
    const name=el.getAttribute('name');
    if(!name||seen.has(name))return;
    seen.add(name);
    const node=el.closest('.q')||el.closest('div')||el;
    const answer=valueFor(name);
    nameQ.push({
      id:name,
      group:node.closest('.practice-group')?.querySelector('.group-head h3')?.textContent||'练习',
      groupReview:groupReview(node),
      title:node.querySelector('h3')?.textContent||name,
      tags:questionTags(node),
      answer,
      answered:answeredFor(node,answer),
      status:statusFor(node)
    });
  });
  
  return [...dataQ,...nameQ];
}

function generateRecord(){
  const questions=collectQuestions();
  const groups=new Map();
  const missing=[];
  questions.forEach(q=>{
    if(!q.answered)missing.push(q.title);
    if(!groups.has(q.group))groups.set(q.group,{review:q.groupReview,items:[]});
    groups.get(q.group).items.push(q);
  });
  const course=document.body.dataset.course||'学习资料';
  const unit=document.body.dataset.unit||document.title.replace(/\s+/g,' ').trim();
  const contexts=exportContexts();
  let out=`# ${course}｜${unit}｜练习记录\n\n`;
  if(contexts.length){
    out+='## 核心复盘上下文\n\n';
    contexts.forEach(item=>{
      out+=`### ${item.title}\n\n`;
      if(item.lang==='table'){
        out+=item.text+'\n\n';
      }else{
        out+='```'+item.lang+'\n'+item.text+'\n```\n\n';
      }
    });
  }
  groups.forEach((groupData,group)=>{
    out+=`## ${group}\n\n`;
    if(groupData.review)out+=`复盘提示：${groupData.review}\n\n`;
    groupData.items.forEach(item=>{
      out+=`### ${item.title}\n`;
      if(item.tags)out+=`题型：${item.tags}\n\n`;
      if(item.status)out+=`状态：${item.status}\n\n`;
      out+=`${item.answer||'（未填写）'}\n\n`;
    });
  });
  document.getElementById('record').textContent=out;
  const quality=document.getElementById('quality');
  quality.style.display='block';
  quality.textContent=missing.length?`还有 ${missing.length} 题未填写：\n`+missing.join('\n'):'练习记录完整，可以继续复盘。';
  return out;
}

function copyRecord(){
  const current=document.getElementById('record').textContent;
  const text=current.includes('还没有生成')?generateRecord():current;
  navigator.clipboard.writeText(text).catch(()=>{});
}
