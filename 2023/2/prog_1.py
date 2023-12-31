valid_game_ids: list[int] = []

bag = {"red": 12, "green": 13, "blue": 14}


def parse(line: str) -> tuple[int, list[str]]:
    game_info, raw_games = line.split(":")
    game_id: int = int(game_info.strip()[5:])
    # print(game_id)
    # print(f"bag: {bag}")
    games: list[str] = raw_games.strip().split(";")
    games = [role.strip() for role in games]
    return game_id, games


def eval_games(games: list[str]) -> bool:
    for game in games:
        roles = [r.strip() for r in game.split(",")]
        roles_data: dict[str, int] = {
            role.split()[1]: role.split()[0] for role in roles
        }
        # print(roles_data)
        for role_color, count in roles_data.items():
            if int(count) > bag[role_color]:
                # print(f"invalid: {role_color} {count}")
                return False
    return True


with open("input.txt", "r") as file:
    for line in file.readlines():
        game_id, games = parse(line)
        games_are_valid = eval_games(games)
        if games_are_valid:
            valid_game_ids.append(game_id)

print(sum(valid_game_ids))
