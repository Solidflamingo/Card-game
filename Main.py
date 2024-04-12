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
drawn_cards = []
current_suit_type = 1


# # Game menu Function


def game_menu():
    # This function is the starting point of the game interface, greeting the player and explaining the basic premise and rules of the game.
    print("\nWelcome to the greatest card game of all time!")
    print("This game pits you against the computer in a random card draw competition.")
    print("\nTo start the game, select option 1 followed by the deck type number. For example, '1 2' starts the game with Emoji Suits 1.")
    print("You will then select option '2' to draw a card. The robot will also draw a hidden every time you draw.")
    print("\nThe game will end once you either each 6 cards or select option '5' to compare your cards to the cards the robot.")
    print("The game will determine a winner based on a priority of four rules. To view the winning hands, select option '6'.")
    print("Please note: The suit type can only be selected when starting a new game.")

    print("-" * 80)
    print("\nMenu Options:")
    print("1. Start Game")
    print("2. Pick a Card")
    print("3. Shuffle Deck")
    print("4. Show My Cards")
    print("5. Check Win/Lose")
    print("6  Show Winning Combinations")
    print("7. Exit")

    print("-" * 80)
    print("\nAvailable Suit Types:")
    print("1. Traditional Suits (♥, ♦, ♣, ♠)")
    print("2. Emoji Suits 1 (😃, 😈, 😵, 🤢, 😨)")
    print("3. Emoji Suits 2 (🤡, 👹, 👺, 👻, 👽, 👾, 🤖)")

    # The function uses print statements to display this information, with lines of hyphens to visually separate different sections for enhanced readability.


# # Create Deck Function


def create_deck(suits, values):
    global deck # Use the global 'deck' variable to ensure changes are reflected outside the function.
    deck.clear()

    for suit in suits:
        for value in values:
            # Create a card by combining the value and suit, and add it to the deck.
            deck.append(f"{value}{suit}")


# # Shuffle Deck Function


def shuffle_deck():
    global deck, suits, current_suit_type, drawn_cards

    selected_suits = suits[current_suit_type]  # Retrieves the array of suits for the selected deck type

    # Special cards based on the current suit type
    special_cards = {
        'A': 'A' + selected_suits[0],
        'Q': 'Q' + selected_suits[min(1, len(selected_suits) - 1)],
        'K': 'K' + selected_suits[-1]
    }

    # Exclude previously drawn cards and special cards for shuffling
    deck = [card for card in deck if card not in drawn_cards and card not in special_cards.values()]
    random.shuffle(deck)

    # Re-insert the special cards at their designated positions
    if special_cards['A'] not in drawn_cards:
        deck.insert(0, special_cards['A'])
    if special_cards['Q'] not in drawn_cards:
        deck.insert(len(deck) // 2, special_cards['Q'])
    if special_cards['K'] not in drawn_cards:
        deck.append(special_cards['K'])

    print("Deck has been shuffled with special cards in place.")


# # Pick Card Function


def pick_card(for_robot=False):
    global deck, player_cards, robot_cards, drawn_cards, suits  # Access global variables for deck and hands.

    # Define the three specials that cannot be drawn as they always must be in the deck in the corresponding position
    special_cards = {
        'A' + suits[1][0],  # 'A' of the first suit
        'Q' + suits[1][1] if len(suits[1]) > 1 else 'Q' + suits[1][0],  # 'Q' of the second suit (or first if only one)
        'K' + suits[1][-1],  # 'K' of the last suit
    }

    eligible_cards = [card for card in deck if card not in special_cards]  # Exclude special cards from draw pool

    if not eligible_cards:  # Check if there are any cards left to draw
        print("No more cards left to pick.")
        return None

    # Implement a 50/50 chance to skip the robot's turn to draw.
    if for_robot and not random.choice([True, False]):
        return None

    # Proceed if the deck is not empty.
    if deck:
        chosen_card = random.choice(deck)  # Randomly select a card from the global deck
        deck.remove(chosen_card)  # Remove the selected card from the global deck
        drawn_cards.append(chosen_card)  # keep track of drawn cards

        # Add the card to the robot's hand or return it for the player.
        if for_robot:
            robot_cards.append(chosen_card)  # Append directly to robot's hand.
        else:
            return chosen_card  # Return the card for the player to handle.

    else:
        print("The deck is empty. No more cards can be picked.")
        return None

# #Show Cards Function


def show_cards(player_cards):
    # Check if the player has any cards in their hand.
    if player_cards:
        # If there are cards, join them into a single string with commas and print.
        print("Your cards are: " + ", ".join(player_cards))
    else:
        # If the player has no cards, present a message.
        print("You have no cards.")


# # Check Result Function


def check_result(player_cards, robot_cards, suits):
    def card_value(card):
        value = card[:-1]
        # Use the dictionary to get the numeric value for both number and face cards
        return numerical_card_values[value]

    def evaluate_rule_1(cards):
        # Initialize a count dictionary for the values of the cards, disregarding suits.
        values_count = {card[:-1]: 0 for card in cards} # Initialize count for each card value.
        for card in cards: # Count occurrences of each value.
            values_count[card[:-1]] += 1
        # If all values are identical and equal to the number of suits in the deck, rule 1 is satisfied.
        return all(count == len(suits) for count in values_count.values())

    def evaluate_rule_2(cards):
        values_count = {card[:-1]: 0 for card in cards} # Count occurrences for each value.
        for card in cards:
            values_count[card[:-1]] += 1
        # Rule 2 is met if there's at least one value with its count equal to or one less than the total number of suits.
        return sum(count >= len(suits) - 1 for count in values_count.values()) >= len(suits) - 1

    def evaluate_rule_3(cards):
        second_suit = suits[1] # Identifies the second suit.
        return len([card for card in cards if card.endswith(second_suit)]) # Counts cards that end with the second suit symbol.

    def evaluate_rule_4(cards):
        total_value = sum(card_value(card) for card in cards) # Sum card values.
        return total_value / len(cards) if cards else 0 # Calculate average.

     # Applies the rules to the player and robot's cards, storing results in dictionaries.mw
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
        player_meets = player_rules[rule]  # Whether the player meets the current rule.
        robot_meets = robot_rules[rule]  # Whether the robot meets the current rule.
        if rule == 3 or rule == 4:   # For rules based on comparisons (3 and 4), reassess meeting criteria.
            player_meets = player_rules[rule] > robot_rules[rule]
            robot_meets = robot_rules[rule] > player_rules[rule]

        # Determine the winner based on who meets the rule criteria.
        if player_meets and not robot_meets:
            return True, f"Player wins by Rule {rule}."
        elif robot_meets and not player_meets:
            return False, f"Robot wins by Rule {rule}."
    # If none of the rules are met, the player loses by default.
    return False, "No rules met. Player loses by default."


def explain_rules():
    # list of print functions just explaining the winning rules.
    print("\nHow the game works:")

    print(
        "\nRule 1: The strongest winning hand is collecting cards with the same value across all suits available in the game.")
    print(
        "       - For example, having a card of each suit with the same value of '2' satisfies this rule. The winning cards would be 2♥, 2♦, 2♣ and 2♠.")

    print(
        "\nRule 2: A variation of Rule 1 where the player needs to collect almost a complete set of value-matching cards.")
    print(
        "       - For exxample, missing one card from the complete set of suits satisfies this rule which would look something like: 2♥, 2♦, 2♣ and 9♥.")

    print("\nRule 3: The player holds more cards from the suit in position 2 than the robot.")
    print(
        "       - For example, if the player holds cards A♥', K♦, J♣, 7♦ and the robot has cards 6♥, 3♦, 4♣, 5♠, the player will win as they have two ♦ cards and the robot has one")

    print(
        "\nRule 4: This rule evaluates the average numerical value of the cards in a player's hand. The higher the average, the better the hand")
    print(
        "       - For example, if the player has cards 5♦, 9♦, 2♥, 7♣ and the robot has cards 2♣, 3♦, 6♦, 4♠, then the player would win as they have a higher average of 23/4 = 5.75 and the robot has 15/4 = 3.75")

    print("\nThese rules are evaluated in order, with Rule 1 being the highest priority, and rule 4 being the lowest.")
    print(
        "For example, if the player satisfies rule 3, but not 1 and 2, but the robots' cards satisfy rule 2; then the robot will win as the 2nd rule is a stronger winning hand.")


## Play Game Function
def play_game():
    global deck, player_cards, robot_cards, suits, values, current_suit_type
    player_cards, robot_cards = [], []  # Initialise the player and robot hands as empty lists.
    game_started = False  # Flag to track if the game has been started.

    while True:  # Main game loop to continuously prompt for user input.
        if not game_started:
            game_menu()
        else:
            print("\nMenu Options:")
            print("1. Start Game")
            print("2. Pick a Card")
            print("3. Shuffle Deck")
            print("4. Show My Cards")
            print("5. Check Win/Lose")
            print("6. Show Winning Combinations")
            print("7. Exit")

        # Capturing user input and cleaning it up.
        user_input = input("\nEnter your choice (e.g., '1' or '1 2'): ").strip()
        # Visual separator for readability.
        print("*" * 80)
        print("\n\n")
        # Splitting the input for multi-part commands (e.g., '1 2').
        inputs = user_input.split()

        if inputs[0] == "1":
            suit_type_key = int(inputs[1]) if len(inputs) > 1 and inputs[1].isdigit() else 1
            current_suit_type = suit_type_key  # Update the current suit type based on player's choice
            create_deck(suits[suit_type_key], values)
            drawn_cards.clear()  # Reset drawn cards tracking
            player_cards.clear()  # Reset player's hand
            robot_cards.clear()  # Reset robot's hand
            shuffle_deck()
            print(f"Game started with deck type {suit_type_key}:")
            print(deck)
            print("\n\n")
            game_started = True

        elif inputs[0] == "2":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                print("\n\n")
                continue
            card = pick_card()  # Attempt to draw a card for the player.
            if card:  # If a card was drawn, add it to the player's hand.
                player_cards.append(card)
                print(f"You picked: {card}")
                print("\n\n")
                pick_card(for_robot=True)  # Robot also attempts to draw a card.
                if len(player_cards) == 6:  # Check if the game end condition is met.
                    player_win, reason = check_result(player_cards, robot_cards, suits[suit_type_key])
                    print("\nFinal Results:")
                    print(f"Your cards: {' '.join(player_cards)}")
                    print(f"Robot's cards: {' '.join(robot_cards)}")
                    print("\n\n")
                    if player_win:
                        print(f"Congratulations, you win! {reason}")
                        print("\n\n")
                    else:
                        print(f"You lose. {reason}")
                        print("\n\n")
                    # Resetting for a new game
                    player_cards, robot_cards = [], []
                    game_started = False
            else:
                print("No more cards left to pick.")
                print("\n\n")

        elif inputs[0] == "3":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                print("\n\n")
                continue
            shuffle_deck()
            print("The deck has been shuffled.")
            print(deck)
            print("\n\n")

        elif inputs[0] == "4":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                print("\n\n")
                continue
            show_cards(player_cards)

        elif inputs[0] == "5":
            if not game_started:
                print("Please start a game first by selecting option 1.")
                print("\n\n")
                continue
            if player_cards and robot_cards:
                player_win, reason = check_result(player_cards, robot_cards, suits[suit_type_key])
                print("\nCurrent Game Status:")
                print(f"Your cards: {' '.join(player_cards)}")
                print(f"Robot's cards: {' '.join(robot_cards)}")
                print("\n\n")
                if player_win:
                    print(f"Current status: You're winning! {reason}")
                    print("\n\n")
                else:
                    print(f"Current status: You're losing. {reason}")
                    print("\n\n")
            else:
                print("You or the robot have no cards to check. Please pick a card first.")
                print("\n\n")

        elif inputs[0] == "6":
            explain_rules()

        elif inputs[0] == "7":
            print("Exiting the game. Thank you for playing!")
            print("\n\n")
            break

        else:
            print("Invalid option. Please try again.")
            print("\n\n")

        # For visual purposes to separate text between each input
        print("*" * 80)

play_game()