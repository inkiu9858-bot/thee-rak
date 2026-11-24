# -*- coding: utf-8 -*-
"""
ฉากภาพเคลื่อนไหวทั้งหมด (HTML/CSS/JS ล้วน) สำหรับฝังด้วย st.components.v1.html
 - intro_html   : หน้าเปิด (เรือ + ตัวการ์ตูนสองคน + พระจันทร์เต็มดวง)
 - sail_html    : แล่นเรือความทรงจำ (โพลารอยด์ลอยขึ้นจากเรือ → พิมพ์ข้อความ → confetti)
 - pair_preview_html : พรีวิวกระทงสองใบตอนตกแต่ง
 - float_html   : ปล่อยโคม (ข้อความคำอธิษฐานบนโคม) + ลอยกระทง
ตัวการ์ตูน/กระทง/เรือ เป็น SVG วาดเองทั้งหมด (ตัวละครออริจินัล) — ใบหน้าใส่จากไฟล์ assets/faces/
"""
from __future__ import annotations

import html as _html
import json
import math

FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Mali:wght@400;600;700&family=Itim&display=swap"
)

# ════════════════════════════ ตัวเลือกกระทง ════════════════════════════
BASES = {  # (สีฐาน, สีขอบ/ด้านข้าง, สีกลีบใบตอง)
    "leaf": ("#8fd19e", "#58a86b", "#6cbf7e"),
    "pink": ("#ffc2d9", "#f08fb4", "#ff9ec7"),
    "lilac": ("#d3c3ff", "#a98cf0", "#b9a0ff"),
    "cream": ("#ffefc4", "#f0c887", "#ffdc8f"),
}
BASE_LABELS = {"leaf": "ใบตอง 🌿", "pink": "ชมพู 🌸", "lilac": "ม่วงพาสเทล 💜", "cream": "ครีม 🍞"}
FLOWER_LABELS = {"lotus": "ดอกบัว 🪷", "daisy": "เดซี่ 🌼", "rose": "กุหลาบ 🌹"}
CANDLES = {"pink": "#ff9ec7", "yellow": "#ffd166", "blue": "#8ecbff"}
CANDLE_LABELS = {"pink": "เทียนชมพู", "yellow": "เทียนเหลือง", "blue": "เทียนฟ้า"}
STICKERS = {"heart": "💖", "star": "⭐", "moon": "🌙", "cat": "🐱", "none": ""}
STICKER_LABELS = {"heart": "💖 หัวใจ", "star": "⭐ ดาว", "moon": "🌙 เดือน", "cat": "🐱 แมว", "none": "ไม่ติด"}

DEFAULT_STYLE = {"base": "pink", "flower": "lotus", "candle": "pink", "sticker": "heart"}


def _flower(kind: str, x: float, y: float, s: float) -> str:
    if kind == "daisy":
        petals = "".join(
            f'<ellipse cx="0" cy="-9" rx="4.6" ry="8.6" fill="#fff" stroke="#e8e0f5" stroke-width=".6" '
            f'transform="rotate({a})"/>'
            for a in range(0, 360, 45)
        )
        body = petals + '<circle r="5.4" fill="#ffcf3f"/><circle r="2" fill="#ff9f45"/>'
    elif kind == "rose":
        body = (
            '<circle r="11.5" fill="#ff6f9c"/><circle r="8" fill="#ff8fb4"/>'
            '<path d="M-5 -1 Q0 -9 5 -1 Q0 5 -3.5 1.5" fill="none" stroke="#ffd0e0" stroke-width="1.7" stroke-linecap="round"/>'
            '<circle r="3" fill="#ff6f9c"/>'
            '<path d="M-11 4 Q-14 12 -6 12" fill="#58a86b"/><path d="M11 4 Q14 12 6 12" fill="#58a86b"/>'
        )
    else:  # lotus
        petals = "".join(
            f'<path d="M0 0 Q-9.5 -11 0 -27 Q9.5 -11 0 0Z" fill="{c}" stroke="#fff" stroke-width="1" '
            f'transform="rotate({a})"/>'
            for a, c in ((-72, "#ff8fb9"), (72, "#ff8fb9"), (-36, "#ff9ec7"), (36, "#ff9ec7"), (0, "#ffb8d6"))
        )
        body = petals + '<circle r="3" cy="-2" fill="#ffe08a"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{body}</g>'


def krathong_svg(style: dict | None = None) -> str:
    """กระทงใบตอง SVG (viewBox 240x170) — style: base/flower/candle/sticker"""
    st = {**DEFAULT_STYLE, **(style or {})}
    base_main, base_dark, leaf = BASES.get(st["base"], BASES["pink"])
    candle = CANDLES.get(st["candle"], CANDLES["pink"])
    cx, cy, rx, ry = 120, 128, 92, 27

    def leaves(front: bool) -> str:
        out = []
        for k in range(16):
            th = k * 22.5
            s = math.sin(math.radians(th))
            if (s >= 0) != front:
                continue
            px = cx + (rx - 5) * math.cos(math.radians(th))
            py = cy + (ry - 3) * s
            col = leaf if k % 2 == 0 else base_main
            out.append(
                f'<g transform="translate({px:.1f} {py:.1f}) scale(1 .66) rotate({th + 90:.1f})">'
                f'<path d="M0 0 Q-10.5 -13 0 -31 Q10.5 -13 0 0Z" fill="{col}" stroke="{base_dark}" stroke-width=".8"/>'
                f'<path d="M0 -4 L0 -23" stroke="#fff" stroke-opacity=".4" stroke-width="1.2"/></g>'
            )
        return "".join(out)

    parts = [leaves(False)]
    parts.append(f'<ellipse cx="{cx}" cy="{cy + 11}" rx="{rx + 4}" ry="{ry + 2}" fill="{base_dark}"/>')
    parts.append(f'<rect x="{cx - rx - 4}" y="{cy}" width="{2 * (rx + 4)}" height="11" fill="{base_dark}"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{base_main}"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy - 2}" rx="{rx - 14}" ry="{ry - 8}" fill="#fff" fill-opacity=".18"/>')
    parts.append(leaves(True))
    # ธูป
    parts.append(
        '<path d="M106 114 L93 52 M134 114 L147 50" stroke="#9b6a3c" stroke-width="2.4" stroke-linecap="round"/>'
        '<circle cx="93" cy="51" r="2.6" fill="#ff6b3d"/><circle cx="147" cy="49" r="2.6" fill="#ff6b3d"/>'
    )
    # เทียน + เปลวไฟ
    parts.append(
        f'<rect x="110" y="72" width="20" height="46" rx="3.5" fill="{candle}"/>'
        '<rect x="110" y="72" width="7" height="46" rx="3" fill="#fff" fill-opacity=".28"/>'
        '<ellipse cx="120" cy="72" rx="10" ry="3" fill="#fff" fill-opacity=".35"/>'
        '<circle cx="120" cy="58" r="20" fill="url(#kglow)"/>'
        '<path class="flame" d="M120 45 Q112 57 120 69 Q128 57 120 45Z" fill="#ffae3b"/>'
        '<path class="flame" d="M120 54 Q116.5 60 120 66 Q123.5 60 120 54Z" fill="#fff3b0"/>'
    )
    # ดอกไม้
    fl = st["flower"]
    for (x, y, s) in ((62, 116, .85), (178, 116, .85), (92, 106, 1.0), (148, 106, 1.0), (120, 114, 1.12)):
        parts.append(_flower(fl, x, y, s))
    for (x, y, s) in ((84, 132, .8), (156, 132, .8)):
        parts.append(_flower(fl, x, y, s))
    # สติกเกอร์
    emoji = STICKERS.get(st["sticker"], "")
    if emoji:
        parts.append(
            f'<circle cx="120" cy="143" r="14" fill="#fff" stroke="{base_dark}" stroke-width="2"/>'
            f'<text x="120" y="149" font-size="16" text-anchor="middle">{emoji}</text>'
        )
    defs = '<defs><radialGradient id="kglow"><stop offset="0" stop-color="#ffd77a" stop-opacity=".85"/><stop offset="1" stop-color="#ffd77a" stop-opacity="0"/></radialGradient></defs>'
    return '<svg viewBox="0 30 240 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;overflow:visible">' + defs + "".join(parts) + "</svg>"


# ════════════════════════════ ตัวการ์ตูน + เรือ ════════════════════════════
def _face(cx, cy, r, uri, cid, hair, tilt):
    if uri:
        inner = (
            f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<image href="{uri}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-width="3.2"/>'
        )
    else:  # ใบหน้าตัวอย่างน่ารักๆ ระหว่างรอรูปจริง
        inner = (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffe3c9" stroke="#fff" stroke-width="3.2"/>'
            f'<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy} Q{cx} {cy - r * .5} {cx - r} {cy}Z" fill="{hair}"/>'
            f'<circle cx="{cx - r * .36}" cy="{cy + r * .08}" r="{r * .085}" fill="#3b2a4a"/>'
            f'<circle cx="{cx + r * .36}" cy="{cy + r * .08}" r="{r * .085}" fill="#3b2a4a"/>'
            f'<ellipse cx="{cx - r * .55}" cy="{cy + r * .38}" rx="{r * .16}" ry="{r * .1}" fill="#ff9ab8" fill-opacity=".7"/>'
            f'<ellipse cx="{cx + r * .55}" cy="{cy + r * .38}" rx="{r * .16}" ry="{r * .1}" fill="#ff9ab8" fill-opacity=".7"/>'
            f'<path d="M{cx - r * .18} {cy + r * .38} Q{cx} {cy + r * .55} {cx + r * .18} {cy + r * .38}" '
            f'fill="none" stroke="#3b2a4a" stroke-width="2" stroke-linecap="round"/>'
        )
    return f'<g transform="rotate({tilt} {cx} {cy})" style="filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))">{inner}</g>'


def boat_svg(me_uri: str | None, partner_uri: str | None, uid: str = "b") -> str:
    """เรือไม้ + ตัวการ์ตูนสองคน (ซ้าย = เรา, ขวา = แฟน) หน้าเป็นรูปจริงตัดวงกลม"""
    r = 39
    me = _face(88, 68, r, me_uri, f"cm{uid}", "#3a2a3a", -6)
    pa = _face(172, 68, r, partner_uri, f"cp{uid}", "#6b3f3f", 6)
    body = (
        # ตัวซ้าย (ฟ้า)
        '<rect x="62" y="100" width="52" height="48" rx="20" fill="#8ec5ff"/>'
        '<path d="M80 100 Q88 112 96 100" fill="#fff" fill-opacity=".85"/>'
        '<ellipse cx="60" cy="126" rx="9" ry="15" fill="#7bb6f5" transform="rotate(8 60 126)"/>'
        '<ellipse cx="117" cy="122" rx="9" ry="14" fill="#7bb6f5" transform="rotate(-18 117 122)"/>'
        # ตัวขวา (ชมพู)
        '<rect x="146" y="100" width="52" height="48" rx="20" fill="#ffb3d1"/>'
        '<path d="M164 100 Q172 112 180 100" fill="#fff" fill-opacity=".85"/>'
        '<ellipse cx="200" cy="126" rx="9" ry="15" fill="#ff9fc4" transform="rotate(-8 200 126)"/>'
        '<ellipse cx="143" cy="122" rx="9" ry="14" fill="#ff9fc4" transform="rotate(18 143 122)"/>'
    )
    heart = (
        '<g class="heart-float"><path d="M130 40 C112 26 118 12 128 14 C134 15 130 22 130 24 '
        'C130 22 126 15 132 14 C142 12 148 26 130 40Z" fill="#ff6b9a" transform="translate(0 4)"/></g>'
    )
    hull = (
        f'<defs><linearGradient id="wood{uid}" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#d49a5b"/><stop offset="1" stop-color="#8f5a2b"/></linearGradient>'
        f'<radialGradient id="bglow{uid}"><stop offset="0" stop-color="#ffc86b" stop-opacity=".8"/><stop offset="1" stop-color="#ffc86b" stop-opacity="0"/></radialGradient></defs>'
        f'<path d="M8 128 Q22 150 50 152 L210 152 Q238 150 252 128 Q250 178 205 189 L55 189 Q10 178 8 128Z" fill="url(#wood{uid})"/>'
        '<path d="M8 128 Q22 150 50 152 L210 152 Q238 150 252 128" fill="none" stroke="#f6d19a" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M26 167 L234 167 M38 178 L222 178" stroke="#000" stroke-opacity=".16" stroke-width="2"/>'
    )
    lantern = (
        '<path d="M243 128 L243 82" stroke="#6b4423" stroke-width="3.2" stroke-linecap="round"/>'
        f'<circle cx="243" cy="96" r="26" fill="url(#bglow{uid})"/>'
        '<rect x="232" y="82" width="22" height="27" rx="7" fill="#ffc86b"/><rect x="232" y="82" width="22" height="6" rx="3" fill="#b8641f"/>'
    )
    wake = '<ellipse cx="130" cy="194" rx="112" ry="5" fill="#fff" fill-opacity=".16"/>'
    return (
        '<svg viewBox="0 0 260 205" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;overflow:visible">'
        + wake + lantern + body + me + pa + heart + hull + "</svg>"
    )


# ════════════════════════════ CSS / JS กลาง ════════════════════════════
BASE_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%;overflow:hidden;background:transparent;font-family:'Mali','Itim','Leelawadee UI','Sarabun','Tahoma',sans-serif;color:#fff}
.stage{position:relative;width:100%;height:100vh;overflow:hidden;border-radius:22px;
 background:linear-gradient(180deg,#0b0833 0%,#1f1658 32%,#44277f 58%,#7b3f9d 67%,#d16fa6 70%)}
.stars,.bgls{position:absolute;inset:0;pointer-events:none}
.star{position:absolute;border-radius:50%;background:#fff;animation:tw 2.4s ease-in-out infinite alternate}
@keyframes tw{from{opacity:.12}to{opacity:1}}
.moon{position:absolute;top:5%;right:11%;width:clamp(78px,22vw,124px);aspect-ratio:1;border-radius:50%;
 background:radial-gradient(circle at 34% 30%,#fffef4 0%,#fff6cf 52%,#ffe7a3 100%);
 box-shadow:0 0 30px 10px rgba(255,240,180,.55),0 0 90px 40px rgba(255,220,140,.28);animation:moonGlow 4s ease-in-out infinite alternate}
.moon::before{content:"";position:absolute;left:22%;top:26%;width:22%;height:22%;border-radius:50%;background:rgba(228,196,128,.38)}
.moon::after{content:"";position:absolute;left:55%;top:52%;width:28%;height:28%;border-radius:50%;background:rgba(228,196,128,.30);box-shadow:-30px 12px 0 -5px rgba(228,196,128,.26)}
@keyframes moonGlow{from{box-shadow:0 0 26px 8px rgba(255,240,180,.45),0 0 80px 34px rgba(255,220,140,.22)}to{box-shadow:0 0 36px 14px rgba(255,240,180,.65),0 0 110px 52px rgba(255,220,140,.34)}}
.water{position:absolute;left:0;right:0;bottom:0;height:32%;overflow:hidden;
 background:linear-gradient(180deg,#5d3190 0%,#2c1c68 38%,#140e3b 100%)}
.reflect{position:absolute;right:calc(11% - 6px);top:0;width:clamp(90px,26vw,150px);height:78%;
 background:radial-gradient(ellipse at 50% 0%,rgba(255,236,170,.6),rgba(255,236,170,0) 70%);filter:blur(2px);animation:shimmer 3s ease-in-out infinite alternate}
@keyframes shimmer{from{opacity:.55;transform:scaleX(.92)}to{opacity:1;transform:scaleX(1.06)}}
.wave{position:absolute;left:0;right:0;height:16px;background-repeat:repeat-x;animation:waveMove 9s linear infinite}
.w1{top:12%;opacity:.8;background-size:120px 14px;--shift:-240px;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='14' viewBox='0 0 120 14'%3E%3Cpath d='M0 7 Q15 0 30 7 T60 7 T90 7 T120 7' fill='none' stroke='white' stroke-opacity='.38' stroke-width='1.6'/%3E%3C/svg%3E")}
.w2{top:40%;opacity:.55;background-size:160px 18px;--shift:320px;animation-duration:13s;animation-direction:reverse;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='18' viewBox='0 0 160 18'%3E%3Cpath d='M0 9 Q20 0 40 9 T80 9 T120 9 T160 9' fill='none' stroke='white' stroke-opacity='.34' stroke-width='1.8'/%3E%3C/svg%3E")}
.w3{top:68%;opacity:.4;background-size:120px 14px;--shift:-240px;animation-duration:17s;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='14' viewBox='0 0 120 14'%3E%3Cpath d='M0 7 Q15 0 30 7 T60 7 T90 7 T120 7' fill='none' stroke='white' stroke-opacity='.3' stroke-width='1.6'/%3E%3C/svg%3E")}
@keyframes waveMove{to{background-position-x:var(--shift)}}
.bgl{position:absolute;bottom:-60px;width:var(--s);height:calc(var(--s)*1.3);border-radius:30% 30% 38% 38%/22% 22% 42% 42%;
 background:linear-gradient(#ffe6a6,#ff9f45);box-shadow:0 0 14px 4px rgba(255,170,70,.55);opacity:0;animation:rise var(--d) linear infinite;animation-delay:var(--dl)}
@keyframes rise{0%{transform:translate(0,0);opacity:0}6%{opacity:.9}25%{transform:translate(10px,-32%)}50%{transform:translate(-9px,-66%)}75%{transform:translate(12px,-100%)}90%{opacity:.8}100%{transform:translate(0,-140%);opacity:0}}
.flame{transform-box:fill-box;transform-origin:center bottom;animation:flick .2s ease-in-out infinite alternate}
@keyframes flick{from{transform:scale(1,1) rotate(-3deg)}to{transform:scale(.9,1.1) rotate(3deg)}}
.heart-float{animation:hf 2.2s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
@keyframes hf{from{transform:translateY(0) scale(.92)}to{transform:translateY(-7px) scale(1.08)}}
@keyframes bob{0%,100%{transform:translateY(0) rotate(-1.2deg)}50%{transform:translateY(-6px) rotate(1.2deg)}}
.pill{position:absolute;left:50%;transform:translateX(-50%);z-index:30;white-space:nowrap;border-radius:999px;font-weight:700}
"""

BASE_JS = r"""
function rnd(a,b){return a+Math.random()*(b-a)}
function initSky(stage,o){
  const sky=stage.querySelector('.stars');
  if(sky){for(let i=0;i<o.stars;i++){const s=document.createElement('i');s.className='star';const z=rnd(1,2.8);
    s.style.cssText='left:'+rnd(0,100)+'%;top:'+rnd(0,60)+'%;width:'+z+'px;height:'+z+'px;animation-delay:'+rnd(0,3)+'s;animation-duration:'+rnd(1.6,3.4)+'s';sky.appendChild(s);}}
  const bl=stage.querySelector('.bgls');
  if(bl){for(let i=0;i<o.lanterns;i++){const l=document.createElement('i');l.className='bgl';
    l.style.cssText='left:'+rnd(2,96)+'%;--s:'+rnd(16,34)+'px;--d:'+rnd(20,34)+'s;--dl:'+(-rnd(0,30))+'s';bl.appendChild(l);}}
}
"""

SKY_HTML = '<div class="stars"></div><div class="moon"></div><div class="bgls"></div><div class="water"><div class="reflect"></div><div class="wave w1"></div><div class="wave w2"></div><div class="wave w3"></div></div>'


def _json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def _page(body: str, css: str, js: str) -> str:
    return (
        '<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<link rel="stylesheet" href="{FONT_URL}">'
        f"<style>{BASE_CSS}{css}</style></head><body>{body}<script>{BASE_JS}{js}</script></body></html>"
    )


# ════════════════════════════ หน้าเปิด / หน้าจบ ════════════════════════════
_INTRO_CSS = r"""
.stage .moon{top:3.5%;right:auto;left:50%;transform:translateX(-50%);width:clamp(60px,17vw,90px)}
.stage .reflect{right:auto;left:50%;margin-left:calc(clamp(90px,26vw,150px)/-2)}
.title{position:absolute;top:22%;left:0;right:0;text-align:center;z-index:5;padding:0 14px}
.title .tag{display:inline-block;font-size:12px;letter-spacing:1.5px;padding:3px 12px;border-radius:999px;background:rgba(255,230,160,.18);color:#ffe6a8;border:1px solid rgba(255,230,160,.4)}
.title h1{font-family:'Itim','Mali',sans-serif;font-weight:400;font-size:clamp(27px,8.2vw,46px);line-height:1.2;margin-top:8px;color:#fff7dc;text-shadow:0 0 18px rgba(255,214,120,.85),0 2px 0 rgba(0,0,0,.25)}
.title p{margin-top:6px;font-size:clamp(13px,3.6vw,16px);color:#f0e3ff}
.boatpos{position:absolute;left:0;right:0;bottom:15%;display:flex;justify-content:center;z-index:6}
.boatwrap{width:clamp(190px,58vw,310px);animation:bob 3.4s ease-in-out infinite}
.compact .title{top:19%}.compact .title h1{font-size:clamp(25px,7.4vw,40px);margin-top:6px}.compact .boatpos{bottom:5%}.compact .boatwrap{width:clamp(150px,44vw,230px)}
.foot{position:absolute;left:0;right:0;bottom:3.5%;text-align:center;font-size:clamp(12px,3.4vw,15px);color:#ffe6a8;z-index:6;text-shadow:0 1px 6px rgba(0,0,0,.5)}
"""


def intro_html(faces: dict, title: str, subtitle: str, tag: str = "Happy Anniversary 🌕", foot: str = "", compact: bool = False) -> str:
    boat = boat_svg(faces.get("me"), faces.get("partner"), "i")
    title, subtitle, tag, foot = (_html.escape(x) for x in (title, subtitle, tag, foot))
    title = title.replace("\n", "<br>")
    body = (
        f'<div class="stage{" compact" if compact else ""}">{SKY_HTML}'
        f'<div class="title"><span class="tag">{tag}</span><h1>{title}</h1><p>{subtitle}</p></div>'
        f'<div class="boatpos"><div class="boatwrap">{boat}</div></div>'
        + (f'<div class="foot">{foot}</div>' if foot else "")
        + "</div>"
    )
    return _page(body, _INTRO_CSS, "initSky(document.querySelector('.stage'),{stars:80,lanterns:12});")


# ════════════════════════════ แล่นเรือความทรงจำ ════════════════════════════
_SAIL_CSS = r"""
.boatwrap.sail{position:absolute;left:3%;bottom:15%;width:clamp(150px,42vw,235px);z-index:6;animation:bob 3.2s ease-in-out infinite}
#pols{position:absolute;inset:0;z-index:8;pointer-events:none}
.pol{position:absolute;width:clamp(110px,40vw,205px);background:#fffdf6;padding:7px 7px 24px;border-radius:5px;opacity:0;
 box-shadow:0 8px 22px rgba(0,0,0,.45),0 0 26px rgba(255,214,130,.35);will-change:transform,opacity}
.pol img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 38%;border-radius:2px;background:#eee}
.pol .cap{position:absolute;left:6px;right:6px;bottom:3px;text-align:center;font-size:clamp(10px,2.8vw,13px);color:#6b4a8a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pol .tape{position:absolute;top:-9px;left:50%;width:46px;height:16px;margin-left:-23px;background:rgba(255,224,138,.8);transform:rotate(-3deg);border-radius:2px}
.pill-top{position:absolute;top:10px;left:10px;z-index:30;font-size:12px;padding:5px 12px;border-radius:999px;background:rgba(20,12,60,.55);border:1px solid rgba(255,230,160,.35);color:#ffe6a8;backdrop-filter:blur(4px)}
.pill-bottom{bottom:9%;padding:9px 20px;font-size:clamp(13px,3.7vw,16px);background:linear-gradient(135deg,#ffe27a,#ffc23d);color:#5a3500;box-shadow:0 0 20px rgba(255,200,70,.55)}
.hint{position:absolute;left:0;right:0;bottom:3.2%;text-align:center;font-size:11px;color:#e7dcff;opacity:.85;z-index:30}
#confetti{position:absolute;inset:0;z-index:40;pointer-events:none}
.finale{position:absolute;inset:0;z-index:25;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:22% 14px 0;gap:12px;text-align:center;
 background:radial-gradient(circle at 50% 38%,rgba(18,9,56,.62),rgba(18,9,56,.12) 72%);opacity:0;pointer-events:none;transition:opacity 1.2s}
.finale.show{opacity:1}
.fin-text{font-family:'Itim','Mali',sans-serif;font-size:clamp(28px,8.6vw,46px);line-height:1.2;color:#fff7dc;text-shadow:0 0 18px rgba(255,214,120,.95),0 2px 0 rgba(0,0,0,.3);min-height:1.3em}
.fin-text::after{content:'▍';margin-left:2px;animation:blink .8s steps(1) infinite;color:#ffd166}
.fin-sub{font-size:clamp(13px,3.8vw,17px);color:#ffe6a8;opacity:0;transition:opacity 1s}
.fin-sub.show{opacity:1}
#replay{pointer-events:auto;margin-top:4px;border:1px solid rgba(255,230,160,.5);background:rgba(255,255,255,.1);color:#fff0c8;border-radius:999px;padding:5px 14px;font:inherit;font-size:12px;cursor:pointer}
.pause-ico{position:absolute;top:50%;left:50%;width:70px;height:70px;margin:-35px 0 0 -35px;border-radius:50%;z-index:45;display:grid;place-items:center;font-size:28px;background:rgba(20,12,60,.65);opacity:0;transition:opacity .2s;pointer-events:none}
.pause-ico.show{opacity:1}
@keyframes blink{50%{opacity:0}}
"""

_SAIL_JS = r"""
(function(){
const D=__DATA__;
const stage=document.getElementById('stage');
initSky(stage,{stars:70,lanterns:10});
const pols=document.getElementById('pols'),boat=document.getElementById('boat');
const counter=document.getElementById('counter'),statusEl=document.getElementById('status');
const finale=document.getElementById('finale'),finText=document.getElementById('finText'),finSub=document.getElementById('finSub');
const ico=document.getElementById('pauseIco');
const N=D.photos.length,INTERVAL=D.interval,LIFE=INTERVAL*2-0.2,START=0.8;
const FIN_AT=START+(N-1)*INTERVAL+LIFE*0.55;
boat.animate([{left:'3%'},{left:'44%'}],{duration:(FIN_AT+3)*1000,fill:'forwards',easing:'ease-in-out'});
let t=0,last=null,paused=false,idx=0,done=false,held=[],confTimer=0;

/* ---------- confetti ---------- */
const cv=document.getElementById('confetti'),ctx=cv.getContext('2d');let parts=[];
function fit(){const r=stage.getBoundingClientRect(),d=window.devicePixelRatio||1;cv.width=r.width*d;cv.height=r.height*d;ctx.setTransform(d,0,0,d,0,0)}
fit();addEventListener('resize',fit);
const COLORS=['#ffd166','#ff9ec7','#8ecbff','#b9a0ff','#fff3b0','#ff8a5c'];
function burst(n,top){const w=stage.clientWidth,h=stage.clientHeight;
  for(let i=0;i<n;i++)parts.push({x:top?rnd(0,w):w/2+rnd(-30,30),y:top?-10:h*.34,vx:top?rnd(-25,25):rnd(-240,240),vy:top?rnd(40,110):rnd(-340,-80),
    w:rnd(4,8),h:rnd(6,12),r:rnd(0,6.28),vr:rnd(-6,6),c:COLORS[(Math.random()*COLORS.length)|0]});}
function stepParts(dt){const h=stage.clientHeight;ctx.clearRect(0,0,stage.clientWidth,h);
  parts=parts.filter(p=>p.y<h+20);
  for(const p of parts){p.vy+=300*dt;if(p.vy>170)p.vy=170;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=0.99;p.r+=p.vr*dt;
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.r);ctx.fillStyle=p.c;ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();}}

/* ---------- photos ---------- */
const SLOTS=[4,52],TOPS=[10,22];
function spawn(i){
  const p=D.photos[i],el=document.createElement('div');el.className='pol';
  const tape=document.createElement('i');tape.className='tape';
  const im=document.createElement('img');im.src=p.src;im.alt='';im.style.aspectRatio=Math.min(1.4,Math.max(.72,p.ar||.8));
  const cap=document.createElement('div');cap.className='cap';cap.textContent=p.cap||'';
  el.append(tape,im,cap);
  el.style.left=(SLOTS[i%2]+rnd(-1.5,1.5))+'%';el.style.top=(TOPS[i%2]+rnd(-1.5,1.5))+'%';el.style.zIndex=10+i;
  pols.appendChild(el);
  const rot=rnd(-5,5),br=boat.getBoundingClientRect(),er=el.getBoundingClientRect();
  const dx=(br.left+br.width*.3)-(er.left+er.width/2),dy=(br.top+br.height*.2)-(er.top+er.height/2);
  const a=el.animate([
    {offset:0,transform:'translate('+dx+'px,'+dy+'px) scale(.12) rotate(0deg)',opacity:0},
    {offset:.13,transform:'translate(0,0) scale(1) rotate('+rot+'deg)',opacity:1},
    {offset:.5,transform:'translate(0,-9px) scale(1.02) rotate('+(rot*.6)+'deg)',opacity:1},
    {offset:.86,transform:'translate(0,-3px) scale(1) rotate('+rot+'deg)',opacity:1},
    {offset:1,transform:'translate(0,-46px) scale(.96) rotate('+rot+'deg)',opacity:0}
  ],{duration:LIFE*1000,fill:'forwards',easing:'ease-in-out'});
  a.onfinish=()=>el.remove();
  counter.textContent='ความทรงจำ: '+(i+1)+' / '+N;
}

/* ---------- finale ---------- */
function typeWrite(el,text,ms,cb){const ch=Array.from(text);let i=0;el.textContent='';
  (function step(){i++;el.textContent=ch.slice(0,i).join('');if(i<ch.length)setTimeout(step,ms);else if(cb)cb();})();}
function finish(){done=true;statusEl.textContent='👇 กดปุ่มด้านล่าง ไปลอยกระทงด้วยกันนะ';
  finale.classList.add('show');burst(170,false);
  typeWrite(finText,D.endText,95,()=>{finSub.textContent=D.endSub;finSub.classList.add('show');});}

/* ---------- pause / play ---------- */
function setPaused(p){if(done)return;paused=p;
  if(p){held=document.getAnimations().filter(a=>a.playState==='running');held.forEach(a=>a.pause());}
  else{held.forEach(a=>a.play());held=[];}
  ico.classList.toggle('show',p);}
stage.addEventListener('click',e=>{if(e.target.closest('button'))return;setPaused(!paused);});
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();setPaused(!paused);}});
document.getElementById('replay').onclick=()=>location.reload();

function loop(ts){
  if(last===null)last=ts;const dt=Math.min(.1,(ts-last)/1000);last=ts;
  if(!paused){
    t+=dt;
    if(idx<N&&t>=START+idx*INTERVAL){spawn(idx);idx++;}
    if(!done&&t>=FIN_AT)finish();
    if(done){confTimer+=dt;if(confTimer>.14){confTimer=0;burst(2,true);}}
    stepParts(dt);
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
"""


def sail_duration(n_photos: int, interval: float, end_text: str) -> float:
    """เวลาทั้งหมด (วินาที) ที่ฉากแล่นเรือใช้จนข้อความจบ — ใช้ล็อกปุ่ม 'ไปต่อ' ฝั่ง Python"""
    life = interval * 2 - 0.2
    return 0.8 + (n_photos - 1) * interval + life * 0.55 + len(end_text) * 0.095 + 1.2


def sail_html(photos: list[dict], faces: dict, interval: float, end_text: str, end_sub: str) -> str:
    n = len(photos)
    data = _json({"photos": photos, "interval": interval, "endText": end_text, "endSub": end_sub})
    boat = boat_svg(faces.get("me"), faces.get("partner"), "s")
    body = (
        f'<div class="stage" id="stage">{SKY_HTML}'
        f'<div class="boatwrap sail" id="boat">{boat}</div>'
        '<div id="pols"></div>'
        f'<div class="pill-top" id="counter">ความทรงจำ: 0 / {n}</div>'
        '<div class="pill pill-bottom" id="status">⛵ กำลังแล่นเรือชมความทรงจำ...</div>'
        '<div class="hint">แตะที่หน้าจอเพื่อหยุด / เล่นต่อ</div>'
        '<div class="finale" id="finale"><div class="fin-text" id="finText"></div>'
        '<div class="fin-sub" id="finSub"></div><button id="replay">↻ ดูอีกครั้ง</button></div>'
        '<canvas id="confetti"></canvas><div class="pause-ico" id="pauseIco">⏸</div></div>'
    )
    return _page(body, _SAIL_CSS, _SAIL_JS.replace("__DATA__", data))


# ════════════════════════════ พรีวิวกระทงคู่ ════════════════════════════
_PAIR_CSS = r"""
.stage{background:linear-gradient(180deg,#120c3d 0%,#2a1b6b 45%,#5b2f8e 62%,#2c1c68 63%,#140e3b 100%)}
.stage .moon{top:6%;width:56px;right:auto;left:50%;transform:translateX(-50%)}
.row{position:absolute;left:0;right:0;bottom:7%;display:flex;justify-content:center;gap:4%;padding:0 4%;z-index:5}
.col{width:42%;max-width:210px;text-align:center}
.col .k{animation:bob 3.6s ease-in-out infinite}
.col:nth-child(2) .k{animation-delay:-1.6s}
.col .nm{display:inline-block;margin-top:4px;font-size:clamp(10px,2.9vw,13px);white-space:nowrap;padding:3px 10px;border-radius:999px;background:rgba(20,12,60,.6);border:1px solid rgba(255,230,160,.4);color:#ffe6a8}
.col .nm b{color:#fff}
"""


def pair_preview_html(my_style: dict, partner_style: dict, my_name: str, partner_name: str) -> str:
    my_name, partner_name = _html.escape(my_name), _html.escape(partner_name)
    body = (
        f'<div class="stage">{SKY_HTML}<div class="row">'
        f'<div class="col"><div class="k">{krathong_svg(my_style)}</div><span class="nm">ของ<b>{my_name}</b> (ตกแต่งไว้แล้ว)</span></div>'
        f'<div class="col"><div class="k">{krathong_svg(partner_style)}</div><span class="nm">ของ<b>{partner_name}</b> (ตกแต่งเลย ✨)</span></div>'
        "</div></div>"
    )
    return _page(body, _PAIR_CSS, "initSky(document.querySelector('.stage'),{stars:46,lanterns:6});")


# ════════════════════════════ ปล่อยโคม + ลอยกระทง ════════════════════════════
_FLOAT_CSS = r"""
.stage .moon{top:4%;right:auto;left:50%;transform:translateX(-50%)}
.stage .reflect{right:auto;left:50%;margin-left:calc(clamp(90px,26vw,150px)/-2)}
.lan{position:absolute;width:clamp(134px,40vw,208px);z-index:12;transform-origin:50% 0;opacity:0}
.lan.sway{opacity:1;animation:sway 4.6s ease-in-out infinite alternate}
@keyframes sway{from{transform:translateY(0) rotate(-2deg)}to{transform:translateY(-8px) rotate(2deg)}}
.lan .cap-t{height:13px;margin:0 14%;background:linear-gradient(#c8742a,#8b4513);border-radius:9px 9px 0 0}
.lan .body{position:relative;padding:15px 12px 20px;text-align:center;color:#5b2a00;
 border-radius:16px 16px 26px 26px/16px 16px 34px 34px;
 background:radial-gradient(ellipse at 50% 58%,#fff3c2 0%,#ffd06e 55%,#ff9f45 100%);
 box-shadow:0 0 30px 10px rgba(255,170,60,.6),inset 0 0 20px rgba(255,255,255,.6)}
.lan .owner{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:#d9622b;padding:2px 10px;border-radius:999px;margin-bottom:8px}
.lan .wish{font-size:clamp(13px,3.8vw,17px);line-height:1.45;font-weight:700;overflow-wrap:break-word}
.lan .cap-b{height:10px;margin:0 20%;background:#8b4513;border-radius:0 0 9px 9px}
.lan .tassel{width:2px;height:24px;margin:0 auto;background:#d9a441;position:relative}
.lan .tassel::after{content:"";position:absolute;bottom:-9px;left:-5px;width:12px;height:12px;border-radius:50%;background:#ff8fab}
.krath{position:absolute;bottom:8%;width:clamp(140px,41vw,215px);z-index:6;opacity:0}
.krath.on{opacity:1;animation:drift 5.2s ease-in-out infinite}
@keyframes drift{0%,100%{transform:translate(0,0) rotate(-1.6deg)}50%{transform:translate(9px,-5px) rotate(1.6deg)}}
.rip{position:absolute;left:8%;right:8%;bottom:-2%;height:16%;border:2px solid rgba(255,255,255,.4);border-radius:50%;animation:rip 3.2s ease-out infinite}
.rip.b{animation-delay:-1.6s}
@keyframes rip{0%{transform:scale(.6);opacity:.8}100%{transform:scale(1.5,1.9);opacity:0}}
.nm{position:absolute;bottom:1.6%;z-index:7;font-size:clamp(11px,3.1vw,13px);white-space:nowrap;padding:3px 12px;border-radius:999px;background:rgba(20,12,60,.6);border:1px solid rgba(255,230,160,.4);color:#ffe6a8;transform:translateX(-50%)}
.pill-bottom{bottom:29%;padding:8px 18px;font-size:clamp(12px,3.4vw,15px);background:rgba(20,12,60,.62);border:1px solid rgba(255,230,160,.5);color:#ffe9b0;backdrop-filter:blur(4px);transition:opacity .6s}
"""

_FLOAT_JS = r"""
(function(){
const D=__DATA__;
const stage=document.getElementById('stage');
initSky(stage,{stars:70,lanterns:12});
const H=stage.clientHeight;
function lantern(id,text,owner,delay){
  const el=document.getElementById(id);if(!el)return;
  el.querySelector('.wish').textContent=text;el.querySelector('.owner').textContent=owner;
  const dy=H-el.getBoundingClientRect().top+30;
  const a=el.animate([
    {transform:'translateY('+dy+'px) scale(.35)',opacity:0},
    {offset:.12,opacity:1},
    {transform:'translateY(0) scale(1)',opacity:1}
  ],{duration:7600,delay:delay,easing:'cubic-bezier(.22,.7,.25,1)',fill:'both'});
  a.onfinish=()=>{a.cancel();el.classList.add('sway');};
}
function krathong(id,delay){
  const el=document.getElementById(id);
  const a=el.animate([{transform:'translateY(-46px) scale(.7)',opacity:0},{transform:'translateY(0) scale(1)',opacity:1}],
    {duration:900,delay:delay,easing:'cubic-bezier(.3,1.4,.5,1)',fill:'both'});
  a.onfinish=()=>{a.cancel();el.classList.add('on');};
}
krathong('k1',300);krathong('k2',900);
lantern('l1',D.my.wish,D.my.owner,1300);
lantern('l2',D.partner.wish,D.partner.owner,2700);
setTimeout(()=>{const s=document.getElementById('status');s.style.opacity=0;
  setTimeout(()=>{s.textContent=D.doneText;s.style.opacity=1;},600);},11000);
})();
"""


def float_html(my_wish: str, partner_wish: str, my_style: dict, partner_style: dict, my_name: str, partner_name: str) -> str:
    data = _json(
        {
            "my": {"wish": my_wish, "owner": f"ของ{my_name}"},
            "partner": {"wish": partner_wish, "owner": f"ของ{partner_name}"},
            "doneText": "🌕 คำอธิษฐานของเราลอยขึ้นฟ้าแล้ว",
        }
    )
    my_name_h, partner_name_h = _html.escape(my_name), _html.escape(partner_name)
    lan = (
        '<div class="lan" id="{id}" style="left:{left}%;top:{top}%"><div class="cap-t"></div>'
        '<div class="body"><span class="owner"></span><div class="wish"></div></div>'
        '<div class="cap-b"></div><div class="tassel"></div></div>'
    )
    body = (
        f'<div class="stage" id="stage">{SKY_HTML}'
        + (lan.format(id="l1", left=4, top=9) if my_wish.strip() else "")
        + lan.format(id="l2", left=54 if my_wish.strip() else 29, top=21 if my_wish.strip() else 14)
        + f'<div class="krath" id="k1" style="left:6%">{krathong_svg(my_style)}<i class="rip"></i><i class="rip b"></i></div>'
        + f'<div class="krath" id="k2" style="left:53%">{krathong_svg(partner_style)}<i class="rip"></i><i class="rip b"></i></div>'
        + f'<span class="nm" style="left:27%">กระทงของ{my_name_h}</span><span class="nm" style="left:74%">กระทงของ{partner_name_h}</span>'
        + '<div class="pill pill-bottom" id="status">🏮 กำลังปล่อยโคมและลอยกระทง...</div></div>'
    )
    return _page(body, _FLOAT_CSS, _FLOAT_JS.replace("__DATA__", data))
