
(function(){
  var WA='https://wa.me/2347066153757?text=',b=document.body,picks=[];
  var bar=document.getElementById('barBtn'),sum=document.getElementById('barSum');
  var single=b.dataset.single==='1';
  function msg(){
    if(!picks.length)return b.dataset.msg;
    return b.dataset.pickmsg+'\n\n'+picks.map(function(p){return '• '+p}).join('\n')+'\n\n'+b.dataset.pickend;
  }
  function upd(){
    var url=WA+encodeURIComponent(msg());
    [].forEach.call(document.querySelectorAll('[data-wa]'),function(a){a.href=a.dataset.wa?WA+encodeURIComponent(a.dataset.wa):url});
    sum.textContent='';
    var s=document.createElement('b');
    s.textContent=picks.length?(single?picks[0]:picks.length+' in your plan'):b.dataset.bar;
    sum.appendChild(s);
    if(picks.length&&!single)sum.appendChild(document.createTextNode(' · '+picks.join(', ')));
    bar.textContent=picks.length?b.dataset.barcta:'Chat on WhatsApp';
  }
  [].forEach.call(document.querySelectorAll('.pick'),function(btn){
    btn.addEventListener('click',function(){
      var n=btn.dataset.name,on=btn.getAttribute('aria-pressed')!=='true';
      if(single){picks=[];[].forEach.call(document.querySelectorAll('.pick'),function(o){o.setAttribute('aria-pressed','false');o.textContent=o.dataset.off})}
      if(on)picks.push(n);else picks=picks.filter(function(p){return p!==n});
      btn.setAttribute('aria-pressed',on);btn.textContent=on?btn.dataset.on:btn.dataset.off;
      upd();
    });
  });
  upd();
})();
