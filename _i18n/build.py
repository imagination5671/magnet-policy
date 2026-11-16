# 5개 언어 조각(_i18n/*.html)을 한 주소의 페이지로 합친다.
# 휴대폰 언어(또는 주소 끝 #en 같은 표시)에 맞는 언어를 먼저 보여 주고, 위쪽 버튼으로 바꿀 수 있다.
# 자바스크립트가 꺼져 있으면 5개 언어가 차례로 모두 보인다.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
LANGS = [("ko", "한국어"), ("en", "English"), ("ja", "日本語"), ("zh-Hant", "繁體中文"), ("es", "Español")]
TITLE = {
    "privacy": {"ko": "Magnet 개인정보처리방침", "en": "Magnet Privacy Policy", "ja": "Magnet プライバシーポリシー",
                "zh-Hant": "Magnet 隱私權政策", "es": "Magnet Política de privacidad"},
    "terms": {"ko": "Magnet 이용약관", "en": "Magnet Terms of Use", "ja": "Magnet 利用規約",
              "zh-Hant": "Magnet 使用條款", "es": "Magnet Términos de uso"},
}
INDEX = {
    "ko": ("상상을 현실로", "Magnet 앱의 약관과 방침이에요.", "개인정보처리방침", "어떤 정보를 왜 받고 어떻게 지키는지",
           "이용약관", "서비스를 쓰는 규칙과 유료 이용권 안내", "문의하기"),
    "en": ("Make your imagination real", "Terms and policies for the Magnet app.", "Privacy Policy",
           "What we collect, why, and how we protect it", "Terms of Use", "Rules for the service and the paid subscription",
           "Contact us"),
    "ja": ("想像を現実に", "Magnetアプリの規約とポリシーです。", "プライバシーポリシー", "どんな情報をなぜ受け取り、どう守るか",
           "利用規約", "サービスのルールと有料プランのご案内", "お問い合わせ"),
    "zh-Hant": ("讓想像成真", "Magnet App 的條款與政策。", "隱私權政策", "我們收集哪些資訊、為什麼收集、如何保護",
                "使用條款", "服務規則與付費訂閱說明", "聯絡我們"),
    "es": ("Haz real tu imaginación", "Términos y políticas de la app Magnet.", "Política de privacidad",
           "Qué datos recopilamos, por qué y cómo los protegemos", "Términos de uso",
           "Reglas del servicio y de la suscripción de pago", "Contacto"),
}
EMAIL = "imagination5671@gmail.com"

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{title}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<nav class="langbar" aria-label="Language">{buttons}</nav>
"""
TAIL = """<script>
(function () {
  var codes = %s;
  function pick() {
    var h = (location.hash || '').slice(1);
    if (codes.indexOf(h) >= 0) return h;
    var prefs = navigator.languages || [navigator.language || 'ko'];
    for (var i = 0; i < prefs.length; i++) {
      var p = (prefs[i] || '').toLowerCase();
      if (p.indexOf('ko') === 0) return 'ko';
      if (p.indexOf('ja') === 0) return 'ja';
      if (p.indexOf('zh') === 0) return 'zh-Hant';
      if (p.indexOf('es') === 0) return 'es';
      if (p.indexOf('en') === 0) return 'en';
    }
    return 'en';
  }
  function show(c) {
    document.querySelectorAll('main[data-lang]').forEach(function (m) { m.classList.toggle('on', m.dataset.lang === c); });
    document.querySelectorAll('.langbar a').forEach(function (a) { a.classList.toggle('on', a.dataset.lang === c); });
    document.documentElement.lang = c;
  }
  show(pick());
  window.addEventListener('hashchange', function () { show(pick()); });
})();
</script>
</body>
</html>
"""


def buttons():
    return "".join(f'<a href="#{c}" data-lang="{c}">{n}</a>' for c, n in LANGS)


def page(name):
    parts = []
    for c, _ in LANGS:
        frag = open(os.path.join(HERE, f"{name}.{c}.html"), encoding="utf-8").read().strip()
        parts.append(f'<main data-lang="{c}" lang="{c}">\n{frag}\n</main>\n')
    html = HEAD.format(title=" / ".join(TITLE[name][c] for c, _ in LANGS[:2]), buttons=buttons()) + "".join(parts) \
        + TAIL % repr([c for c, _ in LANGS]).replace("'", '"')
    open(os.path.join(SITE, f"{name}.html"), "w", encoding="utf-8").write(html)


def index():
    parts = []
    for c, _ in LANGS:
        h1, meta, p, ps, t, ts, contact = INDEX[c]
        parts.append(f"""<main data-lang="{c}" lang="{c}">
<header>
  <span class="brand">Magnet</span>
  <h1>{h1}</h1>
  <p class="meta">{meta}</p>
</header>
<nav class="links">
  <a href="privacy.html#{c}">{p}<span>{ps}</span></a>
  <a href="terms.html#{c}">{t}<span>{ts}</span></a>
  <a href="mailto:{EMAIL}">{contact}<span>{EMAIL}</span></a>
</nav>
<footer>© Sangsanglyeog (상상력)</footer>
</main>
""")
    html = HEAD.format(title="Magnet", buttons=buttons()) + "".join(parts) + TAIL % repr([c for c, _ in LANGS]).replace("'", '"')
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    page("privacy")
    page("terms")
    index()
    print("ok")
