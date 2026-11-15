#!/usr/bin/env python3
"""Erzeugt die Startseiten /noka/ und /noka/en/ (statisches HTML) und tauscht Kopf/Fuß der übrigen Seiten."""
import re, sys
from pathlib import Path
W = Path("/Users/thomas/Developer/thomasnagel.org/noka")
TF = "https://testflight.apple.com/join/RnpF52G6"
SITE = "https://thomasnagel.org"

SYM = {
 "person": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6"/>',
 "auge": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/><path d="M4 20L20 4"/>',
 "werbung": '<path d="M4 10v4h3l6 4V6L7 10H4z"/><path d="M17 9l4 6M21 9l-4 6"/>',
 "schild": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "stern": '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
 "mond": '<path d="M20 14.5A8 8 0 1 1 9.5 4 6.5 6.5 0 0 0 20 14.5z"/>',
 "schrift": '<path d="M4 19l5-14 5 14M6 14h6M15 19l3-8 3 8M16 16.5h4"/>',
 "waage": '<path d="M12 4v16M5 20h14M5 8h14M7 8l-3 6h6zM17 8l-3 6h6z"/>',
 "sichern": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v3h16v-3"/>',
 "korb": '<path d="M3 4h2l2 11h11l2-8H6.5"/><circle cx="9" cy="19" r="1.4"/><circle cx="17" cy="19" r="1.4"/>',
}
def sym(n):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SYM[n]}</svg>'

# Fotos: (Grundname, Breite, Höhe) – Maße aus den gerahmten Bildern
FOTO = {
 "liste":  (640, 1308),
 "haus":   (640, 1308),
 "maria":  (640, 1308),
 "ringbuch": (1500, 1090),
 "halb":   (1500, 1205),
}
def pic(sp, name, alt, lazy=True, pre=""):
    b, h = FOTO[name]
    l = ' loading="lazy"' if lazy else ""
    d = f'{pre}img/{name}-{sp}'
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{d}-dunkel.webp">'
            f'<img src="{d}-hell.webp" width="{b}" height="{h}"{l} alt="{alt}"></picture>')

T = {
 "de": dict(
  lang="de", titel="noka – Einkaufsliste für jeden Laden",
  desc="Einmal aufschreiben, in jedem Laden die richtige Liste. Mit Datenschutz: kein Tracking, keine Werbung, kein Account. Kostenlos für das iPhone.",
  og_locale="de_DE", og_url=SITE+"/noka/", og_bild=SITE+"/noka/img/vorschau-de.png",
  og_alt="noka: Wortmarke, Claim und die Ladenliste auf einem iPhone",
  claim="Einmal aufschreiben. In jedem Laden die richtige Liste.",
  schutz='Mit Datenschutz.<br><span>Kein Tracking,</span> <span>keine Werbung,</span> <span>kein Account.</span>',
  knopf="Jetzt in TestFlight testen", knopf_klein="Testen", unter="Kostenlos · iPhone · iOS 17 oder neuer",
  app_label="Laden im App Store",
  hilfe="Hilfe", hilfe_url="hilfe/", andere_url="en/", sprachnav="Sprache / Language",
  startlink="noka – Startseite",
  so="So funktioniert noka",
  schritte=[("Läden einrichten","In zwei Minuten aus Vorlagen."),("Einmal aufschreiben","noka weiß, wo es Milch gibt."),("Im Laden abhaken","Sortiert wie dein Weg durch den Laden.")],
  g_ueber="Gemeinsam einkaufen", g_h="Gemeinsam aufschreiben. Gemeinsam einkaufen.",
  g_lead="Teilt euren Haushalt über iCloud, mit allen Läden und Listen. Alle schreiben auf, ändern und haken ab, und alles ist sofort bei allen. Wer gerade im Laden steht, hat genau dessen Liste dabei.",
  g_live_hin="Und wenn jemand gerade einkauft, sieht man das live.", g_live="live · Maria kauft hier ein · 2 im Korb",
  g_acc="Ohne Account. Ihr braucht nur eure Apple-ID.",
  d_ueber="Datenschutz", d_h="Deine Einkaufsliste geht niemanden etwas an.",
  d_lead="Deine Listen liegen auf deinem iPhone und in deinem iCloud. noka hat keinen eigenen Server. Ich kann deine Daten nicht sehen.",
  d_karten=[("person","Kein Account","Keine Anmeldung, keine E-Mail-Adresse. Einfach loslegen."),("auge","Kein Tracking","Keine Analyse, keine fremden Dienste, nichts wird ausgewertet."),("werbung","Keine Werbung","Nicht jetzt und nicht später. noka lebt von freiwilligen Kaffees.")],
  d_kachel="Keine Daten erfasst", d_kachel_t="So steht es im Datenschutz-Label von noka.", d_kachel_t_store="So steht es im Datenschutz-Label von noka im App Store.",
  d_link="Datenschutzerklärung lesen", d_url="datenschutz/",
  u_ueber="Gemacht fürs iPhone Duo", u_h="Aufgeklappt wird noka zum Ringbuch.",
  u_lead="Links deine Läden, rechts die Liste. Halb geöffnet hältst du es wie ein Buch: links tippen, rechts abhaken.",
  k_ueber="Die kleinen Dinge", k_h="Durchdacht bis in die Ecken.",
  kacheln=[("stern","Vorschläge für das, was du regelmäßig kaufst"),("mond","Hell und dunkel, beide mit Liebe gemacht"),("schrift","Große Schrift und VoiceOver auf jeder Seite"),("waage","Metrisch oder US-Einheiten, auch gemischt im Haushalt"),("sichern","Deine Daten jederzeit als Datei sichern"),("korb","Erinnerung, wenn ein Einkauf noch offen ist")],
  p_ueber="Preis", p_h="Kostenlos. Ohne Abo, ohne Werbung.",
  p_lead="Wenn dir noka hilft, kannst du mir in der App einen Kaffee ausgeben. Das schaltet nichts frei. Es hilft nur, noka weiterzumachen.",
  fuss=[("Hilfe","hilfe/"),("Presse","press/"),("Datenschutz","datenschutz/"),("Impressum","/impressum/")], fuss_andere="English", fuss_von="Gemacht von Thomas Nagel",
  alt=dict(
   liste="noka auf dem iPhone: die Liste „Supermarkt“ nach Kategorien sortiert, zwei Einträge liegen im Korb, oben steht „live · Maria kauft hier ein“.",
   haus="noka auf dem iPhone, Haus-Seite: im Suchfeld steht „Milch“, darunter ein Vorschlag.",
   maria="noka auf dem iPhone von Maria: in der Liste „Supermarkt“ steht „Milch“, die gerade aufgeschrieben wurde.",
   ringbuch="noka auf einem aufgeklappten iPhone Duo quer: links die Läden, rechts die Liste, wie in einem Ringbuch.",
   halb="noka auf einem halb geöffneten iPhone Duo, gehalten wie ein Buch: links Läden und Suche, rechts die Liste.")),
 "en": dict(
  lang="en", titel="noka – A shopping list for every store",
  desc="Write it down once, get the right list in every store. Built for privacy: no tracking, no ads, no account. Free for iPhone.",
  og_locale="en_US", og_url=SITE+"/noka/en/", og_bild=SITE+"/noka/img/vorschau-en.png",
  og_alt="noka: wordmark, tagline and the store list on an iPhone",
  claim="Write it down once. The right list in every store.",
  schutz='With privacy.<br><span>No tracking,</span> <span>no ads,</span> <span>no account.</span>',
  knopf="Try it on TestFlight", knopf_klein="Try it", unter="Free · iPhone · iOS 17 or later",
  app_label="Download on the App Store",
  hilfe="Help", hilfe_url="help/", andere_url="../", sprachnav="Sprache / Language",
  startlink="noka – home",
  so="How noka works",
  schritte=[("Set up your stores","In two minutes, from templates."),("Write it down once","noka knows where to get milk."),("Check it off in the store","Sorted the way you walk through the store.")],
  g_ueber="Shop together", g_h="Write it down together. Shop together.",
  g_lead="Share your household through iCloud, with all your stores and lists. Everyone can add, change and check off items, and it shows up for everyone right away. Whoever is in a store has exactly that store's list.",
  g_live_hin="And when someone is shopping, you see it live.", g_live="live · Maria is shopping here · 2 in cart",
  g_acc="No account. All you need is your Apple ID.",
  d_ueber="Privacy", d_h="Your shopping list is nobody else's business.",
  d_lead="Your lists live on your iPhone and in your iCloud. noka has no server of its own. I can't see your data.",
  d_karten=[("person","No account","No sign-up, no email address. Just start."),("auge","No tracking","No analytics, no third-party services, nothing is analyzed."),("werbung","No ads","Not now, not later. noka runs on optional coffees.")],
  d_kachel="Data Not Collected", d_kachel_t="That's what noka's privacy label says.", d_kachel_t_store="That's what noka's privacy label on the App Store says.",
  d_link="Read the privacy policy", d_url="privacy/",
  u_ueber="Made for iPhone Duo", u_h="Unfolded, noka becomes a ring binder.",
  u_lead="Your stores on the left, the list on the right. Half open, you hold it like a book: tap on the left, check off on the right.",
  k_ueber="The little things", k_h="Thoughtful down to the details.",
  kacheln=[("stern","Suggestions for what you buy regularly"),("mond","Light and dark, both made with care"),("schrift","Large text and VoiceOver on every screen"),("waage","Metric or US units, even mixed in one household"),("sichern","Back up your data as a file anytime"),("korb","A reminder when a shopping trip is still open")],
  p_ueber="Price", p_h="Free. No subscription, no ads.",
  p_lead="If noka helps you, you can buy me a coffee in the app. It doesn't unlock anything. It just helps keep noka going.",
  fuss=[("Help","help/"),("Press","../press/"),("Privacy","privacy/"),("Imprint","/impressum/")], fuss_andere="Deutsch", fuss_von="Made by Thomas Nagel",
  alt=dict(
   liste="noka on an iPhone: the “Grocery Store” list sorted by category, two items in the cart, and “live · Maria is shopping here” at the top.",
   haus="noka on an iPhone, home page: “Milk” typed into the search field, with a suggestion below.",
   maria="noka on Maria's iPhone: the “Grocery Store” list with “Milk”, just added.",
   ringbuch="noka on an unfolded iPhone Duo in landscape: your stores on the left, the list on the right, like a ring binder.",
   halb="noka on a half-open iPhone Duo, held like a book: stores and search on the left, the list on the right.")),
}

def kopf_html(L, pre, de_url, en_url, kn_url):
    t = T[L]
    if L == "de":
        sp = f'<span aria-current="page" lang="de">DE</span><span class="punkt" aria-hidden="true">·</span><a href="{en_url}" hreflang="en" lang="en">EN</a>'
    else:
        sp = f'<a href="{de_url}" hreflang="de" lang="de">DE</a><span class="punkt" aria-hidden="true">·</span><span aria-current="page" lang="en">EN</span>'
    return (f'<header class="kopf"><div class="innen">\n'
     f'<a class="wm" href="{kn_url}">n<img src="{pre}kiwi.svg" alt="o">ka</a>\n'
     f'<nav aria-label="{t["sprachnav"]}"><a class="weg" href="{{HILFE}}">{t["hilfe"]}</a><span class="sp">{sp}</span>'
     f'<a class="knopf-klein" href="{TF}">{t["knopf_klein"]}</a></nav>\n</div></header>')

def fuss_html(L, pre, other, hilfe, press, datenschutz, impressum):
    t = T[L]
    links = [(t["fuss"][0][0], hilfe), (t["fuss"][1][0], press), (t["fuss"][2][0], datenschutz), (t["fuss"][3][0], impressum)]
    a = "".join(f'<a href="{u}">{n}</a>' for n, u in links)
    other_l = "en" if L == "de" else "de"
    return (f'<footer class="fuss"><div class="innen">\n{a}<a href="{other}" hreflang="{other_l}" lang="{other_l}">{t["fuss_andere"]}</a>'
            f'<span class="rechts">{t["fuss_von"]}</span>\n</div></footer>')

def start(L):
    t = T[L]; de = L == "de"
    pre = "" if de else "../"           # Pfad zu noka.css, kiwi.svg usw.
    bild = "" if de else "../"          # Bilder liegen in /noka/img/
    h_url = t["hilfe_url"]
    sp = L
    def P(n, lazy=True): return pic(sp, n, t["alt"][n], lazy, bild)
    kopf = kopf_html(L, pre, "../" if not de else "./", "en/", "./" if de else "./").replace("{HILFE}", h_url)
    fuss = fuss_html(L, pre, t["andere_url"], h_url, "press/" if de else "../press/", t["d_url"], "/impressum/")
    hreflang = (f'<link rel="alternate" hreflang="de" href="{SITE}/noka/">\n<link rel="alternate" hreflang="en" href="{SITE}/noka/en/">')
    fremd = ('''<p class="fremd" id="fremd" lang="en" hidden><a href="en/" hreflang="en">This page is also available in English ›</a></p>
<script>(function(){var l=(navigator.languages&&navigator.languages[0])||navigator.language||"";if(l&&!/^de/i.test(l)){var e=document.getElementById("fremd");if(e)e.hidden=false}})();</script>\n''' if de else "")
    schritte = "".join(f'<li><b aria-hidden="true">{i+1}</b><div><h3>{a}</h3><p>{b}</p></div></li>\n' for i, (a, b) in enumerate(t["schritte"]))
    karten = "".join(f'<div class="punkt-karte">{sym(s)}<h3>{h}</h3><p>{p}</p></div>\n' for s, h, p in t["d_karten"])
    kacheln = "".join(f'<div class="kachel">{sym(s)}<p>{x}</p></div>\n' for s, x in t["kacheln"])
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["titel"]}</title>
<meta name="description" content="{t["desc"]}">
{hreflang}
<link rel="canonical" href="{t["og_url"]}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="noka">
<meta property="og:title" content="{t["titel"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:url" content="{t["og_url"]}">
<meta property="og:locale" content="{t["og_locale"]}">
<meta property="og:image" content="{t["og_bild"]}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t["og_alt"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t["titel"]}">
<meta name="twitter:description" content="{t["desc"]}">
<meta name="twitter:image" content="{t["og_bild"]}">
<!-- Smart App Banner, erst zum App-Store-Start einschalten: <meta name="apple-itunes-app" content="app-id=[APP-ID]"> -->
<link rel="icon" href="{pre}icon.png">
<link rel="apple-touch-icon" href="{pre}icon.png">
<link rel="preload" href="{pre}Fredoka-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}noka.css">
</head>
<body>
{fremd}{kopf}
<main class="start">

<div class="held"><div class="innen">
<div>
<h1>{t["claim"]}</h1>
<p class="schutz">{t["schutz"]}</p>
<div class="aktion">
<a class="knopf-gross" href="{TF}">{t["knopf"]}</a>
<!-- Zum App-Store-Start statt des Knopfs oben: das offizielle Badge von Apple, URL ergänzen
<a href="[APP-STORE-URL]"><img src="{bild}img/app-store-badge-{L}.svg" height="54" alt="{t["app_label"]}"></a> -->
<span class="klein">{t["unter"]}</span>
</div>
</div>
<div class="bild">
<img class="scheibe" src="{pre}kiwi.svg" alt="" aria-hidden="true">
<div class="foto-schraeg">{P("liste", lazy=False)}</div>
</div>
</div></div>

<section class="schritte-zeile"><div class="innen">
<h2 class="vh">{t["so"]}</h2>
<ol class="schritte">
{schritte}</ol>
</div></section>

<section><div class="innen zwei">
<div>
<p class="ueber">{t["g_ueber"]}</p>
<h2>{t["g_h"]}</h2>
<p class="lead">{t["g_lead"]}</p>
<p class="lead klein">{t["g_live_hin"]}</p>
<span class="live"><i></i>{t["g_live"]}</span>
<p class="lead klein">{t["g_acc"]}</p>
</div>
<div class="paar-live">
{P("haus")}
{P("maria")}
</div>
</div></section>

<section class="band"><div class="innen">
<p class="ueber">{t["d_ueber"]}</p>
<h2>{t["d_h"]}</h2>
<p class="lead">{t["d_lead"]}</p>
<div class="drei">
{karten}</div>
<div class="label">{sym("schild")}<div><b>{t["d_kachel"]}</b><span>{t["d_kachel_t"]}</span>
<!-- Zum App-Store-Start: <span>{t["d_kachel_t_store"]}</span> statt der Zeile oben -->
</div></div>
<p style="margin:18px 0 0"><a href="{t["d_url"]}">{t["d_link"]}</a></p>
</div></section>

<section class="duo-mitte"><div class="innen">
<p class="ueber">{t["u_ueber"]}</p>
<h2>{t["u_h"]}</h2>
<p class="lead">{t["u_lead"]}</p>
<div class="duo-bilder">
<div class="gross">{P("ringbuch")}</div>
<div class="halb">{P("halb")}</div>
</div>
</div></section>

<section class="klein-dinge"><div class="innen">
<p class="ueber">{t["k_ueber"]}</p>
<h2>{t["k_h"]}</h2>
<div class="kacheln">
{kacheln}</div>
</div></section>

<!-- Stimmen: vorerst ausgeblendet, bis echte Zitate mit Einverständnis vorliegen.
<section class="band"><div class="innen">
<p class="ueber">…</p><h2>…</h2>
<div class="stimmen"><blockquote><p>…</p><footer>…</footer></blockquote></div>
</div></section>
-->

<section class="preis"><div class="innen">
<p class="ueber">{t["p_ueber"]}</p>
<h2>{t["p_h"]}</h2>
<p class="lead">{t["p_lead"]}</p>
</div></section>

<div class="schluss"><div class="innen">
<div class="wm" aria-hidden="true">n<img src="{pre}kiwi.svg" alt="">ka</div>
<p class="claim">{t["claim"].replace(". ", ".<br>", 1)}</p>
<a class="knopf-gross" href="{TF}">{t["knopf"]}</a>
</div></div>
</main>

{fuss}
</body>
</html>
'''

def schreibe(pfad, text):
    p = W / pfad; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")

import subprocess
def alt(pfad):
    return subprocess.run(["git", "-C", str(W.parent), "show", "HEAD:noka/" + pfad], capture_output=True, text=True, check=True).stdout

SEITEN = {  # Datei: (Sprache, pre, DE-Link, EN-Link, Startseite, Hilfe, Presse, Datenschutz, andere Sprache im Fuß)
 "datenschutz/index.html": ("de", "../", "./", "../en/privacy/", "../", "../hilfe/", "../press/", "./", "../en/privacy/"),
 "en/privacy/index.html": ("en", "../../", "../../datenschutz/", "./", "../", "../help/", "../../press/", "./", "../../datenschutz/"),
 "press/index.html": ("en", "../", "../", "./", "../en/", "../en/help/", "./", "../en/privacy/", "../"),
 "hilfe/index.html": ("de", "../", "./", "../en/help/", "../", "./", "../press/", "../datenschutz/", "../en/help/"),
 "en/help/index.html": ("en", "../../", "../../hilfe/", "./", "../", "./", "../../press/", "../privacy/", "../../hilfe/"),
}
def kopf_fuss(L, pre, de_u, en_u, home, hilfe, press, ds, other):
    return (kopf_html(L, pre, de_u, en_u, home).replace("{HILFE}", hilfe),
            fuss_html(L, pre, other, hilfe, press, ds, "/impressum/"))

def hilfe_seite(L):
    de = L == "de"
    datei = "hilfe/index.html" if de else "en/help/index.html"
    cfg = SEITEN[datei]
    kopf, fuss = kopf_fuss(*cfg)
    quelle = alt("index.html" if de else "en/index.html")
    beta = re.search(r'<section class="beta".*?</section>', quelle, re.S).group(0)
    teil = re.search(r'<h2 id="(?:hilfe|help)">.*?</dl>', quelle, re.S).group(0)
    teil = re.sub(r"^<h2 (id=\"[a-z]+\")>(.*?)</h2>", r"<h1 \1>\2</h1>", teil)   # eigene Seite: Überschrift wird h1, Text unverändert
    titel = "noka – Hilfe und Kontakt" if de else "noka – Help and contact"
    pre = cfg[1]
    alt_url = "../en/help/" if de else "../../hilfe/"
    fremd = ('<p class="fremd" id="fremd" lang="en" hidden><a href="../en/help/" hreflang="en">This page is also available in English ›</a></p>\n'
             '<script>(function(){var l=(navigator.languages&&navigator.languages[0])||navigator.language||"";if(l&&!/^de/i.test(l)){var e=document.getElementById("fremd");if(e)e.hidden=false}})();</script>\n') if de else ""
    return f'''<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{"Fragen und Antworten zu noka: Wo liegen meine Daten, Teilen mit der Familie, Umzug aufs neue iPhone, Kontakt." if de else "Questions and answers about noka: where your data lives, sharing with family, moving to a new iPhone, contact."}">
<link rel="alternate" hreflang="de" href="{SITE}/noka/hilfe/">
<link rel="alternate" hreflang="en" href="{SITE}/noka/en/help/">
<link rel="icon" href="{pre}icon.png">
<link rel="apple-touch-icon" href="{pre}icon.png">
<link rel="stylesheet" href="{pre}noka.css">
</head>
<body>
{fremd}{kopf}
<main class="seite">
{beta}

{teil}
</main>

{fuss}
</body>
</html>
'''

def tausche(datei):
    L, *cfg = SEITEN[datei]
    p = W / datei; t = alt(datei)
    kopf, fuss = kopf_fuss(L, *cfg)
    # Kopf: alter Umschalter und (Presse) Wortmarke + Unterzeile raus; neuer Kopf vor <main>
    t = re.sub(r'<nav class="sprache".*?</nav>\n', "", t, flags=re.S)
    t = re.sub(r'<p class="wort">.*?</p>\n<p class="unter">.*?</p>\n\n?', "", t, flags=re.S)
    t = re.sub(r"(?=<main)", kopf + "\n", t, count=1)
    t = re.sub(r"<footer>.*?</footer>\n</main>", "</main>\n\n" + fuss.replace("\\", "\\\\"), t, flags=re.S)
    p.write_text(t, encoding="utf-8")

if __name__ == "__main__":
    schreibe("index.html", start("de"))
    schreibe("en/index.html", start("en"))
    schreibe("hilfe/index.html", hilfe_seite("de"))
    schreibe("en/help/index.html", hilfe_seite("en"))
    for d in ("datenschutz/index.html", "en/privacy/index.html", "press/index.html"):
        tausche(d)
