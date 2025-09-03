import csv
from dataclasses import dataclass, asdict
from typing import List, Optional

CSV_FILE = "./database/players.csv"

@dataclass
class Player:
    Name: str
    Team: str
    Season: int
    Photo: str
    Physical: int
    Speed: int
    Vision: int
    Attacking: int
    Technical: int
    Aerial: int
    Defending: int
    Mental: int
    Goals: int
    Assists: int
    Matches: int
    Minutes: int


class PlayerRepository:
    @staticmethod
    def load_all() -> List[Player]:
        players = []
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append(Player(
                    Name=row["Name"],
                    Team=row["Team"],
                    Season=int(row["Season"]),
                    Photo=row["Photo"],
                    Physical=int(row["Physical"]),
                    Speed=int(row["Speed"]),
                    Vision=int(row["Vision"]),
                    Attacking=int(row["Attacking"]),
                    Technical=int(row["Technical"]),
                    Aerial=int(row["Aerial"]),
                    Defending=int(row["Defending"]),
                    Mental=int(row["Mental"]),
                    Goals=int(row["Goals"]),
                    Assists=int(row["Assists"]),
                    Matches=int(row["Matches"]),
                    Minutes=int(row["Minutes"]),
                ))
        return players

    @staticmethod
    def save_all(players: List[Player]) -> None:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=Player.__annotations__.keys())
            writer.writeheader()
            for player in players:
                writer.writerow(asdict(player))

    @staticmethod
    def add(player: Player) -> None:
        players = PlayerRepository.load_all()
        players.append(player)
        PlayerRepository.save_all(players)

    @staticmethod
    def find_by_name(name: str) -> Optional[Player]:
        players = PlayerRepository.load_all()
        for p in players:
            if p.Name.lower() == name.lower():
                return p
        return None

    @staticmethod
    def update(name: str, new_data: dict) -> bool:
        players = PlayerRepository.load_all()
        updated = False
        for i, p in enumerate(players):
            if p.Name.lower() == name.lower():
                for key, value in new_data.items():
                    if hasattr(p, key):
                        setattr(p, key, value)
                players[i] = p
                updated = True
                break
        if updated:
            PlayerRepository.save_all(players)
        return updated

    @staticmethod
    def delete(name: str) -> bool:
        players = PlayerRepository.load_all()
        new_players = [p for p in players if p.Name.lower() != name.lower()]
        if len(new_players) != len(players):
            PlayerRepository.save_all(new_players)
            return True
        return False
