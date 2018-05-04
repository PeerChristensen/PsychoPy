# Speeded response task testing cross-modal correspondences for pitch

#import
from psychopy.visual import Circle
from psychopy import visual, event, core, sound, gui
import random, os, csv

#log
log_path = '/Users/peerchristensen/Desktop/Projects/pitch_perception/RT_logs/' 
info = {'participant':'','age':'','language':"",'gender':['male', 'female']}
if not gui.DlgFromDict(info, order=['participant', 'age', 'language', 'gender']).OK:      
    core.quit()  
log = open(log_path+str(info['participant'])+".csv",'w')   
writer = csv.writer(log, delimiter=";")
cols="participant","language","gender","age","condition","block","trial","sound","visual","key","RT"
writer.writerow(cols)

#window
win = visual.Window(fullscr=True,useRetina=False,allowGUI=True,monitor='testMonitor',units='pix',color=(0,0,0))
black=[-1,-1,-1]
center = [-0.1,0]

#messages
msg = visual.TextStim(win, text="->",pos=center,units="deg", color=black,height=3)

#constants
#if int(info['participant']) % 2 == 0:
#    conditions = ['size','height']
#else:
#     conditions = ['height', 'size']   
nBlocks = 20 #20
nTrials = 16 #16


conditions = ['height', 'size'] * (nBlocks/2)
random.shuffle(conditions)

#time
RT=core.Clock()

#sound stimuli
#highSound = sound.Sound('A',octave=4,sampleRate=44100,secs=0.120,stereo=True,name = "high")
highSound = sound.Sound("/Users/peerchristensen/Desktop/PsPy/high_low_short/high_a4.wav",name = "high")
#lowSound  = sound.Sound('A',octave=2,sampleRate=44100,secs=0.120,stereo=True,name = "low")
lowSound = sound.Sound("/Users/peerchristensen/Desktop/PsPy/high_low_short/low_a1.wav",name = "low")
sounds=[highSound,lowSound] * (nTrials/2)
    
# Visual stimuli
#fixation cross
fixCross = visual.TextStim(win, text="+",pos=center,units="deg", color=black,height=3)
#HEIGHT
circleHIGH = Circle(win=win,units="deg",radius= 3, fillColor=black,lineColor=black,pos=[-0.1,8],name="high")
circleLOW = Circle(win=win,units="deg",radius= 3, fillColor=black,lineColor=black,pos=[-0.1,-8],name="low")
#SIZE
circleBIG = Circle(win=win,units="deg",radius= 6, fillColor=black,lineColor=black,pos=center,name="big")
circleSMALL = Circle(win=win,units="deg",radius= 1.5, fillColor=black,lineColor=black,pos=center,name="small")

stimsSize= [circleBIG,circleSMALL] * (nTrials/2)
stimsHeight=[circleHIGH,circleLOW] * (nTrials/2)

#warm up
circles=[circleBIG,circleSMALL,circleHIGH,circleLOW] * 2
random.shuffle(circles)
voices=[highSound,lowSound] * 4
random.shuffle(voices)
msg.draw()
win.flip()
event.waitKeys(keyList=['return'])

for i in range(len(circles)):
    fixCross.draw()
    win.flip()
    core.wait(0.50)
    circles[i].draw()
    win.flip()
    voices[i].play()
    core.wait(0.120)
    win.flip()
    press = event.waitKeys(keyList=["s","k"], timeStamped=False)
    
#experiment
time=core.Clock()

for i in range(0,nBlocks):
    if conditions[i] == "size":
        stims = stimsSize
    else:
        stims = stimsHeight
    msg.draw()
    win.flip()
    event.waitKeys('return')
    win.flip()
    random.shuffle(sounds)
    random.shuffle(stims)
    core.wait(1)
    for s in range(len(stims)):
        fixCross.draw()
        win.flip()
        core.wait(0.50)
        stims[s].draw()
        win.flip()
        sounds[s].play()
        RT.reset()
        core.wait(0.120)
        win.flip()
        press = event.waitKeys(keyList=["s","k"], timeStamped=RT)
        row=info['participant'],info['language'],info['gender'],info['age'],conditions[i],i+1,s+1,sounds[s].name,stims[s].name,press[0][0],press[0][1]
        writer.writerow(row)
    win.flip()
    core.wait(1)
log.close()    
estimate=time.getTime()
print(estimate)
win.close()
core.quit()