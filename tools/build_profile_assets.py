from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

ASCII_ART = r"""
                                                             
                             =*##%%#####.-                  
                            +++*#####*****:                 
                            =+##########*=                  
                           -=-   .==-   :=-                 
                         #.=-:   .-*.    -=:                
                        :-=*#=--=:##=-:-==+-=               
                         -==###+=#####=====:-               
                         ##===-.=  - .--===-=               
                           ===-:  ===  ===                  
                           ====--=---=--=-                  
                           =.-= *-:.:. -=                   
                         #===:.--     -=                    
                     %%%%##==--::-----==#                   
                  %%%%%%%%%====---===-=-*#%                 
               %%%%%%%%%%%%%##=--=-=----*###%%%             
            =%%%%%%%%%%%%%%%%##**#####****###%%%%           
           %%%%%%%%%%%%%%%%%%%#*++++++++**####%%%%          
         %%%%%%%%%%%%%%%%%%%%%#+++++++++***#####%%%         
        %%%%%%%%%%%%%%%%%%%%%%%#*++++++*****######%%        
       %%%%%%%%%%%%%%%%%%%%%%%%%#*+++++******###%*#*        
      #%%#%%%%%%#%%%%%%%%%%%%%%%%+=--=- =.--*##%%+#*        
      %##%#+#%#%%##%#%%%%%%%%%%%%%+======++==##%%#++        
     %%###*##+*#%#%#=##%%%%%%%%%%%%++*+++***###%%%+*        
     %###++++#*++##*=+**#%%%%%%%%%%#***+*****##%%%+#        
     ####++==#**+==*=+++*#%%%%%%%%%%***++*****####**        
    #++%#*+==+*+++=*==++*##%%%%%%%##***++*****#**#+##      
   ##+#%##++==*==+=*==++++#%%%#####*****++*+++*#**+##      
   **+###%*+===*===+=+++++++##*###**#****+**++*#*=*#%+     
  **+##%###*+==+++.=+++++++****###**##****+#*++**=+##      
 %#*++######+++++=====+++++##*+##***##*#+**##+**==+#%%     
 %*%#%#%###%*+++++-====+++***+*#**++##***+*###**#=+= =     
%##%##%*%%###++++=-======+***+###*++##***++*##**+   .==    
      %%%%%%%++++:======++*+++###*+*###**+**###**   ===:   
      ::   .+##*=======++**++*###*++###*****###**   =---   
      =====     :.:====+*++++##*#+++###****+#****   -::    
      ======      -====+++=++##**+++###*+**+*##++   ::     
      -==+++=    :-===+++++++%##++++####++****#**    .     
     .:===+++=  .:--=++=++++###*++++####*+***+#*+          
     =.-======.  ..=====++**%##*++++*###*+***##*+     ...  
       .-=-====   =====++**%%##*++++####**+**##*+-    .-:  
     -  ..:---=  ======++*%%#**+++++#**#**+***#*+=.   .--: 
     :    ..:---:=-====+#%%%#**+++++***##******#*=-   .-=- 
     :    .::---.:-==+#%%%%#+*+++++************##===   -=-.
           ----:..-==%%%%%%**++++*********+*****#+:-:  -== 
      #   .-===-.:=+%%%%%%#*++=++*+*************##+  ..====
          .=====.:=%%%%%%#++++++**+**+++*********#+ -       
           -====.=%%##%%%++++==++++*+++++*******##*         
""".strip("\n").splitlines()


THEMES = {
    "dark": {
        "bg": "#050D09",
        "panel": "#081A12",
        "panel_alt": "#0E2419",
        "ink": "#E7F4EC",
        "muted": "#8AA596",
        "grid": "#173A2A",
        "cyan": "#2DD49A",
        "green": "#8BE0B8",
        "blue": "#58D6A4",
        "violet": "#D1AA68",
        "shadow": "#010604",
    },
    "light": {
        "bg": "#F2F7F4",
        "panel": "#FFFFFF",
        "panel_alt": "#E7F2EC",
        "ink": "#173026",
        "muted": "#61786B",
        "grid": "#D4E5DB",
        "cyan": "#0A7F55",
        "green": "#2E7D5A",
        "blue": "#15966A",
        "violet": "#8C652F",
        "shadow": "#7C9487",
    },
}


def ascii_tspans() -> str:
    rows = []
    for index, line in enumerate(ASCII_ART):
        y = 103 + index * 9.2
        rows.append(
            f'<tspan x="42" y="{y:.1f}" xml:space="preserve">{escape(line)}</tspan>'
        )
    return "\n".join(rows)


def header_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    sans = 'font-family="Inter, Segoe UI, Arial, sans-serif" letter-spacing="0"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="230" viewBox="0 0 1180 230" role="img" aria-labelledby="title desc">
<title id="title">Renan Oliveira, desenvolvedor Full-Stack em formação</title>
<desc id="desc">Cabeçalho animado com ondas fluidas, o nome Renan Oliveira e sua área de atuação.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['cyan']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="0.52" stop-color="{theme['blue']}"><animate attributeName="stop-color" values="{theme['blue']};{theme['violet']};{theme['blue']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['violet']}"><animate attributeName="stop-color" values="{theme['violet']};{theme['green']};{theme['violet']}" dur="8s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}" stop-opacity="0.38"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['cyan']}" dur="11s" repeatCount="indefinite"/></stop>
    <stop offset="0.5" stop-color="{theme['blue']}" stop-opacity="0.26"><animate attributeName="stop-color" values="{theme['blue']};{theme['violet']};{theme['blue']}" dur="11s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['violet']}" stop-opacity="0.42"><animate attributeName="stop-color" values="{theme['violet']};{theme['green']};{theme['violet']}" dur="11s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['ink']}"/>
    <stop offset="0.48" stop-color="{theme['ink']}"/>
    <stop offset="0.58" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['violet']};{theme['cyan']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['blue']}"><animate attributeName="stop-color" values="{theme['blue']};{theme['violet']};{theme['cyan']};{theme['blue']}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{theme['grid']}" stroke-width="1" opacity="0.48"/>
  </pattern>
  <clipPath id="frameClip"><rect width="1180" height="230" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frameClip)">
  <rect width="1180" height="230" fill="{theme['bg']}"/>
  <rect width="1180" height="230" fill="url(#grid)"/>
  <path id="backWave" d="M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164V230H0Z" fill="url(#wave)" opacity="0.78">
    <animate attributeName="d" values="M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164V230H0Z;M0 174C220 182 420 174 620 164C820 154 1000 162 1180 179V230H0Z;M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164V230H0Z" dur="13s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.66;0.84;0.66" dur="13s" repeatCount="indefinite"/>
  </path>
  <path id="frontWave" d="M0 204C230 188 426 184 618 191C820 198 1008 201 1180 188V230H0Z" fill="{theme['panel']}" fill-opacity="0.9">
    <animate attributeName="d" values="M0 204C230 188 426 184 618 191C820 198 1008 201 1180 188V230H0Z;M0 193C224 201 426 198 620 188C818 178 1006 184 1180 202V230H0Z;M0 204C230 188 426 184 618 191C820 198 1008 201 1180 188V230H0Z" dur="16s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
  </path>
  <path id="waveLine" d="M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164" fill="none" stroke="url(#accent)" stroke-width="2.5" opacity="0.94">
    <animate attributeName="d" values="M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164;M0 174C220 182 420 174 620 164C820 154 1000 162 1180 179;M0 183C220 164 420 162 620 171C820 180 1000 177 1180 164" dur="13s" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" repeatCount="indefinite"/>
  </path>
</g>
<rect x="3" y="3" width="1174" height="224" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<g text-anchor="middle">
  <text x="590" y="72" {sans} font-size="58" font-weight="800" fill="url(#name)">Renan Oliveira</text>
  <text x="590" y="114" {sans} font-size="25" font-weight="700" fill="{theme['ink']}">Desenvolvedor Full-Stack em Formação</text>
  <text x="590" y="146" {mono} font-size="16" font-weight="700" fill="{theme['cyan']}">INTERFACES WEB / APIs / DADOS / AUTOMAÇÃO</text>
</g>
</svg>'''


def hero_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    tiny = f'{mono} font-size="13" fill="{theme["muted"]}"'
    label = f'{mono} font-size="14" font-weight="700" fill="{theme["cyan"]}"'
    key = f'{mono} font-size="14" font-weight="700" fill="{theme["muted"]}"'
    value = f'{mono} font-size="15" font-weight="600" fill="{theme["ink"]}"'
    portrait = 'font-family="Consolas, Courier New, monospace" font-size="7.6" fill="url(#portrait)"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="620" viewBox="0 0 1180 620" role="img" aria-labelledby="title desc">
<title id="title">Painel de perfil do desenvolvedor nan733</title>
<desc id="desc">Interface de terminal animada com retrato ASCII, stack de desenvolvimento e foco profissional.</desc>
<defs>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{theme['violet']}"><animate attributeName="stop-color" values="{theme['violet']};{theme['cyan']};{theme['green']};{theme['violet']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="0.52" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['green']};{theme['blue']};{theme['cyan']}" dur="10s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['green']}"><animate attributeName="stop-color" values="{theme['green']};{theme['blue']};{theme['violet']};{theme['green']}" dur="10s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="portrait" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0" stop-color="{theme['cyan']}"/>
    <stop offset="0.5" stop-color="{theme['blue']}"/>
    <stop offset="1" stop-color="{theme['violet']}"/>
  </linearGradient>
  <radialGradient id="glow" cx="74%" cy="20%" r="72%">
    <stop offset="0" stop-color="{theme['blue']}" stop-opacity="0.14"/>
    <stop offset="0.55" stop-color="{theme['violet']}" stop-opacity="0.05"/>
    <stop offset="1" stop-color="{theme['bg']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{theme['grid']}" stroke-width="1" opacity="0.46"/>
  </pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="scanClip"><rect x="22" y="62" width="1136" height="496" rx="12"/></clipPath>
</defs>
<rect width="1180" height="620" rx="16" fill="{theme['bg']}"/>
<rect width="1180" height="620" rx="16" fill="url(#grid)"/>
<rect width="1180" height="620" rx="16" fill="url(#glow)"/>
<g>
  <rect x="3" y="3" width="1174" height="614" rx="14" fill="none" stroke="url(#frame)" stroke-width="2"/>
  <path d="M3 43H1177" stroke="{theme['grid']}"/>
  <circle cx="23" cy="23" r="5" fill="#F43F5E"/><circle cx="41" cy="23" r="5" fill="#F59E0B"/><circle cx="59" cy="23" r="5" fill="{theme['green']}"/>
  <circle cx="1097" cy="22" r="4" fill="{theme['green']}" filter="url(#softGlow)"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>
  <text x="1110" y="27" {mono} font-size="12" font-weight="700" fill="{theme['green']}">ATIVO</text>

  <rect x="22" y="62" width="420" height="496" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M22 91H442" stroke="{theme['grid']}"/>
  <text x="38" y="81" {label}>IDENTIDADE.SCAN</text>
  <text x="425" y="81" text-anchor="end" {tiny}>FONTE // AVATAR PÚBLICO</text>
  <text {portrait}>{ascii_tspans()}</text>
  <rect x="38" y="529" width="388" height="1" fill="url(#frame)" opacity="0.65"/>
  <text x="38" y="547" {tiny}>ASSINATURA VISUAL</text>
  <text x="180" y="547" {mono} font-size="13" font-weight="700" fill="{theme['green']}">RENAN.OLIVEIRA // VERIFICADO</text>

  <rect x="462" y="62" width="696" height="496" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M462 91H1158" stroke="{theme['grid']}"/>
  <text x="478" y="81" {label}>PERFIL.OS</text>
  <text x="1140" y="81" text-anchor="end" {tiny}>VERSÃO 2026.07 // PT-BR</text>

  <text x="484" y="132" {mono} font-size="31" font-weight="800" fill="{theme['ink']}">@nan733 <tspan fill="{theme['muted']}">//</tspan> <tspan fill="{theme['cyan']}">Renan Oliveira</tspan></text>
  <rect x="484" y="150" width="650" height="2" fill="url(#frame)" opacity="0.72"/>

  <text x="484" y="182" {key}>PERFIL</text><text x="625" y="182" {value}>Desenvolvedor Full-Stack em formação</text>
  <text x="484" y="211" {key}>OBJETIVO</text><text x="625" y="211" {value}>Interfaces web úteis e bem construídas</text>
  <text x="484" y="240" {key}>MOMENTO</text><text x="625" y="240" {value}>Aprendendo, construindo e evoluindo</text>
  <text x="484" y="269" {key}>FOCO</text><text x="625" y="269" {value}>React / Python / APIs / automação</text>

  <text x="484" y="306" {label}>STACK.PRINCIPAL</text>
  <path d="M484 317H1134" stroke="{theme['grid']}"/>
  <text x="484" y="348" {key}>FRONTEND</text><text x="625" y="348" {value}>React 19 / Vite / JavaScript</text>
  <text x="484" y="378" {key}>BACKEND</text><text x="625" y="378" {value}>Python / APIs / SQLite / Turso</text>
  <text x="484" y="408" {key}>VISUAL</text><text x="625" y="408" {value}>Recharts / Motion / Three.js</text>

  <rect x="484" y="421" width="650" height="84" rx="8" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <text x="501" y="446" {label}>PRÓXIMO.PASSO</text>
  <text x="501" y="475" {mono} font-size="20" font-weight="800" fill="{theme['ink']}">Evoluir como Desenvolvedor Full-Stack</text>
  <text x="501" y="497" {tiny}>produtos claros / úteis / confiáveis</text>
  <circle cx="1108" cy="463" r="9" fill="none" stroke="{theme['green']}" opacity="0.38"/>
  <circle cx="1108" cy="463" r="4" fill="{theme['green']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>

  <rect x="484" y="516" width="650" height="28" rx="7" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <circle cx="505" cy="530" r="5" fill="{theme['cyan']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" repeatCount="indefinite"/></circle><text x="518" y="534" {tiny}>CRIAR</text>
  <path d="M580 530H681" stroke="{theme['grid']}" stroke-width="2"/><circle cx="699" cy="530" r="5" fill="{theme['blue']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.35s" repeatCount="indefinite"/></circle><text x="712" y="534" {tiny}>APRENDER</text>
  <path d="M804 530H899" stroke="{theme['grid']}" stroke-width="2"/><circle cx="917" cy="530" r="5" fill="{theme['violet']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.7s" repeatCount="indefinite"/></circle><text x="930" y="534" {tiny}>ENTREGAR</text>
</g>
<g clip-path="url(#scanClip)" opacity="0.58">
  <rect x="22" y="32" width="1136" height="2" fill="url(#frame)" filter="url(#softGlow)">
    <animate attributeName="y" from="50" to="570" dur="5.2s" repeatCount="indefinite"/>
  </rect>
</g>
</svg>'''


def mission_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    sans = 'font-family="Inter, Segoe UI, Arial, sans-serif" letter-spacing="0"'
    title = f'{mono} font-size="14" font-weight="800" fill="{theme["cyan"]}"'
    head = f'{sans} font-size="22" font-weight="800" fill="{theme["ink"]}"'
    body = f'{mono} font-size="14" font-weight="600" fill="{theme["muted"]}"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="240" viewBox="0 0 1180 240" role="img" aria-labelledby="title desc">
<title id="title">Central de missão de nan733</title>
<desc id="desc">Foco profissional, objetivos de estudo e princípios de desenvolvimento.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{theme['cyan']}"/><stop offset="0.52" stop-color="{theme['blue']}"/><stop offset="1" stop-color="{theme['violet']}"/></linearGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{theme['grid']}" opacity="0.42"/></pattern>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="240" rx="14" fill="{theme['bg']}"/>
<rect width="1180" height="240" rx="14" fill="url(#grid)"/>
<rect x="3" y="3" width="1174" height="234" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<text x="24" y="32" {title}>VISÃO.GERAL</text>
<text x="1156" y="32" text-anchor="end" {body}>FOCO / APRENDIZADO / PRINCÍPIOS</text>
<path d="M24 43H1156" stroke="{theme['grid']}"/>

<rect x="24" y="62" width="360" height="152" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="43" y="89" {title}>01 // FOCO</text>
<text x="43" y="123" {head}>Desenvolvimento Full-Stack</text>
<text x="43" y="153" {body}>interfaces web responsivas</text>
<text x="43" y="178" {body}>React, Python, APIs e automação</text>
<rect x="43" y="198" width="286" height="4" rx="2" fill="{theme['grid']}"/><rect x="43" y="198" width="196" height="4" rx="2" fill="{theme['green']}"><animate attributeName="width" values="150;196;182;196" dur="4s" repeatCount="indefinite"/></rect>

<rect x="410" y="62" width="360" height="152" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="429" y="89" {title}>02 // APRENDIZADO</text>
<text x="429" y="123" {head}>Estudos em andamento</text>
<text x="429" y="153" {body}>APIs + modelagem de dados</text>
<text x="429" y="178" {body}>interfaces + testes confiáveis</text>
<circle cx="740" cy="118" r="5" fill="{theme['blue']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" repeatCount="indefinite"/></circle>

<rect x="796" y="62" width="360" height="152" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="815" y="89" {title}>03 // PRINCÍPIOS</text>
<text x="815" y="123" {head}>Como eu construo</text>
<text x="815" y="153" {body}>clareza antes de complexidade</text>
<text x="815" y="178" {body}>qualidade desde o início</text>
<circle cx="1126" cy="118" r="5" fill="{theme['violet']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" begin="0.5s" repeatCount="indefinite"/></circle>
</svg>'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"profile-header-v4-{name}.svg").write_text(
            header_svg(theme), encoding="utf-8"
        )
        (ASSETS / f"profile-v5-{name}.svg").write_text(hero_svg(theme), encoding="utf-8")
        (ASSETS / f"mission-control-v5-{name}.svg").write_text(
            mission_svg(theme), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
