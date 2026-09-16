from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "public_company_history.csv"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

INK = "#152536"
MUTED = "#637282"
GRID = "#dbe3ea"
BLUE = "#1769aa"
TEAL = "#008b8b"
ORANGE = "#e07a2d"
PAPER = "#f7fafc"


def load_rows():
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in (
            "fiscal_year",
            "revenue_inr_crore",
            "operating_profit_inr_crore",
            "net_profit_inr_crore",
            "employees",
            "operating_margin_pct",
        ):
            row[key] = float(row[key]) if row[key] else None
    return rows


def load_csv(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line_path(points):
    return " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(points))


def svg_start(title, subtitle):
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img">',
        f"<title>{esc(title)}</title>",
        f"<desc>{esc(subtitle)}</desc>",
        f'<rect width="1200" height="680" rx="24" fill="{PAPER}"/>',
        f'<text x="72" y="72" fill="{INK}" font-family="Arial,sans-serif" font-size="34" font-weight="700">{esc(title)}</text>',
        f'<text x="72" y="108" fill="{MUTED}" font-family="Arial,sans-serif" font-size="18">{esc(subtitle)}</text>',
    ]


def axes(svg, y_ticks, y_label):
    left, top, width, height = 92, 150, 1030, 430
    for label, frac in y_ticks:
        y = top + height * (1 - frac)
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + width}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        svg.append(f'<text x="{left - 14}" y="{y + 6:.1f}" text-anchor="end" fill="{MUTED}" font-family="Arial,sans-serif" font-size="15">{esc(label)}</text>')
    svg.append(f'<text x="24" y="365" transform="rotate(-90 24 365)" text-anchor="middle" fill="{MUTED}" font-family="Arial,sans-serif" font-size="15">{esc(y_label)}</text>')
    return left, top, width, height


def save(name, svg):
    svg.append("</svg>")
    (ASSETS / name).write_text("\n".join(svg) + "\n", encoding="utf-8")


def indexed_scale(rows):
    svg = svg_start("Scale, earnings and workforce", "Indexed to FY2007 = 100 · Infosys public filings")
    left, top, width, height = axes(svg, [("0", 0), ("400", .25), ("800", .5), ("1,200", .75), ("1,600", 1)], "Index (FY2007 = 100)")
    years = [int(r["fiscal_year"]) for r in rows]
    series = [
        ("Revenue", "revenue_inr_crore", BLUE),
        ("Net profit", "net_profit_inr_crore", ORANGE),
        ("Employees", "employees", TEAL),
    ]
    for label, key, color in series:
        base = rows[0][key]
        values = [r[key] / base * 100 for r in rows]
        pts = []
        for i, value in enumerate(values):
            x = left + width * i / (len(rows) - 1)
            y = top + height * (1 - value / 1600)
            pts.append((x, y))
        svg.append(f'<path d="{line_path(pts)}" fill="none" stroke="{color}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
        x, y = pts[-1]
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}"/>')
        svg.append(f'<text x="{x - 8:.1f}" y="{y - 13:.1f}" text-anchor="end" fill="{color}" font-family="Arial,sans-serif" font-size="17" font-weight="700">{esc(label)} {values[-1]:.0f}</text>')
    for year in (2007, 2010, 2014, 2018, 2022, 2026):
        i = years.index(year)
        x = left + width * i / (len(rows) - 1)
        svg.append(f'<text x="{x:.1f}" y="612" text-anchor="middle" fill="{MUTED}" font-family="Arial,sans-serif" font-size="15">FY{str(year)[-2:]}</text>')
    svg.append(f'<text x="72" y="650" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Author calculations. Revenue and profit are nominal ₹ values; workforce is year-end headcount.</text>')
    save("public-scale.svg", svg)


def productivity(rows):
    svg = svg_start("Revenue per year-end employee", "A directional operating-leverage proxy · ₹ million")
    values = [r["revenue_inr_crore"] * 10 / r["employees"] for r in rows]
    left, top, width, height = axes(svg, [("0", 0), ("1.5", .25), ("3.0", .5), ("4.5", .75), ("6.0", 1)], "₹ million per employee")
    pts = []
    for i, value in enumerate(values):
        x = left + width * i / (len(rows) - 1)
        y = top + height * (1 - value / 6)
        pts.append((x, y))
    area = f"M {pts[0][0]:.1f} {top + height} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in pts) + f" L {pts[-1][0]:.1f} {top + height} Z"
    svg.append(f'<path d="{area}" fill="{BLUE}" opacity="0.10"/>')
    svg.append(f'<path d="{line_path(pts)}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round"/>')
    for i in (0, 6, 12, 16, 19):
        x, y = pts[i]
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}"/>')
        svg.append(f'<text x="{x:.1f}" y="{y - 14:.1f}" text-anchor="middle" fill="{INK}" font-family="Arial,sans-serif" font-size="15" font-weight="700">{values[i]:.2f}</text>')
        svg.append(f'<text x="{x:.1f}" y="612" text-anchor="middle" fill="{MUTED}" font-family="Arial,sans-serif" font-size="15">FY{str(int(rows[i]["fiscal_year"]))[-2:]}</text>')
    svg.append(f'<text x="72" y="650" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Revenue ÷ fiscal year-end employees. Nominal values; not adjusted for inflation or average headcount.</text>')
    save("public-productivity.svg", svg)


def margin(rows):
    rows = [r for r in rows if r["operating_margin_pct"] is not None]
    svg = svg_start("Operating margin: durable, but lower", "FY2012–FY2026 · percent of revenue")
    left, top, width, height = axes(svg, [("18%", 0), ("21%", .25), ("24%", .5), ("27%", .75), ("30%", 1)], "Operating margin")
    pts = []
    for i, row in enumerate(rows):
        value = row["operating_margin_pct"]
        x = left + width * i / (len(rows) - 1)
        y = top + height * (1 - (value - 18) / 12)
        pts.append((x, y))
    svg.append(f'<path d="{line_path(pts)}" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-linejoin="round"/>')
    for i, row in enumerate(rows):
        if int(row["fiscal_year"]) in (2012, 2015, 2020, 2021, 2023, 2026):
            x, y = pts[i]
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{ORANGE}"/>')
            svg.append(f'<text x="{x:.1f}" y="{y - 14:.1f}" text-anchor="middle" fill="{INK}" font-family="Arial,sans-serif" font-size="15" font-weight="700">{row["operating_margin_pct"]:.1f}%</text>')
            svg.append(f'<text x="{x:.1f}" y="612" text-anchor="middle" fill="{MUTED}" font-family="Arial,sans-serif" font-size="15">FY{str(int(row["fiscal_year"]))[-2:]}</text>')
    svg.append(f'<text x="72" y="650" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Reported consolidated operating margin from Infosys historical-data disclosures.</text>')
    save("public-margin.svg", svg)


def geography():
    rows = load_csv("public_geography_mix.csv")
    categories = ["North America", "Europe", "India", "Rest of World"]
    colors = [BLUE, TEAL, ORANGE, "#8090a5"]
    svg = svg_start("The revenue map broadened", "Geographic revenue share · FY2010 versus FY2026")
    left, width = 130, 940
    for n, year in enumerate((2010, 2026)):
        y = 220 + n * 170
        svg.append(f'<text x="110" y="{y + 43}" text-anchor="end" fill="{INK}" font-family="Arial,sans-serif" font-size="22" font-weight="700">FY{year}</text>')
        x = left
        year_rows = {r["category"]: float(r["revenue_share_pct"]) for r in rows if int(r["fiscal_year"]) == year}
        for category, color in zip(categories, colors):
            value = year_rows[category]
            w = width * value / 100
            svg.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="78" fill="{color}"/>')
            if value >= 8:
                svg.append(f'<text x="{x + w / 2:.1f}" y="{y + 47}" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="19" font-weight="700">{value:.1f}%</text>')
            x += w
    for i, (category, color) in enumerate(zip(categories, colors)):
        x = 105 + i * 260
        svg.append(f'<rect x="{x}" y="525" width="18" height="18" rx="3" fill="{color}"/>')
        svg.append(f'<text x="{x + 28}" y="540" fill="{INK}" font-family="Arial,sans-serif" font-size="15">{esc(category)}</text>')
    svg.append(f'<text x="72" y="635" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Public issuer disclosures. Europe gained 9.1 percentage points; North America declined 9.7 points.</text>')
    save("public-geography.svg", svg)


def business_mix():
    rows = load_csv("public_business_mix_fy2026.csv")
    total = sum(float(r["revenue_inr_crore"]) for r in rows)
    rows = sorted(rows, key=lambda r: float(r["revenue_inr_crore"]), reverse=True)
    svg = svg_start("FY2026 revenue is diversified by industry", "Business-segment revenue share · ₹178,650 crore total")
    left, top, width = 390, 154, 690
    max_share = max(float(r["revenue_inr_crore"]) / total * 100 for r in rows)
    for i, row in enumerate(rows):
        y = top + i * 56
        share = float(row["revenue_inr_crore"]) / total * 100
        w = width * share / max_share
        color = BLUE if i == 0 else TEAL if i < 4 else "#6e8299"
        svg.append(f'<text x="{left - 18}" y="{y + 23}" text-anchor="end" fill="{INK}" font-family="Arial,sans-serif" font-size="16">{esc(row["category"])}</text>')
        svg.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="32" rx="7" fill="{color}"/>')
        svg.append(f'<text x="{left + w + 12:.1f}" y="{y + 23}" fill="{INK}" font-family="Arial,sans-serif" font-size="16" font-weight="700">{share:.1f}%</text>')
    svg.append(f'<text x="72" y="635" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Shares calculated from reported FY2026 segment revenue; labels shortened from issuer definitions.</text>')
    save("public-business-mix.svg", svg)


def capital_returns(history_rows):
    rows = load_csv("public_capital_returns.csv")
    svg = svg_start("Cash generation supports rising distributions", "Dividend per share, FY2014–FY2026 · recent free cash flow at right")
    left, top, width, height = 92, 175, 700, 360
    for value in (0, 10, 20, 30, 40, 50):
        y = top + height * (1 - value / 50)
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + width}" y2="{y:.1f}" stroke="{GRID}"/>')
        svg.append(f'<text x="{left - 14}" y="{y + 5:.1f}" text-anchor="end" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">₹{value}</text>')
    pts = []
    for i, row in enumerate(rows):
        value = float(row["dividend_per_share_inr"])
        x = left + width * i / (len(rows) - 1)
        y = top + height * (1 - value / 50)
        pts.append((x, y))
    svg.append(f'<path d="{line_path(pts)}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round"/>')
    for i in (0, 4, 8, 10, 12):
        x, y = pts[i]
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}"/>')
        label_x = x + 18 if i == 0 else x
        svg.append(f'<text x="{label_x:.1f}" y="{y - 13:.1f}" text-anchor="middle" fill="{INK}" font-family="Arial,sans-serif" font-size="14" font-weight="700">₹{float(rows[i]["dividend_per_share_inr"]):.2f}</text>')
        svg.append(f'<text x="{x:.1f}" y="560" text-anchor="middle" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">FY{rows[i]["fiscal_year"][-2:]}</text>')
    profits = {int(r["fiscal_year"]): r["net_profit_inr_crore"] for r in history_rows}
    svg.append(f'<text x="850" y="174" fill="{INK}" font-family="Arial,sans-serif" font-size="18" font-weight="700">Free cash flow</text>')
    for j, row in enumerate([r for r in rows if r["free_cash_flow_inr_crore"]]):
        year = int(row["fiscal_year"])
        fcf = float(row["free_cash_flow_inr_crore"])
        conversion = fcf / profits[year] * 100
        y = 205 + j * 112
        svg.append(f'<rect x="840" y="{y}" width="290" height="88" rx="14" fill="#ffffff" stroke="{GRID}"/>')
        svg.append(f'<text x="862" y="{y + 27}" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">FY{year}</text>')
        svg.append(f'<text x="862" y="{y + 58}" fill="{INK}" font-family="Arial,sans-serif" font-size="22" font-weight="700">₹{fcf:,.0f} cr</text>')
        svg.append(f'<text x="1108" y="{y + 58}" text-anchor="end" fill="{TEAL}" font-family="Arial,sans-serif" font-size="15" font-weight="700">{conversion:.1f}% of PAT</text>')
    svg.append(f'<text x="72" y="635" fill="{MUTED}" font-family="Arial,sans-serif" font-size="14">Issuer-adjusted dividend history; special dividends included where reported. FCF uses the issuer definition.</text>')
    save("public-capital-returns.svg", svg)


if __name__ == "__main__":
    data = load_rows()
    indexed_scale(data)
    productivity(data)
    margin(data)
    geography()
    business_mix()
    capital_returns(data)
    print("Wrote public charts to assets/")
