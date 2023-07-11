#!/usr/bin/env python3.10
import os
import subprocess
import tkinter as tk
from datetime import datetime as dt
from datetime import timedelta as td
import re
root = tk.Tk()
thetime = tk.StringVar()
time = tk.Entry(root, width=5, font="Times 48", textvariable=thetime, justify="center")
time.pack(padx=20,pady=20,side=tk.TOP)
instructions = tk.Label(root, text="Press return to start timer.\nClick time to pause or change.",
                        font="Times-Italic 12")
instructions.pack(side=tk.TOP)
thetime.set("15:00")

def topretty(delta):
    print(str(delta))
    return re.sub("^0:0?([0-9]+:[0-9]+)\..*$","\\1",str(delta))

def frompretty(pretty):
    tt = pretty.split(":")
    if tt == ['']: return td(seconds=0)
    if len(tt) == 1: return td(seconds=int(tt[0]))
    return td(minutes=int(tt[0]),seconds=int(tt[1]))
#    tt = list(map(int,re.sub("[^0-9 ]","",tt)))
#    if(tt==''): return 0
#    if len(tt)==1: return tt
#    return tt[0]*60 + tt[1]

def PlayBell():
    if os.path.exists("/usr/bin/afplay"):
        subprocess.run(["afplay","Bell.m4a"])
    else:
        root.bell()
        root.after(100,root.bell)
        root.after(200,root.bell)
    pass
def run():
    if run.stoptime: return
    now = dt.now()
    elapsed = now - run.begin
    if elapsed >= run.countfrom:
        thetime.set("0:00")
        run.stoptime = True
        PlayBell()
        return
    thetime.set(topretty(run.countfrom - elapsed))
    root.after(1000,run)

def startclock(e=None):
    root.focus_set()
    run.begin = dt.now()
    run.countfrom = frompretty(thetime.get())
    run.stoptime = False
    run()

def pause(e=None):
    run.stoptime = True
    time.select_from(0)
    time.select_to(tk.END)
time.bind("<FocusIn>",pause)
time.bind("<Key-Return>",startclock)

time.focus_set()
tk.mainloop()
