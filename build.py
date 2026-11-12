#!/usr/bin/env python3
"""Builds the Demoski Digital static site into ./dist (no dependencies).
Run: python3 build.py   Edit page content in this file; shared header/footer live in page()."""
import re, os, json, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SITE = "https://demoskidigital.com"
WA = "https://wa.me/2347066153757"
proto = open(os.path.join(ROOT, "home-prototype.html"), encoding="utf-8").read()

base_css = re.search(r"<style>(.*?)</style>", proto, re.S).group(1)
planner_js = re.search(r"<script>(.*?)</script>", proto, re.S).group(1)
home_main = re.search(r"(<main id=\"top\">.*?</main>)", proto, re.S).group(1)

EXTRA_CSS = """
/* ---- subpages ---- */
.top nav a[aria-current="page"]{color:var(--band-ink);border-bottom:2px solid var(--spend)}
.phero .wrap{padding-block:48px 40px}
.phero h1{font-size:clamp(42px,6.6vw,96px);font-weight:800;max-width:16ch;margin-top:14px}
.phero h1 mark{background:var(--mark);color:var(--mark-ink);padding:0 .12em}
.phero .lede{max-width:60ch}
.group{margin-top:44px}
.group h2{font-size:clamp(28px,3.4vw,44px)}
.group>p{color:var(--muted);margin-top:8px;max-width:60ch}
.group .tablewrap{margin-top:18px}
td ul{margin:0;padding-left:18px;color:var(--muted);font-size:14px;display:grid;gap:2px}
td .tag{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;background:var(--mark);color:var(--mark-ink);padding:2px 6px;margin-left:8px;vertical-align:middle;white-space:nowrap}
.pick{background:transparent;border:2px solid var(--ink);padding:8px 12px;font-size:14px;font-weight:600;white-space:nowrap}
.pick[aria-pressed="true"]{background:var(--profit);border-color:var(--profit);color:var(--panel)}
.notes{margin-top:44px;display:grid;gap:10px;padding:20px;border:2px solid var(--ink);background:var(--panel);max-width:900px}
.notes ul{margin:0;padding-left:20px;display:grid;gap:6px;color:var(--muted)}
.grid3{display:grid;gap:0;margin-top:28px;border-top:1px solid var(--line)}
@media(min-width:760px){.grid3{grid-template-columns:repeat(3,minmax(0,1fr))}}
.grid3>div{padding:20px 20px 24px 0;border-bottom:1px solid var(--line)}
.grid3 h3{font-size:24px;margin-bottom:8px}
.grid3 p{color:var(--muted);font-size:15px}
.band .grid3,.band .grid3>div{border-color:var(--band-line)}
.band .grid3 p{color:var(--band-muted)}
.course{border-bottom:1px solid var(--line);padding:18px 0;display:grid;gap:12px}
@media(min-width:860px){.course{grid-template-columns:minmax(0,5fr) minmax(0,5fr) auto;gap:32px;align-items:start}}
.course h3{font-size:28px}
.course .meta{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:8px}
.course p{color:var(--muted);margin-top:8px}
.course ul{margin:0;padding-left:18px;color:var(--muted);display:grid;gap:4px}
.story{display:grid;gap:18px;max-width:68ch;font-size:18px;margin-top:24px}
.story p{color:var(--muted)}
.story strong{color:var(--ink)}
.photo{aspect-ratio:4/5;max-width:100%;border:2px dashed var(--line);display:grid;place-items:center;text-align:center;font-family:var(--mono);font-size:12px;color:var(--muted);padding:16px}
.split{display:grid;gap:32px}
@media(min-width:900px){.split{grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:56px}}
.tools{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px}
.tools span{font-family:var(--mono);font-size:12px;border:1px solid var(--band-line);padding:5px 9px;color:var(--band-muted)}
.cta-line{margin-top:28px}
.more{display:inline-block;margin-top:20px;font-weight:600}
.case{border:2px solid var(--ink);background:var(--panel);padding:18px;display:grid;gap:6px;align-content:start}
.case .big{font-size:clamp(44px,5vw,64px);font-weight:700;line-height:1;color:var(--profit);margin-top:8px}
.case .what{font-family:var(--display);font-weight:700;font-size:20px}
.case dl{margin:10px 0 0;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:14px;border-top:1px solid var(--line);padding-top:12px}
.case dt{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding-top:2px}
.case dd{margin:0}
.src{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:14px}
@media(min-width:800px){.proof.four{grid-template-columns:repeat(2,minmax(0,1fr))}}
.price{font-size:clamp(30px,4vw,52px);font-weight:700;margin-top:24px}
.price span{display:block;font-size:13px;font-weight:400;color:var(--muted);letter-spacing:.04em;margin-top:4px}
tr.total td{border-top:2px solid var(--ink);font-weight:600}
tr.total s{color:var(--muted);font-weight:400;margin-right:8px}
.top nav{gap:8px 16px;font-size:13.5px}
.navmore{position:relative}
.navmore summary{cursor:pointer;color:var(--band-muted);list-style:none}
.navmore summary::-webkit-details-marker{display:none}
.navmore summary::after{content:" ▾"}
.navmore summary:hover,.navmore[open] summary,.navmore summary.on{color:var(--band-ink)}
.navmenu{position:absolute;right:0;top:calc(100% + 12px);z-index:20;background:var(--band);border:1px solid var(--band-line);border-top:3px solid var(--spend);min-width:270px;max-width:calc(100vw - 32px);display:grid;padding:6px 0}
.top nav .navmenu a{padding:9px 16px;color:var(--band-ink);display:grid;gap:1px;border:0}
.top nav .navmenu a:hover,.top nav .navmenu a[aria-current="page"]{background:var(--band-line)}
.navmenu small{font-family:var(--mono);font-size:11px;color:var(--band-muted)}
@media(max-width:1100px){.top{position:relative;top:0}}
@media(max-width:700px){.navmore{position:static}.navmenu{left:16px;right:16px;top:100%;min-width:0}}
.footgrid{display:grid!important;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:24px 32px}
.footgrid>div{display:grid;gap:6px;align-content:start;font-size:14px}
.footgrid .label{margin-bottom:4px}
.offers{display:grid;gap:0;margin-top:28px;border-top:2px solid var(--ink)}
@media(min-width:760px){.offers{grid-template-columns:repeat(2,minmax(0,1fr))}}
.offers a{display:grid;gap:4px;padding:18px 18px 20px 0;border-bottom:1px solid var(--line);text-decoration:none}
.offers a b{font-family:var(--display);font-size:24px;letter-spacing:-.01em}
.offers a span{color:var(--muted);font-size:15px}
.offers a:hover b{color:var(--spend)}
.legal-about{font-size:18px;max-width:60ch;margin-top:12px}
.legal-dl{margin:12px 0 0;display:grid;grid-template-columns:auto 1fr;gap:8px 18px;font-size:16px}
.legal-dl dt{color:var(--muted)}
.legal-dl dd{margin:0;font-weight:600;overflow-wrap:anywhere}
.legal-foot{display:grid!important;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px 32px}
.legal-foot p{margin-top:6px;max-width:70ch}
footer .wrap{display:flex;gap:10px 24px;flex-wrap:wrap;justify-content:space-between}
footer a{text-decoration:none}
footer a:hover{text-decoration:underline}
"""

SITE_JS = r"""
(function(){
  var WA='https://wa.me/2347066153757?text=',b=document.querySelector('[data-msg]')||document.body,picks=[];
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
      var max=+(b.dataset.max||0);
      if(on&&max&&picks.length>=max){var note=document.getElementById('maxNote');if(note)note.hidden=false;return}
      if(on)picks.push(n);else picks=picks.filter(function(p){return p!==n});
      var mn=document.getElementById('maxNote');if(mn)mn.hidden=true;
      btn.setAttribute('aria-pressed',on);btn.textContent=on?btn.dataset.on:btn.dataset.off;
      upd();
    });
  });
  upd();
})();
"""

NAV = [("/", "Planner"), ("/packages/", "Packages"), ("/done-for-you/", "Done-For-You"), ("/training/", "Training"), ("/autobuild-funnel/", "AutoBuild"), ("/ai-funnel-generator/", "AI Funnel"), ("/affiliate/", "Affiliates"), ("/portfolio/", "Proof")]
WP = "https://demoskidigital.com"  # pages still served by WordPress; change to the subdomain at launch
OFFERS = [("/done-for-you/", "Done-For-You Setup", "Your whole system built in 14 days"),
        ("/autobuild-funnel/", "AutoBuild", "Funnel-building course"),
        ("/ai-funnel-generator/", "AI Funnel Accelerator", "AI funnels with WhatsApp follow-up"),
        ("/affiliate/", "Affiliates", "Earn 20% per referral"),
        (WP + "/template-bundle-customizer/", "Template Bundle", "54 ready-made business templates"),
        (WP + "/course-os/", "Course OS", "Course platform for creators")]
MORE = [("/about/", "About", "Who runs your account"), ("/contact/", "Contact Us", "Phone, WhatsApp and email")] + [o for o in OFFERS if o[1] in ("Template Bundle", "Course OS")]
LEGAL_NAME = "Demoski Designs and Geospatial Consult"
LEGAL_PHONE = "+2347066153757"
LEGAL_ABOUT = "Demoski Digital is the operating brand of Demoski Designs and Geospatial Consult, a registered Nigerian business providing professional geospatial, surveying, mapping, digital design and related consultancy services."
LEGAL_DL = f"""<dl class="legal-dl"><dt>Legal Business Name</dt><dd>{LEGAL_NAME}</dd><dt>Trading/Brand Name</dt><dd>Demoski Digital</dd><dt>Phone</dt><dd><a href="tel:{LEGAL_PHONE}">{LEGAL_PHONE}</a></dd><dt>Email</dt><dd><a href="mailto:hello@demoskidigital.com">hello@demoskidigital.com</a></dd><dt>Website</dt><dd>demoskidigital.com</dd></dl>"""
LEGAL_SECTION = f"""<section class="sec" id="business"><div class="wrap">
  <div class="split">
    <div><p class="label">About the Business</p><p class="legal-about">{LEGAL_ABOUT}</p></div>
    <div><p class="label">Business Contact Information</p>{LEGAL_DL}</div>
  </div>
</div></section>"""
LD = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Demoski Digital", "legalName": LEGAL_NAME,
                 "url": SITE, "telephone": LEGAL_PHONE, "email": "hello@demoskidigital.com", "address": {"@type": "PostalAddress", "addressCountry": "NG"}})
FOOT = [("Agency", [("/", "Campaign planner"), ("/packages/", "Packages"), ("/done-for-you/", "Done-For-You Setup"), ("/portfolio/", "Proof"), ("/about/", "About"), ("/contact/", "Contact")]),
        ("Learn", [("/training/", "Training"), ("/autobuild-funnel/", "AutoBuild"), ("/ai-funnel-generator/", "AI Funnel Accelerator")]),
        ("Products", [(WP + "/template-bundle-customizer/", "Template Bundle"), (WP + "/course-os/", "Course OS"), ("/affiliate/", "Affiliates")])]
FAVICON = "data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2310131C'/%3E%3Ctext x='5' y='24' font-family='Arial' font-weight='900' font-size='22' fill='%23ECEEF2'%3ED%3C/text%3E%3Ccircle cx='25' cy='22' r='3' fill='%23F0431A'/%3E%3C/svg%3E"

def e(s): return html.escape(s, quote=True)

def page(path, title, desc, acct, main, body_attrs="", script="site.js", noindex=False):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == path else "", t) for h, t in NAV)
    more = "".join('<a href="%s"%s>%s<small>%s</small></a>' % (h, ' aria-current="page"' if h == path else "", t, d) for h, t, d in MORE)
    nav += '<details class="navmore"><summary%s>More</summary><div class="navmenu">%s</div></details>' % (' class="on"' if any(h == path for h, _, _ in MORE) else "", more)
    foot = "".join('<div><p class="label">%s</p>%s</div>' % (g, "".join('<a href="%s">%s</a>' % (h, t) for h, t in links)) for g, links in FOOT)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Demoski Digital Agency">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<script type="application/ld+json">{LD}</script>
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body {body_attrs}>
<header class="top"><div class="wrap">
  <a class="brand" href="/">Demoski<i>.</i></a>
  <span class="acct"><span class="dot"></span><span>{'Account preview: ' if path == '/' else ''}<span id="acctName">{e(acct)}</span></span></span>
  <nav aria-label="Main">{nav}</nav>
</div></header>
{main}
<footer><div class="wrap footgrid">
  {foot}
  <div><p class="label">Contact</p><span>WhatsApp +234 706 615 3757</span><a href="mailto:hello@demoskidigital.com">hello@demoskidigital.com</a><span>Nigeria and worldwide</span></div>
</div>
<div class="wrap legal-foot">
  <div><p class="label">About the Business</p><p>{LEGAL_ABOUT}</p></div>
  <div><p class="label">Business Contact Information</p><p>Legal Business Name: {LEGAL_NAME}<br>Trading/Brand Name: Demoski Digital<br>Phone: {LEGAL_PHONE}</p></div>
</div>
<div class="wrap" style="border-top:0;padding-top:0"><span>© 2026 {LEGAL_NAME}, trading as Demoski Digital</span>
</div></footer>
<div class="bar" role="region" aria-label="Contact"><span class="sum" id="barSum"></span><a class="btn" id="barBtn" data-wa="" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
<script src="/assets/{script}" defer></script>
</body>
</html>
"""
    out = os.path.join(DIST, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)

def attrs(msg, bar, pickmsg="", pickend="", barcta="Send my plan", single=False, maxn=0):
    return 'data-msg="%s" data-bar="%s" data-pickmsg="%s" data-pickend="%s" data-barcta="%s"%s%s' % (
        e(msg), e(bar), e(pickmsg), e(pickend), e(barcta), ' data-single="1"' if single else "", ' data-max="%d"' % maxn if maxn else "")

# ---------------------------------------------------------------- PACKAGES
GROUPS = [
 ("Brand", "A brand that looks worth the price you charge.", "5–10 working days", [
   ("Basic Branding", "", ["Logo (2 concepts, 3 revisions)", "Colour palette and typography", "Business card", "PNG, SVG and PDF files"]),
   ("Standard Branding", "Most chosen", ["Everything in Basic", "5 social media templates", "Letterhead and email signature", "Brand pattern", "Source files (AI, PSD)", "Unlimited minor revisions"]),
   ("Premium Branding", "", ["Everything in Standard", "Brand guidelines document", "Full stationery set", "Social profile kit", "Icon and favicon", "Pitch deck template"])]),
 ("Website", "Fast, mobile-first WordPress sites built to turn visitors into customers.", "2–4 weeks", [
   ("Starter Website", "", ["Up to 5 pages", "Contact form and WhatsApp button", "Basic on-page SEO", "Google Analytics", "1 month support"]),
   ("Business Website", "Best value", ["Up to 10 pages", "Blog setup", "Full on-page SEO", "Speed optimisation", "Email capture", "WhatsApp and live chat", "3 months support"]),
   ("E-commerce Website", "", ["WooCommerce store", "Payment gateway", "Product, inventory and order management", "Mobile checkout", "Abandoned cart recovery", "Product SEO", "3 months support"])]),
 ("Funnel", "Pages and follow-up sequences that turn cold traffic into buyers.", "1–3 weeks", [
   ("Single Sales Page", "", ["Sales page design and copy", "Lead capture or checkout", "Analytics and heatmap", "Ready for A/B testing"]),
   ("Full Sales Funnel", "Most effective", ["Landing and thank-you pages", "Upsell and downsell pages", "Email capture and CRM", "5-email automated sequence", "All copywriting", "Conversion tracking", "WhatsApp follow-up"]),
   ("Lead Gen Funnel", "", ["Opt-in page design and copy", "Lead magnet setup", "3-email welcome sequence", "CRM or Mailchimp connection", "WhatsApp follow-up", "Analytics dashboard"])]),
 ("Ads", "Meta, Google and TikTok campaigns managed against revenue.", "3–5 working days to launch", [
   ("Ads Setup", "", ["Campaign structure", "Audience research", "Creative for 3 ad sets", "Pixel and conversion tracking", "Launch report"]),
   ("Monthly Management", "Most chosen", ["Daily monitoring", "A/B testing of ads and audiences", "New creative every month", "Budget reallocation and scaling", "Retargeting", "Monthly report and call"]),
   ("Full Service Ads", "", ["Strategy, setup and management", "Meta, Google and TikTok together", "Retargeting and lookalikes", "Landing page optimisation", "Weekly reports and strategy calls"])]),
 ("Growth system", "Brand, site, funnel and ads combined into one engagement.", "3–6 weeks to set up, then monthly", [
   ("Starter Growth", "", ["Logo and brand style guide", "5-page WordPress site", "Basic SEO", "Ads account setup on 1 platform", "30 days support"]),
   ("Sales & Lead Gen", "Most chosen", ["Everything in Starter Growth", "Sales funnel", "Meta and Google ads management", "Email automation", "Monthly reports", "Dedicated account manager"]),
   ("E-commerce Scaling", "", ["Full WooCommerce build", "Ads on Meta, Google and TikTok", "Retargeting", "Abandoned cart automation", "Conversion and speed optimisation", "Weekly reports and calls"]),
   ("Monthly Retainer", "", ["Ongoing ads management", "Website maintenance", "Monthly content", "Social media management", "Strategy review every two weeks", "Priority support within 24 hours"])]),
]
g_html = ""
for name, blurb, delivery, items in GROUPS:
    rows = ""
    for n, tag, inc in items:
        rows += '<tr><td>%s%s</td><td><ul>%s</ul></td><td class="mono">Quoted on call</td><td><button class="pick" aria-pressed="false" data-name="%s" data-on="Added ✓" data-off="Add to plan">Add to plan</button></td></tr>' % (
            e(n), '<span class="tag">%s</span>' % e(tag) if tag else "", "".join("<li>%s</li>" % e(i) for i in inc), e(n))
    g_html += f"""<div class="group" id="{e(name.lower().replace(' ', '-'))}">
    <p class="label">Layer · delivery {e(delivery)}</p><h2 style="margin-top:8px">{e(name)}</h2><p>{e(blurb)}</p>
    <div class="tablewrap"><table><thead><tr><th>Package</th><th>Includes</th><th>Price</th><th>Your plan</th></tr></thead><tbody>{rows}</tbody></table></div></div>"""

packages = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">Packages</p>
  <h1>Take one layer. Or the <mark>whole</mark> system.</h1>
  <p class="lede">Add what you need to your plan. The bar at the bottom keeps count and sends the list to us on WhatsApp, so the strategy call starts with a real scope.</p>
</div></div>
<section class="sec"><div class="wrap" style="padding-top:8px">
  {g_html}
  <div class="notes" style="margin-bottom:-20px"><p class="label">Want all of it at once?</p><p>The Done-For-You setup builds your website, tracking, email automation and ads in 14 days for one price. <a href="/done-for-you/"><strong>See the Done-For-You setup →</strong></a></p></div>
  <div class="notes"><p class="label">Good to know</p><ul>
    <li>Every package is quoted to your scope after a free 30-minute strategy call. You get a written quote before any work starts.</li>
    <li>Ad spend is separate. You pay Meta, Google or TikTok directly. We recommend at least ₦100,000 a month.</li>
    <li>You can mix packages across layers.</li>
    <li>Larger projects can be paid 50% up front and 50% on delivery, or monthly.</li>
  </ul></div>
</div></section>
</main>"""

# ---------------------------------------------------------------- TRAINING
COURSES = [
 ("Graphic Design & Branding", "Beginner", 12, "5 hrs", "Design logos, brand kits and social graphics that make a business look established.", ["Adobe Photoshop and Illustrator", "Brand identity design", "Social media graphics", "Logo design fundamentals"]),
 ("WordPress Website Design", "Beginner", 10, "3.5 hrs", "Build and launch a professional business website without writing code.", ["WordPress setup and hosting", "Theme customisation", "Page building with Elementor", "Website optimisation"]),
 ("Funnels & Automation", "Intermediate", 14, "5 hrs", "Build sales funnels and automate the follow-up so leads keep moving.", ["Funnel strategy and design", "Email automation", "CRM setup", "Lead nurturing sequences"]),
 ("Paid Advertising Mastery", "Intermediate", 16, "6 hrs", "Run profitable campaigns on Meta, Google and TikTok.", ["Meta Ads", "Google Ads fundamentals", "TikTok advertising", "Campaign optimisation"]),
 ("E-commerce & Affiliate Marketing", "Intermediate", 13, "5 hrs", "Set up and grow an online store or an affiliate business.", ["WooCommerce setup", "Product sourcing", "Affiliate programme setup", "Sales optimisation"]),
 ("Digital Marketing Strategy", "Advanced", 20, "8 hrs", "Combine ads, SEO, funnels and automation into one revenue system.", ["Full-stack growth strategy", "SEO and organic growth", "Social media content system", "Persuasive copywriting"]),
]
c_html = ""
for n, lvl, k, h, d, items in COURSES:
    c_html += f"""<div class="course"><div><h3>{e(n)}</h3><p class="meta">{e(lvl)} · {k} lessons · {e(h)}</p><p>{e(d)}</p></div>
    <ul>{''.join('<li>%s</li>' % e(i) for i in items)}</ul>
    <button class="pick" aria-pressed="false" data-name="{e(n)}" data-on="Selected ✓" data-off="Choose this">Choose this</button></div>"""

training = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">Training</p>
  <h1>Learn the skill from people who <mark>use it</mark> daily.</h1>
  <p class="lede">Six programmes, from first logo to full growth strategy. Choose one and ask us for the price and start date on WhatsApp.</p>
</div></div>
<section class="sec"><div class="wrap">
  <p class="label">Open for enrolment now</p>
  <div class="grid3" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
    <div><h3>AutoBuild</h3><p>Build and automate a full sales funnel on free hosting. Four self-paced modules. ₦25,000.</p><a class="more" href="/autobuild-funnel/">See AutoBuild →</a></div>
    <div><h3>AI Funnel Accelerator</h3><p>AI-built funnels wired to WhatsApp, with a live workshop and a 14-day refund guarantee. ₦25,000.</p><a class="more" href="/ai-funnel-generator/">See the Accelerator →</a></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <p class="label">Programmes</p>
  <div style="margin-top:12px;border-top:1px solid var(--line)">{c_html}</div>
</div></section>
<section class="sec band"><div class="wrap">
  <p class="label">How it works</p>
  <h2 style="margin-top:10px">Built for people who need to earn from it.</h2>
  <div class="grid3">
    <div><h3>Video lessons</h3><p>Step-by-step screen recordings you can replay on any device.</p></div>
    <div><h3>Lifetime access</h3><p>Pay once. Updates to the course are included.</p></div>
    <div><h3>Certificate</h3><p>One for every course you finish, ready for LinkedIn or a portfolio.</p></div>
    <div><h3>Community</h3><p>A private student group for feedback and accountability.</p></div>
    <div><h3>Live Q&amp;A</h3><p>A monthly call with the Demoski team to get your questions answered.</p></div>
    <div><h3>Team workshops</h3><p>Private training and one-to-one coaching for businesses. <a data-wa="Hi Demoski. I want a private training workshop for my team. Can we talk about what you offer?" target="_blank" rel="noopener">Ask about a workshop →</a></p></div>
  </div>
</div></section>
</main>"""

# ---------------------------------------------------------------- PROOF
CASES = [
 ("Games tables", "Snooker and table tennis tables. Sales campaign, orders taken on WhatsApp", "383", "buyer conversations on WhatsApp", "₦486", "per conversation", "₦186,146", "148,931", "4 campaigns"),
 ("4-in-1 product, e-commerce brand", "Sales campaign, orders taken on WhatsApp", "479", "buyer conversations on WhatsApp", "₦395", "per conversation", "₦188,971", "139,268", "5 campaigns"),
 ("Home treadmills", "Sales campaign, orders taken on WhatsApp", "311", "buyer conversations on WhatsApp", "₦878", "per conversation", "₦273,135", "150,366", "9 campaigns"),
 ("Consulting firm", "Instant lead forms", "23", "form leads", "₦1,663", "per lead", "₦38,242", "5,032", "2 campaigns"),
]
def case(c):
    return f'''<div class="case"><p class="label">{e(c[0])} · {e(c[8])}</p><p class="big mono">{e(c[2])}</p><p class="what">{e(c[3])}</p>
    <dl><dt>Cost</dt><dd class="mono">{e(c[4])} {e(c[5])}</dd><dt>Spend</dt><dd class="mono">{e(c[6])}</dd><dt>Views</dt><dd class="mono">{e(c[7])}</dd><dt>How</dt><dd>{e(c[1])}</dd></dl></div>'''
slots = "".join(case(c) for c in CASES)
SOURCE = "Source: Meta Ads Manager, lifetime totals read on 12 November 2026. Client names withheld."
portfolio = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">Proof</p>
  <h1>Real accounts. <mark>Real</mark> numbers.</h1>
  <p class="lede">Every figure here comes straight from Meta Ads Manager: what was spent and what came back. Small budgets, counted exactly.</p>
</div></div>
<section class="sec"><div class="wrap">
  <p class="label">Cases</p>
  <div class="proof four">{slots}</div>
  <p class="src">{SOURCE}</p>
</div></section>
<section class="sec band"><div class="wrap">
  <p class="label">How we report</p>
  <h2 style="margin-top:10px">The numbers you will see on your own account.</h2>
  <div class="grid3">
    <div><h3>Spend</h3><p>Exactly what went to the ad platforms, taken from the platform itself.</p></div>
    <div><h3>Cost per result</h3><p>What one lead or one sale cost you, by campaign and by ad.</p></div>
    <div><h3>Return on ad spend</h3><p>Revenue tracked back to ads, divided by spend. The number that decides whether to scale.</p></div>
  </div>
</div></section>
</main>"""

# ---------------------------------------------------------------- ABOUT
about = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">About</p>
  <h1>We don't run ads. We build <mark>revenue systems.</mark></h1>
</div></div>
<section class="sec"><div class="wrap">
  <div class="split">
    <div>
      <p class="label">Why Demoski exists</p>
      <div class="story">
        <p>Most businesses do not have a traffic problem. They have a <strong>conversion problem</strong>, and they are paying an agency to ignore it.</p>
        <p>We work with e-commerce brands, small and medium businesses and founders who are done experimenting and want a system that brings in <strong>consistent, predictable revenue</strong>. Every engagement starts with strategy, not ad spend.</p>
        <p>From the first ad creative to the landing page, the offer, the funnel and the follow-up, we own the whole chain. A great ad sending traffic to a weak page is a fast way to burn budget.</p>
        <p>If you want pretty reports, we are not the right fit. If you want <strong>leads, sales and a return you can measure</strong>, talk to us.</p>
      </div>
    </div>
    <div>
      <div class="photo">Founder photo<br>to be added</div>
      <h2 style="font-size:30px;margin-top:16px">Ademola Adeniran</h2>
      <p style="color:var(--muted);margin-top:6px">Founder, performance marketer and media buyer. Six years running Meta and Google campaigns, each one built backwards from the revenue target.</p>
      <div class="niches" style="margin-top:14px"><span>Health &amp; beauty</span><span>Gadgets &amp; tech</span><span>Security</span><span>FMCG</span><span>Real estate</span><span>Education</span><span>Food</span><span>Affiliate</span></div>
    </div>
  </div>
</div></section>
<section class="sec band"><div class="wrap">
  <p class="label">How we work</p>
  <h2 style="margin-top:10px">Six rules we hold ourselves to.</h2>
  <div class="grid3">
    <div><h3>Data before decisions</h3><p>Targeting, creative and budget choices come from pixel data and audience insight.</p></div>
    <div><h3>Full-funnel ownership</h3><p>Ads, pages, copy and follow-up are aligned to one outcome: your revenue.</p></div>
    <div><h3>Conversion first</h3><p>Traffic that does not convert is noise. We work on every step between click and sale.</p></div>
    <div><h3>Built to scale</h3><p>A campaign that works at ₦20,000 a month should still work at ₦200,000.</p></div>
    <div><h3>You see everything</h3><p>Every number, every report and the reason behind each decision. No hidden fees.</p></div>
    <div><h3>Speed</h3><p>We reply within one hour in business hours and we keep to deadlines.</p></div>
  </div>
  <p class="label" style="margin-top:36px">Tools we use every day</p>
  <div class="tools"><span>Meta Ads Manager</span><span>Google Ads</span><span>TikTok Ads</span><span>Meta Pixel &amp; Events Manager</span><span>Google Analytics</span><span>Google Tag Manager</span><span>Hotjar</span><span>WordPress</span><span>Elementor</span><span>Thrive Architect</span><span>Mailchimp</span></div>
</div></section>
{LEGAL_SECTION}
<section class="sec"><div class="wrap">
  <h2>Want to see what your budget could do?</h2>
  <div class="btnrow cta-line"><a class="btn" href="/">Open the planner</a><a class="btn ghost" data-wa="" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
</div></section>
</main>"""

# ---------------------------------------------------------------- HOME
home = home_main.replace('href="#build"', 'href="#build"')
offers = "".join('<a href="%s"><b>%s →</b><span>%s</span></a>' % (h, t, d) for h, t, d in OFFERS)
home = home.replace('</main>', LEGAL_SECTION + '\n</main>')
home = home.replace('<section class="sec" id="faq">', '<section class="sec" id="more"><div class="wrap"><p class="label">Everything else we run</p><h2 style="margin-top:10px">More from Demoski.</h2><div class="offers">' + offers + '</div></div></section>\n\n<section class="sec" id="faq">')
home = home.replace(
    '<tbody id="courseRows"></tbody>\n  </table></div>',
    '<tbody id="courseRows"></tbody>\n  </table></div>\n  <a class="more" href="/training/">See every curriculum →</a>')
home = home.replace(
    '</table></div>\n</div></section>\n\n<section class="sec band" id="days">',
    '</table></div>\n  <a class="more" href="/packages/">See every package and build your plan →</a>\n</div></section>\n\n<section class="sec band" id="days">')
home = re.sub(r'<div class="proof">.*?</div>\n</div></section>\n\n<section class="sec" id="founder">',
    lambda m: '<div class="proof">' + "".join(case(c) for c in CASES[:3]) + '</div>\n  <p class="src">' + SOURCE + '</p>\n</div></section>\n\n<section class="sec" id="founder">', home, flags=re.S)
home = home.replace('Real accounts. Unedited screenshots.', 'Real accounts. Real numbers.').replace(
    'Each case below shows the Ads Manager screenshot next to what was spent and what came back.', 'Figures straight from Meta Ads Manager: what was spent and what came back.')
home = home.replace(
    '<div class="proof">', '<a class="more" href="/portfolio/" style="margin-top:14px">How we report results →</a>\n  <div class="proof">')

# ---------------------------------------------------------------- DONE FOR YOU
DFY_ITEMS = [
 ("Website", "Complete WordPress site built in Elementor, with the copy written for you", "₦1,500,000"),
 ("Tracking", "Google Tag Manager and Google Analytics, installed and tested", "₦750,000"),
 ("Email automation", "Nurture, abandoned cart and buyer follow-up sequences, copy included", "₦1,500,000"),
 ("Paid ads", "Campaigns set up on up to 3 platforms of your choice", "₦2,400,000"),
]
DFY_FAQ = [
 ("How long does it take?", "Typically 14 days from the day we receive your brief."),
 ("How much of my time do you need?", "One brief at the start. After that we only come back to you if something needs clarifying."),
 ("Do I need hosting or an existing website?", "No. Neither is required."),
 ("Can I use my existing ad accounts and tools?", "Yes. We build inside what you already have where it makes sense."),
 ("Which ad platforms do you support?", "Meta, Google, TikTok, Microsoft and LinkedIn, among others. You choose up to three."),
 ("Who owns what you build?", "You do. The site, the accounts, the automations and all access are yours."),
 ("Is the copywriting included?", "Yes, for the website and the email sequences."),
 ("Can I edit things after launch?", "Yes. You get instructions for managing everything yourself."),
 ("What support do I get after handover?", "We answer questions and make reasonable adjustments."),
 ("Are there extra costs?", "Nothing beyond the quoted price. Your ad spend is separate and goes to the platforms."),
 ("What about revisions and refunds?", "Reasonable revisions are included. Refunds are available only within 24 hours of purchase and before work begins; after that, sales are final. The Terms and Conditions govern the details."),
]
PLATFORMS = ["Meta (Facebook and Instagram)", "Google", "TikTok", "Microsoft", "LinkedIn"]
dfy_rows = "".join('<tr><td>%s</td><td>%s</td><td class="mono">%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in DFY_ITEMS)
dfy_faq = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", e(q), e(a)) for i, (q, a) in enumerate(DFY_FAQ))
dfy_picks = "".join('<button class="pick" aria-pressed="false" data-name="%s" data-on="%s ✓" data-off="%s">%s</button>' % (e(p), e(p), e(p), e(p)) for p in PLATFORMS)
dfy = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">Done-for-you setup</p>
  <h1>Your whole marketing system, built in <mark>14 days.</mark></h1>
  <p class="lede">Website, tracking, email automation and ad campaigns. You send one brief. We build it, test it and hand you the keys.</p>
  <p class="price mono">₦2,400,000 <span>one payment · everything below</span></p>
</div></div>
<section class="sec"><div class="wrap">
  <p class="label">What gets built</p>
  <h2 style="margin-top:10px">Four layers, one invoice.</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>Layer</th><th>What you get</th><th>Listed separately</th></tr></thead>
    <tbody>{dfy_rows}
    <tr class="total"><td>All four</td><td>Delivered in 14 days with handover training and full ownership</td><td class="mono"><s>₦6,150,000</s> ₦2,400,000</td></tr></tbody>
  </table></div>
</div></section>
<section class="sec band"><div class="wrap">
  <p class="label">The 14 days</p>
  <h2 style="margin-top:10px">One brief. Very few calls.</h2>
  <ol class="timeline" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
    <li><span class="day">Day 0</span><h3>You send the brief</h3><p>A short questionnaire about your business and goals.</p></li>
    <li><span class="day">Day 1</span><h3>We confirm</h3><p>We review it and follow up only if something needs clarifying.</p></li>
    <li><span class="day">Days 2–14</span><h3>We build</h3><p>Site, tracking, email and campaigns are built and tested.</p></li>
    <li><span class="day">Day 14</span><h3>You take over</h3><p>Handover with instructions so you can run it yourself.</p></li>
  </ol>
</div></section>
<section class="sec" id="brief"><div class="wrap">
  <p class="label">Start your brief</p>
  <h2 style="margin-top:10px">Pick your ad platforms.</h2>
  <p class="intro">Choose up to three. The bar at the bottom sends your choices to us on WhatsApp and we reply with the questionnaire.</p>
  <div class="btnrow">{dfy_picks}</div>
  <p class="src" id="maxNote" hidden>Three is the limit. Remove one to add another.</p>
</div></section>
<section class="sec"><div class="wrap">
  <p class="label">Before you ask</p>
  <h2 style="margin-top:10px">Straight answers.</h2>
  <div class="faq">{dfy_faq}</div>
</div></section>
</main>"""

# ---------------------------------------------------------------- COURSE SALES PAGES
def course_page(label, h1, lede, price, price_note, mod_label, mods, extras_label, extras, who, faq, closing):
    mod_html = "".join('<div class="course"><div><p class="meta">%s</p><h3 style="margin-top:6px">%s</h3></div><ul style="grid-column:span 2">%s</ul></div>' % (
        e(tag), e(name), "".join("<li>%s</li>" % e(i) for i in items)) for tag, name, items in mods)
    ex_html = "".join("<div><h3>%s</h3><p>%s</p></div>" % (e(a), e(b)) for a, b in extras)
    who_html = "".join("<span>%s</span>" % e(w) for w in who)
    faq_html = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", e(q), e(a)) for i, (q, a) in enumerate(faq))
    return f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">{e(label)}</p>
  <h1>{h1}</h1>
  <p class="lede">{e(lede)}</p>
  <p class="price mono">{e(price)} <span>{e(price_note)}</span></p>
  <div class="btnrow"><a class="btn" data-wa="" target="_blank" rel="noopener">Enrol on WhatsApp</a></div>
</div></div>
<section class="sec"><div class="wrap">
  <p class="label">{e(mod_label)}</p>
  <div style="margin-top:12px;border-top:1px solid var(--line)">{mod_html}</div>
</div></section>
<section class="sec band"><div class="wrap">
  <p class="label">{e(extras_label)}</p>
  <div class="grid3">{ex_html}</div>
</div></section>
<section class="sec"><div class="wrap">
  <p class="label">Who it is for</p>
  <div class="niches" style="margin-top:14px">{who_html}</div>
  <h2 style="margin-top:44px">Straight answers.</h2>
  <div class="faq">{faq_html}</div>
  <p class="intro" style="margin-top:28px">{e(closing)}</p>
</div></section>
</main>"""

autobuild = course_page(
  "Course · AutoBuild", "Build a full funnel in <mark>30 minutes.</mark> Pay for no tools.",
  "Four self-paced modules that take you from free hosting to a live, automated sales funnel. No WordPress, no coding.",
  "₦25,000", "current price · listed full price ₦50,000 · one payment",
  "The four modules", [
   ("Module 01", "Free hosting and free domain", ["Choosing the free hosting platform", "Step-by-step setup", "Connecting a free domain", "Putting your pages live"]),
   ("Module 02", "The complete funnel build", ["A landing page built without templates or drag-and-drop", "Payments with Paystack, Flutterwave, PayPal or another processor", "Thank-you page and lead capture flow", "Where calls to action go and why"]),
   ("Module 03", "Automation", ["Your own automation server with n8n", "Databases for leads and customers", "Chatbots that answer from your own knowledge base", "AI assistants that qualify leads and reply", "Follow-up by email, live chat, WhatsApp, Instagram and Telegram", "Simple dashboards for leads and sales"]),
   ("Module 04", "The speed framework", ["A funnel in under 30 minutes", "Duplicating and customising quickly", "Six steps: imagine, describe, generate, customise, deploy, automate"]),
  ],
  "Included with the course", [
   ("Client acquisition system", "How to position this skill as a premium service, find business owners and close them."),
   ("Private community", "Feedback on your pages, shared opportunities and ongoing updates."),
   ("Direct support", "Ask questions, get unstuck and get feedback on what you build."),
  ],
  ["Ads professionals who never learned funnels", "Business owners who want better sales pages", "Marketers and designers", "Beginners with no coding experience"],
  [("Can beginners join?", "Yes. It starts from zero and follows the order of a real project."),
   ("Do I need to code?", "No. Every step is shown."),
   ("Do I need WordPress?", "No. AutoBuild uses a lighter approach that replaces WordPress and plugin stacks."),
   ("Can I really use free hosting?", "Yes. Module 01 covers the free tiers and how to set them up."),
   ("Does it cover automation?", "Yes. Module 03 covers n8n, databases, messaging channels and AI agents."),
   ("How long is it?", "Four self-paced modules. You set the pace.")],
  "To enrol, send the WhatsApp message from the bar below. We reply with payment details and your access.")

aifunnel = course_page(
  "Course · AI Funnel Accelerator", "AI-powered funnels that bring leads <mark>on autopilot.</mark>",
  "A system for building sales funnels with AI, wiring them to WhatsApp, and publishing them anywhere. Full refund within 14 days if you do not see the value.",
  "₦25,000", "one payment · 14-day refund guarantee",
  "What you get", [
   ("Part 1", "AI Funnel Blueprint", ["Building modern funnels from scratch with AI-assisted workflows"]),
   ("Part 2", "AI Automation Playbook", ["Connecting funnels to AI workflows that run and reply around the clock"]),
   ("Part 3", "WhatsApp Lead Engine", ["Capturing, qualifying and following up with prospects on WhatsApp"]),
   ("Part 4", "One-Click Deployment System", ["Publishing to WordPress, Netlify, Vercel or Systeme.io"]),
   ("Part 5", "Prompt Library", ["Prompts for funnels, marketing and automation, added to over time"]),
  ],
  "How it runs", [
   ("Instant access", "Modules, templates and workflows open as soon as you enrol."),
   ("Live funnel workshop", "A live session where a complete automated funnel is built from start to finish. Ask us for the next date."),
   ("The guarantee", "Complete the training, use the templates, follow the system. If you do not see the value, tell us within 14 days of enrolling for a full refund."),
  ],
  ["Business owners", "Coaches", "Freelancers", "Agencies", "Digital marketers", "Course creators", "Virtual assistants"],
  [("How do I enrol?", "Send the WhatsApp message from the bar below. We reply with payment details and your access."),
   ("Is it live or recorded?", "The modules are available on demand. The funnel workshop is live."),
   ("What if it is not for me?", "Ask for a full refund within 14 days of enrolling.")],
  "Questions before you enrol? Ask on WhatsApp and a person answers.")

affiliate = """<main>
<div class="phero"><div class="wrap">
  <p class="label">Affiliate programme</p>
  <h1>Refer a business. Earn <mark>20%.</mark></h1>
  <p class="lede">You know business owners who need marketing help. Send them to us and earn a commission on their first package or training enrolment.</p>
  <div class="btnrow"><a class="btn" data-wa="" target="_blank" rel="noopener">Apply on WhatsApp</a></div>
</div></div>
<section class="sec band"><div class="wrap">
  <p class="label">How it works</p>
  <ol class="timeline" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
    <li><span class="day">Step 1</span><h3>Apply</h3><p>Send a short application on WhatsApp.</p></li>
    <li><span class="day">Step 2</span><h3>Share your link</h3><p>You get a unique referral link to share with your network.</p></li>
    <li><span class="day">Step 3</span><h3>Get paid</h3><p>When someone you referred buys, you earn 20% of that first purchase.</p></li>
  </ol>
</div></section>
<section class="sec"><div class="wrap">
  <p class="label">What 20% looks like</p>
  <div class="tablewrap"><table>
    <thead><tr><th>They buy</th><th>Price</th><th>You earn</th></tr></thead>
    <tbody>
      <tr><td>AutoBuild course</td><td class="mono">₦25,000</td><td class="mono">₦5,000</td></tr>
      <tr><td>AI Funnel Accelerator</td><td class="mono">₦25,000</td><td class="mono">₦5,000</td></tr>
      <tr><td>A service package</td><td class="mono">Quoted per client</td><td class="mono">20% of the quote</td></tr>
    </tbody>
  </table></div>
  <p class="src">Commission applies to a referred client's first package or training enrolment. All terms are subject to the Demoski Digital affiliate agreement, which you receive when you apply.</p>
</div></section>
</main>"""

# ---------------------------------------------------------------- WRITE
if os.path.exists(DIST): shutil.rmtree(DIST)
os.makedirs(os.path.join(DIST, "assets"))
open(os.path.join(DIST, "assets", "site.css"), "w", encoding="utf-8").write(base_css + EXTRA_CSS)
open(os.path.join(DIST, "assets", "planner.js"), "w", encoding="utf-8").write(planner_js)
open(os.path.join(DIST, "assets", "site.js"), "w", encoding="utf-8").write(SITE_JS)

page("/", "Demoski Digital Agency | See your ad account before you pay for it",
     "Plan a 30-day ad campaign with your own budget, see the maths, and send the plan to Demoski Digital on WhatsApp. Performance marketing, websites, funnels and training from Lagos.",
     "Your business", home, script="planner.js")
page("/packages/", "Packages | Demoski Digital Agency",
     "Branding, WordPress websites, sales funnels, paid ads and complete growth systems. Build your plan and get a written quote after a free strategy call.",
     "Packages", packages,
     attrs("Hi Demoski. I am looking at your packages and would like to book the free strategy call.", "Add packages to build your plan",
           "Hi Demoski. I built a plan on your packages page. I am interested in:", "Can we book the free strategy call and get a quote?"))
page("/training/", "Training | Demoski Digital Agency",
     "Six practical programmes in design, WordPress, funnels, paid advertising, e-commerce and digital marketing strategy, taught by working practitioners.",
     "Training", training,
     attrs("Hi Demoski. I am interested in your training. Which programme do you recommend for me?", "Choose a programme",
           "Hi Demoski. I want to enrol in:", "Please send me the price, the start date and how to enrol.", "Ask about this", single=True))
page("/portfolio/", "Proof | Demoski Digital Agency",
     "Real ad accounts and unedited Ads Manager screenshots from Demoski Digital clients: spend, cost per result and return on ad spend.",
     "Proof", portfolio,
     attrs("Hi Demoski. I have seen your results and would like to talk about my business.", "Want results like these?"), noindex=True)
page("/about/", "About | Demoski Digital Agency",
     "Demoski Digital is a performance-first growth agency founded by Ademola Adeniran. We own the whole chain from ad to landing page to follow-up.",
     "About", about,
     attrs("Hi Demoski. I read about how you work and would like to book the free strategy call.", "Free 30-minute strategy call"))

page("/done-for-you/", "Done-For-You Marketing Setup | Demoski Digital Agency",
     "Website, tracking, email automation and ad campaigns on up to three platforms, built and handed over in 14 days for one price.",
     "Done-for-you setup", dfy,
     attrs("Hi Demoski. I want the Done-For-You marketing setup (₦2,400,000). Please send me the brief questionnaire.", "₦2,400,000 · built in 14 days",
           "Hi Demoski. I want the Done-For-You marketing setup (₦2,400,000). Ad platforms I want:", "Please send me the brief questionnaire.", "Send my brief", maxn=3))

page("/autobuild-funnel/", "AutoBuild Funnel Course | Demoski Digital Agency",
     "A four-module, self-paced course on building and automating sales funnels with free hosting, payments, n8n and AI agents. No coding.",
     "AutoBuild", autobuild, attrs("Hi Demoski. I want to enrol in AutoBuild (₦25,000). Please send me the payment details.", "AutoBuild · ₦25,000"))
page("/ai-funnel-generator/", "AI Funnel Accelerator | Demoski Digital Agency",
     "Build AI-powered sales funnels, automate WhatsApp follow-up and deploy anywhere. Includes a live funnel workshop and a 14-day refund guarantee.",
     "AI Funnel Accelerator", aifunnel, attrs("Hi Demoski. I want to enrol in the AI Funnel Accelerator (₦25,000). Please send me the payment details and the next workshop date.", "AI Funnel Accelerator · ₦25,000"))
page("/affiliate/", "Affiliate Programme | Demoski Digital Agency",
     "Refer business owners to Demoski Digital and earn 20% commission on their first package or training enrolment.",
     "Affiliates", affiliate, attrs("Hi Demoski. I want to apply to your affiliate programme.", "Earn 20% per referral"))

contact = f"""<main>
<div class="phero"><div class="wrap">
  <p class="label">Contact Us</p>
  <h1>Talk to <mark>Demoski Digital.</mark></h1>
  <p class="lede">WhatsApp is fastest. We reply within one hour during business hours.</p>
  <div class="btnrow"><a class="btn" data-wa="" target="_blank" rel="noopener">Chat on WhatsApp</a><a class="btn ghost" href="tel:{LEGAL_PHONE}">Call {LEGAL_PHONE}</a><a class="btn ghost" href="mailto:hello@demoskidigital.com">hello@demoskidigital.com</a></div>
</div></div>
{LEGAL_SECTION}
</main>"""
page("/contact/", "Contact Us | Demoski Digital (Demoski Designs and Geospatial Consult)",
     "Contact Demoski Digital, the operating brand of Demoski Designs and Geospatial Consult. Phone and WhatsApp +2347066153757.",
     "Contact", contact, attrs("Hi Demoski. I would like to talk about my business.", "We reply within one hour"))

urls = ["/contact/", "/", "/packages/", "/done-for-you/", "/training/", "/autobuild-funnel/", "/ai-funnel-generator/", "/affiliate/", "/about/"]
open(os.path.join(DIST, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
json.dump({
  "cleanUrls": True, "trailingSlash": True,
  "redirects": [{"source": s, "destination": "/", "permanent": False} for s in ["/sample-page/", "/elementor-173/", "/fresh-page/", "/blog/"]]
      + [{"source": "/social-media-management-training/", "destination": "/training/", "permanent": False},
         {"source": "/affilate/", "destination": "/affiliate/", "permanent": False}],
  # Remove this header block on launch day. It keeps the preview out of Google.
  "headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]}]
}, open(os.path.join(DIST, "vercel.json"), "w"), indent=2)
print("built", sum(len(f) for _, _, f in os.walk(DIST)), "files")
