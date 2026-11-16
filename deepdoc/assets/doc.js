(function(){
  const $  = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  const KEY = 'sqli-doc-v1';

  /* 主题 */
  const root = document.documentElement;
  const store = {
    get(){ try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e){ return {}; } },
    set(o){ try { localStorage.setItem(KEY, JSON.stringify(Object.assign(this.get(), o))); } catch(e){} }
  };
  const saved = store.get();
  const theme = saved.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.setAttribute('data-theme', theme);
  const themeBtn = $('#themeBtn');
  const syncTheme = () => { themeBtn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀' : '☾'; };
  syncTheme();
  themeBtn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    store.set({theme: next}); syncTheme();
  });

  /* 进度条 */
  const bar = $('#progress');
  const onScrollProgress = () => {
    const h = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + '%';
    $('#toTop').classList.toggle('show', scrollY > 700);
  };
  addEventListener('scroll', onScrollProgress, {passive:true});
  onScrollProgress();

  $('#toTop').addEventListener('click', () => scrollTo({top:0, behavior:'smooth'}));

  /* 目录：展开 + 高亮 */
  const groups = $$('.toc > li.g');
  const links = $$('.toc a');
  const heads = $$('.content h2[id], .content h3[id]');
  const linkFor = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));

  function setActive(id){
    links.forEach(a => a.classList.remove('active'));
    groups.forEach(g => g.classList.remove('open'));
    const a = linkFor.get(id);
    if (a){
      a.classList.add('active');
      const g = a.closest('li.g');
      if (g) g.classList.add('open');
      const r = a.getBoundingClientRect();
      if (r.top < 70 || r.bottom > innerHeight - 20) a.scrollIntoView({block:'nearest'});
    }
  }
  let ticking = false;
  function spy(){
    let cur = heads[0];
    for (const h of heads){
      if (h.getBoundingClientRect().top <= 96) cur = h; else break;
    }
    if (cur) setActive(cur.id);
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking){ requestAnimationFrame(spy); ticking = true; } }, {passive:true});
  spy();

  /* 手机菜单 */
  const menuBtn = $('#menuBtn');
  if (menuBtn) menuBtn.addEventListener('click', () => document.body.classList.toggle('nav-open'));
  const scrim = $('#scrim');
  if (scrim) scrim.addEventListener('click', () => document.body.classList.remove('nav-open'));
  links.forEach(a => a.addEventListener('click', () => document.body.classList.remove('nav-open')));
  $$('.caret').forEach(btn => btn.addEventListener('click', e => {
    e.preventDefault(); e.stopPropagation();
    btn.closest('li.g').classList.toggle('open');
  }));

  /* 复制代码 */
  document.addEventListener('click', e => {
    const btn = e.target.closest('.copy');
    if (!btn) return;
    const block = btn.closest('.codeblock');
    const text = block.querySelector('pre').innerText.replace(/\n$/, '');
    const done = () => { btn.textContent = '已复制'; setTimeout(() => btn.textContent = '复制', 1400); };
    if (navigator.clipboard && isSecureContext){
      navigator.clipboard.writeText(text).then(done).catch(() => fallback(text, done));
    } else fallback(text, done);
  });
  function fallback(text, done){
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch(e){}
    ta.remove(); done();
  }

  /* 任务清单持久化 */
  const tasks = $$('li.task input');
  const taskState = store.get().tasks || {};
  tasks.forEach((t, i) => {
    const key = 't' + i;
    if (taskState[key]){ t.checked = true; t.closest('li').classList.add('done'); }
    t.addEventListener('change', () => {
      t.closest('li').classList.toggle('done', t.checked);
      const s = store.get().tasks || {};
      s[key] = t.checked; store.set({tasks: s});
    });
  });

  /* 搜索 */
  const layer = $('#searchLayer'), input = $('#searchInput'), resBox = $('#searchResults');
  const index = [];
  heads.forEach(h => {
    let node = h.nextElementSibling, buf = [];
    while (node && !/^H[23]$/.test(node.tagName)){
      buf.push(node.innerText); node = node.nextElementSibling;
    }
    index.push({
      id: h.id,
      title: h.innerText.replace(/#$/, '').trim(),
      text: buf.join(' ').replace(/\s+/g, ' ').slice(0, 1200)
    });
  });
  let sel = 0, hits = [];
  function esc(s){ return s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
  function render(q){
    const kw = q.trim().toLowerCase();
    hits = !kw ? [] : index.filter(it => (it.title + ' ' + it.text).toLowerCase().includes(kw)).slice(0, 30);
    sel = 0;
    if (!kw){ resBox.innerHTML = '<div class="sr-empty">输入关键词，例如：时间盲注、二次注入、ORDER BY、sqlmap</div>'; return; }
    if (!hits.length){ resBox.innerHTML = '<div class="sr-empty">没有找到「' + esc(q) + '」</div>'; return; }
    resBox.innerHTML = hits.map((it, i) => {
      const low = (it.text || '').toLowerCase();
      const p = low.indexOf(kw);
      let frag = it.text.slice(0, 110);
      if (p > 40) frag = '…' + it.text.slice(p - 40, p + 90);
      return '<a class="sr-item' + (i === 0 ? ' sel' : '') + '" href="#' + it.id + '" data-i="' + i + '">' +
        '<div class="sr-t">' + esc(it.title) + '</div>' +
        '<div class="sr-d">' + esc(frag) + '</div></a>';
    }).join('');
  }
  function openSearch(){
    layer.classList.add('open'); document.body.classList.add('search-open');
    input.value = ''; render(''); setTimeout(() => input.focus(), 30);
  }
  function closeSearch(){
    layer.classList.remove('open'); document.body.classList.remove('search-open');
  }
  input.addEventListener('input', e => render(e.target.value));
  layer.addEventListener('click', e => { if (e.target === layer) closeSearch(); });
  resBox.addEventListener('click', e => {
    const a = e.target.closest('.sr-item'); if (!a) return;
    closeSearch();
    const h = document.getElementById(a.getAttribute('href').slice(1));
    if (h){ h.scrollIntoView({behavior:'smooth', block:'start'}); h.classList.add('flash'); setTimeout(() => h.classList.remove('flash'), 1800); }
  });
  addEventListener('keydown', e => {
    const mac = navigator.platform.toUpperCase().includes('MAC');
    if ((e.ctrlKey || (mac && e.metaKey)) && e.key.toLowerCase() === 'k'){ e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') closeSearch();
    if (!layer.classList.contains('open') || !hits.length) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp'){
      e.preventDefault();
      const items = $$('.sr-item', resBox);
      items[sel] && items[sel].classList.remove('sel');
      sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + hits.length) % hits.length;
      items[sel] && (items[sel].classList.add('sel'), items[sel].scrollIntoView({block:'nearest'}));
    }
    if (e.key === 'Enter'){
      const a = $$('.sr-item', resBox)[sel];
      if (a) a.click();
    }
  });
  $('#searchBtn').addEventListener('click', openSearch);
})();
