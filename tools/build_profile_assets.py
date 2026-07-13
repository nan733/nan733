from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

ASCII_ART = r"""
                                       .: -
                                .::::.
                            .-*********==-::.
                           -**+****####******=.
                          :*++***######****++=*:
                          ********#######***+=--=
                         .*=---==++*##%#++===**:.
                         ===*******#%##*===-:..:
                         *+***#*+**###*++*****:..
                       ..*+=----++**#+=+=++****..
                      +*=**++++******==+++:::.-*
                      +*++*######**##+=+*****==*.*
                      -*+**#####**###*+=*##**+=-:*
                      :*+**#####++*#*===+###**+-::
                       +=+*###***++====+**##**=:-
                        .***#+-==++**+===-***+-..
                         =**#*+=+*##*+=--+**+*.
                         .+**##**+++++++***+=:
                         .+=+**##*+++***+==-:.
                         .*==+***#****+*=--::-
                         :+*+==+*###***=-::-+*.
                      -*#==+*+========-::-=*+=:*+-:
                   -*%@@%+=+**+++==-----=**+==-#%@%#+:
               .=#%@@%%@@#=+***+++**+===++++=-*%%%%%%%%+:
            .-*%%%%%%%@@@@#++***++++++++*++++#%@@%%%%%%%%#+:
         .=*%%%%%%%%%@@@@@@%#***++*++++++++*%@@@%%%%%%%%%%%%#+:.
     .=*#%%%%%%%%%%%%@@@@@@@@%##**+++****#%@@@%%%%%%%%%%%%%#%%%%#=
    -%@%%%%%%%%%%%%%%%%%@@@@@@@@@@%%%%@@@@@@@%%%%%%%%%%%%%%%%%##%#*.
  .*@%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%#%%+.
 .%%%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%%%#=
:%%%%%%%%@%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%%###*
#%%%%%%%%%@%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%####
%%%%%%%%%%%%@%%%%%@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%%#%###
""".strip("\n").splitlines()


THEMES = {
    "dark": {
        "bg": "#010403",
        "panel": "#030C08",
        "panel_alt": "#06150E",
        "ink": "#DDEBE3",
        "muted": "#728D7E",
        "grid": "#0C291B",
        "cyan": "#20B978",
        "green": "#4BC98F",
        "blue": "#13734D",
        "deep": "#2E7D57",
        "shadow": "#000000",
    },
    "light": {
        "bg": "#030806",
        "panel": "#06110B",
        "panel_alt": "#0A1A12",
        "ink": "#E3F0E9",
        "muted": "#7F9A8C",
        "grid": "#113020",
        "cyan": "#24B77C",
        "green": "#52C994",
        "blue": "#187A53",
        "deep": "#357C5A",
        "shadow": "#000000",
    },
}


def ascii_tspans() -> str:
    rows = []
    for index, line in enumerate(ASCII_ART):
        y = 128 + index * 11.4
        rows.append(
            f'<tspan x="46" y="{y:.1f}" xml:space="preserve">{escape(line)}</tspan>'
        )
    return "\n".join(rows)


def header_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    sans = 'font-family="Inter, Segoe UI, Arial, sans-serif" letter-spacing="0"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="280" viewBox="0 0 1180 280" role="img" aria-labelledby="title desc">
<title id="title">Renan Oliveira, desenvolvedor Full-Stack em formação</title>
<desc id="desc">Cabeçalho animado com ondas fluidas, o nome Renan Oliveira e sua área de atuação.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['cyan']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="0.52" stop-color="{theme['blue']}"><animate attributeName="stop-color" values="{theme['blue']};{theme['deep']};{theme['blue']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['deep']}"><animate attributeName="stop-color" values="{theme['deep']};{theme['green']};{theme['deep']}" dur="8s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}" stop-opacity="0.38"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['cyan']}" dur="11s" repeatCount="indefinite"/></stop>
    <stop offset="0.5" stop-color="{theme['blue']}" stop-opacity="0.26"><animate attributeName="stop-color" values="{theme['blue']};{theme['deep']};{theme['blue']}" dur="11s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['deep']}" stop-opacity="0.42"><animate attributeName="stop-color" values="{theme['deep']};{theme['green']};{theme['deep']}" dur="11s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['ink']}"/>
    <stop offset="0.48" stop-color="{theme['ink']}"/>
    <stop offset="0.58" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['deep']};{theme['cyan']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['blue']}"><animate attributeName="stop-color" values="{theme['blue']};{theme['deep']};{theme['cyan']};{theme['blue']}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{theme['grid']}" stroke-width="1" opacity="0.48"/>
  </pattern>
  <clipPath id="frameClip"><rect width="1180" height="280" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frameClip)">
  <rect width="1180" height="280" fill="{theme['bg']}"/>
  <rect width="1180" height="280" fill="url(#grid)"/>
  <path id="backWave" d="M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202V280H0Z" fill="url(#wave)" opacity="0.78">
    <animate attributeName="d" values="M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202V280H0Z;M0 212C220 220 420 212 620 202C820 192 1000 200 1180 217V280H0Z;M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202V280H0Z" dur="13s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.66;0.84;0.66" dur="13s" repeatCount="indefinite"/>
  </path>
  <path id="frontWave" d="M0 247C230 231 426 227 618 234C820 241 1008 244 1180 231V280H0Z" fill="{theme['panel']}" fill-opacity="0.9">
    <animate attributeName="d" values="M0 247C230 231 426 227 618 234C820 241 1008 244 1180 231V280H0Z;M0 236C224 244 426 241 620 231C818 221 1006 227 1180 245V280H0Z;M0 247C230 231 426 227 618 234C820 241 1008 244 1180 231V280H0Z" dur="16s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
  </path>
  <path id="waveLine" d="M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202" fill="none" stroke="url(#accent)" stroke-width="2.5" opacity="0.94">
    <animate attributeName="d" values="M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202;M0 212C220 220 420 212 620 202C820 192 1000 200 1180 217;M0 221C220 202 420 200 620 209C820 218 1000 215 1180 202" dur="13s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
  </path>
</g>
<rect x="3" y="3" width="1174" height="274" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<g text-anchor="middle">
  <text x="590" y="82" {sans} font-size="68" font-weight="800" fill="url(#name)">Renan Oliveira</text>
  <text x="590" y="132" {sans} font-size="31" font-weight="700" fill="{theme['ink']}">Desenvolvedor Full-Stack em Formação</text>
  <text x="590" y="172" {mono} font-size="19" font-weight="700" fill="{theme['cyan']}">INTERFACES WEB / APIs / DADOS / AUTOMAÇÃO</text>
</g>
</svg>'''


def hero_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    tiny = f'{mono} font-size="15" font-weight="600" fill="{theme["muted"]}"'
    label = f'{mono} font-size="17" font-weight="800" fill="{theme["cyan"]}"'
    key = f'{mono} font-size="16" font-weight="700" fill="{theme["muted"]}"'
    value = f'{mono} font-size="18" font-weight="650" fill="{theme["ink"]}"'
    portrait = 'font-family="Consolas, Courier New, monospace" font-size="9.2" fill="url(#portrait)"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760" role="img" aria-labelledby="title desc">
<title id="title">Painel de perfil do desenvolvedor nan733</title>
<desc id="desc">Interface de terminal animada com retrato ASCII, stack de desenvolvimento e foco profissional.</desc>
<defs>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{theme['deep']}"><animate attributeName="stop-color" values="{theme['deep']};{theme['cyan']};{theme['green']};{theme['deep']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="0.52" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['green']};{theme['blue']};{theme['cyan']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['green']}"><animate attributeName="stop-color" values="{theme['green']};{theme['blue']};{theme['deep']};{theme['green']}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="portrait" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0" stop-color="{theme['cyan']}"/>
    <stop offset="0.5" stop-color="{theme['blue']}"/>
    <stop offset="1" stop-color="{theme['deep']}"/>
  </linearGradient>
  <radialGradient id="glow" cx="74%" cy="20%" r="72%">
    <stop offset="0" stop-color="{theme['blue']}" stop-opacity="0.14"/>
    <stop offset="0.55" stop-color="{theme['deep']}" stop-opacity="0.05"/>
    <stop offset="1" stop-color="{theme['bg']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{theme['grid']}" stroke-width="1" opacity="0.46"/>
  </pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="scanClip"><rect x="22" y="66" width="1136" height="646" rx="12"/></clipPath>
</defs>
<rect width="1180" height="760" rx="16" fill="{theme['bg']}"/>
<rect width="1180" height="760" rx="16" fill="url(#grid)"/>
<rect width="1180" height="760" rx="16" fill="url(#glow)"/>
<g>
  <rect x="3" y="3" width="1174" height="754" rx="14" fill="none" stroke="url(#frame)" stroke-width="2"/>
  <path d="M3 50H1177" stroke="{theme['grid']}"/>
  <circle cx="24" cy="25" r="6" fill="{theme['deep']}"/><circle cx="45" cy="25" r="6" fill="{theme['blue']}"/><circle cx="66" cy="25" r="6" fill="{theme['green']}"/>
  <circle cx="1089" cy="25" r="5" fill="{theme['green']}" filter="url(#softGlow)"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>
  <text x="1105" y="31" {mono} font-size="14" font-weight="800" fill="{theme['green']}">ATIVO</text>

  <rect x="22" y="66" width="408" height="646" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M22 106H430" stroke="{theme['grid']}"/>
  <text x="40" y="92" {label}>IDENTIDADE.SCAN</text>
  <text x="412" y="92" text-anchor="end" {tiny}>AVATAR PÚBLICO</text>
  <text {portrait}>{ascii_tspans()}</text>
  <rect x="40" y="670" width="372" height="2" fill="url(#frame)" opacity="0.7"/>
  <text x="40" y="698" {tiny}>ASSINATURA</text>
  <text x="174" y="698" {mono} font-size="15" font-weight="800" fill="{theme['green']}">RENAN.OLIVEIRA // VERIFICADO</text>

  <rect x="448" y="66" width="710" height="646" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M448 106H1158" stroke="{theme['grid']}"/>
  <text x="474" y="92" {label}>PERFIL.OS</text>
  <text x="1134" y="92" text-anchor="end" {tiny}>VERSÃO 2026.07 // PT-BR</text>

  <text x="474" y="153" {mono} font-size="38" font-weight="800" fill="{theme['ink']}">@nan733 <tspan fill="{theme['muted']}">//</tspan> <tspan fill="{theme['cyan']}">Renan Oliveira</tspan></text>
  <rect x="474" y="173" width="660" height="2" fill="url(#frame)" opacity="0.72"/>

  <text x="474" y="205" {label}>PERFIL.PROFISSIONAL</text>
  <path d="M474 216H1134" stroke="{theme['grid']}"/>
  <text x="474" y="247" {key}>PERFIL</text><text x="655" y="247" {value}>Desenvolvedor Full-Stack em formação</text>
  <text x="474" y="282" {key}>OBJETIVO</text><text x="655" y="282" {value}>Criar produtos web claros e funcionais</text>
  <text x="474" y="317" {key}>MOMENTO</text><text x="655" y="317" {value}>Aprendendo, construindo e evoluindo</text>
  <text x="474" y="352" {key}>FOCO</text><text x="655" y="352" {value}>React / Node.js / Python / APIs</text>

  <text x="474" y="392" {label}>STACK.PRINCIPAL</text>
  <path d="M474 404H1134" stroke="{theme['grid']}"/>
  <text x="474" y="439" {key}>FRONTEND</text><text x="655" y="439" {value}>React / Vite / JavaScript</text>
  <text x="474" y="474" {key}>BACKEND</text><text x="655" y="474" {value}>Python / Flask / APIs REST</text>
  <text x="474" y="509" {key}>DADOS</text><text x="655" y="509" {value}>SQLite / Turso / Supabase</text>
  <text x="474" y="544" {key}>FLUXO</text><text x="655" y="544" {value}>Git / GitHub / automação</text>

  <rect x="474" y="566" width="660" height="86" rx="8" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <text x="494" y="593" {label}>PRÓXIMO.PASSO</text>
  <text x="494" y="624" {mono} font-size="22" font-weight="800" fill="{theme['ink']}">Consolidar minha evolução Full-Stack</text>
  <text x="494" y="646" {tiny}>projetos úteis / código claro / melhoria contínua</text>
  <circle cx="1106" cy="609" r="10" fill="none" stroke="{theme['green']}" opacity="0.42"/>
  <circle cx="1106" cy="609" r="5" fill="{theme['green']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>

  <rect x="474" y="666" width="660" height="32" rx="7" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <circle cx="496" cy="682" r="6" fill="{theme['cyan']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" repeatCount="indefinite"/></circle><text x="512" y="687" {tiny}>CRIAR</text>
  <path d="M581 682H684" stroke="{theme['grid']}" stroke-width="2"/><circle cx="704" cy="682" r="6" fill="{theme['blue']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.35s" repeatCount="indefinite"/></circle><text x="720" y="687" {tiny}>EVOLUIR</text>
  <path d="M814 682H910" stroke="{theme['grid']}" stroke-width="2"/><circle cx="930" cy="682" r="6" fill="{theme['deep']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.7s" repeatCount="indefinite"/></circle><text x="946" y="687" {tiny}>ENTREGAR</text>
</g>
<g clip-path="url(#scanClip)" opacity="0.58">
  <rect x="22" y="32" width="1136" height="2" fill="url(#frame)" filter="url(#softGlow)">
    <animate attributeName="y" from="58" to="726" dur="5.8s" repeatCount="indefinite"/>
  </rect>
</g>
</svg>'''


def mission_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    sans = 'font-family="Inter, Segoe UI, Arial, sans-serif" letter-spacing="0"'
    title = f'{mono} font-size="17" font-weight="800" fill="{theme["cyan"]}"'
    head = f'{sans} font-size="26" font-weight="800" fill="{theme["ink"]}"'
    body = f'{mono} font-size="17" font-weight="650" fill="{theme["muted"]}"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="330" viewBox="0 0 1180 330" role="img" aria-labelledby="title desc">
<title id="title">Central de missão de nan733</title>
<desc id="desc">Foco profissional, objetivos de estudo e princípios de desenvolvimento.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{theme['cyan']}"/><stop offset="0.52" stop-color="{theme['blue']}"/><stop offset="1" stop-color="{theme['deep']}"/></linearGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{theme['grid']}" opacity="0.42"/></pattern>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="330" rx="14" fill="{theme['bg']}"/>
<rect width="1180" height="330" rx="14" fill="url(#grid)"/>
<rect x="3" y="3" width="1174" height="324" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<text x="24" y="38" {title}>VISÃO.GERAL</text>
<text x="1156" y="38" text-anchor="end" {body}>FOCO / APRENDIZADO / PRINCÍPIOS</text>
<path d="M24 52H1156" stroke="{theme['grid']}"/>

<rect x="24" y="72" width="360" height="230" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="43" y="104" {title}>01 // FOCO</text>
<text x="43" y="145" {head}>Desenvolvimento Full-Stack</text>
<text x="43" y="184" {body}>aplicações web completas</text>
<text x="43" y="216" {body}>React / Node.js / Python</text>
<text x="43" y="248" {body}>APIs / dados / automação</text>
<rect x="43" y="274" width="286" height="5" rx="2.5" fill="{theme['grid']}"/><rect x="43" y="274" width="196" height="5" rx="2.5" fill="{theme['green']}"><animate attributeName="width" values="150;196;182;196" dur="4s" repeatCount="indefinite"/></rect>

<rect x="410" y="72" width="360" height="230" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="429" y="104" {title}>02 // APRENDIZADO</text>
<text x="429" y="145" {head}>Estudos em andamento</text>
<text x="429" y="184" {body}>arquitetura de APIs REST</text>
<text x="429" y="216" {body}>modelagem de dados</text>
<text x="429" y="248" {body}>testes e integração</text>
<circle cx="740" cy="138" r="6" fill="{theme['blue']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" repeatCount="indefinite"/></circle>

<rect x="796" y="72" width="360" height="230" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="815" y="104" {title}>03 // PRINCÍPIOS</text>
<text x="815" y="145" {head}>Como eu construo</text>
<text x="815" y="184" {body}>clareza antes de complexidade</text>
<text x="815" y="216" {body}>código simples e sustentável</text>
<text x="815" y="248" {body}>qualidade desde o início</text>
<circle cx="1126" cy="138" r="6" fill="{theme['deep']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" begin="0.5s" repeatCount="indefinite"/></circle>
</svg>'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"profile-header-v6-{name}.svg").write_text(
            header_svg(theme), encoding="utf-8"
        )
        (ASSETS / f"profile-v7-{name}.svg").write_text(hero_svg(theme), encoding="utf-8")
        (ASSETS / f"mission-control-v7-{name}.svg").write_text(
            mission_svg(theme), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
