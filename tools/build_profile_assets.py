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
        "bg": "#070B14",
        "panel": "#0B1220",
        "panel_alt": "#0E1728",
        "ink": "#DCE8F5",
        "muted": "#7E93AA",
        "grid": "#172337",
        "cyan": "#22D3EE",
        "green": "#2DD4BF",
        "blue": "#60A5FA",
        "violet": "#A78BFA",
        "shadow": "#020617",
    },
    "light": {
        "bg": "#F4F8FC",
        "panel": "#FFFFFF",
        "panel_alt": "#EDF5FB",
        "ink": "#172033",
        "muted": "#64748B",
        "grid": "#DCE7F1",
        "cyan": "#0891B2",
        "green": "#0F766E",
        "blue": "#2563EB",
        "violet": "#7C3AED",
        "shadow": "#94A3B8",
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="190" viewBox="0 0 1180 190" role="img" aria-labelledby="title desc">
<title id="title">Renan Oliveira, desenvolvedor Full-Stack em formação</title>
<desc id="desc">Cabeçalho visual com o nome Renan Oliveira e sua área de atuação.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}"><animate attributeName="stop-color" values="{theme['cyan']};{theme['blue']};{theme['cyan']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="0.52" stop-color="{theme['blue']}"><animate attributeName="stop-color" values="{theme['blue']};{theme['violet']};{theme['blue']}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{theme['violet']}"><animate attributeName="stop-color" values="{theme['violet']};{theme['green']};{theme['violet']}" dur="8s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{theme['cyan']}" stop-opacity="0.34"/>
    <stop offset="0.5" stop-color="{theme['blue']}" stop-opacity="0.24"/>
    <stop offset="1" stop-color="{theme['violet']}" stop-opacity="0.38"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="18%" r="76%">
    <stop offset="0" stop-color="{theme['cyan']}" stop-opacity="0.14"/>
    <stop offset="0.5" stop-color="{theme['blue']}" stop-opacity="0.06"/>
    <stop offset="1" stop-color="{theme['bg']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{theme['grid']}" stroke-width="1" opacity="0.48"/>
  </pattern>
  <filter id="softGlow" x="-40%" y="-80%" width="180%" height="260%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="frameClip"><rect width="1180" height="190" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frameClip)">
  <rect width="1180" height="190" fill="{theme['bg']}"/>
  <rect width="1180" height="190" fill="url(#grid)"/>
  <rect width="1180" height="190" fill="url(#glow)"/>
  <path d="M0 0H1180V126C1000 105 829 99 660 108C448 119 232 145 0 160Z" fill="url(#wave)"/>
  <path d="M0 151C214 133 410 116 604 116C805 116 1000 140 1180 148V190H0Z" fill="{theme['panel']}" fill-opacity="0.78"/>
  <path d="M0 151C214 133 410 116 604 116C805 116 1000 140 1180 148" fill="none" stroke="url(#accent)" stroke-width="2" opacity="0.72" filter="url(#softGlow)"/>
</g>
<rect x="3" y="3" width="1174" height="184" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<g text-anchor="middle">
  <text x="590" y="76" {sans} font-size="46" font-weight="800" fill="{theme['ink']}">Renan <tspan fill="{theme['cyan']}">Oliveira</tspan></text>
  <text x="590" y="111" {mono} font-size="17" font-weight="700" fill="{theme['ink']}">DESENVOLVEDOR FULL-STACK EM FORMAÇÃO</text>
  <path d="M530 132H650" stroke="url(#accent)" stroke-width="3" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="518" cy="132" r="3" fill="{theme['cyan']}"/>
  <circle cx="662" cy="132" r="3" fill="{theme['violet']}"/>
</g>
</svg>'''


def hero_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    tiny = f'{mono} font-size="10" fill="{theme["muted"]}"'
    label = f'{mono} font-size="11" font-weight="700" fill="{theme["cyan"]}"'
    key = f'{mono} font-size="11" font-weight="700" fill="{theme["muted"]}"'
    value = f'{mono} font-size="12" font-weight="600" fill="{theme["ink"]}"'
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
  <text x="1110" y="26" {mono} font-size="10" fill="{theme['green']}">ATIVO</text>

  <rect x="22" y="62" width="420" height="496" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M22 91H442" stroke="{theme['grid']}"/>
  <text x="38" y="81" {label}>IDENTIDADE.SCAN</text>
  <text x="425" y="81" text-anchor="end" {tiny}>FONTE // AVATAR PÚBLICO</text>
  <text {portrait}>{ascii_tspans()}</text>
  <rect x="38" y="529" width="388" height="1" fill="url(#frame)" opacity="0.65"/>
  <text x="38" y="547" {tiny}>ASSINATURA VISUAL</text>
  <text x="176" y="547" {mono} font-size="12" font-weight="600" fill="{theme['green']}">RENAN.OLIVEIRA // VERIFICADO</text>

  <rect x="462" y="62" width="696" height="496" rx="12" fill="{theme['panel']}" fill-opacity="0.84" stroke="{theme['grid']}"/>
  <path d="M462 91H1158" stroke="{theme['grid']}"/>
  <text x="478" y="81" {label}>PERFIL.OS</text>
  <text x="1140" y="81" text-anchor="end" {tiny}>VERSÃO 2026.07 // PT-BR</text>

  <text x="484" y="128" {mono} font-size="25" font-weight="800" fill="{theme['ink']}">nan733 <tspan fill="{theme['muted']}">//</tspan> <tspan fill="{theme['cyan']}">Renan Oliveira</tspan></text>
  <rect x="484" y="142" width="650" height="2" fill="url(#frame)" opacity="0.72"/>

  <text x="484" y="174" {key}>IDENTIDADE</text><text x="620" y="174" {value}>desenvolvedor em evolução constante</text>
  <text x="484" y="199" {key}>FUNÇÃO</text><text x="620" y="199" {value}>desenvolvedor full-stack em formação</text>
  <text x="484" y="224" {key}>MODO</text><text x="620" y="224" {value}>construindo / aprendendo / entregando</text>
  <text x="484" y="249" {key}>FOCO</text><text x="620" y="249" {value}>apps web / dashboards / automação</text>

  <text x="484" y="290" {label}>STACK.ATUAL</text>
  <path d="M484 300H1134" stroke="{theme['grid']}"/>
  <text x="484" y="325" {key}>FRONTEND</text><text x="620" y="325" {value}>React 19 / Vite / JavaScript</text>
  <text x="484" y="350" {key}>BACKEND</text><text x="620" y="350" {value}>Python / APIs / SQLite / Turso</text>
  <text x="484" y="375" {key}>VISUAL</text><text x="620" y="375" {value}>Recharts / Motion / Three.js</text>

  <rect x="484" y="398" width="650" height="82" rx="8" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <text x="501" y="420" {label}>DIREÇÃO.ATUAL</text>
  <text x="501" y="446" {mono} font-size="17" font-weight="800" fill="{theme['ink']}">Evolução Full-Stack</text>
  <text x="501" y="466" {tiny}>interfaces // APIs // dados // automação</text>
  <circle cx="1108" cy="438" r="9" fill="none" stroke="{theme['green']}" opacity="0.38"/>
  <circle cx="1108" cy="438" r="4" fill="{theme['green']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>

  <rect x="484" y="500" width="650" height="38" rx="7" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
  <circle cx="505" cy="519" r="5" fill="{theme['cyan']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" repeatCount="indefinite"/></circle><text x="518" y="523" {tiny}>CRIAR</text>
  <path d="M575 519H681" stroke="{theme['grid']}" stroke-width="2"/><circle cx="699" cy="519" r="5" fill="{theme['blue']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.35s" repeatCount="indefinite"/></circle><text x="712" y="523" {tiny}>APRENDER</text>
  <path d="M793 519H899" stroke="{theme['grid']}" stroke-width="2"/><circle cx="917" cy="519" r="5" fill="{theme['violet']}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="0.7s" repeatCount="indefinite"/></circle><text x="930" y="523" {tiny}>ENTREGAR</text>
  <rect x="1098" y="509" width="8" height="18" fill="{theme['green']}"><animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></rect>
</g>
<g clip-path="url(#scanClip)" opacity="0.58">
  <rect x="22" y="32" width="1136" height="2" fill="url(#frame)" filter="url(#softGlow)">
    <animate attributeName="y" from="50" to="570" dur="5.2s" repeatCount="indefinite"/>
  </rect>
</g>
</svg>'''


def mission_svg(theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    title = f'{mono} font-size="12" font-weight="800" fill="{theme["cyan"]}"'
    head = f'{mono} font-size="18" font-weight="800" fill="{theme["ink"]}"'
    body = f'{mono} font-size="11" fill="{theme["muted"]}"'
    strong = f'{mono} font-size="11" font-weight="700" fill="{theme["ink"]}"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="210" viewBox="0 0 1180 210" role="img" aria-labelledby="title desc">
<title id="title">Central de missão de nan733</title>
<desc id="desc">Foco profissional, objetivos de estudo e princípios de desenvolvimento.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{theme['cyan']}"/><stop offset="0.52" stop-color="{theme['blue']}"/><stop offset="1" stop-color="{theme['violet']}"/></linearGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{theme['grid']}" opacity="0.42"/></pattern>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="210" rx="14" fill="{theme['bg']}"/>
<rect width="1180" height="210" rx="14" fill="url(#grid)"/>
<rect x="3" y="3" width="1174" height="204" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<text x="24" y="31" {title}>CENTRAL.DE.MISSÃO</text>
<text x="1156" y="31" text-anchor="end" {body}>MÓDULOS // 03</text>
<path d="M24 43H1156" stroke="{theme['grid']}"/>

<rect x="24" y="62" width="360" height="126" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="43" y="86" {title}>01 // FOCO.ATUAL</text>
<text x="43" y="116" {head}>Desenvolvimento Full-Stack</text>
<text x="43" y="140" {body}>interfaces web responsivas</text>
<text x="43" y="160" {body}>APIs + dados + visualizações</text>
<rect x="43" y="174" width="286" height="3" rx="2" fill="{theme['grid']}"/><rect x="43" y="174" width="196" height="3" rx="2" fill="{theme['green']}"><animate attributeName="width" values="150;196;182;196" dur="4s" repeatCount="indefinite"/></rect>

<rect x="410" y="62" width="360" height="126" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="429" y="86" {title}>02 // PRÓXIMOS.ESTUDOS</text>
<text x="429" y="116" {strong}>design de APIs + modelagem de dados</text>
<text x="429" y="140" {strong}>sistemas de interfaces responsivas</text>
<text x="429" y="164" {strong}>testes + entregas confiaveis</text>
<circle cx="740" cy="112" r="5" fill="{theme['blue']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" repeatCount="indefinite"/></circle>

<rect x="796" y="62" width="360" height="126" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<text x="815" y="86" {title}>03 // VALORES.DE.ENTREGA</text>
<text x="815" y="116" {strong}>util antes de chamativo</text>
<text x="815" y="140" {strong}>claro antes de complexo</text>
<text x="815" y="164" {strong}>seguro por padrão</text>
<circle cx="1126" cy="112" r="5" fill="{theme['violet']}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" begin="0.5s" repeatCount="indefinite"/></circle>
</svg>'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"profile-header-v1-{name}.svg").write_text(
            header_svg(theme), encoding="utf-8"
        )
        (ASSETS / f"profile-v3-{name}.svg").write_text(hero_svg(theme), encoding="utf-8")
        (ASSETS / f"mission-control-v3-{name}.svg").write_text(
            mission_svg(theme), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
