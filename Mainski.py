import random

# Global variables
suits = {
    1: ["♥", "♦", "♣", "♠"],
    2: ["😃", "😈", "😵", "🤢", "😨"],
    3: ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
}
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
numerical_card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 1
}

# Initialize deck, player cards, and robot cards as empty lists
deck, player_cards, robot_cards = [], [], []
game_started = False

# Function to create a deck of cards
def create_deck(selected_suit_type):
    global deck
    deck = [f"{value}{suit}" for suit in suits[selected_suit_type] for value in values]
    shuffle_deck()

# Function to shuffle the deck
def shuffle_deck():
    global deck
    random.shuffle(deck)

# Function to pick a card from the deck
def pick_card():
    global deck  # Use the global deck variable
    if deck:
        chosen_card = random.choice(deck)  # Randomly select a card from the global deck
        deck.remove(chosen_card)  # Remove the selected card from the global deck
        return chosen_card
    else:
        print("The deck is empty. No more cards can be picked.")
        return None

# Function to check the result (placeholder for the complete logic)
def check_result():
    def card_value(card):
        # Extract the card's value (which might include numbers or face card letters)
        value = card[:-1]  # Assuming the last character is the suit, and everything before is the value

        # Use the dictionary to get the numeric value for both number and face cards
        return numerical_card_values[value]

    def evaluate_rule_1(cards):
        values_count = {card[:-1]: 0 for card in cards}
        for card in cards:
            values_count[card[:-1]] += 1
        return all(count == len(suits) for count in values_count.values())

    def evaluate_rule_2(cards):
        values_count = {card[:-1]: 0 for card in cards}
        for card in cards:
            values_count[card[:-1]] += 1
        return sum(count >= len(suits) - 1 for count in values_count.values()) >= len(suits) - 1

    def evaluate_rule_3(cards):
        second_suit = suits[1]
        return len([card for card in cards if card.endswith(second_suit)])

    def evaluate_rule_4(cards):
        total_value = sum(card_value(card) for card in cards)
        return total_value / len(cards) if cards else 0

    player_rules = {
        1: evaluate_rule_1(player_cards),
        2: evaluate_rule_2(player_cards),
        3: evaluate_rule_3(player_cards),
        4: evaluate_rule_4(player_cards)
    }

    robot_rules = {
        1: evaluate_rule_1(robot_cards),
        2: evaluate_rule_2(robot_cards),
        3: evaluate_rule_3(robot_cards),
        4: evaluate_rule_4(robot_cards)
    }

    for rule in sorted(player_rules.keys()):
        player_meets = player_rules[rule]
        robot_meets = robot_rules[rule]
        if rule == 3 or rule == 4:  # These rules require comparison of values
            player_meets = player_rules[rule] > robot_rules[rule]
            robot_meets = robot_rules[rule] > player_rules[rule]

        if player_meets and not robot_meets:
            return True, f"Player wins by Rule {rule}."
        elif robot_meets and not player_meets:
            return False, f"Robot wins by Rule {rule}."
    return False, "No rules met. Player loses by default."

# Placeholder for showing cards
def show_cards():
    global player_cards
    return ' '.join(player_cards)

# Start the game with a chosen suit type
def start_game(suits_key):
    global game_started, deck, player_cards, robot_cards
    game_started = True
    player_cards = []
    robot_cards = []
    create_deck(suits_key)
    shuffle_deck()

# A function to call when exiting the game
def exit_game():
    global game_started
    game_started = False
    # Any other cleanup can go here

