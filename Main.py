import random
import math

# # Global Variables

# Suits available for the game, categorised for player selection via the game menu
suits = {
    1: ["♥", "♦", "♣", "♠"],
    2: ["😃", "😈", "😵", "🤢", "😨"],
    3: ["🤡", "👹", "👺", "👻", "👽", "👾", "🤖"]
}


# Fixed list of card values which includes numbers and the face cards.
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


# Assigning face card values to the numerical equivalents, along with the rest of the numbers.
numerical_card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13, "A": 1
}


# Initialise global deck, player cards and robots cards variable as empty list
deck = []
player_cards = []
robot_cards = []


# # Game menu Function


def game_menu():
    print("\nWelcome to the Card Game!")
    print("This game pits you against the computer in a strategic card draw competition.")
    print(
        "\nTo start the game, select option 1 followed by the deck type number. For example, '1 2' starts the game with Emoji Suits 1.")
    print("For other actions, simply enter the number corresponding to your desired action.")
    print("Note: The deck type can only be selected when starting a new game.")

    print("\nMenu Options:")
    print("1. Start Game")
    print("2. Pick a Card")
    print("3. Shuffle Deck")
    print("4. Show My Cards")
    print("5. Check Win/Lose")
    print("6. Exit")

    print("\nAvailable Suit Types:")
    print("1. Traditional Suits (♥, ♦, ♣, ♠)")
    print("2. Emoji Suits 1 (😃, 😈, 😵, 🤢, 😨)")
    print("3. Emoji Suits 2 (🤡, 👹, 👺, 👻, 👽, 👾, 🤖)")


# # Create Deck Function


def create_deck(suits, values):
    global deck
    deck.clear()

    for suit in suits:
        for value in values:
            deck.append(f"{value}{suit}")


# # Shuffle Deck Function


def shuffle_deck():
    global deck, suits
    # If the deck has less than 3 cards, we cannot maintain the special card order
    if len(deck) < 3:
        print("Not enough cards to shuffle according to the rules.")
        return

    # Shuffle the deck
    random.shuffle(deck)

    # Place the 'A' of the first suit at the beginning, 'Q' of the second in the middle, and 'K' of the last at the end
    first_suit_A = 'A' + suits[1][0]
    second_suit_Q = 'Q' + suits[1][1] if len(suits[1]) > 1 else 'Q' + suits[1][0]
    last_suit_K = 'K' + suits[1][-1]

    # Remove these cards if they exist in the deck
    deck = [card for card in deck if card not in (first_suit_A, second_suit_Q, last_suit_K)]

    # Insert them back at the required positions
    deck.insert(0, first_suit_A)
    deck.insert(len(deck) // 2, second_suit_Q)
    deck.append(last_suit_K)

    print("Deck has been shuffled with special cards in place.")


# # Pick Card Function


def pick_card():
    global deck  # Use the global deck variable
    if deck:
        chosen_card = random.choice(deck)  # Randomly select a card from the global deck
        deck.remove(chosen_card)  # Remove the selected card from the global deck
        return chosen_card
    else:
        print("The deck is empty. No more cards can be picked.")
        return None


# #Show Cards Function


def show_cards(player_cards):
    if player_cards:
        print("Your cards are: " + ", ".join(player_cards))
    else:
        print("You have no cards.")


# # Check Result Function


def check_result(player_cards, robot_cards, suits):
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


## Play Game Function
def play_game():
    global deck, player_cards, robot_cards, suits, values
    player_cards, robot_cards = [], []
    game_started = False

    while True:
        if not game_started:
            game_menu()
        else:
            print("\nMenu Options:")
            print("1. Start Game")
            print("2. Pick a Card")
            print("3. Shuffle Deck")
            print("4. Show My Cards")
            print("5. Check Win/Lose")
            print("6. Exit")

        user_input = input("\nEnter your choice (e.g., '1' or '1 2'): ").strip()
        inputs = user_input.split()

        if inputs[0] == "1":
            suit_type_key = int(inputs[1]) if len(inputs) > 1 and inputs[1].isdigit() else 1
            create_deck(suits[suit_type_key], values)
            shuffle_deck()
            print(f"Game started with deck type {suit_type_key}.")
            game_started = True

        elif inputs[0] == "2":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                continue
            card = pick_card()
            if card:
                player_cards.append(card)
                print(f"You picked: {card}")
                # Ensure the robot picks a card if there are cards left in the deck
                if deck:
                    robot_card = pick_card()
                    robot_cards.append(robot_card)
                if len(player_cards) == 6:
                    player_win, reason = check_result(player_cards, robot_cards, suits[suit_type_key])
                    print("\nFinal Results:")
                    print(f"Your cards: {' '.join(player_cards)}")
                    print(f"Robot's cards: {' '.join(robot_cards)}")
                    if player_win:
                        print(f"Congratulations, you win! {reason}")
                    else:
                        print(f"You lose. {reason}")
                    # Resetting for a new game
                    player_cards, robot_cards = [], []
                    game_started = False
            else:
                print("No more cards left to pick.")

        elif inputs[0] == "3":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                continue
            shuffle_deck()
            print("The deck has been shuffled.")

        elif inputs[0] == "4":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                continue
            show_cards(player_cards)

        elif inputs[0] == "5":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                continue
            if player_cards and robot_cards:
                player_win, reason = check_result(player_cards, robot_cards, suits[suit_type_key])
                print("\nCurrent Game Status:")
                print(f"Your cards: {' '.join(player_cards)}")
                print(f"Robot's cards: {' '.join(robot_cards)}")
                if player_win:
                    print(f"Current status: You're winning! {reason}")
                else:
                    print(f"Current status: You're losing. {reason}")
            else:
                print("You or the robot have no cards to check. Please pick a card first.")

        elif inputs[0] == "6":
            print("Exiting the game. Thank you for playing!")
            break

        else:
            print("Invalid option. Please try again.")

        print("-" * 80)


play_game()