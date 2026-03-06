import os

level = 1
gold = 0
courses = ["Maths", "English", "Science"]
script_dir = os.path.dirname(os.path.abspath(__file__)) #finds the filepath to this python file.
filepath = os.path.join(script_dir, "player_stats.txt") #uses script_dir to make the files save to same location.

def main():
    name, char_class, new_player = character_customisation()
    main_menu(name, char_class, new_player)

def character_customisation():
    try:
        with open(filepath, "x"):
            print("No save file found. Creating one now...")
    except FileExistsError:
        with open(filepath, "r") as file:
            data = file.readlines()
            print(file.read())
            name = data[0].split(": ")[1].strip()
            char_class = data[1].split(": ")[1].strip()
            level = int(data[2].split(": ")[1].strip())
            gold = int(data[3].split(": ")[1].strip())
            courses = eval(data[4].split(": ")[1].strip())
            new_player = False
            return name, char_class, new_player
    else:
        with open(filepath, "w") as file:
            while True:
                name = input("Please input your name. It must be between 2 and 16 characters: ")
                if 2 <= len(name) <= 16:
                    print("Artificer: Better at STEM.")
                    print("Bard: Better at the Humanities")
                    class_list = ["Artificer", "Bard"]
                    char_class = input("What type of student are you? ").capitalize()
                    if char_class in class_list:
                        file.write(f"Name: {name}\n")
                        file.write(f"Class: {char_class}\n")
                        file.write(f"Level: {level}\n")
                        file.write(f"Gold: {gold}\n")
                        file.write(f"Courses: {courses}")
                        new_player = True
                        return name, char_class, new_player

def main_menu(name, char_class, new_player):
    while True:
        print()
        save_game(name, char_class)
        print("[1] Training Grounds\n[2] Dungeons\n[3] Marketplace\n[4] Well of Reflection\n[0] Rest")
        option = input("Where would you like to go? ").upper()
        if option == "1":
            notes(new_player)
        elif option == "2":
            quiz(new_player)
        elif option == "3":
            shop(new_player)
        elif option == "4":
            character_customisation()
        elif option == "0":
            quit_program()

def notes(new_player):
    global courses
    print()
    if new_player:
        print("This is the Training Grounds,\nHere you can make notes on various subjects and recall them.\nTry it.")
    while True:
        print()
        print("[A] Edit Courses")
        print("[B] Go Back")
        print("Here are your subjects:")
        for unit in courses:
            print(f"{unit}")
        subject = input("What subject would you like to study? Alternatively, you can Edit Courses or Go Back:  ").capitalize()
        if subject in courses:
            note_revision(subject)
        elif subject == "A":
            course_edit()
        elif subject == "B":
            return

def note_revision(subject):
    print()
    print(f"[A] View {subject} Notes\n[B] Edit {subject} Notes")
    option = input("What would you like to do?")

def course_edit():
    print()
    print(f"[A] Add Subject\n[B] Remove Subject\n[C] Go Back")
    option = input("What would you like to do? ").upper()
    if option == "A":
        subject = input("What subject would you like to add to your courses? ").upper().strip()
        if subject in courses:
            print(f"{subject} is already a part of your courses.")
        else:
            courses.append(subject)
            print(f"{subject} has been added to your courses.")
    elif option == "B":
        subject = input("What subject would you like to remove? ")
        if subject in courses:
            courses.remove(subject)
            print("The subject has been removed.")
        else:
            print("This subject is not a part of your courses.")

def quiz(new_player):
    print()
    if new_player:
        print("This is the Dungeons.\n Here you can take quizzes on certain subjects and level up.\nTry it.")

def shop(new_player):
    global level, gold
    print()
    if new_player:
        print("This is the Marketplace.\nHere you can purchase items with the gold you get from the Dungeons.\nTry it.")
    level += 1

def quit_program():
    print()
    confirmation = input("[Y/N] Are you sure you want to quit? ").upper
    if confirmation == "Y":
        quit()

def save_game(name, char_class):
    global script_dir, filepath
    with open(filepath, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Class: {char_class}\n")
        file.write(f"Level: {level}\n")
        file.write(f"Gold: {gold}\n")
        file.write(f"Courses: {courses}")

main()