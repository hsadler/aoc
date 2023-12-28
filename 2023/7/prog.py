import sys
sys.path.append('..')

import json

from helpers import functions
functions.test_sort_list()

# cards
# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card,

# 1. rank hands worst to best
# 2. calculate payout of each hand
# 3. sum payouts

# Python custom sorting example
def custom_sort(element):
    # Define your custom sorting logic here
    return len(element)
# Original list
my_list = ["apple", "banana", "kiwi", "orange", "grape"]
# Sort the list using the custom_sort function
sorted_list = sorted(my_list, key=custom_sort)
# print("Original List:", my_list)
# print("Sorted List:", sorted_list)

FIVE_OF_A_KIND = "FIVE_OF_A_KIND"
FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
FULL_HOUSE = "FULL_HOUSE"
THREE_OF_A_KIND = "THREE_OF_A_KIND"
TWO_PAIR = "TWO_PAIR"
ONE_PAIR = "ONE_PAIR"
HIGH_CARD = "HIGH_CARD"

classification_order = [
    FIVE_OF_A_KIND,
    FOUR_OF_A_KIND,
    FULL_HOUSE,
    THREE_OF_A_KIND,
    TWO_PAIR,
    ONE_PAIR,
    HIGH_CARD,
]

classification_to_score = {
    FIVE_OF_A_KIND: 100,
    FOUR_OF_A_KIND: 90,
    FULL_HOUSE: 80,
    THREE_OF_A_KIND: 70,
    TWO_PAIR: 60,
    ONE_PAIR: 50,
    HIGH_CARD: 40,
}

card_to_score = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

class Hand:
    cards: str
    cards_permutations: list[list[str]]
    best_permutation: str
    bid: int
    classification: str | None
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.payout = 0
        self.classification = self.classify_hand(list(self.cards))
        self.calc_cards_permutations()
    def __repr__(self) -> str:
        return f"{self.cards} {self.bid} {self.payout} {self.classification} {self.best_permutation} {self.cards_permutations}"
    def __str__(self) -> str:
        return f"{self.cards} {self.bid} {self.payout} {self.classification} {self.best_permutation} {self.cards_permutations}"
    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=4)
    def classify_hand(self, cards: list[str]) -> str:
        card_counts = {}
        for c in cards:
            if c not in card_counts:
                card_counts[c] = 0
            card_counts[c] += 1
        if len(card_counts) == 1:
            return FIVE_OF_A_KIND
        elif len(card_counts) == 2:
            if 4 in card_counts.values():
                return FOUR_OF_A_KIND
            else:
                return FULL_HOUSE
        elif len(card_counts) == 3:
            if 3 in card_counts.values():
                return THREE_OF_A_KIND
            else:
                return TWO_PAIR
        elif len(card_counts) == 4:
            return ONE_PAIR
        else:
            return HIGH_CARD
    def calc_cards_permutations(self):
        self.cards_permutations = [self.cards]
        joker_indices = []
        for i, card in enumerate(self.cards):
            if card == "J":
                joker_indices.append(i)
        for joker_index in joker_indices:
            new_permutations = []
            for permutation in self.cards_permutations:
                for card in "AKQT98765432":
                    new_permutation = permutation[:joker_index] + card + permutation[joker_index+1:]
                    new_permutations.append(new_permutation)
            self.cards_permutations = new_permutations
    def get_best_permutation(self) -> str:
        classification_to_hands = {
            FIVE_OF_A_KIND: [],
            FOUR_OF_A_KIND: [],
            FULL_HOUSE: [],
            THREE_OF_A_KIND: [],
            TWO_PAIR: [],
            ONE_PAIR: [],
            HIGH_CARD: [],
        }
        for permutation in self.cards_permutations:
            classification = self.classify_hand(list(permutation))
            classification_to_hands[classification].append(permutation)
        for classification in classification_order:
            if len(classification_to_hands[classification]) > 0:
                return classification_to_hands[classification][0]
    def reclassify_hand_from_wildcards(self):
        self.best_permutation = self.get_best_permutation()
        self.classification = self.classify_hand(list(self.best_permutation))
    @staticmethod
    def compare_hands(h1: 'Hand', h2: 'Hand') -> bool:
        for i in range(0, len(h1.cards)):
            if card_to_score[h1.cards[i]] == card_to_score[h2.cards[i]]:
                continue
            if card_to_score[h1.cards[i]] > card_to_score[h2.cards[i]]:
                return True
            return False
        return False
    @classmethod
    def sort_hands(cls, hands: list['Hand']) -> list['Hand']:
        return functions.sort_list(hands, compare=cls.compare_hands)[::-1]
    @classmethod
    def get_classification_to_hands(cls, hands: list['Hand']) -> dict[str, list['Hand']]:
        classification_to_hands: dict[str, list[Hand]] = {}
        for classification in classification_order:
            classification_to_hands[classification] = []
        for h in hands:
            classification_to_hands[h.classification].append(h)
        for classification in classification_order:
            curr_hands = classification_to_hands[classification]
            classification_to_hands[classification] = cls.sort_hands(curr_hands)
        return classification_to_hands
    
def test_compare_hands():
    hand1 = Hand("AAAAA", 0)
    hand2 = Hand("KKKKK", 0)
    hand3 = Hand("KKKKQ", 0)
    hand4 = Hand("KKKKK", 0)
    hand5 = Hand("KKKKQ", 0)
    hand6 = Hand("KKKKQ", 0)
    assert Hand.compare_hands(hand1, hand2) == True
    assert Hand.compare_hands(hand2, hand3) == True
    assert Hand.compare_hands(hand3, hand4) == False
    assert Hand.compare_hands(hand5, hand4) == False
    assert Hand.compare_hands(hand5, hand6) == False
test_compare_hands()

def test_sort_hands():
    hand1 = Hand("AQJTK", 0)
    hand2 = Hand("KQJTA", 0)
    hand3 = Hand("JQATA", 0)
    hand4 = Hand("JQKTA", 0)
    hand5 = Hand("TQJKA", 0)
    hand6 = Hand("2QJKA", 0)
    hands = [hand5, hand1, hand3, hand6, hand2, hand4]
    sorted_hands = Hand.sort_hands(hands)
    assert sorted_hands == [hand1, hand2, hand3, hand4, hand5, hand6]
test_sort_hands()

hands: list[Hand] = []
with open("input.txt") as f:
    lines = f.readlines()
    for l in lines:
        cards, bid = l.split()
        hand = Hand(cards, int(bid))
        hands.append(hand)

classification_to_hands = Hand.get_classification_to_hands(hands)

# compose final ranked hands
ranked_hands = []
for classification in classification_order:
    ranked_hands += classification_to_hands[classification]

# calculate total payout
total_payout = 0
for i, hand in enumerate(ranked_hands[::-1]):
    payout = hand.bid * (i+1)
    total_payout += payout

print(total_payout)
# know if total payout for part 1 has changed
assert total_payout == 248836197
print("----------")

# modify rules and reclassify hands
card_to_score["J"] = 1
for hand in hands:
    hand.reclassify_hand_from_wildcards()
classification_to_hands = Hand.get_classification_to_hands(hands)

# compose final ranked hands
ranked_hands = []
for classification in classification_order:
    ranked_hands += classification_to_hands[classification]

# calculate total payout
total_payout = 0
for i, hand in enumerate(ranked_hands[::-1]):
    payout = hand.bid * (i+1)
    total_payout += payout
[print(h) for h in ranked_hands]
print(total_payout)
