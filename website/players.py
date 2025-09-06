import csv
from dataclasses import dataclass, asdict
from typing import List, Optional

CSV_FILE = "./database/players_preserved_exact.csv"

@dataclass
class Player:
    # Basic Info
    Name: str
    Team: str
    Season: str
    Position: str
    Age: int
    Height: float
    Weight: float
    Photo: str

    # Physical
    Acceleration: Optional[float] = None
    Agility: Optional[float] = None
    Balance: Optional[float] = None
    JumpingReach: Optional[float] = None
    NaturalFitness: Optional[float] = None
    Pace: Optional[float] = None
    Stamina: Optional[float] = None
    Strength: Optional[float] = None
    GoalkeeperAbility: Optional[float] = None
    Condition: Optional[float] = None
    PreferredFoot: Optional[str] = None

    # Technical
    Dribbling: Optional[float] = None
    Passing: Optional[float] = None
    Corners: Optional[float] = None
    Crossing: Optional[float] = None
    FirstTouch: Optional[float] = None
    Finishing: Optional[float] = None
    Penalty: Optional[float] = None
    FreeKick: Optional[float] = None
    LongShots: Optional[float] = None
    LongThrows: Optional[float] = None
    Heading: Optional[float] = None
    Marking: Optional[float] = None
    Tackling: Optional[float] = None
    Technique: Optional[float] = None

    # Mental
    Aggression: Optional[float] = None
    Anticipation: Optional[float] = None
    Bravery: Optional[float] = None
    Composure: Optional[float] = None
    Concentration: Optional[float] = None
    Decisions: Optional[float] = None
    Determination: Optional[float] = None
    Flair: Optional[float] = None
    Leadership: Optional[float] = None
    OffTheBall: Optional[float] = None
    Positioning: Optional[float] = None
    Teamwork: Optional[float] = None
    Vision: Optional[float] = None
    WorkRate: Optional[float] = None

    # Match Stats
    Goals: Optional[int] = None
    Assists: Optional[int] = None
    Matches: Optional[int] = None
    Minutes: Optional[int] = None


class PlayerRepository:
    @staticmethod
    def load_all() -> List[Player]:
        players = []
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append(Player(
                    # Basic Info
                    Name=row["Name"],
                    Team=row["Team"],
                    Season=row["Season"],
                    Position=row["Position"],
                    Age=row["Age"],
                    Height=row["Height"],
                    Weight=row["Weight"],
                    Photo=row["Photo"],

                    # Physical
                    Acceleration=row["Acceleration"],
                    Agility=row["Agility"],
                    Balance=row["Balance"],
                    JumpingReach=row["JumpingReach"],
                    NaturalFitness=row["NaturalFitness"],
                    Pace=row["Pace"],
                    Stamina=row["Stamina"],
                    Strength=row["Strength"],
                    GoalkeeperAbility=row["GoalkeeperAbility"],
                    Condition=row["Condition"],
                    PreferredFoot=row["PreferredFoot"],

                    # Technical
                    Dribbling=row["Dribbling"],
                    Passing=row["Passing"],
                    Corners=row["Corners"],
                    Crossing=row["Crossing"],
                    FirstTouch=row["FirstTouch"],
                    Finishing=row["Finishing"],
                    Penalty=row["Penalty"],
                    FreeKick=row["FreeKick"],
                    LongShots=row["LongShots"],
                    LongThrows=row["LongThrows"],
                    Heading=row["Heading"],
                    Marking=row["Marking"],
                    Tackling=row["Tackling"],
                    Technique=row["Technique"],

                    # Mental
                    Aggression=row["Aggression"],
                    Anticipation=row["Anticipation"],
                    Bravery=row["Bravery"],
                    Composure=row["Composure"],
                    Concentration=row["Concentration"],
                    Decisions=row["Decisions"],
                    Determination=row["Determination"],
                    Flair=row["Flair"],
                    Leadership=row["Leadership"],
                    OffTheBall=row["OffTheBall"],
                    Positioning=row["Positioning"],
                    Teamwork=row["Teamwork"],
                    Vision=row["Vision"],
                    WorkRate=row["WorkRate"],

                    # Match Stats
                    Goals=row["Goals"],
                    Assists=row["Assists"],
                    Matches=row["Matches"],
                    Minutes=row["Minutes"],
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
