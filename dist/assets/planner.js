
(function(){
  var WA='https://wa.me/2347066153757?text=';
  // Starting assumptions per market. Replace with Demoski's real account averages before launch.
  var NICHES=[
    {id:'fashion',name:'Fashion',cpm:1500,ctr:1.8,lead:8,sale:1.8,aov:25000},
    {id:'beauty',name:'Beauty & skincare',cpm:1400,ctr:2.0,lead:9,sale:2.2,aov:18000},
    {id:'gadgets',name:'Gadgets & tech',cpm:1800,ctr:1.5,lead:7,sale:1.2,aov:85000},
    {id:'realestate',name:'Real estate',cpm:2600,ctr:1.2,lead:6,sale:0.3,aov:2500000},
    {id:'food',name:'Food & restaurants',cpm:1200,ctr:2.2,lead:10,sale:2.5,aov:9000},
    {id:'education',name:'Courses & education',cpm:1700,ctr:1.6,lead:9,sale:1.5,aov:45000},
    {id:'other',name:'Something else',cpm:1800,ctr:1.6,lead:8,sale:1.5,aov:30000}
  ];
  var COURSES=[
    {n:'Graphic Design & Branding',d:'Design logos, brand kits and social graphics clients pay for',l:'Beginner',k:12,h:'5 hrs'},
    {n:'WordPress Website Design',d:'Build and launch a business website without code',l:'Beginner',k:10,h:'3.5 hrs'},
    {n:'Funnels & Automation',d:'Build sales funnels with email and CRM follow-up',l:'Intermediate',k:14,h:'5 hrs'},
    {n:'Paid Advertising Mastery',d:'Run profitable Meta, Google and TikTok campaigns',l:'Intermediate',k:16,h:'6 hrs'},
    {n:'E-commerce & Affiliate Marketing',d:'Set up and scale a store or affiliate business',l:'Intermediate',k:13,h:'5 hrs'},
    {n:'Digital Marketing Strategy',d:'Combine ads, SEO, funnels and copy into one system',l:'Advanced',k:20,h:'8 hrs'}
  ];
  var S={door:'grow',niche:NICHES[0],budget:300000,goal:'sales',aov:25000,cpm:1500,ctr:1.8,cvr:1.8,course:COURSES[3]};
  var $=function(id){return document.getElementById(id)};
  function naira(n){
    if(n>=1e9)return '₦'+(n/1e9).toFixed(2).replace(/\.?0+$/,'')+'B';
    if(n>=1e6)return '₦'+(n/1e6).toFixed(2).replace(/\.?0+$/,'')+'M';
    return '₦'+Math.round(n).toLocaleString('en-NG');
  }
  function num(n){return Math.round(n).toLocaleString('en-NG')}

  function plan(){
    var views=S.budget/S.cpm*1000, clicks=views*S.ctr/100, res=clicks*S.cvr/100;
    var lo=res*0.7, hi=res*1.3;
    return {views:views,clicks:clicks,res:res,lo:lo,hi:hi,
      revLo:lo*S.aov,revHi:hi*S.aov,cost:res>0?S.budget/res:0,
      roasLo:lo*S.aov/S.budget,roasHi:hi*S.aov/S.budget};
  }

  function setNiche(n){
    S.niche=n;S.cpm=n.cpm;S.ctr=n.ctr;S.cvr=S.goal==='sales'?n.sale:n.lead;S.aov=n.aov;
    $('aCpm').value=S.cpm;$('aCtr').value=S.ctr;$('aCvr').value=S.cvr;$('aov').value=S.aov;
  }

  function buildChips(){
    var box=$('niches');
    NICHES.forEach(function(n){
      var b=document.createElement('button');b.className='chip';b.textContent=n.name;b.setAttribute('aria-pressed',n===S.niche);
      b.onclick=function(){setNiche(n);render()};b._n=n;box.appendChild(b);
    });
    var tr=$('tracks'),rows=$('courseRows');
    COURSES.forEach(function(c){
      var b=document.createElement('button');b.className='track';b.setAttribute('aria-pressed',c===S.course);
      b.innerHTML='<b></b><small></small><em></em>';
      b.children[0].textContent=c.n;b.children[1].textContent=c.d;b.children[2].textContent=c.k+' lessons · '+c.h;
      b.onclick=function(){S.course=c;render()};b._c=c;tr.appendChild(b);
      var r=document.createElement('tr');
      [c.n,c.d,c.l,c.k,c.h].forEach(function(v,i){var td=document.createElement('td');td.textContent=v;if(i>1)td.className='mono';r.appendChild(td)});
      rows.appendChild(r);
    });
  }

  function message(p){
    if(S.door==='learn')
      return 'Hi Demoski. I want to learn, not hire.\n\nProgramme: '+S.course.n+' ('+S.course.l+', '+S.course.k+' lessons)\n\nPlease send me the price, the start date and how to enrol.';
    var out=S.goal==='sales'
      ? 'Planner estimate: '+num(p.lo)+'–'+num(p.hi)+' sales, '+naira(p.revLo)+'–'+naira(p.revHi)+' revenue.'
      : 'Planner estimate: '+num(p.lo)+'–'+num(p.hi)+' leads at about '+naira(p.cost)+' each.';
    return 'Hi Demoski. I used the planner on your site.\n\nMarket: '+S.niche.name+'\nAd budget: '+naira(S.budget)+' a month\nGoal: '+(S.goal==='sales'?'Sales (average order '+naira(S.aov)+')':'Leads')+'\n'+out+'\n\nCan we book the free strategy call?';
  }

  function render(){
    var p=plan(),grow=S.door==='grow';
    $('doorGrow').setAttribute('aria-pressed',grow);$('doorLearn').setAttribute('aria-pressed',!grow);
    $('planner').hidden=!grow;$('school').hidden=grow;
    $('acctName').textContent=grow?S.niche.name+' brand':'Student';
    [].forEach.call($('niches').children,function(b){b.setAttribute('aria-pressed',b._n===S.niche)});
    [].forEach.call($('goals').children,function(b){b.setAttribute('aria-pressed',b.dataset.goal===S.goal)});
    [].forEach.call($('tracks').children,function(b){b.setAttribute('aria-pressed',b._c===S.course)});
    $('budgetVal').textContent=naira(S.budget);
    $('aovField').hidden=S.goal!=='sales';
    $('legendOut').textContent=S.goal==='sales'?'Revenue':'Leads';
    var k=S.goal==='sales'
      ? [['People reached',num(p.views)],['Clicks to your page',num(p.clicks)],['Sales',num(p.lo)+'–'+num(p.hi)],['Cost per sale',naira(p.cost)],
         ['Ad spend',naira(S.budget)],['Revenue',naira(p.revLo)+'–'+naira(p.revHi),1],['Return on ad spend',p.roasLo.toFixed(1)+'×–'+p.roasHi.toFixed(1)+'×',1],['Period','30 days']]
      : [['People reached',num(p.views)],['Clicks to your page',num(p.clicks)],['Leads',num(p.lo)+'–'+num(p.hi),1],['Cost per lead',naira(p.cost),1]];
    var box=$('kpis');box.textContent='';
    k.forEach(function(x){var d=document.createElement('div');d.className='kpi'+(x[2]?' win':'');
      var s=document.createElement('span');s.className='label';s.textContent=x[0];var b=document.createElement('b');b.textContent=x[1];d.appendChild(s);d.appendChild(b);box.appendChild(d)});
    var m=message(p);$('msg').textContent=m;
    var url=WA+encodeURIComponent(m);$('waBtn').href=url;$('barBtn').href=url;
    var sum=$('barSum');sum.textContent='';
    var b=document.createElement('b');
    if(grow){b.textContent=naira(S.budget)+'/mo';sum.appendChild(b);
      sum.appendChild(document.createTextNode(' → '+(S.goal==='sales'?naira(p.revLo)+'–'+naira(p.revHi)+' est. revenue':num(p.lo)+'–'+num(p.hi)+' est. leads')));
      $('barBtn').textContent='Send my plan';}
    else{b.textContent=S.course.n;sum.appendChild(b);$('barBtn').textContent='Ask about this';}
    draw(p,true);
  }

  // chart: cumulative spend (straight) vs result (slow start while the campaign learns)
  var raf=0;
  function curve(t){return t*t*(3-2*t)*0.55+t*0.45}
  function draw(p,animate){
    var c=$('chart');if(!c.getContext)return;
    var w=c.clientWidth,h=c.clientHeight;if(!w)return;
    var dpr=window.devicePixelRatio||1;c.width=w*dpr;c.height=h*dpr;
    var g=c.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);
    var cs=getComputedStyle(document.documentElement),col=function(v){return cs.getPropertyValue(v).trim()};
    var sales=S.goal==='sales',hiV=sales?p.revHi:p.hi,loV=sales?p.revLo:p.lo,midV=sales?p.res*S.aov:p.res;
    var maxY=Math.max(sales?S.budget:0,hiV)*1.08||1;
    var L=58,R=12,T=10,B=26,pw=w-L-R,ph=h-T-B;
    var X=function(d){return L+pw*d/30},Y=function(v){return T+ph*(1-v/maxY)};
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    var start=performance.now();cancelAnimationFrame(raf);
    function frame(now){
      var prog=(!animate||reduce)?1:Math.min(1,(now-start)/700),end=30*prog,d;
      g.clearRect(0,0,w,h);
      g.font='11px JetBrains Mono, monospace';g.textBaseline='middle';
      for(var i=0;i<=4;i++){var v=maxY/1.08*i/4,y=Y(v);
        g.strokeStyle=col('--line');g.lineWidth=1;g.beginPath();g.moveTo(L,y);g.lineTo(w-R,y);g.stroke();
        g.fillStyle=col('--muted');g.textAlign='right';g.fillText(sales?naira(v):num(v),L-8,y);}
      g.textAlign='center';g.textBaseline='alphabetic';
      [1,7,14,21,30].forEach(function(dd){g.fillText('Day '+dd,Math.min(Math.max(X(dd),L+18),w-R-20),h-6)});
      // band
      g.beginPath();for(d=0;d<=end;d+=.5)g.lineTo(X(d),Y(hiV*curve(d/30)));
      for(d=end;d>=0;d-=.5)g.lineTo(X(d),Y(loV*curve(d/30)));
      g.closePath();g.globalAlpha=.16;g.fillStyle=col('--profit');g.fill();g.globalAlpha=1;
      // result line
      g.beginPath();for(d=0;d<=end;d+=.5)g.lineTo(X(d),Y(midV*curve(d/30)));
      g.strokeStyle=col('--profit');g.lineWidth=3;g.stroke();
      g.beginPath();g.arc(X(end),Y(midV*curve(end/30)),4.5,0,7);g.fillStyle=col('--profit');g.fill();
      if(sales){g.beginPath();g.moveTo(X(0),Y(0));g.lineTo(X(end),Y(S.budget*end/30));g.strokeStyle=col('--spend');g.lineWidth=3;g.stroke();
        g.beginPath();g.arc(X(end),Y(S.budget*end/30),4.5,0,7);g.fillStyle=col('--spend');g.fill();}
      if(prog<1)raf=requestAnimationFrame(frame);
    }
    raf=requestAnimationFrame(frame);
  }

  function numIn(id,key,min){$(id).addEventListener('input',function(){var v=parseFloat(this.value);if(v>=min){S[key]=v;render()}})}
  buildChips();setNiche(S.niche);
  $('budget').addEventListener('input',function(){S.budget=+this.value;render()});
  numIn('aov','aov',1);numIn('aCpm','cpm',1);numIn('aCtr','ctr',0.01);numIn('aCvr','cvr',0.01);
  [].forEach.call($('goals').children,function(b){b.onclick=function(){S.goal=b.dataset.goal;S.cvr=S.goal==='sales'?S.niche.sale:S.niche.lead;$('aCvr').value=S.cvr;render()}});
  $('doorGrow').onclick=function(){S.door='grow';render()};
  $('doorLearn').onclick=function(){S.door='learn';render()};
  $('copyBtn').onclick=function(){
    var btn=this,t=$('msg').textContent,done=function(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy message'},1600)};
    var fallback=function(){var r=document.createRange();r.selectNodeContents($('msg'));var s=getSelection();s.removeAllRanges();s.addRange(r);btn.textContent='Selected. Press copy'};
    try{navigator.clipboard.writeText(t).then(done,fallback)}catch(e){fallback()}
  };
  var redraw=function(){draw(plan(),false)};
  window.addEventListener('resize',redraw);
  if(window.matchMedia)matchMedia('(prefers-color-scheme: dark)').addEventListener('change',redraw);
  new MutationObserver(redraw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(redraw);
  render();
})();
