import os

level = 1
gold = 0
courses = []

def main():
    name, char_class, new_player = character_customisation()
    main_menu(name, char_class, new_player)

def character_customisation():
    global level, gold, courses
    file_name = "player_stats.txt"
    filepath = file_creator(file_name)
    try:
        with open(filepath, "x"):
            print("No save file found. Creating one now...")
    except FileExistsError:
        with open(filepath, "r") as file:
            read_file = file.read()
            print("=====YOUR CHARACTER=====")
            print(read_file)
            print("========================")
        with open(filepath, "r") as file:
            data = file.readlines()
        name = data[0].split(": ")[1].strip() # only reads the part after the colon on the first line
        char_class = data[1].split(": ")[1].strip()
        level = int(data[2].split(": ")[1].strip()) # only reads the part after the colon on the first line. converts to an int
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

def file_creator(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__)) #finds the filepath to this python file by finding the directory of the asbolute path.
    filepath = os.path.join(script_dir, file_name) #uses script_dir to make the files save to same location.
    return filepath

def main_menu(name, char_class, new_player):
    while True:
        print()
        save_game(name, char_class)
        print("[A] Training Grounds\n[B] Dungeons\n[C] Marketplace\n[D] Well of Reflection\n[Q] Rest")
        option = input("Where would you like to go? ").upper()
        if option == "A":
            notes(new_player)
        elif option == "B":
            quiz(new_player)
        elif option == "C":
            shop(new_player)
        elif option == "D":
            print()
            character_customisation()
        elif option == "Q":
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
        if len(courses) == 0:
            print("You have no subjects. Add some!")
        else:
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
    print(f"[A] View {subject} Notes\n[B] Edit {subject} Notes\n[C] Go Back")
    option = input("What would you like to do?")
    if option == "A":
        print("")
    elif option == "B":
        print("")
    elif option == "C":
        return

def course_edit():
    print()
    print(f"[A] Add Subject\n[B] Remove Subject\n[C] Go Back")
    option = input("What would you like to do? ").upper()
    if option == "A":
        subject = input("What subject would you like to add to your courses? ").capitalize().strip()
        if subject in courses:
            print(f"{subject} is already a part of your courses.")
        else:
            courses.append(subject)
            print(f"{subject} has been added to your courses.")
            file_name = subject.lower() + ".txt"
            file_creator(file_name)
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
    print("blah")

def shop(new_player):
    print()
    if new_player:
        print("This is the Marketplace.\nHere you can purchase items with the gold you get from the Dungeons.\nTry it.")
    print("blah")
    
def quit_program():
    print()
    confirmation = input("[Y/N] Are you sure you want to quit? ").upper
    if confirmation == "Y":
        quit()

def save_game(name, char_class):
    file_name = "player_stats.txt"
    filepath = file_creator(file_name)
    with open(filepath, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Class: {char_class}\n")
        file.write(f"Level: {level}\n")
        file.write(f"Gold: {gold}\n")
        file.write(f"Courses: {courses}")

main()