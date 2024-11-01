#
# AniseikoniaTest:Awaya's new aniseikonia test in personal computer.
# Copyright (C) 2024 nurunuru3427.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#/


from psychopy import visual, core, event
from psychopy.hardware import keyboard, joystick
import psychopy
import math
import tkinter as tk
import tkinter.messagebox as messagebox
import configparser
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 粟 屋 忍,菅 原 美 雪,堀 部 福 江,鳥 井 文 恵:新 しい
#不 等 像 視 検 査 法 “New Aniseikonia Test” の 開
#発 と そ の 臨 床 的 応 用.日 眼: 86: 91-96, 1982.

config_ini = configparser.ConfigParser()
config_ini.read('./config.ini', encoding='utf-8')

darkenButton = int(config_ini['Gamepad']['darkenButton'])
brightenButton = int(config_ini['Gamepad']['brightenButton'])
quitButton = int(config_ini['Gamepad']['quitButton'])
resetButton = int(config_ini['Gamepad']['resetButton'])
antiSuppressionONButton = int(config_ini['Gamepad']['antiSuppressionONButton'])
antiSuppressionOFFButton = int(config_ini['Gamepad']['antiSuppressionOFFButton'])
leftJoystickVertical = int(config_ini['Gamepad']['leftJoystickVertical'])
rightJoystickVertical = int(config_ini['Gamepad']['rightJoystickVertical'])
leftJoystickHorizontal = int(config_ini['Gamepad']['leftJoystickHorizontal'])
rightJoystickHorizontal = int(config_ini['Gamepad']['rightJoystickHorizontal'])
greenButton = int(config_ini['Gamepad']['greenButton'])
redButton = int(config_ini['Gamepad']['redButton'])
mmViewDistance = int(config_ini['Monitor']['mmViewDistance'])
mmPerPx = float(config_ini['Monitor']['mmPerPx'])
eclipseSize = int(config_ini['Monitor']['eclipseSize'])
StimuliPos = int(config_ini['Monitor']['StimuliPos'])

windowSize = [2560, 1440]
fillColorR = [1, 0, 0]
fillColorG = [0, 1, 0]
fillColorBackGround = [0.92, 0.92, 0.92]

joystick.backend='pyglet'  # must match the Window


nJoys = joystick.getNumJoysticks()
if nJoys == 0:
    tk.Tk().withdraw()
    messagebox.showinfo('エラー', 'ゲームパッドが認識できません。接続されているか確認してください')
    quit()

# Setup stimulus and so on
win = visual.Window(monitor = "testMonitor", units = "pix", waitBlanking = True, fullscr = True, color = fillColorBackGround, colorSpace = 'rgb', allowGUI = True, winType='pyglet')

joy = joystick.Joystick(0)  # id must be <= nJoys - 1

centerSignVertical = visual.Line(win, lineColor="black", start=[0, -10], end=[0, 10])
centerSignHorizontal = visual.Line(win, lineColor="black", start=[-10, 0], end=[10, 0])
mask = visual.ImageStim(win)
mask.setImage('maskOpaque.png')
mask.autoDraw = False

leftStimulusSize = eclipseSize
rightStimulusSize = eclipseSize
leftStimulusPos = [-StimuliPos, 0]
rightStimulusPos = [StimuliPos, 0]


leftStimulus = visual.Pie(win, fillColor=fillColorR, start=0, end=180, radius=leftStimulusSize, ori=180, pos = [-250, 0])
rightStimulus = visual.Pie(win, fillColor=fillColorG, start=0, end=180, radius=rightStimulusSize, ori=0, pos = [250, 0])
indicatorStim = visual.TextStim(win, color="black", pos=[-400, -330])


sizeStep = 0.1
posStep = 1.0
stripeSize = 20
FPS = 60
frames = 0
stripe2show = False
threshold = 0.5
colorStep = 1 / 1000

antiSuppessionMode = 0

while True:
    if antiSuppessionMode == 1:
        frames = frames + 1
        if (frames >= (FPS / 2) - 1):
            stripe2show = True
        if (frames >= FPS - 1):
            frames = 0
            stripe2show = False
        if stripe2show == True:
            mask.draw()
    centerSignVertical.draw()
    centerSignHorizontal.draw()
    leftStimulus.draw()
    rightStimulus.draw()

    if event.getKeys(['q']):
        leftStimulusSize = leftStimulusSize + sizeStep
    
    if joy.getAxis(leftJoystickVertical) < -threshold and joy.getAxis(rightJoystickVertical) > threshold:
        leftStimulusPos[1] = leftStimulusPos[1] + posStep
        rightStimulusPos[1] = rightStimulusPos[1] - posStep
    elif joy.getAxis(leftJoystickVertical) < -threshold:
        leftStimulusSize = leftStimulusSize + sizeStep
    elif joy.getAxis(5) > threshold:
        rightStimulusSize = rightStimulusSize - sizeStep

    if joy.getAxis(leftJoystickVertical) > threshold and joy.getAxis(rightJoystickVertical) < -threshold:
        leftStimulusPos[1] = leftStimulusPos[1] - posStep
        rightStimulusPos[1] = rightStimulusPos[1] + posStep
    elif joy.getAxis(leftJoystickVertical) > threshold:
        leftStimulusSize = leftStimulusSize - sizeStep
    elif joy.getAxis(rightJoystickVertical) < -threshold:
        rightStimulusSize = rightStimulusSize + sizeStep

    if event.getKeys(['z']):
        leftStimulusSize = leftStimulusSize - sizeStep
    
    if event.getKeys(['e']):
        rightStimulusSize = rightStimulusSize + sizeStep
    
    if event.getKeys('[c]'):
        rightStimulusSize = rightStimulusSize - sizeStep
    if event.getKeys(['1']):
        leftStimulusPos[0] = leftStimulusPos[0] + posStep
        rightStimulusPos[0] = rightStimulusPos[0] - posStep
    if (joy.getAxis(leftJoystickHorizontal) > threshold) or (joy.getAxis(rightJoystickHorizontal) < -threshold) :
        leftStimulusPos[0] = leftStimulusPos[0] + posStep
        rightStimulusPos[0] = rightStimulusPos[0] - posStep
    if event.getKeys(['2']):
        leftStimulusPos[0] = leftStimulusPos[0] - posStep
        rightStimulusPos[0] = rightStimulusPos[0] + posStep
    if (joy.getAxis(leftJoystickHorizontal) < -threshold) or (joy.getAxis(rightJoystickHorizontal) > threshold):
        leftStimulusPos[0] = leftStimulusPos[0] - posStep
        rightStimulusPos[0] = rightStimulusPos[0] + posStep
    if event.getKeys(['a']) or joy.getButton(antiSuppressionONButton) == True:
        antiSuppessionMode = 1
    if event.getKeys(['d']) or joy.getButton(antiSuppressionOFFButton) == True:
        antiSuppessionMode = 0
    if joy.getButton(quitButton) == True:
        print("quitting")
        core.quit()
    if joy.getButton(resetButton) == True:
        leftStimulusPos[0] = -StimuliPos
        rightStimulusPos[0] = StimuliPos
        leftStimulusSize = eclipseSize
        rightStimulusSize = eclipseSize

    if (joy.getAxis(greenButton) > threshold and fillColorR[1] < 1 and fillColorG[0] < 1):
        # fillColorR[2] = math.sqrt(fillColorR[2] - 2 * colorStep * (-fillColorR[0] + fillColorR[1] + colorStep))
        fillColorR[0] = fillColorR[0] - colorStep
        fillColorR[1] = fillColorR[1] + colorStep

        # fillColorG[2] = math.sqrt(fillColorG[2] - 2 * colorStep * (fillColorG[0] - fillColorG[1] + colorStep))
        fillColorG[0] = fillColorG[0] + colorStep
        fillColorG[1] = fillColorG[1] - colorStep
        leftStimulus.fillColor = fillColorR
        rightStimulus.fillColor = fillColorG
    
    if (joy.getAxis(redButton) > threshold and fillColorR[0] < 1 and fillColorG[1] < 1):
        # fillColorR[2] = math.sqrt(fillColorR[2] - 2 * colorStep * (fillColorR[0] - fillColorR[1] + colorStep))
        fillColorR[0] = fillColorR[0] + colorStep
        fillColorR[1] = fillColorR[1] - colorStep

        # fillColorG[2] = math.sqrt(fillColorG[2] - 2 * colorStep * (-fillColorG[0] + fillColorG[1] + colorStep))
        fillColorG[0] = fillColorG[0] - colorStep
        fillColorG[1] = fillColorG[1] + colorStep
        leftStimulus.fillColor = fillColorR
        rightStimulus.fillColor = fillColorG
    

    # Darken the background
    if joy.getButton(darkenButton) == True:
        fillColorBackGround[0] = fillColorBackGround[0] - colorStep
        fillColorBackGround[1] = fillColorBackGround[1] - colorStep
        fillColorBackGround[2] = fillColorBackGround[2] - colorStep
    # Brighten the background
    if joy.getButton(brightenButton) == True:
        fillColorBackGround[0] = fillColorBackGround[0] + colorStep
        fillColorBackGround[1] = fillColorBackGround[1] + colorStep
        fillColorBackGround[2] = fillColorBackGround[2] + colorStep

    win.color = fillColorBackGround


    if leftStimulusSize < rightStimulusSize:
        ratio = rightStimulusSize / leftStimulusSize
        ratio = ratio - 1.0
        ratio = ratio * 100
        ratio = round(ratio, 2)
        strTested = 'R' + str(ratio) + '%'
    elif leftStimulusSize > rightStimulusSize:
        ratio = leftStimulusSize / rightStimulusSize
        ratio = ratio - 1.0
        ratio = ratio * 100
        ratio = round(ratio, 2)
        strTested = 'L' + str(ratio) + '%'
    else:
        strTested = '0%'

    tropia = leftStimulusPos[1] - rightStimulusPos[1]
    tropia = tropia * mmPerPx
    tropia = tropia / mmViewDistance
    tropia = tropia * 100.0
    tropia = round(tropia, 2)
    tropiaStr = "HT" + str(tropia)


            

    indicatorStim.text = strTested + tropiaStr + \
          'DIST' + str(round(rightStimulusPos[0] * 2, 2)) + \
          'fillR' + str([round(fillColorR[n], 2) for n in range(len(fillColorR))]) + \
          'fillG' + str([round(fillColorG[n], 2) for n in range(len(fillColorG))])

    leftStimulus.radius = leftStimulusSize
    rightStimulus.radius = rightStimulusSize
    leftStimulus.pos = leftStimulusPos
    rightStimulus.pos = rightStimulusPos

    indicatorStim.draw()

    if event.getKeys(['escape']):
        print("quitting")
        core.quit()
    win.flip()