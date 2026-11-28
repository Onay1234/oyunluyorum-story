"""Oyunluyorum karusel tuş görselleri.

Kullanım (gen.py içinde, slayt HTML'i üreten kodda):

    import sys; sys.path.insert(0,'/home/claude/oyunluyorum-story/tools')
    from tus import combo, ico

    combo("dpad:down* > options > circle*")          # PS5 (varsayılan)
    combo("l2* + r2", platform='xbox')               # Xbox: LT + RT
    combo("dpad:left* > cross", title='NASIL YAPILIR')
    f"{ico('r3')} bir sonraki açıya geçer."          # metin içi küçük ikon

Sözdizimi:
    >  sırayla bas (ok çizilir)
    +  aynı anda bas (artı çizilir)
    *  basılı tut (altında BASILI TUT etiketi)
    dpad:up|down|left|right  yönü sarı yanar
Tuş adları: cross circle square triangle options share touchpad create
            l1 r1 l2 r2 l3 r3 ls rs dpad
    @2 çift bas (üstte 2× rozeti):  "triangle@2"

Video üstü (şeffaf PNG) için: overlay_html(spec, label, dim=(...)) — bkz. tus_video.py
Xbox karşılıkları otomatik: A B X Y, MENU, LB RB LT RT, LS RS.
"""

PS = {'cross': '#6EA8FF', 'circle': '#FF6B81', 'square': '#F78FC9', 'triangle': '#4ED49A'}
XB = {'cross': ('A', '#4ED49A'), 'circle': ('B', '#FF6B81'), 'square': ('X', '#6EA8FF'), 'triangle': ('Y', '#FFC50D')}
XB_TEXT = {'options': 'MENU', 'l1': 'LB', 'r1': 'RB', 'l2': 'LT', 'r2': 'RT', 'l3': 'LS', 'r3': 'RS', 'ls': 'LS', 'rs': 'RS',
           'share': 'VIEW', 'touchpad': 'VIEW', 'create': 'VIEW'}
PS_TEXT = {'options': 'OPTIONS', 'share': 'SHARE', 'create': 'CREATE', 'touchpad': 'TOUCHPAD',
           'l1': 'L1', 'r1': 'R1', 'l2': 'L2', 'r2': 'R2', 'l3': 'L3', 'r3': 'R3', 'ls': 'L', 'rs': 'R'}
YELLOW = '#FFC50D'
CAP_BG = '#241044'
CAP_BORDER = 'rgba(255,255,255,.38)'


def _svg(inner, size, vb=60):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {vb} {vb}" style="display:block">{inner}</svg>'


def _shape(name, platform):
    """Kare tuşun içindeki ikon (60x60 görünüm kutusu). Metin tuşlar için None döner."""
    if platform == 'xbox' and name in XB:
        ch, col = XB[name]
        return (f'<circle cx="30" cy="30" r="22" fill="none" stroke="{col}" stroke-width="4"/>'
                f'<text x="30" y="39" text-anchor="middle" font-size="26" font-weight="800" fill="{col}" '
                f'font-family="Poppins,sans-serif">{ch}</text>')
    if name == 'circle':
        return f'<circle cx="30" cy="30" r="17" fill="none" stroke="{PS["circle"]}" stroke-width="6"/>'
    if name == 'cross':
        return (f'<path d="M15 15 L45 45 M45 15 L15 45" stroke="{PS["cross"]}" stroke-width="6" '
                f'stroke-linecap="round" fill="none"/>')
    if name == 'square':
        return f'<rect x="14" y="14" width="32" height="32" rx="5" fill="none" stroke="{PS["square"]}" stroke-width="6"/>'
    if name == 'triangle':
        return (f'<path d="M30 12 L48 44 L12 44 Z" fill="none" stroke="{PS["triangle"]}" stroke-width="6" '
                f'stroke-linejoin="round"/>')
    return None


def _dpad(direction):
    arms = {'up': (24, 6, 12, 22), 'down': (24, 32, 12, 22), 'left': (6, 24, 22, 12), 'right': (32, 24, 22, 12)}
    out = ''
    for d, (x, y, w, h) in arms.items():
        col = YELLOW if d == direction else '#6F6A86'
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
    out += '<rect x="24" y="24" width="12" height="12" fill="#6F6A86"/>'
    return out


def _cap(inner_html, wide=False):
    w = 'auto' if wide else '118px'
    pad = '0 28px' if wide else '0'
    return (f'<div style="min-width:140px;width:{w};height:140px;box-sizing:border-box;padding:{pad};'
            f'background:{CAP_BG};border:3px solid {CAP_BORDER};border-radius:28px;display:flex;'
            f'align-items:center;justify-content:center;box-shadow:0 0 22px rgba(255,255,255,.12)">{inner_html}</div>')


def _text(t, size=30):
    return f'<div style="font-size:{size}px;font-weight:800;letter-spacing:1px;color:#fff;white-space:nowrap">{t}</div>'


def key(name, direction=None, platform='ps'):
    """Tek tuşun HTML'i (kutu içinde)."""
    name = name.lower()
    if name == 'dpad':
        return _cap(_svg(_dpad(direction), 92))
    sh = _shape(name, platform)
    if sh:
        return _cap(_svg(sh, 84))
    txt = (XB_TEXT if platform == 'xbox' else PS_TEXT).get(name, name.upper())
    if name in ('l3', 'r3', 'ls', 'rs'):
        # analog: yuvarlak içinde yazı
        return _cap(_svg(f'<circle cx="30" cy="30" r="22" fill="none" stroke="#fff" stroke-width="4"/>'
                         f'<text x="30" y="38" text-anchor="middle" font-size="20" font-weight="800" fill="#fff" '
                         f'font-family="Poppins,sans-serif">{txt}</text>', 74))
    return _cap(_text(txt, 38 if len(txt) <= 3 else 32), wide=len(txt) > 3)


def _sep(kind):
    if kind == '/':
        return f'<div style="font-size:26px;font-weight:800;color:{YELLOW};line-height:140px;letter-spacing:1px">VEYA</div>'
    if kind == '+':
        return f'<div style="font-size:48px;font-weight:800;color:{YELLOW};line-height:140px">+</div>'
    return ('<svg width="46" height="140" viewBox="0 0 46 140"><path d="M6 70 H36 M26 58 L38 70 L26 82" '
            f'stroke="{YELLOW}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def combo(spec, platform='ps', title='NASIL YAPILIR', hold_label='BASILI TUT'):
    """Kart halinde tuş dizisi. spec: "dpad:down* > options > circle*"."""
    items = []
    seq = [s.strip() for s in spec.replace('+', ' + ').replace('>', ' > ').split()]
    parts, cur = [], []
    for tok in seq:
        if tok in ('+', '>'):
            parts.append(tok)
        else:
            parts.append(tok)
    for tok in parts:
        if tok in ('+', '>'):
            items.append(_sep(tok))
            continue
        hold = tok.endswith('*')
        tok = tok.rstrip('*')
        name, _, arg = tok.partition(':')
        lab = (f'<div style="margin-top:12px;font-size:22px;font-weight:800;letter-spacing:1.5px;color:{YELLOW};'
               f'white-space:nowrap;height:26px">{hold_label}</div>') if hold else '<div style="margin-top:12px;height:26px"></div>'
        items.append(f'<div style="display:flex;flex-direction:column;align-items:center">'
                     f'{key(name, arg or None, platform)}{lab}</div>')
    head = (f'<div style="font-size:24px;font-weight:800;letter-spacing:3px;color:#03DDD2;text-align:center">{title}</div>'
            if title else '')
    return (f'<div style="background:#1A0630;border:2px solid rgba(255,255,255,.14);border-radius:28px;'
            f'padding:22px 24px 12px;display:flex;flex-direction:column;gap:18px;align-items:center">{head}'
            f'<div style="display:flex;align-items:flex-start;justify-content:center;gap:10px">{"".join(items)}</div></div>')


def ico(name, size=58, direction=None, platform='ps'):
    """Metin içi küçük tuş ikonu."""
    name = name.lower()
    if name == 'dpad':
        inner, vb = _dpad(direction), 60
    else:
        sh = _shape(name, platform)
        if sh:
            inner, vb = sh, 60
        else:
            txt = (XB_TEXT if platform == 'xbox' else PS_TEXT).get(name, name.upper())
            if name in ('l3', 'r3', 'ls', 'rs'):
                inner = (f'<circle cx="30" cy="30" r="24" fill="none" stroke="#fff" stroke-width="4"/>'
                         f'<text x="30" y="38" text-anchor="middle" font-size="24" font-weight="800" fill="#fff" '
                         f'font-family="Poppins,sans-serif">{txt}</text>')
                vb = 60
            else:
                w = max(56, 18 * len(txt) + 24)
                return (f'<span style="display:inline-flex;align-items:center;justify-content:center;height:{size}px;'
                        f'min-width:{size}px;padding:0 14px;box-sizing:border-box;margin:0 4px;background:{CAP_BG};'
                        f'border:2px solid {CAP_BORDER};border-radius:14px;font-size:{int(size*0.5)}px;font-weight:800;'
                        f'color:#fff;vertical-align:middle;letter-spacing:1px">{txt}</span>')
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;'
            f'margin:0 4px;background:{CAP_BG};border:2px solid {CAP_BORDER};border-radius:14px;vertical-align:middle">'
            f'<svg width="{int(size*0.72)}" height="{int(size*0.72)}" viewBox="0 0 {vb} {vb}">{inner}</svg></span>')


def overlay_html(spec, label=None, platform='ps', dim=(), hold_label='BASILI TUT'):
    """Video üstü tuş görseli (kartsız, şeffaf zemin için). dim: soluk gösterilecek tuş sıraları (0'dan).
    spec örn. "dpad:down* > options > circle*", "triangle@2", "dpad:left* + rs"."""
    toks = [t for t in spec.replace('+', ' + ').replace('>', ' > ').replace('/', ' / ').split()]
    items, idx = [], 0
    for tok in toks:
        if tok in ('+', '>', '/'):
            items.append(_sep(tok))
            continue
        hold = tok.endswith('*')
        tok = tok.rstrip('*')
        tok, _, rep = tok.partition('@')
        name, _, arg = tok.partition(':')
        badge = (f'<div style="position:absolute;top:-22px;right:-16px;background:{YELLOW};color:#1A0630;'
                 f'font-size:30px;font-weight:900;border-radius:20px;padding:2px 14px;line-height:38px">{rep}\u00d7</div>') if rep else ''
        lab = (f'<div style="margin-top:12px;font-size:22px;font-weight:800;letter-spacing:1.5px;color:{YELLOW};'
               f'white-space:nowrap;height:26px;text-shadow:0 2px 8px #000">{hold_label}</div>') if hold else \
              '<div style="margin-top:12px;height:26px"></div>'
        op = '.28' if idx in dim else '1'
        items.append(f'<div style="display:flex;flex-direction:column;align-items:center;opacity:{op}">'
                     f'<div style="position:relative">{key(name, arg or None, platform)}{badge}</div>{lab}</div>')
        idx += 1
    pill = (f'<div style="margin-top:6px;background:#22D3EE;color:#0B1B2B;font-size:30px;font-weight:800;'
            f'letter-spacing:3px;padding:8px 34px;border-radius:30px;box-shadow:0 4px 18px rgba(0,0,0,.5)">{label}</div>'
            if label else '')
    return (f'<div id="ov" style="display:inline-flex;flex-direction:column;align-items:center;gap:4px;padding:30px 40px 10px;'
            f'font-family:Poppins,sans-serif;filter:drop-shadow(0 6px 16px rgba(0,0,0,.55))">'
            f'<div style="display:flex;align-items:flex-start;justify-content:center;gap:10px">{"".join(items)}</div>{pill}</div>')
