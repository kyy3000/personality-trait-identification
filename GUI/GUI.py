#For NatLan Processing
#By R. Valkama

import tkinter as tk
import re
import string
import matplotlib.pyplot as plt
from math import pi
import pandas as pd
from PIL import Image, ImageTk
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from CsvHandler import calculateAverageSentiment
from CsvHandler import getTweetData

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Mainmenu, AccountInfo, Tweetmenu, TweetInfo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row= 0, column=0, sticky="nsew")

        self.show_frame(Mainmenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Mainmenu(tk.Frame):   #The start page for the application. User choice of account is saved into key and the key update other frames with right  information of the account

    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        controller.geometry("1200x1200")
        controller.title("Project 17: Personality Trait Identification and emotion")

        label = tk.Label(self, text = "Main menu", font = ("Helvetica", 20))
        label.pack(pady= 100, padx= 10)

        button1 = tk.Button(self, text= "View @JennyENicholson", command = lambda:[keyholder.setkey(0),controller.show_frame(AccountInfo)])
        button1.pack(pady= 20, padx= 10)

        button2 = tk.Button(self, text= "View @9_volt_", command = lambda:[keyholder.setkey(1),controller.show_frame(AccountInfo)])
        button2.pack(pady= 20, padx= 10)

        button3 = tk.Button(self, text= "View @FoldableHuman", command = lambda:[keyholder.setkey(2),controller.show_frame(AccountInfo)])
        button3.pack(pady= 20, padx= 10)

        button4 = tk.Button(self, text= "View @marinscos", command = lambda:[keyholder.setkey(3),controller.show_frame(AccountInfo)])
        button4.pack(pady= 20, padx= 10)

        button5 = tk.Button(self, text= "View @YingjueChen", command = lambda:[keyholder.setkey(4),controller.show_frame(AccountInfo)])
        button5.pack(pady= 20, padx= 10)


class AccountInfo(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        self.key = keyholder.getkey()

        self.namelist = ["@JennyENicholson", "@9_volt_", "@FoldableHuman", "@marinscos", "@YingjueChen"]
        self.suffix = ["jennyenicholson.csv","9volt.csv","foldablehuman.csv","marinscos.csv","yingjuechen.csv"]
        self.txtfile = ["jennyenicholson.txt","ninevolt.txt","foldablehuman.txt","marinscos.txt","yingjuechen.txt"]
        self.keyname = ["jennyenicholson","9volt","foldablehuman","marinscos","yingjuechen"]
        self.personality_trait = ["openness.png","conscientiousness.png", "extraversion.png", "agreeableness.png", "neuroticism.png"]
        self.data = ""
 
        self.label = tk.Label(self, text= "Account Name", font = ("Helvetica", 16))
        self.label.pack(pady= 10, side= "top", anchor= "n")
        
        values = [0,0,0,0,0]
        createRadarPGN(values)

        self.image = Image.open('images/happy.png')
        self.image = self.image.resize((100,100),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img2 = tk.Label(self, image=self.render)
        self.img2.image = self.render
        self.img2.pack(pady= 10, side= "top", anchor= "n")

        self.sentlabel = tk.Label(self, text = 0, font = ("Helvetica", 12))
        self.sentlabel.pack()

        self.button1 = tk.Button(self, text= "Back", command = lambda:controller.show_frame(Mainmenu))
        self.button1.pack(padx= 100, pady= 100, side="left", anchor= "sw")

        self.button2 = tk.Button(self, text= "View Tweets", command = lambda:controller.show_frame(Tweetmenu))
        self.button2.pack(padx= 100, pady= 100, side="right", anchor= "se")

        self.image = Image.open('images/radar.png')
        self.image = self.image.resize((500,370),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img1 = tk.Label(self, image=self.render)
        self.img1.image = self.render
        self.img1.pack(side= "bottom", pady= 50, anchor= "s")

        self.plotname1 = tk.Label(self, text= "Personality Scores", font = ("Helvetica", 12))
        self.plotname1.pack(pady = 10, side= "bottom", anchor= "s")

        self.image = Image.open("images/" + self.keyname[0] + "/" + self.personality_trait[0])
        self.image = self.image.resize((700,300),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img3 = tk.Label(self, image=self.render)
        self.img3.image = self.render
        self.img3.pack(side= "bottom", pady= 50, anchor= "s")

        self.trait_1 = tk.Button(self, text= "Openness", command= lambda: self.updateImage(0))
        self.trait_1.pack(padx= 25, pady= 10, side= "left", anchor = "n")
        self.trait_2 = tk.Button(self, text= "Conscientiousness", command= lambda: self.updateImage(1))
        self.trait_2.pack(padx= 25, pady= 10, side= "left", anchor = "n")
        self.trait_3 = tk.Button(self, text= "Extraversion", command= lambda: self.updateImage(2))
        self.trait_3.pack(padx= 25, pady= 10, side= "left", anchor = "n")
        self.trait_4 = tk.Button(self, text= "Agreeableness", command= lambda: self.updateImage(3))
        self.trait_4.pack(padx= 25, pady= 10, side= "left", anchor = "n")
        self.trait_5 = tk.Button(self, text= "Neuroticism", command= lambda: self.updateImage(4))
        self.trait_5.pack(padx= 25, pady= 10, side= "left", anchor = "n")
        
        self.updatePage()

    def updatePage(self): #Update the frame when a new key appears
    
        if self.key != keyholder.getkey():

            self.key = keyholder.getkey()
            self.data = "tweets/" + self.suffix[self.key]

            self.label["text"] = self.namelist[self.key]
            self.label.pack(pady= 10, side="top", anchor= "n")

            sentaverage = calculateAverageSentiment(self.data)
            text = "Sentiment Status:    " + str('{0:.5g}'.format(sentaverage))

            self.sentlabel["text"] = text
            self.sentlabel.pack(pady= 10, side= "top", fill= "both")

            if sentaverage > 0:
                photo = Image.open("images/happy.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            if sentaverage < 0:
                photo = Image.open("images/sad.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            if sentaverage == 0:
                photo = Image.open("images/neutral.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            self.img2.config(image = photo)

            textfile = "Final_values/Accounts/" + self.txtfile[self.key]

            values = []
            with open(textfile) as mytxt:
                for line in mytxt:
                    newline = line.rstrip("").split(",")
                    for i in range(len(newline)):
                        values.append(float(newline[i]))

            createRadarPGN(values)

            photo = Image.open("images/radar.png")
            photo = photo.resize((500,370),Image.BICUBIC)
            photo = ImageTk.PhotoImage(photo)
            self.img1.photo_ref = photo
            self.img1.config(image = photo)

            photo = Image.open("images/" + self.keyname[self.key] + "/" + self.personality_trait[0])
            photo = photo.resize((700,300),Image.BICUBIC)
            photo = ImageTk.PhotoImage(photo)
            self.img3.photo_ref = photo
            self.img3.config(image = photo)

        self.after(10, self.updatePage)

    def updateImage(self, idx): #Update the frame when user want to see other image
        photo = Image.open("images/" + self.keyname[self.key] + "/" + self.personality_trait[idx])
        photo = photo.resize((700,300),Image.BICUBIC)
        photo = ImageTk.PhotoImage(photo)
        self.img3.photo_ref = photo
        self.img3.config(image = photo)
        
class Tweetmenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        self.key = keyholder.getkey()
        self.namelist = ["@JennyENicholson", "@9_volt_", "@FoldableHuman", "@marinscos", "@YingjueChen"]
        self.suffix = ["jennyenicholson.csv","9volt.csv","foldablehuman.csv","marinscos.csv","yingjuechen.csv"]
        self.tweetimage = ["images/jennyenicholson/jennyenicholson.png", "images/9volt/9volt.png","images/foldablehuman/foldablehuman.png","images/marinscos/marinscos.png","images/yingjuechen/yingjuechen.png"]
        self.data = ""

        self.label = tk.Label(self, text = "Tweets", font = ("Helvetica", 16))
        self.label.pack(pady= 10, padx= 10)

        self.listbox = tk.Listbox(self, width=50, height=25)
        self.listbox.pack()

        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="left", fill="y", pady=30)

        self.image = Image.open(self.tweetimage[0])
        self.image = self.image.resize((700,400),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img = tk.Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack( pady= 50)

        self.button1 = tk.Button(self, text= "Back", command = lambda:controller.show_frame(AccountInfo))
        self.button1.pack(padx= 100, pady= 100, side="left", anchor= "sw")

        self.button2 = tk.Button(self, text= "View Tweet ", command = lambda:controller.show_frame(TweetInfo))
        self.button2.pack(padx= 100, pady= 100, side="right", anchor= "se")

        self.updatePage()
    
    def onselect(self,event): #listen to user's choice and save tweet's ID for retrieval the right data to TweetInfo frame 

        w = event.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        no_digits = string.printable[10:]
        trans = str.maketrans(no_digits, " "*len(no_digits))
        idholder.setidkey(value.translate(trans).split()[0])
        
    
    def updatePage(self):   #Update the frame when a new key appears

        if self.key != keyholder.getkey():
            self.listbox.destroy()
            self.scrollbar.destroy()
            self.key = keyholder.getkey()
            self.data = "tweets/" + self.suffix[self.key]

            self.df = pd.read_csv(self.data)
            self.IDs = self.df["id"].tolist()
            self.tweet = self.df["original_text"].tolist()
           
            photo = Image.open(self.tweetimage[self.key])
            photo = photo.resize((700,400),Image.BICUBIC)
            photo = ImageTk.PhotoImage(photo)
            self.img.photo_ref = photo
            self.img.config(image = photo)

            self.listbox = tk.Listbox(self, width=112)
            self.listbox.pack(side="left", fill="y", pady=30)

            self.optionlist = [str(self.IDs[i]) + str("    ")+ str(deEmojify(self.tweet[i])) for i in range(len(self.IDs))] 
            self.scrollbar = tk.Scrollbar(self, orient="vertical")
            self.scrollbar.config(command=self.listbox.yview)
            self.scrollbar.pack(side="left", fill="y", pady=30)

            self.listbox.config(yscrollcommand=self.scrollbar.set)

            for item in self.optionlist:

                self.listbox.insert(tk.END, str(item))
        
        self.listbox.bind('<<ListboxSelect>>', self.onselect)
        self.after(10, self.updatePage)

class TweetInfo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        self.key = keyholder.getkey()
        self.idkey = idholder.getidkey()

        self.namelist = ["@JennyENicholson", "@9_volt_", "@FoldableHuman", "@marinscos", "@YingjueChen"]
        self.suffix = ["jennyenicholson.csv","9volt.csv","foldablehuman.csv","marinscos.csv","yingjuechen.csv"]
        self.folders = ["jennyenicholson","9volt","foldablehuman","marinscos","yingjuechen"]
        self.data = ""

        self.label = tk.Label(self, text = "Tweet Info", font = ("Helvetica", 16))
        self.label.pack(pady= 10, padx= 10)

        self.tweetbox = tk.Text(self, height=5, width=120)
        self.tweetbox.pack(pady= 10, padx= 10) 

        self.image = Image.open('images/happy.png')
        self.image = self.image.resize((100,100),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img2 = tk.Label(self, image=self.render)
        self.img2.image = self.render
        self.img2.pack(pady= 10, side= "top", anchor= "n")

        self.sentimentlabel = tk.Label(self, text = "Tweet's Sentiment Status: ", font = ("Helvetica", 12))
        self.sentimentlabel.pack(pady= 10, padx= 10) 

        self.button = tk.Button(self, text= "Back", command = lambda:controller.show_frame(Tweetmenu))
        self.button.pack(padx= 100, pady= 100, side="bottom")

        values = [0,0,0,0,0]

        createRadarPGN(values)

        self.image = Image.open('images/radar.png')
        self.image = self.image.resize((500,370),Image.BICUBIC)
        self.render = ImageTk.PhotoImage(self.image)
        self.img = tk.Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side= "bottom", pady= 50, anchor= "s")

        self.plotname = tk.Label(self, text= "Personality Scores", font = ("Helvetica", 12))
        self.plotname.pack(pady = 10, side= "bottom", anchor= "s")

        self.updatePage()
    
    def updatePage(self): #Update the frame when a new key appears

        if self.idkey != idholder.getidkey():
            self.key = keyholder.getkey()
            self.idkey = idholder.getidkey()

            self.data =  "tweets/" + self.suffix[self.key]
            self.timestamp, self.tw, self.sentiment = getTweetData(self.idkey, self.data)

            self.tweetbox.destroy()

            self.tweetbox = tk.Text(self, height=5, width=120)
            self.tweetbox.pack(pady= 10, padx= 10) 
            self.tweetbox.insert(tk.END, str(deEmojify(self.tw)))
            self.sentimentlabel["text"] = "Tweet's Sentiment Status: " + str('{0:.5g}'.format(self.sentiment))

            if self.sentiment > 0:
                photo = Image.open("images/happy.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            if self.sentiment < 0:
                photo = Image.open("images/sad.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            if self.sentiment == 0:
                photo = Image.open("images/neutral.png")
                photo = photo.resize((100,100),Image.BICUBIC)
                photo = ImageTk.PhotoImage(photo)
                self.img2.photo_ref = photo

            self.img2.config(image = photo)

            textfile = "Final_values/Individual_tweets/" + self.folders[self.key] + "/" + str(idholder.getidkey())  + ".txt"

            values = []
            with open(textfile) as mytxt:
                for line in mytxt:
                    newline = line.rstrip("").split(",")
                    for i in range(len(newline)):
                        values.append(float(newline[i]))

            createRadarPGN(values)
            photo = Image.open("images/radar.png")
            photo = photo.resize((500,370),Image.BICUBIC)
            photo = ImageTk.PhotoImage(photo)
            self.img.photo_ref = photo
            self.img.config(image = photo)

        self.after(10, self.updatePage)
        
class Key: #Keep safe which account is choosen

    def __init__(self, key): 
        self.key = key

    def setkey(self,num):
        self.key = num

    def getkey(self):     
        return self.key

class ID: #Keep safe which tweet is choosen
   
    def __init__(self, idkey): 
        self.idkey = idkey

    def setidkey(self,num):
        self.idkey = num

    def getidkey(self):     
        return self.idkey

def createRadarPGN(values):
    personalities =  ['Extraversion','Emotional stability','Agreeableness','Conscientiousness', 'Openness to experience']

    N = len(personalities)

    x_as = [n / float(N) * 2 * pi for n in range(N)]
    values += values[:1]
    x_as += x_as[:1]

    plt.rc('axes', linewidth=0.5, edgecolor="#888888")

    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)

    plt.xticks(x_as[:-1], [])
    plt.yticks([1, 2, 3, 4, 5, 6, 7], ["1", "2", "3", "4", "5", "6", "7"])

    ax.plot(x_as, values, linewidth=0, linestyle='solid', zorder=3)
    ax.fill(x_as, values, 'b', alpha=0.3)

    plt.ylim(1, 7)

    for i in range(N):
        angle_rad = i / float(N) * 2 * pi

        if angle_rad == 0:
            ha, distance_ax = "center", 1
        elif 0 < angle_rad < pi:
            ha, distance_ax = "left", 0
        elif angle_rad == pi:
            ha, distance_ax = "center", 1
        else:
            ha, distance_ax = "right", 0

        ax.text(angle_rad, 7 + distance_ax, personalities[i], size=8, horizontalalignment=ha, verticalalignment="center")

    plt.savefig('images/radar.png')
    plt.close()

keyholder = Key(7)
idholder = ID(0)
app = GUI()
app.mainloop()
