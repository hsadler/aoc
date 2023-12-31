import sys

sys.path.append("..")

from helpers import functions

cached_id_to_winning_copy_ids: dict[int, list[int]] = {}


class Card:
    data: str
    card_id: int
    winning_numbers: list[int]
    scratch_numbers: list[int]

    def __init__(self, data: str):
        self.data = data
        self.card_id, self.winning_numbers, self.scratch_numbers = self.parse(data)

    @staticmethod
    def parse(data: str) -> tuple[str, list[int], list[int]]:
        ###
        # sample card data:
        # Card   1:  9 32  7 82 10 36 31 12 85 95 |  7 69 23  9 32 22 47 10 95 14 24 71 57 12 31 59 36 68  2 82 38 80 85 21 92
        ###
        card_id = int(data.split(":")[0].split(" ")[-1].strip())
        winning_numbers = data.split("|")[0].split(":")[-1].split()
        winning_numbers = [int(x) for x in winning_numbers]
        scratch_numbers = data.split("|")[1].strip().split()
        scratch_numbers = [int(x) for x in scratch_numbers]
        return (card_id, winning_numbers, scratch_numbers)

    def get_match_count(self) -> int:
        return len([x for x in self.winning_numbers if x in self.scratch_numbers])

    def get_score(self) -> int:
        base_score = self.get_match_count()
        final_score = 0
        for _ in range(0, base_score):
            if final_score == 0:
                final_score = 1
            else:
                final_score *= 2
        return final_score

    def get_winning_copy_ids(self) -> list[int]:
        if self.card_id in cached_id_to_winning_copy_ids:
            return cached_id_to_winning_copy_ids[self.card_id]
        else:
            winning_copy_ids = []
            for i in range(self.card_id + 1, self.card_id + self.get_match_count() + 1):
                winning_copy_ids.append(i)
            cached_id_to_winning_copy_ids[self.card_id] = winning_copy_ids
            return winning_copy_ids

    def print(self) -> None:
        print(
            {
                "card_id": self.card_id,
                "winning_numbers": self.winning_numbers,
                "scratch_numbers": self.scratch_numbers,
                "score": self.get_score(),
            }
        )


def prob_1():
    with open("input.txt", "r") as f:
        lines = f.readlines()
        cards: list[Card] = []
        for l in lines:
            card = Card(l)
            cards.append(card)
        print(sum([c.get_score() for c in cards]))


def prob_2():
    # parse
    with open("input.txt", "r") as f:
        lines = f.readlines()
        cards: list[Card] = []
        card_lookup: dict[int, Card] = {}
        for l in lines:
            card = Card(l)
            cards.append(card)
            card_lookup[card.card_id] = card

    # traverse cards to get winning copies
    def traverse(
        card: Card,
        card_lookup: dict[int, Card],
        accum_cards: list[Card],
        depth: int = 0,
    ) -> None:
        winning_cards = [card_lookup[x] for x in card.get_winning_copy_ids()]
        if len(winning_cards) == 0:
            return
        else:
            for winning_card in winning_cards:
                accum_cards.append(winning_card)
                depth += 1
                traverse(winning_card, card_lookup, accum_cards, depth)

    final_cards: list[Card] = []
    for breadth, card in enumerate(cards):
        # print(f"breadth: {breadth}")
        accum_cards = [card]
        traverse(card, card_lookup, accum_cards)
        final_cards += accum_cards
        # print(len([x.card_id for x in accum_cards]))
    print(len(final_cards))


prob_1()
print("----")
prob_2()
