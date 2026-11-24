# -*- coding: utf-8 -*-
"""
Happy Anniversary — เทศกาลลอยกระทงของเรา 🌕
เว็บแอป Streamlit สำหรับส่งลิงก์ให้แฟนเปิดดูได้ตั้งแต่ต้นจนจบ

ลำดับหน้า:  0 เริ่ม → 1 แล่นเรือความทรงจำ → 2 ตกแต่งกระทง & อธิษฐาน → 3 ปล่อยโคม/ลอยกระทง → 4 จดหมาย
รัน:  streamlit run app.py        (โหมดคนทำ: เติม ?edit=1 ต่อท้ายลิงก์)
"""
from __future__ import annotations

import html
import time

import streamlit as st
import streamlit.components.v1 as components

import assets
import config as C
import scenes

st.set_page_config(
    page_title=f"{C.APP_TITLE} 🌕",
    page_icon="🌕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

EDIT = str(st.query_params.get("edit", "")) == "1"
STEPS = ["เริ่ม", "ความทรงจำ", "กระทง", "ลอยโคม", "จดหมาย"]
CUSTOM = "__custom__"
esc = html.escape

# ───────────────────────────── ธีม / CSS ─────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Mali:wght@400;600;700&family=Itim&display=swap');
html, body, .stApp, .stApp * { font-family: 'Mali','Itim','Leelawadee UI','Sarabun',sans-serif; }
.stApp {
  background:
    radial-gradient(900px 500px at 85% -8%, rgba(255,214,130,.20), transparent 62%),
    linear-gradient(180deg,#120c36 0%,#1d1452 55%,#2d1b66 100%);
}
header[data-testid="stHeader"], footer, #MainMenu, [data-testid="stToolbar"] { display:none !important; }

/* บังคับสีเอง ไม่พึ่ง .streamlit/config.toml (กันตัวหนังสือจางเมื่อเบราว์เซอร์/คลาวด์ใช้ธีมสว่าง) */
.stApp { color:#fff4e0; color-scheme:dark; }
.stApp label, .stApp label p, .stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stRadio"] label p, .stApp [data-testid="stRadio"] label div,
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color:#fff4e0 !important; }
.stApp [data-testid="stRadio"] label div[data-baseweb="radio"] > div:first-child {
  background-color:#ffffff !important; border-color:#ffd166 !important; }
.stApp [data-testid="stRadio"] label div[data-baseweb="radio"] > div:first-child > div { background-color:#ff9f45 !important; }
.stApp [data-testid="stRadio"] label[data-checked="true"] div[data-baseweb="radio"] > div:first-child { background-color:#ff9f45 !important; border-color:#ff9f45 !important; }
.stApp [data-testid="stRadio"] label[data-checked="true"] div[data-baseweb="radio"] > div:first-child > div { background-color:#ffffff !important; }
.stApp input, .stApp textarea { color:#2b1b4d !important; background:#fff8ea !important; -webkit-text-fill-color:#2b1b4d; }
.stApp input::placeholder, .stApp textarea::placeholder { color:#8a7aa8 !important; -webkit-text-fill-color:#8a7aa8; }.block-container { max-width: 720px; padding-top: 1.1rem; padding-bottom: 3rem; }
iframe { border: 0 !important; border-radius: 22px; }

.stButton > button {
  width:100%; border:0; border-radius:999px; padding:.8rem 1.2rem; font-weight:700; font-size:1.05rem;
  background:linear-gradient(135deg,#ffd166,#ff9f45); color:#4a2300;
  box-shadow:0 6px 18px rgba(255,159,69,.35); transition:transform .15s, box-shadow .15s;
}
.stButton > button p { color:#4a2300 !important; font-weight:700; }
.stButton > button:hover { transform:translateY(-1px) scale(1.01); box-shadow:0 10px 24px rgba(255,159,69,.5); color:#4a2300; }
.stButton > button:disabled { background:rgba(255,255,255,.14); box-shadow:none; opacity:.8; }
.stButton > button:disabled p { color:#d9ccff !important; }

.stepper { display:flex; justify-content:center; align-items:center; margin:.1rem 0 .15rem; }
.stepper .dot { width:26px; height:26px; border-radius:50%; display:grid; place-items:center; font-size:12px; font-weight:700;
  background:rgba(255,255,255,.12); color:#cdbff5; }
.stepper .dot.on { background:linear-gradient(135deg,#ffd166,#ff9f45); color:#4a2300; box-shadow:0 0 14px rgba(255,190,90,.75); }
.stepper .dot.done { background:#7ad7a3; color:#14402a; }
.stepper .line { height:2px; width:26px; background:rgba(255,255,255,.18); }
.stepper .line.done { background:#7ad7a3; }
.step-label { text-align:center; font-size:.88rem; color:#ffe6a8; margin-bottom:.7rem; }

.hd h2 { font-family:'Itim','Mali',sans-serif; text-align:center; color:#fff4cf; margin:.2rem 0 .1rem; font-size:1.65rem; font-weight:400; }
.hd p { text-align:center; color:#d9ccff; font-size:.95rem; margin:0 0 .8rem; }
.sec { color:#ffe6a8; font-weight:700; font-size:1.02rem; margin:1rem 0 .1rem; }

.letter { position:relative; background:linear-gradient(180deg,#fffbe9,#fff0c6); color:#4a3320; border-radius:22px;
  padding:1.7rem 1.4rem 1.3rem; box-shadow:0 14px 40px rgba(0,0,0,.38); border:2px solid #ffe08a; margin:.6rem 0 1.1rem; }
.letter::before { content:""; position:absolute; top:-12px; left:50%; width:96px; height:24px; margin-left:-48px;
  background:rgba(255,196,110,.8); transform:rotate(-2deg); border-radius:4px; }
.letter .tag { display:inline-block; background:#ffe6ef; color:#c2406f; border-radius:999px; padding:.1rem .75rem; font-size:.78rem; }
.letter h2 { font-family:'Itim','Mali',sans-serif; font-weight:400; font-size:1.7rem; color:#5a2a82; margin:.45rem 0 .3rem; }
.letter p { font-size:1.05rem; line-height:1.95; margin:.5rem 0; color:#4a3320; opacity:0; animation:fadeUp .9s ease forwards; }
.letter p:nth-of-type(1) { animation-delay:.2s; font-weight:700; color:#c2406f; }
.letter p:nth-of-type(2) { animation-delay:1.1s; }
.letter p:nth-of-type(3) { animation-delay:2.0s; }
.letter .sig { text-align:right; font-size:1.05rem; color:#7a4a8a; margin-top:.8rem; opacity:0; animation:fadeUp .9s 2.8s ease forwards; }
@keyframes fadeUp { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
"""

HIDE_SIDEBAR = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display:none !important; }
"""


# ───────────────────────────── helpers ─────────────────────────────
@st.cache_data(show_spinner="กำลังเตรียมความทรงจำ ...")
def _photos(sig):  # sig ใช้เป็น key ให้ cache รีเฟรชเมื่อไฟล์รูปเปลี่ยน
    return assets.load_photos()


@st.cache_data(show_spinner=False)
def _faces(sig):
    return assets.load_faces()


def render_scene(page_html: str, height: int) -> None:
    components.html(page_html, height=height, scrolling=False)


def pill_button(label: str, key: str, disabled: bool = False) -> bool:
    try:
        return st.button(label, key=key, disabled=disabled, width="stretch")
    except TypeError:  # Streamlit รุ่นเก่า
        return st.button(label, key=key, disabled=disabled, use_container_width=True)


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("step", 0)
    ss.setdefault("sail_t0", 0.0)
    for k, v in scenes.DEFAULT_STYLE.items():
        ss.setdefault(f"p_{k}", v)
    ss.setdefault("wish_choice", C.WISH_OPTIONS[0])
    ss.setdefault("wish_custom", "")


def go(step: int) -> None:
    st.session_state.step = step
    if step == 1:
        st.session_state.sail_t0 = time.time()
    st.rerun()


def partner_style() -> dict:
    return {k: st.session_state.get(f"p_{k}", v) for k, v in scenes.DEFAULT_STYLE.items()}


def stepper(step: int) -> None:
    parts = []
    for i in range(len(STEPS)):
        cls = "on" if i == step else ("done" if i < step else "")
        parts.append(f'<div class="dot {cls}">{"✓" if i < step else i + 1}</div>')
        if i < len(STEPS) - 1:
            parts.append(f'<div class="line {"done" if i < step else ""}"></div>')
    st.markdown(
        f'<div class="stepper">{"".join(parts)}</div><div class="step-label">{esc(STEPS[step])}</div>',
        unsafe_allow_html=True,
    )


def heading(title: str, sub: str = "") -> None:
    st.markdown(f'<div class="hd"><h2>{esc(title)}</h2><p>{esc(sub)}</p></div>', unsafe_allow_html=True)


# ───────────────────────────── หน้า 0: เริ่ม ─────────────────────────────
def page_intro(faces: dict) -> None:
    render_scene(
        scenes.intro_html(faces, C.INTRO_TITLE, C.INTRO_SUBTITLE, tag=f"{C.APP_TITLE} 🌕"),
        C.INTRO_HEIGHT,
    )
    st.write("")
    if pill_button("เริ่มแล่นเรือชมความทรงจำ ⛵", "start"):
        go(1)


# ───────────────────────────── หน้า 1: แล่นเรือความทรงจำ ─────────────────────────────
@st.fragment(run_every=2)
def sail_next(total: float) -> None:
    left = total - (time.time() - st.session_state.sail_t0)
    if C.LOCK_NEXT_UNTIL_SAIL_ENDS and not EDIT and left > 0:
        pill_button(f"⛵ กำลังแล่นเรือ… ดูให้จบก่อนนะ (อีกราว {int(left) + 1} วิ)", "sail_locked", disabled=True)
    elif pill_button("ไปลอยกระทงด้วยกัน 🏮", "to_wish"):
        go(2)


def page_sail(photos: list, faces: dict) -> None:
    render_scene(
        scenes.sail_html(photos, faces, C.SECONDS_PER_PHOTO, C.SAIL_END_TEXT, C.SAIL_END_SUB),
        C.SAIL_HEIGHT,
    )
    st.write("")
    total = scenes.sail_duration(len(photos), C.SECONDS_PER_PHOTO, C.SAIL_END_TEXT) + 3  # +3 วิ เผื่อโหลดฉาก
    sail_next(total)


# ───────────────────────────── หน้า 2: ตกแต่งกระทง + คำอธิษฐาน ─────────────────────────────
def page_decorate() -> None:
    heading(
        "ตกแต่งกระทง & อธิษฐาน",
        f"กระทงของ{C.ME_NAME}ตกแต่งรอไว้แล้ว — ส่วนของ{C.PARTNER_NAME} ตกแต่งเองได้เลย แล้วลอยไปด้วยกัน",
    )
    render_scene(
        scenes.pair_preview_html(C.ME_KRATHONG, partner_style(), C.ME_NAME, C.PARTNER_NAME), 290
    )

    st.markdown(f'<div class="sec">🎨 ตกแต่งกระทงของ{esc(C.PARTNER_NAME)}</div>', unsafe_allow_html=True)
    st.radio("ฐานกระทง", list(scenes.BASE_LABELS), format_func=scenes.BASE_LABELS.get, key="p_base", horizontal=True)
    st.radio("ดอกไม้", list(scenes.FLOWER_LABELS), format_func=scenes.FLOWER_LABELS.get, key="p_flower", horizontal=True)
    st.radio("เทียน", list(scenes.CANDLE_LABELS), format_func=scenes.CANDLE_LABELS.get, key="p_candle", horizontal=True)
    st.radio("สติกเกอร์", list(scenes.STICKER_LABELS), format_func=scenes.STICKER_LABELS.get, key="p_sticker", horizontal=True)

    if EDIT:
        st.caption("โหมดคนทำ: อยากใช้ลุคนี้เป็นกระทงของตัวเอง ก๊อปบรรทัดนี้ไปวางทับ ME_KRATHONG ใน config.py")
        st.code(f"ME_KRATHONG = {partner_style()!r}", language="python")

    st.markdown('<div class="sec">🙏 เลือกคำอธิษฐาน</div>', unsafe_allow_html=True)
    choices = list(C.WISH_OPTIONS) + [CUSTOM]
    st.radio(
        "คำอธิษฐาน",
        choices,
        format_func=lambda x: "✍️ พิมพ์คำอธิษฐานเอง" if x == CUSTOM else x,
        key="wish_choice",
        label_visibility="collapsed",
    )
    if st.session_state.wish_choice == CUSTOM:
        st.text_input(
            "พิมพ์คำอธิษฐานตรงนี้",
            key="wish_custom",
            max_chars=C.WISH_MAX_CHARS,
            placeholder="พิมพ์คำอธิษฐานของเธอตรงนี้ …",
        )
        wish = st.session_state.wish_custom.strip()
    else:
        wish = st.session_state.wish_choice

    st.write("")
    if pill_button("ปล่อยโคม & ลอยกระทงด้วยกัน 🏮", "to_float", disabled=not wish):
        st.session_state.final_wish = wish
        st.session_state.final_style = partner_style()
        go(3)
    if not wish:
        st.caption("พิมพ์คำอธิษฐานก่อน แล้วปุ่มจะกดได้นะ 💛")


# ───────────────────────────── หน้า 3: ปล่อยโคม + ลอยกระทง ─────────────────────────────
def page_float() -> None:
    wish = st.session_state.get("final_wish") or C.WISH_OPTIONS[0]
    style = st.session_state.get("final_style") or partner_style()
    render_scene(
        scenes.float_html(C.ME_WISH, wish, C.ME_KRATHONG, style, C.ME_NAME, C.PARTNER_NAME),
        C.FLOAT_HEIGHT,
    )
    st.write("")
    if pill_button("ไปอ่านจดหมาย 💌", "to_letter"):
        go(4)


# ───────────────────────────── หน้า 4: จดหมาย ─────────────────────────────
def page_letter(faces: dict) -> None:
    paras = "".join(f"<p>{esc(t)}</p>" for t in C.LETTER_PARAGRAPHS)
    st.markdown(
        f'<div class="letter"><span class="tag">💌 {esc(C.LETTER_TAG)}</span>'
        f"<h2>{esc(C.LETTER_TITLE)}</h2>{paras}"
        f'<div class="sig">{esc(C.LETTER_SIGNATURE)}</div></div>',
        unsafe_allow_html=True,
    )
    render_scene(
        scenes.intro_html(
            faces,
            C.END_TITLE,
            C.ANNIVERSARY_DATE_TEXT or C.END_SUBTITLE,
            tag="🏮 ลอยกระทงด้วยกันแล้ว",
            compact=True,
        ),
        C.END_HEIGHT,
    )
    st.write("")
    if pill_button("↻ ย้อนกลับไปดูตั้งแต่ต้น", "restart"):
        go(0)


# ───────────────────────────── main ─────────────────────────────
def main() -> None:
    st.markdown(f"<style>{CSS}{'' if EDIT else HIDE_SIDEBAR}</style>", unsafe_allow_html=True)
    init_state()

    photos, is_placeholder = _photos(assets.photos_signature())
    faces = _faces(assets.face_signature())

    if EDIT:
        with st.sidebar:
            st.markdown("### 🛠 โหมดคนทำ")
            for i, name in enumerate(STEPS):
                if st.button(f"{i + 1}. {name}", key=f"jump{i}"):
                    go(i)
            st.caption(f"รูปความทรงจำ: {'ยังไม่มี (ใช้รูปตัวอย่าง)' if is_placeholder else str(len(photos)) + ' รูป'}")
            st.caption(
                "ใบหน้า: "
                + ", ".join(f"{k} {'✓' if v else '✗'}" for k, v in (("me", faces.get('me')), ("partner", faces.get('partner'))))
            )

    step = st.session_state.step
    stepper(step)

    if EDIT and not C.ME_WISH.strip() and step in (2, 3):
        st.warning("ยังไม่ได้พิมพ์คำอธิษฐานของคุณ — ใส่ที่ ME_WISH ใน config.py (ตอนนี้บนโคมจะมีแค่ของแฟน)")

    if EDIT and is_placeholder and step == 1:
        st.info("ยังไม่มีรูปใน assets/photos/ — กำลังโชว์รูปตัวอย่าง ใส่รูปจริงแล้วรีเฟรชได้เลย")
    if EDIT and step in (0, 1, 4) and not all(faces.values()):
        st.info("ยังไม่มีรูปใบหน้าใน assets/faces/ (me.jpg / partner.jpg) — ตอนนี้ใช้หน้าตัวอย่างอยู่")

    if step == 0:
        page_intro(faces)
    elif step == 1:
        page_sail(photos, faces)
    elif step == 2:
        page_decorate()
    elif step == 3:
        page_float()
    else:
        page_letter(faces)


main()
