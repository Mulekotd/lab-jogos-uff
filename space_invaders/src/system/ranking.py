from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


RANKING_FILE = Path(__file__).resolve().parents[2] / "ranking.txt"


@dataclass(frozen=True)
class RankingEntry:
    name: str
    score: int
    date: str


def save_ranking_entry(name: str, score: int):
    player_name = _sanitize_name(name)
    game_score = int(score)
    game_date = datetime.now().strftime("%d-%m-%Y")

    RANKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RANKING_FILE.open("a", encoding="utf-8") as ranking_file:
        ranking_file.write(f"{player_name};{game_score};{game_date}\n")


def load_top_ranking(limit: int = 5) -> list[RankingEntry]:
    entries = _load_ranking_entries()
    entries.sort(key=lambda entry: entry.score, reverse=True)
    return entries[:limit]


def _load_ranking_entries() -> list[RankingEntry]:
    if not RANKING_FILE.exists():
        return []

    entries: list[RankingEntry] = []
    with RANKING_FILE.open("r", encoding="utf-8") as ranking_file:
        for line in ranking_file:
            parts = [part.strip() for part in line.strip().split(";")]
            if len(parts) != 3:
                continue

            name, score_text, game_date = parts
            try:
                score = int(score_text)
            except ValueError:
                continue

            entries.append(RankingEntry(name=name, score=score, date=game_date))

    return entries


def _sanitize_name(name: str) -> str:
    sanitized = name.replace(";", " ").replace("\n", " ").strip()
    return sanitized[:20] if sanitized else "ANONIMO"
