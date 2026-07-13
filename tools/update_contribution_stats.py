#!/usr/bin/env python3
"""Generate local, cache-safe contribution statistics for the profile README."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
API_URL = "https://api.github.com/graphql"
README_START = "<!-- contribution-stats:start -->"
README_END = "<!-- contribution-stats:end -->"
MONTHS = (
    "",
    "JAN",
    "FEV",
    "MAR",
    "ABR",
    "MAI",
    "JUN",
    "JUL",
    "AGO",
    "SET",
    "OUT",
    "NOV",
    "DEZ",
)

THEMES = {
    "dark": {
        "bg": "#070B14",
        "panel": "#0B1220",
        "panel_alt": "#0E1728",
        "grid": "#172337",
        "ink": "#DCE8F5",
        "muted": "#7E93AA",
        "cyan": "#22D3EE",
        "blue": "#60A5FA",
        "green": "#2DD4BF",
        "violet": "#A78BFA",
    },
    "light": {
        "bg": "#F7FAFC",
        "panel": "#FFFFFF",
        "panel_alt": "#EDF5FB",
        "grid": "#DCE7F1",
        "ink": "#172033",
        "muted": "#64748B",
        "cyan": "#0891B2",
        "blue": "#2563EB",
        "green": "#0F766E",
        "violet": "#7C3AED",
    },
}

USER_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
  }
}
"""

CALENDAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


@dataclass(frozen=True)
class Streak:
    count: int
    start: date | None
    end: date | None


@dataclass(frozen=True)
class ContributionStats:
    login: str
    joined: date
    total: int
    current: Streak
    longest: Streak
    last_activity: date | None
    days: dict[date, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", default=os.environ.get("GITHUB_LOGIN", "nan733"))
    parser.add_argument(
        "--now",
        help="UTC timestamp used for deterministic tests, for example 2026-07-13T12:00:00Z",
    )
    return parser.parse_args()


def utc_now(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def graphql(token: str, query: str, variables: dict[str, str]) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "nan733-profile-stats",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not reach GitHub GraphQL: {error.reason}") from error

    if payload.get("errors"):
        messages = "; ".join(item.get("message", "unknown error") for item in payload["errors"])
        raise RuntimeError(f"GitHub GraphQL error: {messages}")
    return payload["data"]


def fetch_contributions(
    login: str, token: str, now: datetime
) -> tuple[date, dict[date, int], int]:
    profile = graphql(token, USER_QUERY, {"login": login}).get("user")
    if profile is None:
        raise RuntimeError(f"GitHub user not found: {login}")

    created_at = datetime.fromisoformat(profile["createdAt"].replace("Z", "+00:00"))
    joined = created_at.date()
    days: dict[date, int] = {}
    total = 0

    for year in range(joined.year, now.year + 1):
        year_start = datetime.combine(date(year, 1, 1), time.min, timezone.utc)
        year_end = datetime.combine(date(year, 12, 31), time.max, timezone.utc)
        # Query the full signup year so GitHub includes the joined-account contribution.
        period_start = year_start
        period_end = min(now, year_end)
        if period_start > period_end:
            continue

        data = graphql(
            token,
            CALENDAR_QUERY,
            {"login": login, "from": iso_z(period_start), "to": iso_z(period_end)},
        )
        calendar = data["user"]["contributionsCollection"]["contributionCalendar"]
        total += int(calendar["totalContributions"])
        for week in calendar["weeks"]:
            for item in week["contributionDays"]:
                day = date.fromisoformat(item["date"])
                if period_start.date() <= day <= period_end.date():
                    days[day] = int(item["contributionCount"])

    return joined, days, total


def longest_streak(days: dict[date, int], joined: date, today: date) -> Streak:
    best = Streak(0, None, None)
    run_start: date | None = None
    run_count = 0
    day = joined

    while day <= today:
        if days.get(day, 0) > 0:
            if run_count == 0:
                run_start = day
            run_count += 1
            if run_count > best.count:
                best = Streak(run_count, run_start, day)
        else:
            run_start = None
            run_count = 0
        day += timedelta(days=1)
    return best


def current_streak(days: dict[date, int], joined: date, today: date) -> Streak:
    anchor = today
    if days.get(anchor, 0) == 0:
        anchor -= timedelta(days=1)
    if anchor < joined or days.get(anchor, 0) == 0:
        return Streak(0, None, None)

    start = anchor
    while start > joined and days.get(start - timedelta(days=1), 0) > 0:
        start -= timedelta(days=1)
    return Streak((anchor - start).days + 1, start, anchor)


def build_stats(login: str, token: str, now: datetime) -> ContributionStats:
    joined, days, total = fetch_contributions(login, token, now)
    today = now.date()
    active_days = [day for day, count in days.items() if count > 0 and day <= today]
    return ContributionStats(
        login=login,
        joined=joined,
        total=total,
        current=current_streak(days, joined, today),
        longest=longest_streak(days, joined, today),
        last_activity=max(active_days) if active_days else None,
        days=days,
    )


def format_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def format_date(value: date | None) -> str:
    if value is None:
        return "SEM ATIVIDADE"
    return f"{value.day:02d} {MONTHS[value.month]} {value.year}"


def format_range(streak: Streak) -> str:
    if streak.count == 0 or streak.start is None or streak.end is None:
        return "SEM SEQUÊNCIA ATIVA"
    if streak.start == streak.end:
        return format_date(streak.start)
    if streak.start.year == streak.end.year and streak.start.month == streak.end.month:
        return f"{streak.start.day:02d} - {format_date(streak.end)}"
    if streak.start.year == streak.end.year:
        return (
            f"{streak.start.day:02d} {MONTHS[streak.start.month]} - "
            f"{format_date(streak.end)}"
        )
    return f"{format_date(streak.start)} - {format_date(streak.end)}"


def recent_window(stats: ContributionStats, length: int = 48) -> list[tuple[date, int]]:
    end = stats.last_activity or stats.joined
    start = end - timedelta(days=length - 1)
    return [(start + timedelta(days=index), stats.days.get(start + timedelta(days=index), 0)) for index in range(length)]


def activity_color(count: int, theme: dict[str, str]) -> str:
    if count == 0:
        return theme["grid"]
    if count == 1:
        return theme["cyan"]
    if count <= 3:
        return theme["blue"]
    if count <= 7:
        return theme["green"]
    return theme["violet"]


def stats_svg(stats: ContributionStats, theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    label = f'{mono} font-size="11" font-weight="800" fill="{theme["cyan"]}"'
    muted = f'{mono} font-size="10" fill="{theme["muted"]}"'
    number = f'{mono} font-size="54" font-weight="800" fill="{theme["ink"]}"'
    recent = recent_window(stats)
    cells = []
    for index, (_, count) in enumerate(recent):
        x = 370 + index * 16
        color = activity_color(count, theme)
        opacity = "0.58" if count == 0 else "1"
        cells.append(
            f'<rect x="{x}" y="286" width="11" height="11" rx="2" fill="{color}" opacity="{opacity}"/>'
        )

    total = html.escape(format_number(stats.total))
    current = html.escape(format_number(stats.current.count))
    longest = html.escape(format_number(stats.longest.count))
    joined = html.escape(format_date(stats.joined))
    current_range = html.escape(format_range(stats.current))
    longest_range = html.escape(format_range(stats.longest))
    last_activity = html.escape(format_date(stats.last_activity))
    login = html.escape(stats.login)
    description = html.escape(
        f"{stats.total} contribuições, sequência atual de {stats.current.count} dias e "
        f"maior sequência de {stats.longest.count} dias."
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="330" viewBox="0 0 1180 330" role="img" aria-labelledby="title desc">
<title id="title">Estatísticas de contribuições de {login}</title>
<desc id="desc">{description}</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{theme['cyan']}"/><stop offset="0.52" stop-color="{theme['blue']}"/><stop offset="1" stop-color="{theme['violet']}"/></linearGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{theme['grid']}" opacity="0.42"/></pattern>
  <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="330" rx="14" fill="{theme['bg']}"/>
<rect width="1180" height="330" rx="14" fill="url(#grid)"/>
<rect x="3" y="3" width="1174" height="324" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<path d="M24 43H1156" stroke="{theme['grid']}"/>
<text x="24" y="29" {label}>CONTRIBUIÇÕES.LOG // {login.upper()}</text>
<text x="1156" y="29" text-anchor="end" {muted}>API OFICIAL // ÚLTIMA ATIVIDADE {last_activity}</text>

<rect x="24" y="62" width="360" height="190" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<rect x="24" y="62" width="360" height="3" rx="2" fill="{theme['cyan']}"/>
<text x="43" y="91" {label}>01 // TOTAL.DE.CONTRIBUIÇÕES</text>
<text x="43" y="158" {number}>{total}</text>
<text x="43" y="184" {muted}>CONTRIBUIÇÕES REGISTRADAS</text>
<path d="M43 206H348" stroke="{theme['grid']}"/>
<text x="43" y="229" {muted}>CONTA DESDE // {joined}</text>
<circle cx="333" cy="146" r="28" fill="none" stroke="{theme['cyan']}" opacity="0.18"/>
<circle cx="333" cy="146" r="5" fill="{theme['cyan']}" filter="url(#glow)"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.6s" repeatCount="indefinite"/></circle>

<rect x="410" y="62" width="360" height="190" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<rect x="410" y="62" width="360" height="3" rx="2" fill="{theme['green']}"/>
<text x="429" y="91" {label}>02 // SEQUÊNCIA.ATUAL</text>
<text x="429" y="158" {number}>{current}</text>
<text x="429" y="184" {muted}>DIAS CONSECUTIVOS</text>
<path d="M429 206H734" stroke="{theme['grid']}"/>
<text x="429" y="229" {muted}>{current_range}</text>
<circle cx="719" cy="146" r="28" fill="none" stroke="{theme['green']}" opacity="0.18"/>
<circle cx="719" cy="146" r="5" fill="{theme['green']}" filter="url(#glow)"><animate attributeName="r" values="4;7;4" dur="2.4s" repeatCount="indefinite"/></circle>

<rect x="796" y="62" width="360" height="190" rx="8" fill="{theme['panel']}" stroke="{theme['grid']}"/>
<rect x="796" y="62" width="360" height="3" rx="2" fill="{theme['violet']}"/>
<text x="815" y="91" {label}>03 // MAIOR.SEQUÊNCIA</text>
<text x="815" y="158" {number}>{longest}</text>
<text x="815" y="184" {muted}>DIAS CONSECUTIVOS</text>
<path d="M815 206H1120" stroke="{theme['grid']}"/>
<text x="815" y="229" {muted}>{longest_range}</text>
<circle cx="1105" cy="146" r="28" fill="none" stroke="{theme['violet']}" opacity="0.18"/>
<path d="M1097 146L1103 152L1114 139" fill="none" stroke="{theme['violet']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

<rect x="24" y="270" width="1132" height="42" rx="8" fill="{theme['panel_alt']}" stroke="{theme['grid']}"/>
<text x="43" y="296" {label}>ATIVIDADE.RECENTE // 48 DIAS</text>
{''.join(cells)}
</svg>'''


def fingerprint(stats: ContributionStats) -> str:
    payload = {
        "joined": stats.joined.isoformat(),
        "total": stats.total,
        "current": [stats.current.count, str(stats.current.start), str(stats.current.end)],
        "longest": [stats.longest.count, str(stats.longest.start), str(stats.longest.end)],
        "last_activity": str(stats.last_activity),
        "recent": [(str(day), count) for day, count in recent_window(stats)],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:10]


def update_readme(digest: str) -> None:
    block = f'''{README_START}
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nan733/nan733/main/assets/contributions-{digest}-dark.svg">
  <img width="100%" alt="Total de contribuições e sequências de nandek" src="https://raw.githubusercontent.com/nan733/nan733/main/assets/contributions-{digest}-light.svg">
</picture>
{README_END}'''
    content = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(README_START) + r".*?" + re.escape(README_END), re.DOTALL)
    updated, replacements = pattern.subn(block, content)
    if replacements != 1:
        raise RuntimeError("Contribution stats markers are missing or duplicated in README.md")
    README.write_text(updated, encoding="utf-8")


def write_assets(stats: ContributionStats) -> str:
    ASSETS.mkdir(exist_ok=True)
    digest = fingerprint(stats)
    expected = set()
    for name, theme in THEMES.items():
        filename = f"contributions-{digest}-{name}.svg"
        expected.add(filename)
        (ASSETS / filename).write_text(stats_svg(stats, theme), encoding="utf-8")

    for path in ASSETS.glob("contributions-*.svg"):
        if path.name not in expected:
            path.resolve().relative_to(ASSETS.resolve())
            path.unlink()
    update_readme(digest)
    return digest


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN or GH_TOKEN is required")
    stats = build_stats(args.login, token, utc_now(args.now))
    digest = write_assets(stats)
    print(
        json.dumps(
            {
                "asset": digest,
                "total": stats.total,
                "current_streak": stats.current.count,
                "longest_streak": stats.longest.count,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
