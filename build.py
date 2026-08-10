#!/usr/bin/env python3
# Builds the Draworld static site. Style mocked on cortys.de/homepage.
import os, math, random, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BLACK, RED, BRED, BEIGE, GREY = "#000", "#c42c2d", "#ff3638", "#c69f9f", "#e8e8e8"

# ---------------------------------------------------------------- SVG plates
# Each plate is drawn on a 600x400 canvas (3:2) but the hero uses a 900x300 slice
# via preserveAspectRatio, so plates are composed to stay legible at both ratios.

def frame(inner, w=600, h=400):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice" role="img">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{inner}</svg>')

def plate_nodes(seed=1):
    """33 provincial zones, interconnectors, red price nodes. — ElecTRADE"""
    rnd = random.Random(seed); pts = []
    for i in range(33):
        a = i * 2.399963
        r = 150 * math.sqrt((i + .5) / 33)
        pts.append((300 + r * math.cos(a) * 1.35, 200 + r * math.sin(a)))
    s = ""
    for i, (x, y) in enumerate(pts):
        for j in range(i + 1, 33):
            x2, y2 = pts[j]
            if (x - x2) ** 2 + (y - y2) ** 2 < 5200:
                s += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BLACK}" stroke-width=".6" opacity=".5"/>'
    for i, (x, y) in enumerate(pts):
        hot = rnd.random() < .3
        s += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5.5 if hot else 3.4}" '
              f'fill="{RED if hot else "#fff"}" stroke="{BLACK if not hot else RED}" stroke-width="1.1"/>')
    return frame(s)

def plate_bars(seed=2):
    """Capacity build-out stack — MultiEnergy 2035 NDC"""
    rnd = random.Random(seed); s = ""
    n, bw, gap = 11, 34, 12
    x0 = (600 - (n * bw + (n - 1) * gap)) / 2
    for i in range(n):
        x = x0 + i * (bw + gap)
        t = i / (n - 1)
        coal = 150 * (1 - t) ** 1.6 + 8
        ren = 175 * t ** 1.25 + 10
        other = 22 + 14 * math.sin(i)
        y = 340
        for hgt, fill, stroke in ((coal, "#fff", BLACK), (other, GREY, BLACK), (ren, RED, RED)):
            y -= hgt
            s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{hgt:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
    s += f'<line x1="30" y1="340" x2="570" y2="340" stroke="{BLACK}" stroke-width="1.4"/>'
    s += f'<line x1="30" y1="118" x2="570" y2="118" stroke="{RED}" stroke-width="1.2" stroke-dasharray="6 5"/>'
    return frame(s)

def plate_duration(seed=3):
    """Merit-order staircase: efficient units run, inefficient move to reserve
       — Zhejiang coal flexibility"""
    rnd = random.Random(seed); s = ""
    x = 34.0; n = 18
    costs = sorted(60 + 210 * (i / (n - 1)) ** 1.7 + rnd.uniform(-6, 6) for i in range(n))
    for i, c in enumerate(costs):
        w = 20 + rnd.uniform(0, 22)
        reserve = i >= n - 6
        y = 330 - c
        s += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{c:.1f}" '
              f'fill="{"#fff" if reserve else GREY}" stroke="{RED if reserve else BLACK}" '
              f'stroke-width="1.2" {"stroke-dasharray=\'5 4\'" if reserve else ""}/>')
        x += w
    s += f'<line x1="34" y1="196" x2="{x:.1f}" y2="196" stroke="{RED}" stroke-width="2"/>'
    s += f'<line x1="34" y1="330" x2="576" y2="330" stroke="{BLACK}" stroke-width="1.4"/>'
    return frame(s)

def plate_axes():
    """Effectiveness / efficiency / fairness assessment — China Dialogue workshop"""
    s = ""
    labels = 3
    for k in range(labels):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        s += (f'<line x1="300" y1="200" x2="{300+150*math.cos(a):.1f}" y2="{200+150*math.sin(a):.1f}" '
              f'stroke="{BLACK}" stroke-width="1.2"/>')
    for ring, op in ((150, .25), (100, .45), (50, .7)):
        pts = " ".join(f"{300+ring*math.cos(-math.pi/2+k*2*math.pi/3):.1f},"
                       f"{200+ring*math.sin(-math.pi/2+k*2*math.pi/3):.1f}" for k in range(3))
        s += f'<polygon points="{pts}" fill="none" stroke="{GREY}" stroke-width="1.2"/>'
    vals = (.86, .52, .34)
    pts = " ".join(f"{300+150*v*math.cos(-math.pi/2+k*2*math.pi/3):.1f},"
                   f"{200+150*v*math.sin(-math.pi/2+k*2*math.pi/3):.1f}" for k, v in enumerate(vals))
    s += f'<polygon points="{pts}" fill="{RED}" opacity=".14"/>'
    s += f'<polygon points="{pts}" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    for k, v in enumerate(vals):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        s += f'<circle cx="{300+150*v*math.cos(a):.1f}" cy="{200+150*v*math.sin(a):.1f}" r="6" fill="{RED}"/>'
    return frame(s)

def plate_triangle():
    """Trade · Climate · Security nexus"""
    P = [(300, 78), (516, 320), (84, 320)]
    s = ""
    for i in range(3):
        for j in range(i + 1, 3):
            s += f'<line x1="{P[i][0]}" y1="{P[i][1]}" x2="{P[j][0]}" y2="{P[j][1]}" stroke="{BLACK}" stroke-width="1.4"/>'
    for k in range(1, 5):
        t = k / 5
        q = [(P[a][0] + (P[b][0] - P[a][0]) * t, P[a][1] + (P[b][1] - P[a][1]) * t) for a, b in ((0, 1), (1, 2), (2, 0))]
        s += ('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in q) +
              f'" fill="none" stroke="{RED}" stroke-width=".8" opacity="{.85 - k*.14:.2f}"/>')
    for x, y in P:
        s += f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{RED}" stroke-width="2.4"/>'
    return frame(s)

def plate_quadrant():
    """Four indices — Electricity Transparency Project"""
    s = f'<line x1="300" y1="52" x2="300" y2="348" stroke="{BLACK}" stroke-width="1.2"/>'
    s += f'<line x1="52" y1="200" x2="548" y2="200" stroke="{BLACK}" stroke-width="1.2"/>'
    vals = [.78, .93, .46, .62]
    cx = [(176, 126), (424, 126), (176, 274), (424, 274)]
    for (x, y), v in zip(cx, vals):
        s += f'<circle cx="{x}" cy="{y}" r="52" fill="none" stroke="{GREY}" stroke-width="8"/>'
        a = -math.pi / 2 + 2 * math.pi * v
        s += (f'<path d="M {x} {y-52} A 52 52 0 {1 if v>.5 else 0} 1 '
              f'{x + 52*math.cos(a):.1f} {y + 52*math.sin(a):.1f}" fill="none" stroke="{RED}" stroke-width="8"/>')
        s += f'<circle cx="{x}" cy="{y}" r="4" fill="{BLACK}"/>'
    return frame(s)

def plate_flows():
    """Contract paths vs physical flows — provincial barriers myth"""
    s = ""
    for r in range(4):
        for c in range(6):
            x, y = 74 + c * 90, 92 + r * 72
            s += f'<rect x="{x-26}" y="{y-22}" width="52" height="44" fill="none" stroke="{GREY}" stroke-width="1.2"/>'
    s += (f'<path d="M74 92 C 200 60, 340 300, 524 308" fill="none" stroke="{BLACK}" stroke-width="2.4"/>')
    s += (f'<path d="M74 92 C 260 150, 300 120, 524 308" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="8 6"/>')
    s += f'<circle cx="74" cy="92" r="8" fill="{BLACK}"/><circle cx="524" cy="308" r="8" fill="{RED}"/>'
    return frame(s)

def plate_strata():
    """Layered book / ontology — PowerBook"""
    s = ""
    for i in range(9):
        y = 66 + i * 30
        w = 300 + 90 * math.sin(i * .7)
        s += (f'<rect x="{300-w/2:.1f}" y="{y}" width="{w:.1f}" height="20" fill="{"#fff" if i%2 else GREY}" '
              f'stroke="{BLACK}" stroke-width="1"/>')
    s += f'<line x1="300" y1="52" x2="300" y2="350" stroke="{RED}" stroke-width="2"/>'
    return frame(s)

def plate_peak():
    """Peak-hour available capacity vs demand — adequacy"""
    rnd = random.Random(7); s = ""
    n = 24
    for i in range(n):
        x = 40 + i * 22
        h = 90 + 150 * math.exp(-((i - 17) ** 2) / 26) + rnd.uniform(-14, 14)
        s += f'<rect x="{x}" y="{340-h:.1f}" width="15" height="{h:.1f}" fill="{GREY}" stroke="{BLACK}" stroke-width=".9"/>'
    s += f'<line x1="30" y1="150" x2="576" y2="150" stroke="{RED}" stroke-width="2.2"/>'
    s += f'<line x1="30" y1="340" x2="576" y2="340" stroke="{BLACK}" stroke-width="1.4"/>'
    return frame(s)

def plate_tozero():
    """Emissions pathway to zero — carbon neutrality column"""
    pts = [(40 + i * 5.3, 300 - 170 * math.exp(-((i - 22) ** 2) / 900) + 0) for i in range(101)]
    pts = [(x, 130 + 190 / (1 + math.exp(-(i - 42) / 14))) for i, (x, y) in enumerate(pts)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    s = f'<path d="{d} L570 330 L40 330 Z" fill="{RED}" opacity=".08"/>'
    s += f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    s += f'<line x1="40" y1="330" x2="576" y2="330" stroke="{BLACK}" stroke-width="1.4"/>'
    for i in (0, 40, 100):
        x, y = pts[i]
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff" stroke="{BLACK}" stroke-width="1.6"/>'
    return frame(s)

def plate_fork():
    """Two divergent pathways — NDC vs plan"""
    a = "M40 300 C 200 292, 300 260, 570 96"
    b = "M40 300 C 200 300, 320 300, 570 268"
    s = f'<path d="{b}" fill="none" stroke="{BLACK}" stroke-width="2.2"/>'
    s += f'<path d="{a}" fill="none" stroke="{RED}" stroke-width="2.2" stroke-dasharray="9 6"/>'
    s += f'<path d="{a} L570 268 Z" fill="{RED}" opacity=".07"/>'
    s += f'<circle cx="40" cy="300" r="7" fill="{BLACK}"/>'
    s += f'<circle cx="570" cy="96" r="7" fill="{RED}"/><circle cx="570" cy="268" r="7" fill="#fff" stroke="{BLACK}" stroke-width="2"/>'
    s += f'<line x1="30" y1="340" x2="576" y2="340" stroke="{BLACK}" stroke-width="1.2"/>'
    return frame(s)

def plate_rldc():
    """Residual load duration curve — NEA optimal mix study"""
    s = ""
    pts = [(40 + i * 5.3, 90 + 230 * (i / 100) ** 1.9) for i in range(101)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    for lvl, fill in ((0, "#fff"), (60, GREY), (120, RED)):
        dd = "M" + " L".join(f"{x:.1f} {min(y+lvl,320):.1f}" for x, y in pts)
        s += f'<path d="{dd}" fill="none" stroke="{fill if fill!="#fff" else BLACK}" stroke-width="{2.2 if lvl==0 else 1.4}"/>'
    s += f'<path d="{d} L570 320 L40 320 Z" fill="{BLACK}" opacity=".05"/>'
    s += f'<line x1="30" y1="320" x2="576" y2="320" stroke="{BLACK}" stroke-width="1.4"/>'
    return frame(s)

def plate_radial():
    """Multi-benefits radial — Greenpeace study"""
    s = ""
    for i in range(9):
        a = -math.pi / 2 + i * 2 * math.pi / 9
        r = 60 + 90 * (.4 + .6 * abs(math.sin(i * 1.3)))
        x, y = 300 + r * math.cos(a), 200 + r * math.sin(a)
        s += f'<line x1="300" y1="200" x2="{x:.1f}" y2="{y:.1f}" stroke="{BLACK}" stroke-width="1.1"/>'
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{RED}"/>'
    for r in (60, 105, 150):
        s += f'<circle cx="300" cy="200" r="{r}" fill="none" stroke="{GREY}" stroke-width="1"/>'
    s += f'<circle cx="300" cy="200" r="11" fill="#fff" stroke="{BLACK}" stroke-width="2.4"/>'
    return frame(s)

def plate_models():
    """DERC-IAM / DERC-P core tools"""
    s = ""
    for c in range(4):
        for r in range(3):
            x, y = 108 + c * 128, 108 + r * 96
            s += f'<rect x="{x-42}" y="{y-32}" width="84" height="64" fill="none" stroke="{BLACK}" stroke-width="1.2"/>'
            if (c + r) % 3 == 0:
                s += f'<rect x="{x-42}" y="{y-32}" width="84" height="64" fill="{RED}" opacity=".12"/>'
            s += f'<line x1="{x-42}" y1="{y-12}" x2="{x+42}" y2="{y-12}" stroke="{GREY}" stroke-width="1"/>'
    for c in range(3):
        x = 108 + c * 128
        s += f'<line x1="{x+42}" y1="108" x2="{x+86}" y2="108" stroke="{RED}" stroke-width="1.6"/>'
    return frame(s)

def plate_todo():
    s = (f'<rect x="20" y="20" width="560" height="360" fill="none" stroke="{BEIGE}" '
         f'stroke-width="2" stroke-dasharray="10 8"/>'
         f'<rect x="252" y="152" width="96" height="96" fill="none" stroke="{BEIGE}" stroke-width="3"/>'
         f'<text x="300" y="292" text-anchor="middle" font-family="monospace" font-size="18" fill="{BEIGE}">TO BE ADDED</text>')
    return frame(s)

def logo_svg():
    """Hexagonal mark, same geometric family as cortys.de's logo; the dot cloud
    is a stylised 33-node price surface instead of Cortys' scatter."""
    R = 112; cx = cy = 115
    hexp = " ".join(f"{cx + R*math.cos(math.radians(-90 + i*60)):.1f},{cy + R*math.sin(math.radians(-90 + i*60)):.1f}" for i in range(6))
    s = f'<polygon points="{hexp}" fill="none" stroke="{BLACK}" stroke-width="7"/>'
    rnd = random.Random(11)
    for i in range(26):
        a = i * 2.399963
        r = 62 * math.sqrt((i + .5) / 26)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * .92
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6.5 if rnd.random()<.35 else 4.2:.1f}" fill="{BRED}"/>'
    pts = [(cx - 74 + i * 148 / 40, cy + 26 - 52 / (1 + math.exp(-(i - 20) / 5))) for i in range(41)]
    s += '<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f'" fill="none" stroke="{BLACK}" stroke-width="6" stroke-linecap="round"/>'
    return f'<svg width="230" height="230" viewBox="0 0 230 230" xmlns="http://www.w3.org/2000/svg">{s}</svg>'

def footer_svg():
    return (f'<svg viewBox="0 0 34 22" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M17 2 L33 20 L27 20 L17 9 L7 20 L1 20 Z" fill="{BEIGE}"/></svg>')

PLATES = {
    "electrade": plate_nodes, "multienergy": plate_bars, "zhejiang": plate_duration,
    "dialogue": plate_triangle, "transparency": plate_quadrant, "barriers": plate_flows,
    "powerbook": plate_strata, "adequacy": plate_peak, "carbon-column": plate_tozero,
    "ndc-fyp": plate_fork, "rldc": plate_rldc, "multibenefit": plate_radial,
    "models": plate_models, "todo": plate_todo, "axes": plate_axes,
}

# ---------------------------------------------------------------- content
NAV = [("About", "about.html"), ("Projects", "projects.html"),
       ("GitHub", "https://github.com/Shawn-Zhang122"), ("AI Agents", "agents.html")]

P = []  # projects
def prj(slug, year, name, cn, desc, plate, tags, body, actions, todo=False):
    P.append(dict(slug=slug, year=year, name=name, cn=cn, desc=desc, plate=plate,
                  tags=tags, body=body, actions=actions, todo=todo))

prj("pypsa-draworld-electrade", "2026",
    "Pypsa-Draworld-ElecTRADE",
    "基于开放源代码模型架构的电力交易仿真—培训—游戏平台",
    "Day-ahead zonal market clearing for 33 provincial zones, published daily as an open web app.",
    "electrade", "PyPSA · dispatch · market design · AGPL-3.0",
    ["<p>A reproducible day-ahead (D-1) market clearing engine built on PyPSA. It runs a rolling "
     "welfare-maximising optimisation, exports the results, and publishes them through a static web "
     "interface — a digital sandbox that puts simulation, training and competition in one place.</p>",
     "<p><strong>Model design.</strong> 33 provincial zones; linear welfare maximisation; 48-hour rolling "
     "horizon with 24-hour publication; interzonal transmission constraints; storage intertemporal "
     "optimisation; locational marginal pricing aggregated to zones.</p>",
     "<p><strong>Outputs.</strong> Hourly zonal prices, interzonal flows, storage state of charge, and the "
     "full solved PyPSA network as a <code>.nc</code> file.</p>",
     "<p><strong>Separation of years.</strong> The model year (2025 representative system) is kept distinct "
     "from the publication year (real calendar time), so physical consistency survives while the output "
     "stays operationally relevant.</p>",
     "<p><strong>Uses.</strong> Congestion price analysis, coal flexibility diagnostics, renewable "
     "integration stress tests, storage arbitrage demonstration, interprovincial trade evaluation, and "
     "market design comparison.</p>",
     '<p class="note">Statement from the repository: this is a research, toy-electricity-trade-game and '
     'training dispatch engine. It is not an official trading system or a regulatory platform.</p>'],
    [("Open the app", "https://shawn-zhang122.github.io/Pypsa-Draworld-ElecTRADE/", True),
     ("Repository", "https://github.com/Shawn-Zhang122/Pypsa-Draworld-ElecTRADE", False)])

prj("todo-2026", "2026", "◻ 待补充 / To be added", "",
    "Placeholder for a 2026 project not yet described online.",
    "todo", "placeholder",
    ["<p>Reserved slot. Replace the title, description, links and plate when the material is ready.</p>"],
    [], todo=True)

prj("pypsa-china-multienergy-2035ndc", "2025",
    "PyPSA-China-MultiEnergy · 2035 NDC",
    "面向2035年国家自主贡献的多能源系统优化",
    "Provincial, hourly capacity-expansion modelling of China's electricity and heat system against a 2035 NDC framing.",
    "multienergy", "PyPSA · snakemake · capacity expansion · MIT",
    ["<p>An open-source optimisation model of the Chinese energy system covering electricity and heat. It "
     "co-optimises dispatch and investment under user-set constraints — for example limits on "
     "environmental impact — at provincial resolution and hourly time steps across a full year.</p>",
     "<p>The workflow is a Snakemake pipeline around the PyPSA package: it collects data, builds the "
     "network, solves, and plots. It descends from the model first published by Hailiang Liu and "
     "colleagues, extended by Xiaowei Zhou and colleagues for multi-energy horizon planning, and adapted "
     "by the PIK RD3-ETL team with a view to coupling it to the REMIND integrated assessment model.</p>",
     '<p class="note">Repository note: this fork carries the upstream PIK README. The 2035 NDC scenario '
     'definitions, Draworld-specific inputs and a results summary still need to be written up here.</p>'],
    [("Repository", "https://github.com/Shawn-Zhang122/PyPSA-China-MultiEnergy_2035NDC", True)])

prj("zhejiang-coal-flexibility", "2025",
    "Zhejiang Coal Power Flexibility",
    "浙江煤电灵活性:经济与气候收益",
    "With CREA: differentiated coal dispatch cuts emissions 11% in 2025 and system cost 2.5% by 2030.",
    "zhejiang", "CREA · coal flexibility · dispatch · Nov 2025",
    ["<p>A study released with the Centre for Research on Energy and Clean Air (CREA) on how Zhejiang can "
     "cut emissions and cost by optimising a coal-dominated power system. Peak load rose from 120 GW in "
     "2024 to 135 GW in 2025 while renewables still supply under 10%, leaving the province reliant on "
     "coal and imported power.</p>",
     "<p>Differentiated coal dispatch and coal-fleet optimisation could cut coal emissions by 11% in 2025 "
     "and lower system costs by 2.5% in 2030 — on the order of RMB 60–70 billion a year — while nearly "
     "doubling wind and solar shares without curtailment. High-efficiency units would run more than 7,000 "
     "hours; inefficient plants move to reserve and backup.</p>",
     "<p>The argument is about sequencing: flexibility in coal-heavy systems should start with portfolio "
     "optimisation and transparent scheduling, not with expensive storage or demand-side action under "
     "non-stress conditions. The reform list includes adjusting reserve requirements, enabling flexible "
     "interprovincial flows, and strengthening real-time operational transparency.</p>"],
    [("Full report (CREA)", "https://energyandcleanair.org/enhancing-zhejiangs-coal-power-flexibility-the-economic-and-climate-gains/", True)])

prj("todo-2025", "2025", "◻ 待补充 / To be added", "",
    "Placeholder for a 2025 project not yet described online.",
    "todo", "placeholder",
    ["<p>Reserved slot.</p>"], [], todo=True)

prj("trade-climate-security-dialogue", "2024",
    "Trade–Climate–Security Policy Dialogue",
    "贸易—气候—安全政策对话(2025–2030)",
    "A multi-year dialogue series on where trade policy, climate commitments and security concerns collide.",
    "dialogue", "dialogue series · 2025–2030 · launched Dec 2024",
    ["<p>Draworld opened its Trade–Climate–Security Policy Dialogue for 2025–2030 with a first online "
     "session. The salon looked at how competitive interests, sustainable development and geopolitical "
     "stability can be balanced in an increasingly polarised landscape, drawing on economists, policy "
     "researchers and international-relations specialists.</p>",
     "<p>The opening case was EU–China electric vehicle tariffs: the EU's five-year duties on Chinese EVs "
     "as a worked example of trade and climate goals pulling against each other, and of why cooperative "
     "solutions matter if trade tension is not to compound.</p>"],
    [("Events and outreach", "http://www.draworld.org/events-and-outreach.html", False)])

prj("electricity-transparency-project", "2024",
    "Electricity Transparency Project",
    "电力透明度工程(2024–2030)",
    "Four Draworld indices on security, market coupling, market-based pricing and carbon rate.",
    "transparency", "indices · ReGini · MACI · EMPI · Carbon · May 2024",
    ["<p>China's power reform is in its deep-water phase: roughly 15% wind, around 60% coal, and trend "
     "changes that increasingly strain both the traditional dispatch-and-balance paradigm and the "
     "governance paradigm of big top-down targets. Provincial transparency platforms — Henan's "
     "distributed PV hosting-capacity portal, for instance — show what social visibility can do.</p>",
     "<p>The project builds a transparency platform of its own around four indices:</p>",
     "<ul><li><strong>Draworld-ReGini</strong> — security and resilience, computed by province.</li>"
     "<li><strong>Draworld-MACI</strong> — market coupling, from provincial 'should-be' annual average "
     "prices produced by the Draworld-P investment and operation optimisation model; the 2023 value was "
     "0.93, reflecting a coal-dominated and highly similar generation mix across provinces.</li>"
     "<li><strong>Draworld-EMPI</strong> — the degree to which the electricity sector prices through "
     "markets.</li>"
     "<li><strong>Draworld-Carbon Index</strong> — emission rate of the whole power sector; nationally "
     "500–550 gCO₂/kWh in 2023, with Sichuan and Yunnan low, North, East and Northwest China high, and "
     "Beijing an outlier as a pure gas system holding coal only as strategic reserve.</li></ul>",
     "<p>It is designed as a multi-year effort rather than a single report.</p>"],
    [("Read the release", "https://power.in-en.com/html/power-2450386.shtml", True)])

prj("todo-2024", "2024", "◻ 待补充 / To be added", "",
    "Placeholder for a 2024 project not yet described online.",
    "todo", "placeholder", ["<p>Reserved slot.</p>"], [], todo=True)

prj("provincial-barriers-myth", "2023",
    "The Provincial Barriers Myth",
    "省间壁垒迷思与可再生能源消纳",
    "Why curtailment in China is a rules-and-operations problem, not an interprovincial-protectionism problem.",
    "barriers", "renewable integration · market design · Jul 2023",
    ["<p>Chinese hydropower swings with rainfall — too little or too much — and that variation has little "
     "to do with the hard-to-define 'interprovincial barrier' narrative, even where such barriers do exist "
     "at the level of trading contracts.</p>",
     "<p>The real problem is the entanglement of trading and operations. Where system operation lacks "
     "clear value rules, outcomes fall back on higher-level discretion. Trading that determines physical "
     "output and flow appeared in the early market reforms of many countries and was later replaced by "
     "financialised contracts that need no physical execution. FERC Order No. 888 in 1996 said it plainly: "
     "a market built on tracing electricity flow between production and consumption is not workable, "
     "because actual flow paths and contract paths cannot be aligned.</p>"],
    [("Read (Chinese)", "https://www.inengyuan.com/kuaixun/11370.html", True)])

prj("powerbook", "2023",
    "PowerBook · 转型中的电力系统",
    "《转型中的电力系统:本体论与认识论》",
    "Book by chief economist Shawn Zhang on the transformation of China's power system.",
    "powerbook", "book · ontology · epistemology · year to confirm",
    ["<p>A book on the transformation of China's power system that blends technical analysis with "
     "socio-economic perspective, tracing the industry from the nineteenth-century industrial lighting "
     "revolution through to present-day smart energy.</p>",
     '<p class="note">Publication year is not stated on the Draworld site — it is placed here provisionally. '
     'Confirm and move the entry if needed.</p>'],
    [("JD.com", "https://item.jd.com/14213681.html", False),
     ("Dangdang", "https://product.dangdang.com/29750868.html", False)])

prj("power-system-adequacy", "2022",
    "Power System Adequacy",
    "构建“新型电力系统”与容量充足性",
    "With CREA: available generation at peak demand, and why interprovincial balancing beats new coal.",
    "adequacy", "CREA · adequacy · ELCC · Sept 2022",
    ["<p>Published jointly with CREA, this study examines the generation resources actually available at "
     "times of high demand. Compared with building new capacity — coal included — deepening "
     "interprovincial cooperation so that balancing happens above the provincial level secures adequacy "
     "while delivering emission and economic benefits.</p>",
     "<p>The accompanying May 2022 policy briefing argues that adequacy status should be monitored and "
     "published annually. On the model of the European and North American reliability councils, the "
     "regulator should require the system operator to publish an annual adequacy retrospect and forecast, "
     "and should introduce effective load-carrying capacity (ELCC) to measure what stochastic wind and PV "
     "actually contribute to reliability.</p>"],
    [("Chinese version", "https://energyandcleanair.org/publication/cn-china-power-system-adequacy/", True),
     ("English brief", "https://energyandcleanair.org/publication/power-system-adequacy-and-new-power-system-development-in-china/", False)])

prj("todo-2022", "2022", "◻ 待补充 / To be added", "",
    "Placeholder for a 2022 project not yet described online.",
    "todo", "placeholder", ["<p>Reserved slot.</p>"], [], todo=True)

prj("embrace-carbon-neutrality", "2021",
    "Embrace the Carbon Neutrality",
    "拥抱碳中和(专栏)",
    "A long-running column in Energy Magazine building criteria for judging which emission cuts are worth making.",
    "carbon-column", "column · Energy Magazine · from Jul 2021",
    ["<p>The column offers a logical, self-consistent reflection across several frameworks at once, on the "
     "grounds that different disciplines discuss the same issue in very different ways.</p>",
     "<p>Its aim is not to build consensus by appeal to ideology, but to develop a system of value "
     "criteria for judging carbon neutrality — which reductions are desirable, which are less reasonable, "
     "and which are unacceptable. Neutrality by 2060 needs steady, sequenced effort rather than a "
     "one-stop campaign, and a harder question underneath: how to move from a known present to a future "
     "that is still stochastic.</p>",
     "<p>The series was planned to be reorganised into a book, provisionally <em>Carbon Neutral Fate: Six "
     "Approaches to Embrace Carbon Neutrality</em>.</p>"],
    [("Publications", "http://www.draworld.org/publications.html", False)])

prj("china-dialogue-workshop-2021", "2021",
    "14th FYP and the 2060 Vision",
    "与中外对话联合研讨会",
    "Joint workshop with China Dialogue on reading the 14th Five-Year Plan against carbon neutrality by 2060.",
    "axes", "workshop · China Dialogue · Apr 2021",
    ["<p>China has pledged carbon neutrality by 2060, and the question of how to embrace it is being "
     "worked out across levels of government and society. This joint workshop with China Dialogue set out "
     "energy targets, policy measures and transition governance, and mapped the common and specific "
     "challenges along three dimensions: effectiveness, efficiency and fairness.</p>",
     "<p>Recognising the risk of a target-achieving mode that tips into command mobilisation, the "
     "workshop proposed a tailored policy toolkit grounded in four families of economic ideas.</p>"],
    [("Events and outreach", "http://www.draworld.org/events-and-outreach.html", False)])

prj("todo-2021", "2021", "◻ 待补充 / To be added", "",
    "Placeholder for a 2021 project not yet described online.",
    "todo", "placeholder", ["<p>Reserved slot.</p>"], [], todo=True)

prj("ndc-and-14th-power-fyp", "before",
    "China's NDC and the 14th Power FYP",
    "中国国家自主贡献与“十四五”电力规划",
    "2020, with CREA: post-2020 coal build plans contradict the 2060 neutrality target.",
    "ndc-fyp", "CREA · NDC · coal phase-out · Nov 2020",
    ["<p>The report shows that industry plans to build new coal-fired plants after 2020 contradict China's "
     "2060 carbon neutrality target, and calls for a policy process to phase coal power out. Over the same "
     "ten years, the rate of wind and solar expansion needs to double if domestic emission targets are to "
     "be met.</p>",
     "<p>Short- and medium-term plans to decarbonise the power sector before 2050 are the precondition for "
     "the 2060 objective, not an optional supplement to it.</p>"],
    [("Report (EN)", "https://energyandcleanair.org/publications/draworld-china-climate-five-year-plan/", True),
     ("报告 (中文)", "https://energyandcleanair.org/zh/publications/draworld-china-climate-five-year-plan-2/", False)])

prj("optimal-fossil-mix-rldc", "before",
    "Optimal Fossil Generation Mix",
    "基于剩余负荷持续曲线的化石电源结构与市场价格研究",
    "2017–2019, for the National Energy Administration: generation mix and market price from the residual load duration curve.",
    "rldc", "NEA · RLDC · 2017–2019",
    ["<p>A study of the optimal fossil fuel generation mix and resulting market price, derived from the "
     "residual load duration curve, sponsored by China's National Energy Administration.</p>",
     '<p class="note">Only the kick-off note is published on the Draworld site. Scope, method detail and '
     'results are still to be added here.</p>'],
    [])

prj("multi-benefits-wind-solar", "before",
    "Multi-Benefits of Wind and Solar",
    "风电与光伏发展的多重效益",
    "2017, funded by Greenpeace: energy, air quality, green jobs and growth benefits of renewable expansion.",
    "multibenefit", "Greenpeace · co-benefits · Apr 2017",
    ["<p>Produced with several of China's authoritative energy and environment research bodies, this "
     "report synthesises the integrated benefits of expanding renewables in the electricity and wider "
     "energy sector — energy supply, local pollution abatement, green employment and sustained economic "
     "growth.</p>"],
    [])

prj("derc-models", "before",
    "DERC-IAM and DERC-P",
    "核心模型工具",
    "The centre's two long-standing in-house models: a multi-region energy–economy–climate IAM and an hourly power balance model.",
    "models", "core tools · IAM · hourly balance",
    ["<p>Draworld builds and maintains two core working tools:</p>",
     "<ul><li><strong>DERC-IAM</strong> — an integrated energy–economy–climate assessment model with "
     "multi-region economic structure.</li>"
     "<li><strong>DERC-P</strong> — a simulation model of China's power structure at hourly resolution, "
     "used for power balance work; the provincial investment and operation optimisation variant "
     "(Draworld-P) supplies the price surfaces behind the transparency indices.</li></ul>",
     '<p class="note">Version history and documentation are not public. Add them here when available.</p>'],
    [])

prj("todo-before", "before", "◻ 归档待补充 / Archive to be added", "",
    "Placeholder for pre-2021 work not yet described online.",
    "todo", "placeholder", ["<p>Reserved slot.</p>"], [], todo=True)

YEARS = [("2026", "2026"), ("2025", "2025"), ("2024", "2024"), ("2023", "2023"),
         ("2022", "2022"), ("2021", "2021"), ("before", "Before 2021 · Archive")]

# ---------------------------------------------------------------- templates
def head(title, depth, desc):
    up = "../" if depth else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#151515">
<meta name="description" content="{html.escape(desc)}">
<title>{html.escape(title)}</title>
<link rel="icon" href="{up}assets/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
"""

def header(active, depth):
    up = "../" if depth else ""
    items = ""
    for name, href in NAV:
        ext = href.startswith("http")
        h = href if ext else up + href
        cls = ' class="active"' if name == active else ""
        arrow = ' <span class="ext">&#8599;</span>' if ext else ""
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        items += f'<li><a href="{h}"{cls}{tgt}>{name}{arrow}</a></li>'
    return f"""<header id="head">
<a id="logo" href="{up}index.html" aria-label="Draworld — home">
  <img class="back" src="{up}assets/logo.svg" alt="" draggable="false">
  <img class="front" src="{up}assets/logo.svg" alt="" draggable="false">
</a>
<h1 id="title">Draworld<b>.</b></h1>
<p id="subtitle">卓尔德环境研究中心 · DERC Beijing</p>
<nav><ul id="menu">{items}</ul></nav>
</header>
"""

FOOT = """<footer id="foot">
<div class="inner">
<a id="top" href="#head" title="Back to top" aria-label="Back to top">{chev}</a>
<div class="contact">
  <div>
    <h4>Address</h4>
    <p>Floor 12, Locker Time Center</p>
    <p>No. 103 Huizhong Beili, Chaoyang District</p>
    <p>Beijing 100101, China</p>
    <p>北京市朝阳区慧忠北路103号洛克时代中心B座12层</p>
  </div>
  <div>
    <h4>Contact</h4>
    <p>Tel / Fax +86-10-52508037</p>
    <p>Within China <a href="mailto:draworld@126.com">draworld@126.com</a></p>
    <p>Abroad <span class="ph">◻ email to be added</span></p>
  </div>
  <div>
    <h4>Elsewhere</h4>
    <p><a href="http://www.draworld.org/" target="_blank" rel="noopener">draworld.org (current site)</a></p>
    <p><a href="https://twitter.com/Draworld_BJ" target="_blank" rel="noopener">X / Twitter @Draworld_BJ</a></p>
    <p><a href="https://github.com/Shawn-Zhang122" target="_blank" rel="noopener">GitHub</a></p>
  </div>
  <div>
    <h4>Centre</h4>
    <p>Founded June 2012, Beijing</p>
    <p>Independent applied research and consulting on energy and environment policy</p>
  </div>
</div>
<p class="copyright">Copyright 2025–2039 &copy; Draworld DERC · Beijing &amp; Guangzhou, China</p>
</div>
</footer>
</body>
</html>
"""

def page(title, active, depth, desc, body):
    return head(title, depth, desc) + header(active, depth) + body + FOOT.format(chev=footer_svg())

def card(p, depth):
    up = "../" if depth else ""
    cls = "card todo" if p["todo"] else "card"
    cn = f'<p class="tags">{html.escape(p["cn"])}</p>' if p["cn"] else ""
    return (f'<li><a class="{cls}" href="{up}project/{p["slug"]}.html">'
            f'<div class="thumb">{PLATES[p["plate"]]()}</div>'
            f'<div class="meta"><h3 class="name">{html.escape(p["name"])}</h3>'
            f'<p class="desc">{html.escape(p["desc"])}</p>'
            f'<p class="tags">{html.escape(p["tags"])}</p></div></a></li>')

# ---------------------------------------------------------------- write
os.makedirs(f"{ROOT}/assets", exist_ok=True)
os.makedirs(f"{ROOT}/project", exist_ok=True)
open(f"{ROOT}/assets/logo.svg", "w").write(logo_svg())

# --- home
recent = [p for p in P if not p["todo"]][:3]
home_body = f"""<main><div class="wrap narrow">
<p class="lede">Draworld is a boutique research centre working on China's energy and environment policy,
and on the sectoral dynamics underneath it. Founded in Beijing in June 2012. Our work is independent.</p>
<div class="groups">
  <div class="group"><h3>Digitalisation of the energy sector</h3>
  <p>Open models, market simulation and transparency indices for a sector defined by state ownership,
  limited disclosure and unstable rules — where technology, economics and politics all bind.</p></div>
  <div class="group"><h3>China and the rest of the world</h3>
  <p>How China interacts with the EU and the US through trade, climate and security channels as the
  international regime becomes more fragmented and less rule-based.</p></div>
</div>
<hr class="rule">
<div class="year"><h2>Recent</h2><div class="bar"></div>
<span class="count">latest 3</span></div>
<ul class="cards">{''.join(card(p, 0) for p in recent)}</ul>
<hr class="rule">
<p><a class="btn primary" href="projects.html">All projects by year &#8594;</a></p>
</div></main>
"""
open(f"{ROOT}/index.html", "w").write(page(
    "Draworld · DERC Beijing", None, 0,
    "Draworld Environment Research Center — independent applied research on China's energy and environment policy.",
    home_body))

# --- about
about_body = """<main><div class="wrap narrow">
<p class="lede">Draworld Environment Research Center (DERC, Beijing) was founded in June 2012 to do
applied research and consulting on energy and environment policy, planning and project assessment.</p>
<article>
<p>The centre exists to supply knowledge products and policy recommendations for green economy
development in China and for the governance of the global commons. Work between 2014 and 2016
concentrated on the economics of coal and renewables. Support has come from the Environmental Defense
Fund, Energy Foundation Beijing, the China Wind Power Association, the International Institute for
Sustainable Development and the World Bank, among others.</p>
<p>Since early 2020 the centre has worked in two groups: digitalisation of the energy sector in the
Chinese context, and the nexus between China and the rest of the world — currently focused on the
European Green Deal and its Chinese dimension.</p>
<p>Some of the applied work has become policy: funding the renewable surcharge account by reducing the
benchmark coal on-grid price, tightening the stringency of coal reduction policy, removing the flawed
cap on total energy consumption, and reframing peaking as a share of generation rather than an
ancillary service.</p>
<h3 style="margin:26px 0 10px;font-size:var(--font-h3-size)">Core tools</h3>
<ul>
<li><strong>DERC-IAM</strong> — multi-region energy–economy–climate integrated assessment model.</li>
<li><strong>DERC-P</strong> — hourly-resolution simulation of China's power structure and balance.</li>
<li><strong>PyPSA-based open models</strong> — provincial capacity expansion and day-ahead market clearing.</li>
</ul>
<p class="note">People, group leads and funder list are not reproduced here — add them when the
material is ready.</p>
</article>
</div></main>
"""
open(f"{ROOT}/about.html", "w").write(page(
    "About · Draworld", "About", 0, "About Draworld Environment Research Center (DERC, Beijing).", about_body))

# --- agents
agents_body = """<main><div class="wrap narrow">
<p class="lede">AI agents in the modelling workflow.</p>
<article>
<p>Draworld's digitalisation work now includes agent-assisted modelling: retrieving and cleaning
provincial data, generating and checking scenario configurations, running the Snakemake workflows,
and drafting the result narratives that go with each publication run.</p>
<p class="note">◻ Placeholder page. This section was requested but no source material exists yet.
Replace this text with the actual agent stack, the tasks delegated to it, and the review process that
sits between agent output and anything published.</p>
<p><a class="btn primary" href="https://github.com/Shawn-Zhang122" target="_blank" rel="noopener">Code on GitHub &#8599;</a></p>
</article>
</div></main>
"""
open(f"{ROOT}/agents.html", "w").write(page(
    "AI Agents · Draworld", "AI Agents", 0, "Agent-assisted modelling workflow at Draworld.", agents_body))

# --- projects index
sections = ""
for key, label in YEARS:
    items = [p for p in P if p["year"] == key]
    cls = ' class="year archive"' if key == "before" else ' class="year"'
    real = len([p for p in items if not p["todo"]])
    sections += (f'<section><div{cls}><h2>{label}</h2><div class="bar"></div>'
                 f'<span class="count">{real} listed</span></div>'
                 f'<ul class="cards">{"".join(card(p, 0) for p in items)}</ul></section>')
proj_body = f"""<main><div class="wrap">
<p class="lede">Projects, studies and platforms, newest first. Each entry has its own page.</p>
{sections}
</div></main>
"""
open(f"{ROOT}/projects.html", "w").write(page(
    "Projects · Draworld", "Projects", 0, "Draworld projects by year.", proj_body))

# --- project pages
for i, p in enumerate(P):
    acts = ""
    for label, href, primary in p["actions"]:
        acts += (f'<a class="btn{" primary" if primary else ""}" href="{href}" '
                 f'target="_blank" rel="noopener">{html.escape(label)} <span aria-hidden="true">&#8599;</span></a>')
    if not acts:
        acts = '<span class="btn dead">◻ links to be added</span>'
    cn = f'<p class="tagline">{html.escape(p["cn"])}</p>' if p["cn"] else ""
    yl = "Archive" if p["year"] == "before" else p["year"]
    body = f"""<main><div class="wrap narrow">
<div class="proj-head">
  <a class="back" href="../projects.html" aria-label="Back to projects">&#8592;</a>
  <h2>{html.escape(p['name'])}</h2>
  <span class="yr">{yl}</span>
</div>
{cn}
<figure class="hero" style="margin:0 0 20px">{PLATES[p['plate']]()}</figure>
<div class="actions">{acts}</div>
<article>{''.join(p['body'])}</article>
<hr class="rule">
<p class="tagline">{html.escape(p['tags'])}</p>
</div></main>
"""
    open(f"{ROOT}/project/{p['slug']}.html", "w").write(page(
        f"{p['name']} · Draworld", "Projects", 1, p["desc"], body))

print(f"built {len(P)} project pages + 4 top-level pages")
