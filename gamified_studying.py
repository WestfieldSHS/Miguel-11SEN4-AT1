import os

def main():
    new_player = character_customisation()
    main_menu(new_player)

def character_customisation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "player_stats.txt")
    try:
        with open(filepath, "x"):
            print("No save file found. Creating one now...")
    except FileExistsError:
        with open(filepath, "r") as file:
            print(file.read())
            new_player = False
    else:
        with open(filepath, "w") as file:
            while True:
                name = input("Please input your name. It must be between 2 and 16 characters: ")
                if 2 <= len(name) <= 16:
                    file.write(f"Name: {name}\n")
                    print("Artificer: Better at STEM.")
                    print("Bard: Better at the Humanities")
                    char_class = input("What type of student are you? ").capitalize()
                    if char_class == "Artificer" or "Bard":
                        file.write(f"Class: {char_class}\n")
                        file.write(f"")
                        file.write(f"Gold: 0")
                        new_player = True
    return new_player

def main_menu(new_player):
    while True:
        print()
        print("[A] Training Grounds\n[B] Dungeons\n[C] Marketplace\n[D] Well of Reflection\n[Q] Rest")
        function = input("Where would you like to go? ").upper()
        if function == "A":
            notes(new_player)
        elif function == "B":
            quiz(new_player)
        elif function == "C":
            shop(new_player)
        elif function == "D":
            character_customisation(new_player)
        elif function == "Q":
            quit_program()

def notes(new_player):
    if new_player:
        print("This is the Training Grounds,\nHere you can make notes on various subjects and recall them.\nTry it.")

def quiz(new_player):
    if new_player:
        print("This is the Dungeons.\n Here you can take quizzes on certain subjects and level up.\nTry it.")

def shop(new_player):
    if new_player:
        print("This is the Marketplace.\nHere you can purchase items with the gold you get from the Dungeons.\nTry it.")

def quit_program():
    confirmation = input("[Y/N] Are you sure you want to quit? ").upper
    if confirmation == "Y":
        quit()

main()
