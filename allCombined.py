import pyttsx3
import random
import webbrowser
import subprocess
import subprocess
import pyautogui
import os
import time
import speech_recognition as sr
import win32gui, win32con

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

import tensorflow as tf
# tf.compat.v1.reset_default_graph()

from tensorflow.python.framework import ops
ops.reset_default_graph()

# from ahk import AHK
# from ahk.window import Window
# ahk = AHK()

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load('model.tflearn')
except:
    tensorflow.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)








engine = pyttsx3.init()
# getter method(gets the current value of engine property)
voices = engine.getProperty('voices')
# setter method .[0]=male voice and [1]=female voice in set Property.
engine.setProperty('voice', voices[0].id)

def speak(text):
    # Method for the speaking of the the assistant
    engine.say(text)  
    print(f"Sven: {text}")
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()


def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("") 
        return "None"
     
    return query

# GreetingList = ["hi","hello","hey","sup"]
# GreetingResponse = ["hi","hello","hey","sup"]

# CanYouList =["do you get hurt","do you have fingers","do you ever breathe","do you masticate","can you throw up","do you get tired","can you crawl","can you cry","do you dream","do you ever pee","do you ever get hurt","can you breathe","can you masticate","can you burp","can you chew","can you dream","can you eat","can you fart","do you breathe","can you get tired","can you yawn","can you pee","can you poop","can you sneeze","can you sweat","can you vomit","can you get hurt","do you sweat","do you have skin","do you have teeth","do you have toes","do you pee","do you poop","do you ever get tired","do you sneeze","do you have hair","do you throw up","do you vomit","do you yawn","don't you ever masticate","don't you ever sleep","do you have a stomach","do you have intestines","do you sleep","do you ever poop","do you ever sneeze","do you ever sweat","do you ever throw up","do you ever vomit","do you ever walk","do you ever yawn","do you have lungs","do you have legs","do you get zits","do you have a liver","do you have arms","do you have eyes","do you have fingernails","do you have bowels","do you fart","do you ever chew","do you burp","do you chew","do you crawl","do you cry","do you eat","do you ever masticate","do you ever burp","can you walk","do you ever crawl","do you ever cry","do you ever dream","do you ever eat","do you ever fart"]
# CanYouResponse =["I don't have a body.","I don't have the hardware for that.","Not so far.","I know that's a pretty standard human thing, but I'm still a bot.","Nope!","I don't even have a body!"]

# AskMeList = ["what do you want me to inform you who i am?","ama","what can i inform you about me?","want to ask any questions about me?","why don't you ask me questions?","please ask me anything about myself","can you ask me why i'm here?","would you ask me something","why am i the only one asking questions?","what do you want to know about me","can you ask me something about me?","can you ask me anything about myself?","can you ask me anything about me?","can you ask me anything?","can you ask me something?","can you ask anything about myself?","can you ask anything?","ask me something","ask me anything","ask me about something","ask me about anything","ask me a question","can you ask me a question?","do you want to ask me anything?","what do you want me to tell you about?","don't you want to know about me?","don't you want to ask me something?","don't you want to ask me anything","don't you want to ask anything about me?","can you ask me something about myself?","do you want to ask me something?","how about asking me something?","do you want me to tell you anything?","could you ask me something?","could you ask me about something?","can you ask something about myself?","can you ask something about me?","can you ask something?","do you want to know anything about me?","do you have any questions about me?","any questions for me?","is there anything you want to ask me?","just ask me a question","is there anything i can tell you about me?","what's something you want to ask me?","what questions do you have for me?","what are some questions for me?","do you have any questions for me?","would you ask something about myself","would you ask something about me","would you ask something","would you ask me something about myself","what do you want me to teach you who i am","what's something you want to know about me?","i want you to ask me questions","i want you to ask about me","i want you to ask me a question","what do you want to know about me?","can you ask questions?","got any questions for me?","why don't you ask me anything?","would you ask me anything about myself","why don't you ever ask me questions?","now, it's your turn to ask questions","how about you ask me questions?","want to learn more about me?","you have any questions for me?","how about you ask me something?","what do you want to learn about me","would you ask me something about me","why do i have to ask all the questions?","what would you like to learn about me","what would you like to learn about","will you ask anything about me","what would you like to know about","will you ask anything about myself","what do you want to learn about","what do you want to know about","what do you want to ask me about?","what do you want me to tell you who i am?","ask me questions","what would you like to know about me","will you ask something","would you ask me anything about me","would you ask me anything","would you ask anything about myself","would you ask anything about me","would you ask anything","will you ask anything","will you ask something about me","what do you want me to tell you about me?","will you ask me something about myself","will you ask me something about me","will you ask me something","will you ask me anything about myself","will you ask me anything about me","will you ask me anything","will you ask something about myself","please ask something about myself","is there anything i can tell you about myself?","is there anything i can tell you about who i am?","is there anything you want to know about me?","is there something you want to know about me?","please ask anything","please ask anything about me","please ask anything about myself","please ask me anything","please ask me anything about me","please ask me something","please ask me something about me","please ask me something about myself","what can i tell you about me?","what do you want me to teach you about?","what do you want me to teach you about me?","what do you want me to inform you about?","what do you want me to inform you about me?","please ask something","what can i tell you about?","please ask something about me","what can i teach you who i am?","what can i teach you about?","what can i teach you about me?","what can i inform you about?","don't you want to know anything about me?","what can i tell you who i am?","can you ask anything about me?","how about asking something about me?"]
# AskMeResponse = ["I'm better at answering questions.","I'm a much better answerer than asker.","Nah, I'm good.","I'm better at answering questions than asking them."]

                
        
    

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        query = input("Jeff: ").lower()
        if query == "quit":
            break
        
    
   
    ##    query = takeCommand().lower()

        # if(query in GreetingList):
        #     speak(random.choice(GreetingResponse))
        # elif("your name" in query):
        #     speak("My name is Sven")
        # elif(query in CanYouList):
        #     speak(random.choice(CanYouResponse))

        # open stuff
        elif("open youtube" in query):
            webbrowser.open("www.youtube.com")
        elif("open task manager" in query):
            subprocess.Popen('C:\Windows\System32\Taskmgr.exe')
        elif("open settings" in query):
            pyautogui.hotkey('win','i')
        elif("open chrome" in query):
            subprocess.Popen('C:\Program Files\Google\Chrome\Application\chrome.exe')
            # elif("open file explorer"or"open downloads" in query):
            # os.startfile(r'C:\Users\Bregwin Paul\Downloads')
        elif("open notifications" in query):
            pyautogui.hotkey('win','a')
        elif("open downloads" in query):
            os.startfile(r'C:\Users\Bregwin Paul\Downloads')
            # from pathlib import Path
            # downloads_path = str(Path.home() / "Downloads")
        elif("open documents" in query):
            os.startfile(r'C:\Users\Bregwin Paul\Documents')
        elif("open music" in query):
            os.startfile(r'C:\Users\Bregwin Paul\Music')
        elif("open videos" in query):
            os.startfile(r'C:\Users\Bregwin Paul\Videos')
        elif("open pictures" in query):
            os.startfile(r'C:\Users\Bregwin Paul\Pictures')  
        elif("open date and time" in query):
            pyautogui.hotkey('win','alt','d')
        elif("enter" in query):
            pyautogui.press('enter')
        elif("windows" and "search" in query.split()):

            pyautogui.hotkey('win','s')
            time.sleep(1)


            NewQuery = query.split()
            RemoveTheseWords = ["search","windows","in"]
            for i in range(len(RemoveTheseWords)):
                if (RemoveTheseWords[i] in NewQuery):
                    NewQuery.remove(RemoveTheseWords[i])
            pyautogui.write(' '.join(NewQuery))

    ##    elif("create" and "folder" and "named" in query.split()):
        elif( "create" in query.split() and "folder" in query.split() and "named" in query.split() ):
            
            
            NewQuery = query.split()
            RemoveTheseWords = ["create","folder","named","a","new"]
            for i in range(len(RemoveTheseWords)):
                if (RemoveTheseWords[i] in NewQuery):
                    NewQuery.remove(RemoveTheseWords[i])
            # print(' '.join(NewQuery))
            path = "C:\\Users\\Bregwin Paul\\Downloads\\" + ' '.join(NewQuery)
            os.mkdir(path)
    ##        os.startfile(r'C:\Users\Bregwin Paul\Downloads')
    ##        pyautogui.PAUSE = 1
    ##        pyautogui.hotkey('ctrl','shift','n')
    ##        pyautogui.write(' '.join(NewQuery))
    ##        pyautogui.press('enter')
        elif("minimize" in query):
            def enumHandler(hwnd, lParam):
                        if selectWindow in win32gui.GetWindowText(hwnd):
                            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            
            NewQuery = query.split()
            RemoveTheseWords = ["minimize"]
            for i in range(len(RemoveTheseWords)):
                if (RemoveTheseWords[i] in NewQuery):
                    NewQuery.remove(RemoveTheseWords[i])
                    selectWindow = ' '.join(NewQuery).title()
                    win32gui.EnumWindows(enumHandler, None)
            
        else :
            results = model.predict([bag_of_words(query, words)])
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            print(random.choice(responses))

chat()
