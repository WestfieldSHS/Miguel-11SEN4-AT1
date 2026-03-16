# use debugging tools
# record all errors

import os, json, sys, random

# global variables
level = 1
exp = 0
health = 5
gold = 0
courses = []
humanity_dmg_mod = 0
stem_dmg_mod = 0
monster_slain = True
quiz_over = False

def clear():
    os.system("cls")

def main():
    name, char_class, new_player = character_customisation()
    main_menu(name, char_class, new_player)

def character_customisation():
    global level, exp, gold, courses, health, humanity_dmg_mod, stem_dmg_mod
    file_name = "player_stats.txt"
    filepath = filepath_finder(file_name)
    try:
        with open(filepath, "x"): # open for exclusive creation, failing if the file already exists
            print("No save file found. Creating one now...")
    except FileExistsError:
        with open(filepath, "r") as file: # open for reading
            read_file = file.read()
            print("=====YOUR CHARACTER=====")
            print(read_file)
            print("========================")
        with open(filepath, "r") as file:
            data = file.readlines()
            name = data[0].split(": ")[1].strip() # splits the first line of the file into 2 parts of a list, seperated by the colon. saves the second part to the variable
            char_class = data[1].split(": ")[1].strip() # same thing but with the second line
            level = int(data[2].split(": ")[1].strip())
            exp = int(data[3].split(": ")[1].strip())
            health = int(data[4].split(": ")[1].strip())
            gold = int(data[5].split(": ")[1].strip())
            humanity_dmg_mod = int(data[6].split(": ")[1].strip())
            stem_dmg_mod = int(data[7].split(": ")[1].strip())
            courses = eval(data[8].split(": ")[1].strip()) # deals with the global courses variable
            new_player = False
    else:
        with open(filepath, "w") as file: # creates a file and writes in it
            while True:
                name = input("Please input your name. It must be between 2 and 16 characters: ").strip()
                if 2 <= len(name) <= 16: # arbitrary name length
                    print("Bard: Better at the Humanities")
                    print("Artificer: Better at STEM.")
                    class_list = ["Artificer", "Bard"]
                    char_class = input("What type of student are you? ").capitalize().strip()
                    if char_class in class_list:
                        if char_class == "Bard":
                            humanity_dmg_mod = 1
                        else:
                            stem_dmg_mod = 1
                        file.write(f"Name: {name}\n") # 0
                        file.write(f"Class: {char_class}\n") # 1
                        file.write(f"Level: {level}\n") # 2
                        file.write(f"Experience: {exp}\n") # 3
                        file.write(f"Max HP: {health}\n") # 4
                        file.write(f"Gold: {gold}\n") # 5
                        file.write(f"Humanitarian Expertise: {humanity_dmg_mod}\n") # 6
                        file.write(f"STEM Expertise: {stem_dmg_mod}\n") # 7
                        file.write(f"Courses: {courses}") # 8
                        new_player = True
                        break
    return name, char_class, new_player

# use of os.path in these instances was taken from various forums
def filepath_finder(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__)) # returns the directory name of a normalized absolutized version of THIS file
    filepath = os.path.join(script_dir, file_name) # concantates the file_name to the end of the pathway to this file.
    return filepath

def main_menu(name, char_class, new_player):
    while True:
        print()
        save_game(name, char_class)
        print("[A] Training Grounds\n[B] Dungeons\n[C] Marketplace\n[D] Well of Reflection\n[Q] Rest")
        option = input("Where would you like to go? ").upper().strip()
        # standard method of choosing options across my program
        match option:
            case "A":
                notes(new_player, name, char_class)
            case "B":
                quiz(new_player)
            case "C":
                shop(new_player)
            case "D":
                print()
                character_customisation()
            case "Q":
                quit_program()

def notes(new_player, name, char_class):
    global courses
    print()
    if new_player: # only prints this tutorial message if the player is on their first playthrough
        print("This is the Training Grounds,\nHere you can make notes on various subjects and recall them.\nTry it.")
    while True:
        print("[A] Edit Courses\n[B] Go Back")
        if len(courses) == 0:
            print("You have no subjects. Add some!")
        else:
            print("Here are your subjects:")
        for unit in courses:
            print(f"- {unit}")
        subject = input("What subject would you like to study? Alternatively, you can Edit Courses or Go Back: ").capitalize().strip()
        if subject in courses:
            note_revision(subject)
        match subject:
            case "A":
                course_edit(name, char_class)
            case "B":
                return

def note_revision(subject):
    global exp
    print()
    filename = subject.lower() + ".txt"
    filepath = filepath_finder(filename)
    # loads existing file into the dict, or creates a new one.
    if os.path.exists(filepath): # checks to see if the path exists, returns a boolean statement 
        with open(filepath, "r") as file:
            try:
                note_dict = json.load(file) 
            except json.JSONDecodeError: # improper format for json to decode
                note_dict = dict()
    else:
        note_dict = dict() # converts the json file into a dict
    print(f"[A] View {subject} Notes\n[B] Edit {subject} Notes\n[C] Go Back")
    option = input("What would you like to do? ").upper().strip()
    match option:
        case "A":
            print(f"Here are your notes for {subject}:")
            if note_dict:
                for concept, notes in note_dict.items():
                    print(f"- {concept}: {notes}")
            else:
                print("No notes yet.")
        case "B":
            print("CTRL+Z to stop taking notes.\nType 'Remove', followed by the name of the concept, to remove it.")
            while True:
                try:
                    concept = input(f"Key concept for {subject}: ").strip().capitalize()
                except EOFError: # raised when ctrl+z (windows) or ctrl+d (mac) is inputted
                    break
                else:
                    if "Remove " in concept:
                        concept = concept.replace("Remove ", "").capitalize() # deletes the remove keyword
                        if concept in note_dict:
                            del note_dict[concept] # deletes it from the dictionary
                            print(f"{concept} removed from notes.")
                        else:
                            print("This concept is not in your notes.")
                    else:
                        concept_notes = input("Notes for concept: ").strip()
                        note_dict[concept] = concept_notes
                        print(f"{concept} added to your {subject} notes.")
                        exp += 1
                    with open(filepath, "w") as file: # rewrites the entire file to update
                        json.dump(note_dict, file, indent=4) # converts the note_dict object in the location of file, with 4 indents per line
                    print()
        case "C":
            return

def course_edit(name, char_class):
    print()
    print(f"[A] Add Subject\n[B] Remove Subject\n[C] Go Back")
    option = input("What would you like to do? ").upper().strip()
    match option:
        case "A":
            subject = input("What subject would you like to add to your courses? ").capitalize().strip()
            if subject in courses:
                print(f"{subject} is already a part of your courses.")
            else:
                file_name = subject.lower() + ".txt"
                filepath = filepath_finder(file_name)
                with open(filepath, "x"):
                    courses.append(subject) # appends the subject to the user's course list
                    print(f"{subject} has been added to your courses.")
        case "B":
            subject = input("What subject would you like to remove? ").capitalize().strip()
            if subject in courses:
                courses.remove(subject)
                print("The subject has been removed.")
                os.remove(subject.lower() + ".txt") # removes the text file
            else:
                print("This subject is not a part of your courses.")
    save_game(name, char_class)

# start of quiz functions
def quiz(new_player):
    global quiz_over
    print()
    if new_player:
        print("This is the Dungeons.\nHere you can take quizzes on certain subjects and level up.\nTry it.")
    print("[A] Descend into the Malevolent Mines of Mathematics\n[B] Dive into the Legal Lagoon \n[C] Ascend into the Physics Peaks\n[D] Venture into the English Everglades\n[E] Go Back")
    option = input("What dungeon would you like to explore? ").upper().strip()
    match option:
        case "A":
            subject = "maths"
        case  "B":
            subject = "legal_studies"
        case "C":
            subject = "physics"
        case "D":
            subject = "english"
        case "E":
            return
        case _:
            subject = ""
    quiz_main(subject)

def quiz_main(subject):
    global monster_slain, health, quiz_over
    if not subject: # blank variable is False
        return
    print()
    dungeon_lvl = 1
    q_num = 1
    while quiz_over == False:
        if monster_slain == True:
            monster_name, monster_hp = difficulty(dungeon_lvl)
        if dungeon_lvl == 3:
            print(f"The {monster_name} looks at you.")
        else:
            print(f"The {monster_name} readies to attack.")
        correct, q_num = ask_question(subject, q_num)
        quiz_over, monster_hp, monster_slain, dungeon_lvl = battle_calc(monster_name, monster_hp, dungeon_lvl, correct, subject)
        print(f"HP: {health}")
    dungeon_over(dungeon_lvl)

def difficulty(dungeon_lvl):
    print()
    match dungeon_lvl:
        case 1:
            print("You enter the dungeon.")
            monster_list = ["Slime 🧪 ", "Zombie 🧟 ", "Skeleton 🩻 "]
            monster_hp = 3
        case 2:
            print("You delve deeper into the dungeon.")
            monster_list = ["Big Slime 🧪 ", "Big Zombie 🧟 ", "Big Skeleton 🩻 "]
            monster_hp = 5
        case 3:
            print("You open the doors to the final chamber.")
            monster_list = ["Biggest Slime 🧪 ", "Biggest Zombie 🧟 ", "Biggest Skeleton 🩻 "]
            monster_hp = 10
        case 4:
            print("You cleared the Dungeon!")
    monster_name = random.choice(monster_list)
    print(f"A {monster_name} appears before you")
    return monster_name, monster_hp

def ask_question(subject, q_num):
    global exp
    filename = subject+"_questions.txt"
    question, choices, correct_answer = load_questions(filename)
    print()
    choices = choices.replace('"', "").replace("[", "").replace("]", "") # removes the old formatting.
    multiple_choice = choices.split(",") # due to commas being, you know, apart of grammar, this raises a bunch of errors if a comma is present IN the option itself
    shuffled_multiple_choice = multiple_choice[:] # creates a duplicate of the list
    random.shuffle(shuffled_multiple_choice)
    print(f"{q_num}. {question}")
    print(f"[A]{shuffled_multiple_choice[0]}\n[B]{shuffled_multiple_choice[1]}\n[C]{shuffled_multiple_choice[2]}\n[D]{shuffled_multiple_choice[3]}")
    while True:
        answer = input("Answer: ").upper().strip()
        match answer:
            case "A":
                answer = shuffled_multiple_choice[0]
            case "B":
                answer = shuffled_multiple_choice[1]
            case "C":
                answer = shuffled_multiple_choice[2]
            case "D":
                answer = shuffled_multiple_choice[3]
        if answer == multiple_choice[correct_answer]:
            correct = True
        else:
            correct = False
        q_num += 1
        return correct, q_num

def load_questions(filename):
    with open(filename, "r") as file:
        lines = file.read().splitlines() # returns a list of the loaded file's lines
        random_line = random.choice(lines)
        question, rest = random_line.split(":", 1) # splits at the colon, max 1 time, creating 2 items
        choices, correct_answer = rest.split("|") # further splits, creating 3 items in total
        question = question.strip()
        choices = choices.strip()
        correct_answer = int(correct_answer.strip())
    return question, choices, correct_answer

def battle_calc(monster_name, monster_hp, dungeon_lvl, correct, subject):
    global humanity_dmg_mod, stem_dmg_mod, health
    if correct:
        if subject == "legal_studies" or "english":
            dmg = 1 + humanity_dmg_mod
        else:
            dmg = 1 + stem_dmg_mod
        print(f"You damaged {monster_name} by {dmg} points.")
        monster_hp = monster_hp - dmg
        monster_slain = False
        if monster_hp <= 0:
            dungeon_lvl += 1
            monster_slain = True
            if dungeon_lvl == 4:
                quiz_over = True
    else:
        dmg = dungeon_lvl
        health -= dmg
        print(f"The {monster_name} damaged you by {dmg} points.")
        monster_slain = False
        if health <= 0:
            print(f"You were defeated by the {monster_name}")
            quiz_over = True
    return quiz_over, monster_hp, monster_slain, dungeon_lvl

def dungeon_over(dungeon_lvl, quiz_over):
    if dungeon_lvl == 4:
        print("You cleared the dungeon.")
        print("Rewards...")
    else:
        print("The dungeon cleared you...")
        print("Rewards...")
    quiz_over = False
# end of quiz functions

# uncompleted
def shop(new_player):
    print()
    if new_player:
        print("This is the Marketplace.\nHere you can purchase items with the gold you get from the Dungeons.\nTry it.")
    print("blah")

def quit_program():
    print()
    confirmation = input("[Y/N] Are you sure you want to quit? ").upper().strip()
    if confirmation == "Y":
        sys.exit()

# saves the player's stats every time the main menu is accessed
def save_game(name, char_class):
    global exp, level
    file_name = "player_stats.txt"
    filepath = filepath_finder(file_name)
    if exp >= 100:
        exp -= 100
        level += 1
    with open(filepath, "w") as file:
        file.write(f"Name: {name}\n") # 0
        file.write(f"Class: {char_class}\n") # 1
        file.write(f"Level: {level}\n") # 2
        file.write(f"Experience: {exp}\n") # 3
        file.write(f"Max HP: {health}\n") # 4
        file.write(f"Gold: {gold}\n") # 5
        file.write(f"Humanitarian Expertise: {humanity_dmg_mod}\n") # 6
        file.write(f"STEM Expertise: {stem_dmg_mod}\n") # 7
        file.write(f"Courses: {courses}") # 8

main()

# reward system
# ensure the hp doesnt change globally
# give exp
# shop
# modify stats
# rename things
# complete