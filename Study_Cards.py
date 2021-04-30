from guizero import *
import csv
import random
import time

#empty arrays
words = []
words_used = []
right_answer = []
possibilities = []
the_word = []
right = []
wrong = []

#basic variables
height = 400
width = 800
half_width = width / 2
half_height = height / 2
game_live = False
score = 0

#default conditions
o1 = "option 1"
o2 = "option 2"
o3 = "option 3"
o4 = "option 4"

#create word list
# read file containing list of words and definitions

with open('GRE_Vocab.csv', 'r') as GREread:
    lines = csv.reader(GREread)
    for line in lines:
        words.append(line)
        
GREread.close()

# drop list headers
words.pop(0)

length_of_list = len(words) - 1
print(len(words))

#make word lists
def wordselection():
    question.visible = True
    correct_meaning.value = ''
    correct = len(right)
    incorrect = len(wrong)
    total_attempts = int(correct) + int(incorrect)
    random_word = random.randint(0, length_of_list)
    word = words[random_word][0]
    the_word.append(word)
    answer = words[random_word][1].split('.').pop(1)

    definitions = [answer]
    for i in range(3):
        false_definition = random.randint(0, length_of_list)
        entry = words[false_definition][1].split('.').pop(1)
        definitions.append(entry)
    
    for i in definitions:
        possibilities.append(i)
    
    choice_1 = random.choice(definitions)
    definitions.remove(choice_1)
    choice_2 = random.choice(definitions)
    definitions.remove(choice_2)
    choice_3 = random.choice(definitions)
    definitions.remove(choice_3)
    choice_4 = definitions[0]
    
    question.value = ("What is the correct definition of {}?".format(word))
    choices.insert(0, choice_1)
    choices.insert(1, choice_2)
    choices.insert(2, choice_3)
    choices.insert(3, choice_4)
    
    right_answer.append(answer)
    
    #remaining words
    unique_list_of_used_words = list(set(words_used))
    
    if total_attempts > 0:
        attempts_correct = int(correct)/int(total_attempts)
        attempts_incorrect = int(incorrect)/int(total_attempts)
        score_text = "\n\n Correct: {}\t {:.0%}\n Incorrect: {}\t {:.0%}".format(correct, attempts_correct, incorrect, attempts_incorrect)
        score.value = score_text
        remain_text = "Total words used {}/{}".format(len(unique_list_of_used_words), len(words))
        remaining.value = remain_text
    
#play button command
def play():
    screen.update()
    choices.enabled = True
    cancel.visible = False
    submit.visible = True
    play.visible = False
    time_live = True
    question_live = True
    t = 0
    wordselection()
#    print("DEBUG:: " + str(right_answer))
    while time_live is True:
        screen.update()
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        display = "Lapsed Time: {:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        time.sleep(1)
        t += 1        
        clock.value = display

#continue function
def continueplay():
    question.visible = True
    cancel.visible = True
    submit.visible = True
    choices.visible = True
    score.visible = True
    remaining.visible = True
    continueplay.visible = False
    correct_meaining.visible = False
    screen.update()
    return True    

# submit button command
def submit():
#    print("DEBUG:: " + str(right_answer))
#    print("DEBUG:: " + str(possibilities))
    if str(right_answer[0]) == choices.value:
#        print("Correct!")
        right.append(the_word[0])
        words_used.append(the_word[0])
        right_answer.clear()
        the_word.clear()
#        print("DEBUG :: " + str(right))
#        print("DEBUG :: " + str(len(right)))
        for i in possibilities:
            choices.remove(str(i))
        wordselection()
    else:
        response = "Incorrect \nThe correct definition was for {} is {}".format(str(the_word[0]), str(right_answer[0]))
        wrong.append(the_word[0])
        correct_meaning.value = response
        words_used.append(the_word[0])
        right_answer.clear()
        the_word.clear()
#        print(response)
#        print("DEBUG :: " + str(wrong))
#        print("DEBUG :: " + str(len(wrong)))
        for i in possibilities:
            choices.remove(str(i))
        wordselection()

def quit():
    pass
    
#initalize GUI
screen = App(title="Study Cards", width=width, height=height)

#display clock
clock = Text(screen, size=10)

#display question
question = Text(screen, size=18)
respond = Text(screen, size=22)

#display possible definitions
choices = ButtonGroup(screen, options=[], enabled=False, width="fill")

#score display
score = Text(screen, size=16)

#remaining words
remaining = Text(screen, size=16)

#correct word
correct_meaning = Text(screen, size=16)

#submit answers
submit = PushButton(screen, text="submit", command=submit, visible=False, align="bottom")

#stop play
cancel = PushButton(screen, text="cancel", command=quit, visible=False, align="bottom")

#continue
continueplay = PushButton(screen, text="continue", command=continueplay, visible=False)

#play button
play = PushButton(screen, text="play", command=play, align="bottom")

#display game window
screen.display()
screen.update()
