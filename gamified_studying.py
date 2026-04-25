import os, json, sys, random
from prettytable import from_csv
from rich.console import Console
from rich.theme import Theme
custom_theme = Theme({ # keys are the names i assign to the values which are interpreted as different colours to print
    "incorrect": "bold red",
    "correct": "bold green",
    "important": "bold blue",
})
console = Console(theme=custom_theme)

# global variables and their standard values
level = 1
exp = 0
max_health = 5
gold = 0
courses = []
inventory = []
humanity_mod = 0
stem_mod = 0
monster_slain = True
quiz_over = False

# universal functions
def clear():
    # patchwork method of checking if the program is being run on windows or mac
    # bcuz of this, mac users for a fraction of a second may see "'cls' is not a supported class..." or something, however it does not raise an error
    if os.system("cls") == 0: # if os.system("cls") works, which it does on windows, it returns a value of 0
        os.system("cls") # in which case it runs os.system("cls")
    elif os.system("cls") == 1: # if it fails, which it would on windows, it returns a value of 1
        os.system("clear") # in which case it would run os.system("clear") instead, which works on mac and in codespaces

def main():
    # in my tests the special characters do not get confused for ASCII characters
    # however, some characters meld together if there isn't a space between them. 
    # I opted to use a smaller, invisible character over the standard " "
    print("𝔚 𝔢𝔩𝔠𝔬𝔪𝔢 𝔱𝔬 𝔱𝔥𝔢 𝕬 𝖈𝖆𝖉𝖊𝖒𝖎𝖈𝖔𝖓, 𝔞 𝔤𝔞𝔪𝔦𝔣𝔦𝔢𝔡-𝔰𝔱𝔲𝔡𝔶𝔦𝔫𝔤 𝔢𝔵𝔭𝔢𝔯𝔦𝔢𝔫𝔠𝔢.")
    while True:
        # console.print allows for the use of styles
        console.print("[A] Create Save File\n[B] Load Existing File\n[C] Delete Save File\n[D] Teacher Mode\n[Q] Exit", style="important")
        option = input("What would you like to do? ").upper().strip()
        clear()
        match option:
        # should the below code be modularised inside functions?
            case "A":
                save_name = input("Name your save file: ").lower().strip()
                save_name = save_name.replace(" ", "_") # adheres to the formatting of files
                print()
                name, char_class, new_player = character_customisation(save_name)
                main_menu(name, char_class, new_player, save_name)
            case "B":
                saves = list_save_files(True, "_stats.txt")
                if not saves: # if list is empty it returns a boolean statement ("false") that can be detected
                    print("No save files found.")
                else:
                    print("Available save files:")
                    for save in saves:
                        print(f"- {save}")
                    save_name = input("Which save file do you want to load? ").lower().strip()
                    save_name = save_name.replace(" ", "_") # ensures user adds the underscores
                    print()
                    if save_name in saves: # w/o this check, you could accidentally create save files
                        name, char_class, new_player = character_customisation(save_name)
                        main_menu(name, char_class, new_player, save_name)
            case "C":
                saves = list_save_files(True, "_stats.txt")
                # following lines of code would have been apart of the function, however the function was used in other places with minor changes.
                # e.g different words, different format, etc.
                if not saves: # if list is empty
                    print("No save files found.")
                else:
                    print("Available save files:")
                    for save in saves:
                        print(f"- {save}")
                save_name = input("Which save file do you want to delete? ").strip().lower()
                save_name = save_name.replace(" ", "_")
                try:
                    os.remove(save_name + "_stats.txt") # removes the selected file without needing the user to type all of it
                except OSError: # basic error that deals with i/o of the OS variety
                    print("Save file not found.")
                else:
                    # taken from list_save_files function, however condensed and varied slightly
                    print(f"{save_name} has been successfully deleted.")
                    for file in os.listdir():
                        if file.startswith(save_name):
                            os.remove(file) # removal of files such as "player_maths_notes.txt"
            case "D":
                print("Authentication required.")
                password = input("Password: ")
                if password == "1234":
                    teacher_menu()
            case "Q":
                print("Exiting Academicon...")
                sys.exit()

def list_save_files(remove_suffix, suffix): # does smth need to be removed, what needs to be detected and/or removed
    saves = []
    for file in os.listdir(): # returns a list of all files and folders inside a directory
        if file.endswith(suffix):
            if remove_suffix: # checks to see if the program wants to remove the suffix - boolean
                saves.append(file.replace(suffix, ""))  # remove _stats.txt part
            else:
                saves.append(file) # used in the teacher mode to properly open the saves  in read mode
    return saves

# start of teacher specific functions
def teacher_menu():
    while True:
        print()
        console.print("[A] View Student Stats\n[B] Create Quizzes\n[C] Remove Quizzes\n[Q] Exit", style="important")
        option = input("What would you like to do? ").upper().strip()
        clear()
        match option:
            # could be modularised as well
            case "A":
                saves = list_save_files(False, "_stats.txt")
                if not saves:
                    console.print("=====================", style="important")
                    print("No students registered.")
                for save in saves: # for every student, prints out their entire stats
                    console.print("=======STUDENT=======", style="important") 
                    with open(save, "r") as file:
                        read_file = file.read()
                        print(read_file)
                console.print("=====================", style="important")
            case "B":
                create_quiz()
            case "C":
                quizzes = list_save_files(True, "_questions.txt")
                if not quizzes: # if list is empty
                    print("No quizzes made.")
                else:
                    print("Quizzes:")
                    for quiz in quizzes:
                        quiz = quiz.replace("_", " ") # can be removed. just looks nicer for this in my opinion
                        print(f"- {quiz}")
                print("[Q] Return")
                subject = input("Which quiz do you want to remove? ").lower().strip()
                if subject == "q":
                    teacher_menu() # return would return the user to the user_menu
                subject = subject.replace(" ", "_")
                try:
                    os.remove(subject + "_questions.txt")
                except OSError:
                    print("Quiz not found.")
            case "Q":
                main()

def create_quiz():
    print("[Q] Return")
    subject = input("What subject is this? ").lower().strip()
    if subject == "q":
        return # not in a while true statemeent, so break cannot be used
    subject = subject.replace(" ", "_") # formatting
    console.print("[A] STEM\n[B] Humanities", style="important")
    while True:
        subject_type = input("What type of subject is this? ").upper().strip()
        if subject_type == "A":
            subject_type = "STEM"
            break
        elif subject_type == "B":
            subject_type = "humanity"
            break
    count = 0
    if subject in ["legal_studies", "physics", "maths", "english"]: # could be removed
        print("Quizzes already made for these subjects.")
        return
    print("CTRL+Z/D to stop making the quiz.") # ctrl+z/d raises an EOFError when inputted. depends on mac/windows
    try:
        open(f"{subject}_questions.txt", "x") # exclusive creation, fails if file exists
    except FileExistsError:
        with open(f"{subject}_questions.txt", "a") as file: # appends to the file that already exists
            file.write("\n") # does this to start on a fresh line in the already-made file
            quiz_question = create_questions()
            for line in quiz_question: # for each value in the quiz question aka the question, the list of multiple choice, and then the index
                    if count < 2: # 0 Yes so Write, 1 Yes so Write, 2 No so New line, repeat
                        file.write(f"{line}")
                        count += 1
                    else:
                        file.write(f"\n{line}") # new question, so creates a new line before writing
                        count = 0
    else:
        with open(f"{subject}_questions.txt", "w") as file: # new file, so opens in write mode to create and write in it
            file.write(f"{subject_type}\n") # doesn't create a new line, instead assigns the subject type
            quiz_question = create_questions()
            for line in quiz_question: # for each value in the quiz question aka the question, the list of multiple choice, and then the index
                if count < 2: # 0, 1, 2, new line, repeat
                    file.write(f"{line}")
                    count += 1
                else:
                    file.write(f"\n{line}") # new question, so creates a new line before writing
                    count = 0
        
def create_questions():
    quiz_question = [] # list so that all 3 parts of the quiz question are written to the file together
    multiple_choice_questions = [] # seperate list for multiple choice questions since they are stored in a separate list in the questions txt file
    while True:
        print()
        try:
            question = input("Input Question: ").replace(",", "-").replace("'", "`").replace(":", "?") # adheres to _questions.txt formatting
        except EOFError: # raised when user inputs ctrl+z or ctrl+d, depending on their os
            break # terminates the while True loop
        else:
            question = question + ":" # more formatting
            quiz_question.append(question)
            correct_answer_index = input("Correct answer: ").replace(",", "-").replace("'", "`")
            correct_answer_index = " " + correct_answer_index
            multiple_choice_questions.append(correct_answer_index)
            for _ in range(3): # underscore is a placeholder variable with no real meaning
                other_answer = input("Other answer: ").replace(",", "-").replace("'", "`")
                multiple_choice_questions.append(other_answer)
            quiz_question.append(f" {multiple_choice_questions} | 0") # adheres to formatting for indexing
            multiple_choice_questions.clear()
            print(quiz_question)
    return quiz_question

# start of player/student specific functions
def character_customisation(save_name):
    global level, exp, gold, courses, max_health, humanity_mod, stem_mod, inventory
    file_name = f"{save_name}_stats.txt" # this is where the program decides whether or not to create a new save file
    filepath = filepath_finder(file_name)
    try:
        with open(filepath, "x"): # opens file for exclusive creation, failing if the file already exists
            print("Creating new save file now...")
    except FileExistsError:
        with open(filepath, "r") as file: # if the file exists, opens for reading
            # this is what the user sees when they input [D] in the main
            read_file = file.read()
            print("=====YOUR CHARACTER=====")
            print(read_file) # attempting to print(file.read()) actually prints nothing, interestingly enough
            print("========================")
        # attempting to execute file.read() and file.readlines() under the same open... failed
        with open(filepath, "r") as file:
            # reads the file as a list, and uses indexing to assign variables
            data = file.readlines() # turns the file to a list, where each line is a value
            name = data[0].split(": ")[1].strip() # splits the first line of the file into 2 parts of another list, separated by the colon. the second part of this list is then stripped and saved to the variable
            char_class = data[1].split(": ")[1].strip() # same thing but with the second line
            level = int(data[2].split(": ")[1].strip()) # same thing but converts to an integer
            exp = int(data[3].split(": ")[1].strip())
            max_health = int(data[4].split(": ")[1].strip())
            gold = int(data[5].split(": ")[1].strip())
            humanity_mod = int(data[6].split(": ")[1].strip())
            stem_mod = int(data[7].split(": ")[1].strip())
            courses = eval(data[8].split(": ")[1].strip()) # deals with the global courses variable
            inventory = eval(data[9].split(": ")[1].strip())
            new_player = False
    else:
        # if the save_name... file doesn't exist (user wants to make a new file), program executes the following
        # re/sets all the global variables. if this wasnt here, then when u make a new save file, it will automatically have the previous ones' values
        level = 1
        exp = 0
        max_health = 5
        gold = 0
        courses = []
        inventory = []
        with open(filepath, "w") as file: # the file doesn't exist, opens the file in write mode which creates it
            while True:
                name = input("Please input your name. It must be between 2 and 16 characters: ").strip()
                if 2 <= len(name) <= 16: # arbitrary name length
                    console.print("[important][A] Artificer[/important]: Better at STEM (Science, Technology, Engineering, Maths).") # if only a certain part of a string needs to be highlighted, use [placeholder]text[/placeholder] to do so
                    console.print("[important][B] Bard[/important]: Better at the Humanities (English, History, Geography, etc).")
                    option = input("What type of student are you? ").upper().strip()
                    if option == "A" or option == "B":
                        match option:
                            case "A":
                                char_class = "Artificer"
                                stem_mod = 1
                                humanity_mod = 0
                            case "B":
                                char_class = "Bard"
                                humanity_mod = 1
                                stem_mod = 0
                        # writes the standard, global variables into the player stat file
                        file.write(f"Name: {name}\n") # 0
                        file.write(f"Class: {char_class}\n") # 1
                        file.write(f"Level: {level}\n") # 2
                        file.write(f"Experience: {exp}\n") # 3
                        file.write(f"Max HP: {max_health}\n") # 4
                        file.write(f"Gold: {gold}\n") # 5
                        file.write(f"Humanities Expertise: {humanity_mod}\n") # 6
                        file.write(f"STEM Expertise: {stem_mod}\n") # 7
                        file.write(f"Courses: {courses}\n") # 8
                        file.write(f"Inventory: {inventory}") # 9
                        new_player = True
                        break
    return name, char_class, new_player

# use of os.path in these instances was taken from various forums
# using the standard way of opening files did not work. used this function to find the exact location of the file.
# at the start of this project, this was a key function in getting my files, but later in the development stage, i rarely used it. 
# i am unsure why it was so essential at the start, so much so that the program could not run without it.
def filepath_finder(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__)) # returns the directory of a normalized absolutized version of THIS file
    filepath = os.path.join(script_dir, file_name) # concantates the file_name to the end of the pathway to this file.
    return filepath

def main_menu(name, char_class, new_player, save_name):
    global gold
    while True:
        print()
        save_game(name, char_class, save_name)
        console.print("[A] Training Grounds\n[B] Dungeons\n[C] Marketplace\n[D] Well of Reflection\n[E] Rest", style="important")
        option = input("Where would you like to go? ").upper().strip()
        clear()
        # standard method of choosing options across my program
        match option:
            case "A":
                notes(new_player, save_name)
            case "B":
                quiz(new_player)
            case "C":
                shop(new_player)
            case "D":
                character_customisation(save_name)
            case "E":
                quit_game(name)
            case "BOOSTER":
                print("GOLD.")
                gold += 50

def notes(new_player, save_name):
    global gold, courses
    while True:
        print()
        if new_player: # only prints this tutorial message if the player is on their first playthrough
            console.print("This is the [important]Training Grounds[/important],\nHere you can make [important]notes[/important] on various subjects and [important]recall them[/important].\n[important]Try it[/important].")
        console.print("[A] Edit Courses\n[B] Go Back", style="important")
        if not len(courses):
            print("You have no subjects. Add some!")
        else:
            print("Here are your subjects:")
            for unit in courses:
                print(f"- {unit}")
        subject = input("What subject would you like to study? Alternatively, you can Edit Courses or Go Back: ").capitalize().strip()
        clear()
        if subject in courses:
            note_revision(subject, save_name)
        option = subject
        match option:
            case "A":
                course_edit(save_name)
            case "B":
                return

def note_revision(subject, save_name):
    global exp
    print()
    file_name = f"{save_name}_" + subject.lower() + "_notes.txt" # e.g legal_studies_notes.txt
    filepath = filepath_finder(file_name)
    # loads existing file into the dict, or creates a new one.
    if os.path.exists(filepath): # checks to see if the path exists, returns a boolean statement 
        with open(filepath, "r") as file: # if  it does exists, loads the file into a dictionary
            try:
                note_dict = json.load(file) 
            except json.JSONDecodeError: # improper format for json to decode
                note_dict = dict()
    else:
        note_dict = dict() # prepares an empty dictionary for later use
    while True:
        console.print(f"[A] View {subject} Notes\n[B] Edit {subject} Notes\n[C] Go Back", style="important")
        option = input("What would you like to do? ").upper().strip()
        clear()
        match option:
            case "A":
                print(f"Here are your notes for {subject}:")
                if note_dict: # not empty
                    for concept, notes in note_dict.items(): # .items() returns the key and value of a dict as a tuple = (key1, value1), (key2, value2), etc
                        print(f"- {concept}: {notes}")
                else:
                    print("No notes yet.")
            case "B":
                print("CTRL+Z/D to stop taking notes.\nType 'Remove', followed by the name of the concept, to remove it.")
                while True:
                    try:
                        concept = input(f"Key concept for {subject}: ").strip().capitalize()
                    except EOFError: # raised when ctrl+z (windows) or ctrl+d (mac) is inputted
                        clear()
                        break
                    else:
                        if concept[:7] == "Remove ": #checks to see if the first 0-6 characters are equal to the item name since [:x] does not include x
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

def course_edit(save_name):
    print()
    console.print(f"[A] Add Subject\n[B] Remove Subject\n[C] Go Back", style="important")
    option = input("What would you like to do? ").upper().strip()
    clear()
    for unit in courses:
        print(f"- {unit}")
    match option:
        case "A":
            subject = input("What subject would you like to add to your courses? ").capitalize().strip()
            if subject in courses:
                print(f"{subject} is already a part of your courses.")
            else:
                file_name = f"{save_name}_" + subject.lower() + "_notes.txt"
                filepath = filepath_finder(file_name)
                open(filepath, "x")
                courses.append(subject) # appends the subject to the user's course list
                print(f"{subject} has been added to your courses.")
        case "B":
            subject = input("What subject would you like to remove? ").capitalize().strip()
            if subject in courses:
                courses.remove(subject)
                print("The subject has been removed.")
                os.remove(f"{save_name}_" + subject.lower() + "_notes.txt") # removes the text file
            else:
                print("This subject is not a part of your courses.")

# start of quiz functions
def quiz(new_player):
    print()
    if new_player:
        console.print("This is the [important]Dungeons[/important].\nHere you can take [important]quizzes[/important] on certain subjects and [important]level[/important] up.\n[important]Try it[/important].")
    console.print("[A] Descend into the Malevolent Mines of Mathematics\n[B] Dive into the Legal Lagoon \n[C] Ascend into the Physics Peaks\n[D] Venture into the English Everglades\n[E] Teacher-Made Quizzes\n[F] Go Back", style="important")
    option = input("What dungeon would you like to explore? ").upper().strip()
    clear()
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
            quizzes = list_save_files(True, "_questions.txt")
            quizzes.remove("legal_studies") # should i have the program only show teacher made quizzes? and scrap the four pre-made ones?
            for quiz in quizzes:
                quiz = quiz.replace("_", " ")
                print(f"- {quiz}")
            subject = input("Which quiz would you like to do? ").strip().lower()
            subject = subject.replace(" ", "_")
        case "F":
            return
        case _:
            subject = ""
    quiz_main(subject)

def quiz_main(subject):
    global monster_slain, max_health, quiz_over
    if not subject: # blank variable is False
        return
    print()
    # re/sets all the necessary variables:
    dungeon_lvl = 1
    q_num = 1
    quiz_over = False
    monster_slain = True
    correct_count = 0
    temp_health = max_health # creates a temporary, modifiable variable for use in the dungeons
    while quiz_over == False:
        if monster_slain == True:
            monster_name, monster_hp = monster_loader(dungeon_lvl)
        if dungeon_lvl == 3:
            print(f"The {monster_name} looks at you.")
        else:
            print(f"The {monster_name} readies to attack.")
        correct, q_num, subject_type = ask_question(subject, q_num)
        quiz_over, monster_hp, monster_slain, dungeon_lvl, temp_health, correct_count = battle_calc(monster_name, monster_hp, dungeon_lvl, correct, temp_health, correct_count)
        print_hp = "❤️ "*temp_health
        print(f"HP: {print_hp}")
    reward_calc(dungeon_lvl, q_num, subject_type, correct_count)

def monster_loader(dungeon_lvl):
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
            monster_list = ["Dunston 🧪 ", "Biggest Zombie 🧟 ", "Biggest Skeleton 🩻 "]
            monster_hp = 10
    monster_name = random.choice(monster_list)
    print(f"A {monster_name} appears before you")
    return monster_name, monster_hp

def ask_question(subject, q_num):
    global exp
    file_name = f"{subject}_questions.txt"
    question, choices, correct_answer_index, subject_type = question_loader(file_name)
    print()
    choices = choices.replace('"', "").replace("[", "").replace("]", "").replace("'", "") # removes the formatting used in the actual text file.
    multiple_choice_answers = choices.split(",") # due to commas being used to split the 3 variables, this raises a bunch of errors if a comma is present IN the option itself
    shuffled_multiple_choice_answers = multiple_choice_answers[:] # [:] creates a duplicate of the entire list.
    random.shuffle(shuffled_multiple_choice_answers) # if a duplicate was not made, then the correct answer to all questions will be A, regardless of if thats true or not
    print(f"{q_num}. {question}")
    console.print(f"[A]{shuffled_multiple_choice_answers[0]}\n[B]{shuffled_multiple_choice_answers[1]}\n[C]{shuffled_multiple_choice_answers[2]}\n[D]{shuffled_multiple_choice_answers[3]}", style="important")
    option = input("Answer: ").upper().strip()
    clear()
    match option:
        case "A":
            option = shuffled_multiple_choice_answers[0]
        case "B":
            option = shuffled_multiple_choice_answers[1]
        case "C":
            option = shuffled_multiple_choice_answers[2]
        case "D":
            option = shuffled_multiple_choice_answers[3]
    if option == multiple_choice_answers[correct_answer_index]: # matches the answers. possibly unnecessary to include [correct_answer_index]. could have just had [0]
        correct = True
    else:
        correct = False
    q_num += 1
    return correct, q_num, subject_type

def question_loader(file_name):
    with open(file_name, "r") as file:
        lines = file.read().splitlines() # returns a list that contains all loaded file's lines as seperate values
        if lines[0] == "STEM": # checks to see if the first line is either stem or Humanities
            subject_type = "STEM"
            lines.remove("STEM")
        elif lines[0] == "humanities":
            subject_type = "Humanities"
            lines.remove("humanities")
        else:
            print("Quiz Error.")
            quiz(False)
        random_line = random.choice(lines) # randomly chooses one of these lines and saves it to a variable
        question, rest = random_line.split(":", 1) # splits this random variable into 2 variables, dividing it at the colon
        choices, correct_answer_index = rest.split("|") # further splits, creating 3 items in total: the qurestion, choices, and correct answer
        question = question.strip() # removes unnecessary spaces
        choices = choices.strip()
        correct_answer_index = int(correct_answer_index.strip()) # is an integer that always equals zero, so that it can be used for indexing
    return question, choices, correct_answer_index, subject_type

def battle_calc(monster_name, monster_hp, dungeon_lvl, correct, temp_health, correct_count):
    global quiz_over
    if correct:
        console.print(f"You damaged {monster_name}", style="correct")
        monster_hp -= 1
        monster_slain = False
        correct_count += 1
        if monster_hp <= 0: # less than or equal too
            dungeon_lvl += 1
            monster_slain = True
            if dungeon_lvl == 4:
                quiz_over = True
    else:
        temp_health -= dungeon_lvl
        console.print(f"The {monster_name} damaged you by {dungeon_lvl} points.", style="incorrect")
        monster_slain = False
        correct_count += 0
        if temp_health <= 0: # less than or equal too
            console.print(f"You were defeated by the {monster_name}.", style="incorrect")
            quiz_over = True
    print_monster_hp = "🖤 "*monster_hp
    print(f"{monster_name} HP: {print_monster_hp}")
    return quiz_over, monster_hp, monster_slain, dungeon_lvl, temp_health, correct_count

def reward_calc(dungeon_lvl, q_num, subject_type, correct_count):
    global gold, exp, quiz_over, humanity_mod, stem_mod
    if dungeon_lvl == 4: # multiple ways to check if user beat the dungeons. i chose this one since it seems easiest
        console.print("You cleared the dungeon.", style="correct")
        if subject_type == "Humanities":
            exp_modifier = q_num + dungeon_lvl*5 + humanity_mod
            gold_modifier = round((q_num + dungeon_lvl*2 + humanity_mod)/2)
        elif subject_type == "STEM":
            exp_modifier = q_num + dungeon_lvl*5 + stem_mod
            gold_modifier = round((q_num + dungeon_lvl*2 + stem_mod)/2)
        else:
            exp_modifier = 0
            gold_modifier = 0
    else:
        console.print("The dungeon cleared you...", style="incorrect")
        # could possibly add the humanity/stem exp mods
        exp_modifier = round((q_num + dungeon_lvl*5)/2)
        gold_modifier = 0 # must be set for use in next few lines
    print(f"Number of Questions Answered Correctly: {correct_count}")
    print(f"You earned {exp_modifier} EXP\nYou earned {gold_modifier} gold.")
    exp += exp_modifier
    gold += gold_modifier
# end of quiz functions

def shop(new_player):
    global gold, inventory
    while True:
        if new_player:
            console.print("This is the [important]Marketplace[/important].\nHere you can [important]purchase[/important] items with the [important]gold you get from the Dungeons[/important].")
            console.print("The Humanities stat [important]modifies[/important] how much how much [important]EXP[/important] and [important]Gold[/important] in Humanities dungeons\n(For Example, English or Legal Studies)")
            console.print("The STEM stat modifies how much EXP and Gold you earn in STEM dungeons.\n(For example, Maths and Physics)")
        # deals with csv files, or comma seperated value files.
        with open('11SEN_AT1_CSV.csv', encoding="UTF-8-sig") as csvfile: # encodes in UTF-8-sig which removes strange letters from the first cell
            print_shop_menu = from_csv(csvfile) # prints the csv file in a table
        print(print_shop_menu)
        console.print("[A] Purchase\n[B] Sell\n[C] Leave", style = "important")
        with open('11SEN_AT1_CSV.csv','r') as csvfile:
            data = csvfile.readlines() # list of lines
            option = input("What would you like to do? ").upper().strip()
            match option:
                case "C":
                    break
                case "B":
                    item = input("What do you want to sell? ")
                    if item == "":
                        console.print("Please input an item.", style="incorrect")
                    if item in inventory:
                        inventory.remove(item)
                        console.print(f"{item} sold.\n10 Gold acquired.", style="correct")
                        gold += 10
                case "A":
                    item = input("What would you like to purchase? ").title().strip()
                    item_length = len(item) # doesn't start at 0. starts at 1
                    for line in data:
                        if item_length+8 == len(line) or item_length+9 == len(line): # item_length is "item name" while line is: "item name,xx,x,x ", but it must also account for if the item price is 3 digits
                            if item == line[:item_length]: # though [:x] indexes from 0-(x-1), item_length is derived from len() which doesn't start counting from zero, so the full length can be indexed    
                                item_info = list() # empty list
                                word = "" # empty variable
                                for character in line:
                                    if character != "," and character != line[-1]: # if the character isn't a comma or the last letter. this only works since the last char is  technically" "
                                        word = word+character # add onto the word
                                    else: # if it is, that indicates the end of the word or table row
                                        item_info.append(word)
                                        word = "" # resets
                                console.print(f"Name: {item_info[0]}", style="important") # since item_info is a list, its values, or the items values, can be indexed
                                console.print(f"Humanities Modifier: {item_info[2]}", style="important")
                                console.print(f"STEM Modifier: {item_info[3]}", style="important")
                                console.print(f"Current Gold: {gold} gold.", style="important")
                                confirmation = input(f"This costs {item_info[1]} Gold. Are you sure you want to purchase this? (Y/N) ").strip().upper()
                                if confirmation == "Y":
                                    if gold < int(item_info[1]): # less than
                                        console.print("You're too broke.", style="incorrect")
                                    elif item_info[0] in inventory:
                                        console.print("You have already purchased this item!", style="incorrect")
                                    else: # structured like this to avoid too nested if statements
                                        purchasing(item_info)
                                    break # send back to top of shop if user wishes to buy something else, cld be replaced with return to send them back to main
                                else:
                                    break # send back to top of shop if user wishes to buy something else
     
def purchasing(item_info):
    global gold, humanity_mod, stem_mod
    inventory.append(item_info[0])
    gold -= int(item_info[1])
    humanity_mod += int(item_info[2])
    stem_mod += int(item_info[3])
    print("Purchased!")

def quit_game(name):
    print()
    confirmation = input("[Y/N] Are you sure you want to quit? ").upper().strip()
    if confirmation == "Y": # else no, user sent back to main menu
        console.print(f"See you later, {name}!", style="important")
        print()
        main()

# saves the player's stats every time the main menu is accessed
def save_game(name, char_class, save_name):
    global exp, level, max_health
    file_name = f"{save_name}_stats.txt"
    filepath = filepath_finder(file_name)
    if exp >= 100: # level up w/ stat changes
        exp -= 100
        level += 1
        max_health += 1
        print(f"You leveled up!\nYou are now level {level}.\nYour HP is now {max_health}.")
    with open(filepath, "w") as file: # rewrites the file with the new stat values
        file.write(f"Name: {name}\n") # 0
        file.write(f"Class: {char_class}\n") # 1
        file.write(f"Level: {level}\n") # 2
        file.write(f"Experience: {exp}\n") # 3
        file.write(f"Max HP: {max_health}\n") # 4
        file.write(f"Gold: {gold}\n") # 5
        file.write(f"Humanities Expertise: {humanity_mod}\n") # 6
        file.write(f"STEM Expertise: {stem_mod}\n") # 7
        file.write(f"Courses: {courses}\n") # 8
        file.write(f"Inventory: {inventory}")

main()