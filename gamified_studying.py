import os

def main():
    character_customisation()
    main_menu()

def character_customisation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "player_stats.txt")
    try:
        with open(filepath, "x"):
            print("No save file found. Creating one now...")
    except FileExistsError:
        with open(filepath, "r") as file:
            print(file.read())
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
                        break

main()
