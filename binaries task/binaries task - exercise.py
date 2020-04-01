##The Rationale Experiment

##Reinforcement learning
from psychopy import visual, core, event, gui, data
import pandas as pd
import random
import itertools


## Show the dialogue box to record demographics:
# gui requesting participant info
participant_id = gui.Dlg(title='The Rationale Experiment') 
participant_id.addText('Subject Info')
participant_id.addField('Condition: ', choices = ["HCI-example"])
participant_id.addField('ID: ')
participant_id.addField('Age: ')
participant_id.addField('Gender: ', choices = ['female', 'male', 'other'])
participant_id.show()
if participant_id.OK:
    ID = participant_id.data                     #saves data from Gui dialogue box into the variable 'ID'


## Prepare the dataset:
# get date for unique logfile id
date = data.getDateStr()
# define panda dataframe with information
columns = ['Date','ID','Age','Gender','Condition','Stimulus','Choice','Correct', 'RT']
DATA = pd.DataFrame(columns=columns)
filename = 'logfiles/logfile_{}_{}_{}_{}.csv'.format(ID[0],ID[1],ID[2], date)


## Prepare all static elements that will be used:
#define window
win = visual.Window(fullscr=True, color = 'black')
#clock
stopwatch = core.Clock()
# define mouse
myMouse = event.Mouse()
# buttons
like = visual.ImageStim(win, image = 'pictures/like.png', pos = [-0.3, -0.5], size = [0.25,0.4])
dislike = visual.ImageStim(win, image = 'pictures/dislike.png', pos = [0.3, -0.5], size = [0.25, 0.4])
# load the ruleset
rulefile = open("rules/ruleset1.txt", mode="r")
ruleset = rulefile.readlines()  # make a list of combinations
ruleset = [i[:-1] for i in ruleset]  # clean the spaces
rulefile.close()

# show instructions
def instruc(instr, keys = ['space', 'escape']):
    instrus = visual.ImageStim(win, image = instr)
    instrus.draw()
    win.flip()
    key = event.waitKeys(keyList = keys)[0]
    if key == 'escape':
        core.quit()

# message
def msg(txt, keys = ['space', 'escape']):
    message = visual.TextStim(win, text = txt, color = 'white', height = 0.06)
    message.draw()
    win.flip()
    key = event.waitKeys()
    if key == 'escape':
        core.quit()

## Preparing the stimuli:
n_repeat = 2 # define how many times we want to see the whole set of stimuli

# We have 5 independent binary variables, we can create all combinations using itertools function:
# 2^5 = 32, we have 32 different combinations from 00000 to 11111
# With n_repeat = 2, we get 64 trials (32 different combinations * 2)
trial_list = list(itertools.product([0,1], repeat=5)) * n_repeat
random.shuffle(trial_list) # we shuffle the list

# We create a Stimulus class that we will use to define and draw each stimulus
class Stimulus():
    def __init__(self, combination):
        # Here we save each digit of the combination in its own variable in order to be explicit in the following steps
        self.first_n = combination[0]
        self.second_n = combination[1]
        self.third_n = combination[2]
        self.fourth_n = combination[3]
        self.fifth_n = combination[4]
        self.combination_string = "".join(str(i) for i in combination) # save the combination as a string

    # the function that defines the rule for correct combinations
    ## /!\ DO NOT CHANGE /!\
    def is_dangerous(self):
        if self.combination_string in ruleset :
            return True
        else:
            return False
            
    def draw_representation(self):
###### This FUNCTION IS THE ONLY THING YOU NEED TO DEFINE FOR THE PURPOSE OF THIS EXERCISE ##########################
        #
        # You should use it to transform the combination of binary digits into a unified visual representation.
        #
        # You can use any visuals supported by PsychoPy (more here: https://www.psychopy.org/api/visual.html )
        # - You can load images: https://www.psychopy.org/api/visual/imagestim.html#psychopy.visual.ImageStim
        # - Write text: https://www.psychopy.org/api/visual/textstim.html#psychopy.visual.TextStim
        # - Make shapes: ShapeStim, Rect, Circle, Polygon, Line
        #
        # Ideally each number should correspond to a feature of your visual stimulus.
        # You can for example change the font size of a text, the color, the position or shape of a polygon, ...
        # and much much more! Be creative with your solution!
        #
        # To refer to the digits, you simply have to call the following variables:
        # self.first_n ; self.second_n ; self.third_n ; self.fourth_n ; self.fifth_n
        # They correspond to each digit in the the combination as if you would read them from left to right.
        # For example, given 1 0 0 0 0, self.first_n would be the 1, self.fifth_n would be the last 0
        #
        # You can check the rule that determines the solution space in the function "is_dangerous" defined above.
        #
        # There is /!\ ONE IMPORTANT THING /!\:
        # your function should end with you "drawing" the stimulus. Otherwise, nothing will show on screen.
        # Like this:
        #   my_stimulus = visual.something( some parameters )
        #   my_stimulus.draw() <-- THIS IS THE IMPORTANT PART!!!
        # You can find some examples in "binaries task - examples.py"

        pass # please, remove me once you start writing this function.

############################## NOTHING TO CHANGE BEYOND THIS BANNER #################################################

## Run the experiment ##
#Introduction
instructions='pictures/Instructions/'+str(ID[0])
instruc(instructions,['space', 'escape'])

# Iterate through the trial list
for i in trial_list:
    
    # create the stimulus based on the combination of this trial
    stim = Stimulus(combination = i)
    # Recenter the mouse to avoid unfortunate double clicks
    event.Mouse(visible=True, newPos=[0,-0.5], win=win)
    
    while True:
        # show stimuli
        stim.draw_representation() # draw the stimulus itself
        like.draw() # draw like button
        dislike.draw() # draw dislike button
        win.flip()
        
        # get response
        if myMouse.isPressedIn(like):
            choice = 'like'
            reaction_time = stopwatch.getTime()
            if not stim.is_dangerous():
                correct = 1
            else:
                correct = 0
            break
            
        elif myMouse.isPressedIn(dislike):
            choice = 'dislike'
            reaction_time = stopwatch.getTime()
            if stim.is_dangerous():
                correct = 1
            else:
                correct = 0
            break
        
        elif event.getKeys(['escape']):
            DATA.to_csv(filename)
            core.quit()
            
    # display feedback depending on answer
    if correct:
        fb = visual.TextStim(win, text = 'Correct', pos = [0, 0], color = 'white', height = 0.1)
    else:
        fb = visual.TextStim(win, text = 'Incorrect', pos = [0, 0], color = 'white', height = 0.1)      
    fb.draw()
    win.flip()
    core.wait(1.5) # go to next stimulus after 1.5 seconds
        
    
    DATA = DATA.append({
        'Date': date,
        'ID': ID[1],
        'Age': ID[2],
        'Gender': ID[3],
        'Condition': ID[0],
        'Stimulus': stim.combination_string,
        'Choice': choice,
        'Correct': correct,
        'RT': reaction_time, 
        }, ignore_index=True)
    DATA.to_csv(filename)

msg('The experiment is finished. Thank you very much for your participation!', ['space', 'escape'])

win.close()

core.quit
