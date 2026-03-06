import os

def main():
    character_customisation()

def character_customisation():
    filepath = "player_stat"
    try:
        with open(filepath, "x") as file:
            file.write("It exists.")
    except FileExistsError:
        print("The file 'player_stats' already exists.")
        print("Saved file to:", os.getcwd())

main()