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
participant_id.addField('Condition: ', choices = ['binaries', 'aliens', "HCI-example"])
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
        # Load the corresponding alien picture
        self.pict = visual.ImageStim(win, image = 'pictures/aliens/'+self.combination_string+'.png', size = [1.5, 1.2], pos = [0, 0.1])

    # the function that defines the rule for correct combinations
    ## /!\ DO NOT CHANGE /!\ Except if you want to change the rule ##
    def is_dangerous(self):
    # if the third digit is 1 or the fourth is 1 (but not both),
    # then the combination is wrong (hence, the alien is dangerous)
        if self.combination_string in ruleset :
            return True
        else:
            return False
            
    def draw_representation(self):
        ## FIRST CASE, we want to display the combination as it is: with numbers.
        if ID[0] == "binaries":
            # We make rectangular frames, one for each number (so 5 in total)
            self.r1 = visual.Rect(win, width = 0.3, height = 0.3, fillColor = 'white', lineColor = None, pos = [-0.8, 0.2]) 
            self.r2 = visual.Rect(win, width = 0.3, height = 0.3, fillColor = 'white', lineColor = None, pos = [-0.4, 0.2]) 
            self.r3 = visual.Rect(win, width = 0.3, height = 0.3, fillColor = 'white', lineColor = None, pos = [0, 0.2])
            self.r4 = visual.Rect(win, width = 0.3, height = 0.3, fillColor = 'white', lineColor = None, pos = [0.4, 0.2])
            self.r5 = visual.Rect(win, width = 0.3, height = 0.3, fillColor = 'white', lineColor = None, pos = [0.8, 0.2])

            # Then we write the number itself (as psychopy text stimuli)
            self.txt1 = visual.TextStim(win, text = str(self.first_n), color ='black', pos = [-0.8, 0.2])
            self.txt2 = visual.TextStim(win, text = str(self.second_n), color = 'black', pos = [-0.4, 0.2])
            self.txt3 = visual.TextStim(win, text = str(self.third_n), color = 'black', pos = [0, 0.2])
            self.txt4 = visual.TextStim(win, text = str(self.fourth_n), color = 'black', pos = [0.4, 0.2])
            self.txt5 = visual.TextStim(win, text = str(self.fifth_n), color = 'black', pos = [0.8, 0.2])

            # we create a list of all stimuli to display to make it easier to draw them
            screen = [stim.r1, stim.r2, stim.r3, stim.r4, stim.r5,
                     stim.txt1, stim.txt2, stim.txt3, stim.txt4, stim.txt5]
            # we draw all stimuli in the previously made list using a loop
            for s in screen:
                s.draw()

        ## SECOND CASE, we want to use the alien picture to display the stimulus
        # Each combination correspond to a specific alien with different features
        elif ID[0] == "aliens":
        # we simply draw the alien picture corresponding to the current combination
        # The picture was preloaded in the __init__ function above
        # Feel free to check the folder pictures/aliens to see what it looks like
            self.pict.draw()

        ## THIRD CASE, an example using psychopy shape stimuli
        elif ID[0] == "HCI-example":

            ## I decided to use 2 intertwined polygons and make their color and shape depending on the combination

            # The first number will impact the number of vertices of the main shape
            # If first_n = 0, we have a rectangle, if first_n = 1 we have an hexagon
            n_vertices = 4 + 2 * self.first_n

            # The second number will impact the orientation of the main shape
            # If second_n = 1, tilt the shape by 90 degrees
            orientation = self.second_n*90

            s2 = visual.Circle(win, radius=0.25,  pos =[0, 0.3], lineWidth = 6)

            if self.third_n == 1:
                col = "red"
            else:
                col = "yellow"

            if self.fourth_n == 1:
                col2 = "white"
            else:
                col2 = "black"

            # The last number will impact the number of vertices of the secondary shape
            # If fifth_n = 0, we get a small triangle, if fifth_n = 1 we get a small circle
            n_vertices2 = 3 + 32 * self.fifth_n

            # According to the rule we currently use, what really matters is the combinations of colors.
            # If you know anything about heraldic design, the pattern should be easy to notice.
            # In heraldry, BLACK and RED are considered "colors"
            # while WHITE and YELLOW are considered "metals" (silver and gold respectively).
            # When designing a pattern, only combinations of color-metals are allowed, not color-color or metal-metal.
            # More here if interested:
            # https://www.theheraldrysociety.com/wp-content/uploads/2018/03/Heraldry-For-Beginners.pdf
            # (Which I doubt)

            # /!\ IMPORTANT NOTE: this visualisation is overfitting the solution space of the rule we are using.
            # Although it still requires some very specific expertise to figure it out quickly,
            # the benefits of such visualisation would probably be different if the rule is different.

            # Creating our shapes according to our dynamic parameters
            s1 = visual.Polygon(win, edges=n_vertices, fillColor=col, lineColor=col, ori=orientation,  pos =[0, 0.3])
            s2 = visual.Polygon(win, edges=n_vertices2, fillColor=col2, lineColor=col2, radius=0.25, pos=[0, 0.3])
            # Drawing them
            s1.draw()
            s2.draw()


## run experiment ##
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
