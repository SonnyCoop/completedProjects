from tkinter import *
from tkinter import ttk
import tkinter as tkr
import os.path
import sqlite3
global conn

BASE_DIR = os.path.dirname(os.path.abspath('/Users/davidpayne/Desktop/rowing record.db'))
db_path = os.path.join(BASE_DIR, "rowing record.db")
conn = sqlite3.connect(db_path) ##finds database to be called up in rest of program

##finds the distance covered
def dis(meters, timing): 
##    try:
    erg_total = 0
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() ##opens database
    for row in cursor.execute("select * from record"):
        erg_total += int(row[3])
    erg_total = erg_total%50000
    print(str(erg_total)+"egg")
    dis_meters = meters-erg_total
    if dis_meters < 0: ##incase erg runs over 50000m and refreshes
        dis_meters = meters + (50000-erg_total)
        erg_total = meters
    else:
        erg_total += dis_meters
##    except:
##        dis_meters = meters ##if it is the first result in the table
##        erg_total = meters
##        total = meters
    split(dis_meters, timing) ##calls the split function
    return dis_meters ##returns distance covered in that sitting

##called from dis
##calculates the split for that sitting    
def split(covered, timing):
    global split2 ##split is global and so has no return needed
    split_distance = covered/500
    split2 = convert(timing,split_distance) ##calls convert to continue function -- could probably be one function or a class if more efficiency is required

##called from convert
##turns the strings of different times into seconds
def convert2(timing):
    seconds = 0
    
    if timing == "5mins":
        seconds = 5*60
    if timing == "10mins":
        seconds = 10*60
    if timing == "15mins":
        seconds = 15*60
    if timing == "20mins":
        seconds = 20*60
    if timing == "30mins":
        seconds = 30*60
    if timing == "45mins":
        seconds = 45*60
    if timing == "1 hour":
        seconds = 60*60
    if timing == "2 hours":
        seconds = 60*60*2
    if timing == "150mins":
        seconds = 60*150
    else:
        print("shit") ##if you get this it is not good
    return seconds

##continuation of split
##converts time into minutes and seconds
def convert(timing, split_distance):
    secs = convert2(timing) ##calls convert2 function
    secs = int(secs)
    secs = secs/split_distance
    secs = secs % (24*3600)
    secs%= 3600
    minutes = secs//60
    secs%=60
    return "%02d:%02d" % (minutes,secs)

##finds time in hours minutes and seconds from the seconds inputted
def convert3(seconds):
    global hour
    hour = (seconds // 3600)
    print("hour is {}".format(hour))
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60 
    return "%d:%02d:%02d" % (hour, minutes, seconds)

##what happens when the add button is pressed
def add():
    global names
    global Q
    x = name.get() ##gets names
    try:
        names.append(x)
    except:
        names = []
        names.append(x) ## adds names to a list
    name.delete(0,END)
    name.focus_set()
    label.config(text = names) ## adds the names to the little box below
    print(names)
    try:
        Q += 1
    except:
        Q = 1

##what happens when the submit button is pressed
def submit():
    global choice
    global choice2
    global count_er
    global control
    global days
    try: ##open database find recent then add 1
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor() ##opens database
        for row in cursor.execute("select * from record order by ID desc limit 1"):
            theOne = row[0]
        print(theOne)
        count_er = int(theOne) + 1
    except:
        count_er = 1 ##counter shows what entry it is 
    timing = time.get() ##gets time from the time box
    meters = int(distance.get()) ##gets distance from distance box
    distance.delete(0,END)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() ##opens database
    try:
        for row in cursor.execute("select * from record order by ID desc limit 1"):
            theTwo = row[1]
        name = names[0]
        print(name)
        if name == theTwo:
            name = names[1]
    except:
        name = names[0] ##finds the name of the person who will row
    covered = dis(meters,timing) ##calls dis function -- finds distance for that sitting
    myRec = []
    myRec.append(count_er)
    myRec.append(name)
    myRec.append(timing)
    myRec.append(covered)
    myRec.append(split2)
    cursor.execute("insert into record values (?,?,?,?,?)", myRec)
    conn.commit() ##adds the turn, name, time, distance and split into database

    choice2 = 1
    for row in cursor.execute("select * from record order by ID desc limit 10"):
        Label(frame_entry, text=row[0], relief=RIDGE,width=10).grid(row=choice2,column=1) 
        Label(frame_entry, text=row[1], relief=RIDGE,width=10).grid(row=choice2,column=2) 
        Label(frame_entry, text=row[2], relief=RIDGE,width=10).grid(row=choice2,column=3) 
        Label(frame_entry, text=row[3], relief=RIDGE,width=10).grid(row=choice2,column=4)
        Label(frame_entry, text=row[4], relief=RIDGE,width=10).grid(row=choice2,column=5)
        ##finds data from database and adds to the GUI
        choice2 += 1
    i = 0
    x = 0
    q = 1
    while x == 0: ##finding rows for the GUI
        if name == names[i]:
            y = 6 + q
            x = 1
        else:
            i += 1
            q += 1
    ##working out the total times
    times = 0
    for row in cursor.execute("select * from record where Name = '{}'".format(name)):
        add = convert2(row[2])
        times += add ##finds time for that name
    ratio = times
    times = convert3(times) ##puts the time into hours, mins and seconds
    Label(frame_entry, text= times, relief=SUNKEN,width=15).grid(row=1,column=y)
    total_times = 0
    for i in cursor.execute("select * from record"):
        yes = convert2(i[2])
        total_times += yes ##gets total time
    print("add is {}".format(total_times))
    ratio = round(ratio/total_times *100,1)
    ratio2 = round(100-ratio,1)
    ratio = str(ratio)+"%"
    ratio2 = str(ratio2)+"%" ##finds the ratios of the time
    if y+1 == 8:
        q = 8
    else:
        q = 7
    Label(frame_entry, text= ratio, relief=SUNKEN,width=15).grid(row=3,column=y)
    Label(frame_entry, text= ratio2, relief=SUNKEN,width=15).grid(row=3,column=q)
    total_times = convert3(total_times)

    days = hour//24 ##has a day count increaces every 24 hours of rowing
    Label(frame_entry,text="Num of days: {}".format(days), font =('Arial', 24))\
                               .grid(row=5,column=7, padx=10, pady =5, columnspan=2,rowspan=2)
    ##working out the total distance
    meters = 0
    for row in cursor.execute("select * from record where Name = '{}'".format(name)):
        meters += int(row[3])
    meters = str(meters)+"m" ##meters for that name
    Label(frame_entry, text= meters, relief=SUNKEN,width=15).grid(row=2,column=y)
    total_distance = 0
    for i in cursor.execute("select * from record"):
        total_distance += int(i[3])
    total_distance = str(total_distance)+"m" ##total distance
    y = len(names) + 7
    Label(frame_entry, text= total_times, relief=SUNKEN,width=15).grid(row=1,column=y)
    Label(frame_entry, text= total_distance, relief=SUNKEN,width=15).grid(row=2,column=y)
    
##what happens when the start button is pressed (setting up frame for main GUI)
def start():
    global time
    global distance
    global frame_entry
    root.destroy()
    ##setting up dimentions of first page
    window = Tk()
    window.geometry("1300x600")
    window.title("rowing record")
    window.resizable(False,False)
    window.configure(background = "Light Blue")

    ##setting up frames
    frame_heading = Frame(window)
    frame_heading.grid(row=0, column=0, columnspan=2,padx = 30,pady = 5)
    frame_entry = Frame(window)
    frame_entry.grid(row=2, column=0, columnspan=2,padx = 25, pady = 10)
    ##title
    Label(frame_heading,text="Rowing Record",
          font=('Arial',20))\
          .grid(row=0,column=0, padx=0, pady=5, sticky = W)
    ##time and new distance boxes
    Label(frame_entry,text="Time:")\
                               .grid(row=0,column=0, padx=10, pady = 5, sticky = W)
    time = ttk.Combobox(frame_entry, text="5mins",
                     font=('Arial', 11))
    time.grid(row=1, column=0, padx = 10,pady=5, sticky = W)
    time.config(values=("5mins","10mins","15mins","20mins","30mins","45mins","1 hour","2 hours","150mins"))
    Label(frame_entry,text="Distance:")\
                               .grid(row=2,column=0, padx=10, pady = 5, sticky = W)
    distance = Entry(frame_entry, width = 15, bg = "white")
    distance.grid(row=4, column=0, padx = 10,pady=5, sticky = W)
    ##buttons
    submit_button = Button(window,text="Submit",width=7,
                              command=submit)
    submit_button.grid(row= 4, column=0, padx = 10,pady=5, sticky = E)
    ##table headings
    Label(frame_entry, text="Number", relief=SUNKEN,width=10).grid(row=0,column=1) 
    Label(frame_entry, text="Name", relief=SUNKEN,width=10).grid(row=0,column=2) 
    Label(frame_entry, text="Time", relief=SUNKEN,width=10).grid(row=0,column=3) 
    Label(frame_entry, text="Distance", relief=SUNKEN,width=10).grid(row=0,column=4) 
    Label(frame_entry, text="Split", relief=SUNKEN,width=10).grid(row=0,column=5)

    ##totals headings
    x = 7
    try:
        for i in range(10):
            Label(frame_entry, text= names[i], relief=SUNKEN,width=15).grid(row=0,column=x)
            x += 1
    except:
        Label(frame_entry, text= "Total", relief=SUNKEN,width=15).grid(row=0,column=x)
    Label(frame_entry, text= "Time", relief=SUNKEN,width=15).grid(row=1,column=6)
    Label(frame_entry, text= "Distance", relief=SUNKEN,width=15).grid(row=2,column=6)
    Label(frame_entry, text= "Percentage", relief=SUNKEN,width=15).grid(row=3,column=6)
    window.mainloop()
 
        
        

##setting up dimentions of first page
root = Tk()
root.geometry("320x200")
root.title("rowing record")
root.resizable(False,False)
root.configure(background = "Light Blue")
##setting up frames
frame_heading = Frame(root)
frame_heading.grid(row=0, column=0, columnspan=2,padx = 30,pady = 5)
frame_entry = Frame(root)
frame_entry.grid(row=2, column=0, columnspan=2,padx = 25, pady = 10)
##title
Label(frame_heading,text="Competitors",
      font=('Arial',20))\
      .grid(row=0,column=0, padx=0, pady=5)
##number of people
Label(frame_entry,text="Enter Name:")\
                               .grid(row=0,column=0, padx=10, pady = 5)
name = Entry(frame_entry, width = 15, bg = "white")
name.grid(row=0, column=1, padx = 5,pady=5)
##name area
label = Label(root, text = "names")
label.grid(row=3,column = 0, columnspan = 2)
##buttons
enter_button = Button(root,text="Enter",width=7,
                          command=add)
enter_button.grid(row= 4, column=0, padx = 0,pady=5)
start_button = Button(root,text="Start",width=7,
                          command=start)
start_button.grid(row= 4, column=1, padx = 0,pady=5)
root.mainloop()
conn.close()



##Linked functions
##dis -> split <- convert <- convert2

##Errors present in the at this moment
## - when more than 2 people are present in the challenge not all data displayed


