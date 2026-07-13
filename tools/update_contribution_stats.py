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
from dataclasses import dataclass, replace
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
README = ROOT / "README.md"
STATE = ASSETS / "contribution-stats.json"
API_URL = "https://api.github.com/graphql"
README_START = "<!-- contribution-stats:start -->"
README_END = "<!-- contribution-stats:end -->"
LAYOUT_VERSION = 6

try:
    PROFILE_TIMEZONE = ZoneInfo("America/Sao_Paulo")
except ZoneInfoNotFoundError:
    PROFILE_TIMEZONE = timezone(timedelta(hours=-3))
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
    first_activity: date | None
    as_of: date
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
        # Contribution calendars are day-based; querying through today's end avoids
        # transient partial-day replicas without counting activity that does not exist.
        today_end = datetime.combine(now.date(), time.max, timezone.utc)
        period_end = min(today_end, year_end)
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


def build_stats_once(login: str, token: str, now: datetime) -> ContributionStats:
    joined, days, total = fetch_contributions(login, token, now)
    today = now.date()
    active_days = [day for day, count in days.items() if count > 0 and day <= today]
    return ContributionStats(
        login=login,
        joined=joined,
        first_activity=min(active_days) if active_days else None,
        as_of=now.astimezone(PROFILE_TIMEZONE).date(),
        total=total,
        current=current_streak(days, joined, today),
        longest=longest_streak(days, joined, today),
        last_activity=max(active_days) if active_days else None,
        days=days,
    )


def build_stats(login: str, token: str, now: datetime) -> ContributionStats:
    snapshots = [build_stats_once(login, token, now) for _ in range(3)]
    return max(
        snapshots,
        key=lambda stats: (
            stats.total,
            stats.longest.count,
            stats.current.count,
            stats.last_activity or date.min,
        ),
    )


def parse_streak(payload: dict) -> Streak:
    return Streak(
        count=int(payload["count"]),
        start=date.fromisoformat(payload["start"]) if payload.get("start") else None,
        end=date.fromisoformat(payload["end"]) if payload.get("end") else None,
    )


def reconcile_with_state(stats: ContributionStats, today: date) -> ContributionStats:
    if not STATE.exists():
        return stats
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    if payload.get("login") != stats.login:
        return stats

    previous_total = int(payload.get("total", 0))
    previous_longest = parse_streak(payload["longest"])
    previous_current = parse_streak(payload["current"])
    previous_last = (
        date.fromisoformat(payload["last_activity"])
        if payload.get("last_activity")
        else None
    )
    previous_first = (
        date.fromisoformat(payload["first_activity"])
        if payload.get("first_activity")
        else None
    )

    longest = stats.longest
    if previous_longest.count > longest.count:
        longest = previous_longest

    current = stats.current
    if (
        (
            stats.total < previous_total
            or (
                previous_last is not None
                and (stats.last_activity is None or previous_last > stats.last_activity)
            )
        )
        and previous_current.end is not None
        and previous_current.end >= today - timedelta(days=1)
        and previous_current.count > current.count
    ):
        current = previous_current

    last_activity = stats.last_activity
    if previous_last is not None and (
        last_activity is None or previous_last > last_activity
    ):
        last_activity = previous_last

    first_activity = stats.first_activity
    if previous_first is not None and (
        first_activity is None or previous_first < first_activity
    ):
        first_activity = previous_first

    return replace(
        stats,
        first_activity=first_activity,
        total=max(stats.total, previous_total),
        current=current,
        longest=longest,
        last_activity=last_activity,
    )


def save_state(stats: ContributionStats) -> None:
    def streak_payload(streak: Streak) -> dict[str, int | str | None]:
        return {
            "count": streak.count,
            "start": streak.start.isoformat() if streak.start else None,
            "end": streak.end.isoformat() if streak.end else None,
        }

    payload = {
        "login": stats.login,
        "first_activity": (
            stats.first_activity.isoformat() if stats.first_activity else None
        ),
        "updated_on": stats.as_of.isoformat(),
        "total": stats.total,
        "current": streak_payload(stats.current),
        "longest": streak_payload(stats.longest),
        "last_activity": (
            stats.last_activity.isoformat() if stats.last_activity else None
        ),
    }
    STATE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
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


def stats_svg(stats: ContributionStats, theme: dict[str, str]) -> str:
    mono = 'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" letter-spacing="0"'
    label = f'{mono} font-size="15" font-weight="800" fill="{theme["cyan"]}"'
    muted = f'{mono} font-size="13" font-weight="600" fill="{theme["muted"]}"'
    total_number = f'{mono} font-size="70" font-weight="800" fill="{theme["blue"]}"'
    longest_number = f'{mono} font-size="70" font-weight="800" fill="{theme["violet"]}"'

    total = html.escape(format_number(stats.total))
    current = html.escape(format_number(stats.current.count))
    longest = html.escape(format_number(stats.longest.count))
    updated_on = html.escape(format_date(stats.as_of))
    current_range = html.escape(format_range(stats.current))
    longest_range = html.escape(format_range(stats.longest))
    last_activity = html.escape(format_date(stats.last_activity))
    login = html.escape(stats.login)
    description = html.escape(
        f"{stats.total} contribuições, sequência atual de {stats.current.count} dias e "
        f"maior sequência de {stats.longest.count} dias."
    )
    circumference = 2 * 3.141592653589793 * 68
    progress = 0 if stats.longest.count == 0 else min(stats.current.count / stats.longest.count, 1)
    progress_length = circumference * progress
    current_font_size = 60 if len(current) <= 2 else 48 if len(current) <= 3 else 38

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="330" viewBox="0 0 1180 330" role="img" aria-labelledby="title desc">
<title id="title">Estatísticas de contribuições de {login}</title>
<desc id="desc">{description}</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{theme['cyan']}"/><stop offset="0.52" stop-color="{theme['blue']}"/><stop offset="1" stop-color="{theme['violet']}"/></linearGradient>
  <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{theme['grid']}" opacity="0.42"/></pattern>
  <radialGradient id="centerGlow" cx="50%" cy="40%" r="52%"><stop offset="0" stop-color="{theme['cyan']}" stop-opacity="0.13"/><stop offset="1" stop-color="{theme['bg']}" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="330" rx="14" fill="{theme['bg']}"/>
<rect width="1180" height="330" rx="14" fill="url(#grid)"/>
<rect width="1180" height="330" rx="14" fill="url(#centerGlow)"/>
<rect x="3" y="3" width="1174" height="324" rx="12" fill="none" stroke="url(#accent)" stroke-width="2"/>
<path d="M24 43H1156" stroke="{theme['grid']}"/>
<text x="24" y="29" {label}>CONTRIBUIÇÕES.LOG // {login.upper()}</text>
<text x="1156" y="29" text-anchor="end" {muted}>API OFICIAL // ÚLTIMA ATIVIDADE {last_activity}</text>

<rect x="24" y="62" width="1132" height="222" rx="8" fill="{theme['panel']}" fill-opacity="0.88" stroke="{theme['grid']}"/>
<path d="M402 82V264M778 82V264" stroke="{theme['muted']}" stroke-width="2" opacity="0.5"/>

<g text-anchor="middle">
  <text x="213" y="100" {label}>TOTAL</text>
  <text x="213" y="171" {total_number}>{total}</text>
  <text x="213" y="202" {mono} font-size="17" font-weight="800" fill="{theme['ink']}">TOTAL DE CONTRIBUIÇÕES</text>
  <text x="213" y="235" {muted}>ATUALIZADO EM {updated_on}</text>
  <path d="M115 256H311" stroke="{theme['blue']}" stroke-width="2" opacity="0.55"/>

  <circle cx="590" cy="149" r="68" fill="{theme['panel_alt']}" stroke="{theme['grid']}" stroke-width="11"/>
  <circle cx="590" cy="149" r="68" fill="none" stroke="url(#accent)" stroke-width="11" stroke-linecap="round" stroke-dasharray="{progress_length:.1f} {circumference:.1f}" transform="rotate(-90 590 149)" filter="url(#glow)"/>
  <path d="M590 50C590 50 605 64 605 75C605 84 599 91 590 91C581 91 575 84 575 76C575 67 580 61 585 56C585 62 587 66 591 68C596 62 595 56 590 50Z" fill="{theme['panel']}" stroke="{theme['cyan']}" stroke-width="3" stroke-linejoin="round" filter="url(#glow)"/>
  <path d="M590 68C596 73 597 78 594 82C592 86 587 86 585 82C583 78 586 73 590 68Z" fill="{theme['cyan']}"><animate attributeName="opacity" values="0.55;1;0.55" dur="1.8s" repeatCount="indefinite"/></path>
  <text x="590" y="169" {mono} font-size="{current_font_size}" font-weight="800" fill="{theme['ink']}">{current}</text>
  <text x="590" y="246" {label}>SEQUÊNCIA ATUAL</text>
  <text x="590" y="272" {muted}>{current_range}</text>

  <text x="967" y="100" {label}>RECORDE</text>
  <text x="967" y="171" {longest_number}>{longest}</text>
  <text x="967" y="202" {mono} font-size="17" font-weight="800" fill="{theme['ink']}">MAIOR SEQUÊNCIA</text>
  <text x="967" y="235" {muted}>{longest_range}</text>
  <path d="M869 256H1065" stroke="{theme['violet']}" stroke-width="2" opacity="0.55"/>
</g>

<circle cx="24" cy="307" r="4" fill="{theme['green']}" filter="url(#glow)"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="37" y="312" {muted}>STATUS // SINCRONIZADO</text>
<text x="1156" y="312" text-anchor="end" {muted}>FONTE // GITHUB GRAPHQL</text>
</svg>'''


def fingerprint(stats: ContributionStats) -> str:
    payload = {
        "layout": LAYOUT_VERSION,
        "joined": stats.joined.isoformat(),
        "first_activity": str(stats.first_activity),
        "updated_on": stats.as_of.isoformat(),
        "total": stats.total,
        "current": [stats.current.count, str(stats.current.start), str(stats.current.end)],
        "longest": [stats.longest.count, str(stats.longest.start), str(stats.longest.end)],
        "last_activity": str(stats.last_activity),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:10]


def update_readme(digest: str) -> None:
    block = f'''{README_START}
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nan733/nan733/main/assets/contributions-{digest}-dark.svg">
  <img width="100%" alt="Total de contribuições e sequências de Renan Oliveira" src="https://raw.githubusercontent.com/nan733/nan733/main/assets/contributions-{digest}-light.svg">
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
    save_state(stats)
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
    now = utc_now(args.now)
    stats = reconcile_with_state(build_stats(args.login, token, now), now.date())
    digest = write_assets(stats)
    print(
        json.dumps(
            {
                "asset": digest,
                "updated_on": stats.as_of.isoformat(),
                "total": stats.total,
                "current_streak": stats.current.count,
                "longest_streak": stats.longest.count,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
