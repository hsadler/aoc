from dataclasses import dataclass

@dataclass
class Bag:
    red: int = 0
    blue: int = 0
    green: int = 0

    def power(self) -> int:
        return self.red * self.blue * self.green

bags: list[Bag] = []

def parse_game(line: str) -> tuple[int, list[str]]:
    game_info, raw_games = line.split(":")
    game_id: int = int(game_info.strip()[5:])
    # print(game_id)
    games: list[str] = raw_games.strip().split(";")
    games = [role.strip() for role in games]
    return game_id, games

def parse_role_datas(games: list[str]) -> dict[str, int]:
    roles_datas: list[dict[str, int]] = []
    for game in games:
        roles = [r.strip() for r in game.split(',')]
        roles_data: dict[str, int] = { 
            role.split()[1]: role.split()[0]
            for role in roles 
        }
        roles_datas.append(roles_data)
    return roles_datas

def get_bag_from_games(games: list[str]) -> Bag:
    roles_datas = parse_role_datas(games)
    # print(roles_datas)
    b: dict[str, int] = {
        "red": 0,
        "blue": 0,
        "green": 0
    }
    for role_data in roles_datas:
        for role_color, count in role_data.items():
            b[role_color] = int(count) \
            if int(count) > b[role_color] \
            else b[role_color]
    # print(b)
    return Bag(b["red"], b["blue"], b["green"])

with open("input.txt", "r") as file:
    for line in file.readlines():
        game_id, games = parse_game(line)
        bag = get_bag_from_games(games)
        bags.append(bag)

print(sum(b.power() for b in bags))
