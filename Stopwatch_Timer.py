#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os, sys
import RPi.GPIO as GPIO
import time

class Stopwatch(Frame):

    def __init__(self):
        super().__init__() 
        self.initUI()
        
    def initUI(self):
        self.pos        = 1
        self.num        = 1
        self.mo         = 0
        self.run        = 0
        self.old_timer  = 0
        self.timer      = 0
        self.l_time     = 0
        self.h_time     = 0
        self.s_time     = 0
        self.up         = 1
        self.down_timer = 0
        self.Frame01 = tk.Frame(width=480, height=90)
        self.Frame01.grid_propagate(0)
        self.Frame01.grid(row=0, column=0)
        self.Frame02 = tk.Frame(width=480, height=230)
        self.Frame02.grid_propagate(0)
        self.Frame02.grid(row=1, column=0)
        self.Disp_Stopwatch = tk.Label(self.Frame01, height=1, width=11, font=("Helvetica", 57), text="00:00:00.000")
        self.Disp_Stopwatch.grid(row = 0, column = 0, sticky = W)
        self.Labels1 = []
        for pos in range(0,11):
           self.Disp_Laptime = tk.Label(self.Frame02, height=1, width=30, font=("Helvetica", 10), text="")
           self.Disp_Laptime.grid(row = pos+1, column = 4, columnspan = 7, sticky = W, padx = 10)
           self.Labels1.append(self.Disp_Laptime)
        self.Button_Start = tk.Button(self.Frame02, text = "Start", bg = "green",fg = "white",width = 8, height = 4,font = 18, command = self.Start, justify=CENTER)
        self.Button_Start.grid(row = 1, column = 0,columnspan = 2, rowspan = 4)
        self.Button_Stop = tk.Button(self.Frame02, text = "Stop",bg = "red", width = 8, height = 4,font = 18,command=self.Stop, justify=CENTER)
        self.Button_Stop.grid(row = 1, column = 2,columnspan = 2,  rowspan = 4)
        self.Button_Laptime = tk.Button(self.Frame02, text = "Laptime", fg = "black",bg = "light blue", width = 8, height = 3,font = 18,command=self.Laptime, justify=CENTER)
        self.Button_Laptime.grid(row = 5, column = 0,columnspan = 2,  rowspan = 3)
        self.Button_Exit = tk.Button(self.Frame02, text = "Exit", bg = "blue",fg = "white", width = 8, height = 3,font = 18,command=self.Exit, justify=CENTER)
        self.Button_Exit.grid(row = 5, column = 2,columnspan = 2,  rowspan = 3)
        self.Button_Hours = tk.Button(self.Frame02, text = "Hrs", bg = "yellow",fg = "black", width = 2, height = 2,font = 18,command=self.Hours, justify=CENTER,repeatdelay=1000, repeatinterval=250)
        self.Button_Hours.grid(row = 8, column = 0,  rowspan = 2)
        self.Button_Mins = tk.Button(self.Frame02, text = "Min", bg = "yellow",fg = "black", width = 2, height = 2,font = 18,command=self.Mins, justify=CENTER,repeatdelay=1000, repeatinterval=250)
        self.Button_Mins.grid(row = 8, column = 1,  rowspan = 2)
        self.Button_Secs = tk.Button(self.Frame02, text = "Sec", bg = "yellow",fg = "black", width = 2, height = 2,font = 18,command=self.Secs, justify=CENTER,repeatdelay=1000, repeatinterval=250)
        self.Button_Secs.grid(row = 8, column = 2,  rowspan = 2)
        self.Button_Clr = tk.Button(self.Frame02, text = "Clr", bg = "yellow",fg = "black", width = 2, height = 2,font = 18,command=self.Clear, justify=CENTER)
        self.Button_Clr.grid(row = 8, column = 3,  rowspan = 2)
        
        # setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.start_switch = 23  # pin 16, switch to gnd, KEY2
        self.stop_switch  = 24  # pin 18, switch to gnd, KEY3
        self.lap_switch   = 25  # pin 22, switch to gnd, KEY4
        GPIO.setup(self.start_switch,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.stop_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.lap_switch,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.Hours_switch  = 16  # pin 36, switch to gnd, 
        self.Mins_switch   = 20  # pin 38, switch to gnd, 
        self.Secs_switch   = 21  # pin 40, switch to gnd, 
        GPIO.setup(self.Hours_switch,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.Mins_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.Secs_switch,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.Check_GPIO()
        
    def Update(self):
        if self.run == 1:
            if self.up == 1:
                self.timer = time.time() - self.start
            else:
                self.timer = self.down_timer - (time.time() - self.start)
            if self.timer < 0:
                self.timer = 0
                self.Stop()
            elif self.run == 1:
                m,s  = divmod(self.timer,60)
                h,m  = divmod(m,60)
                self.msg  = "%02d:%02d:%02d" % (h,m,s) + str(self.timer - int(self.timer))[1:5]
                if self.up == 1:
                   self.Disp_Stopwatch.config(text = self.msg, fg = "black")
                else:
                   self.Disp_Stopwatch.config(text = self.msg, fg = "red")
                self.after(1, self.Update)
            
    def Check_GPIO(self):
        if GPIO.input(self.start_switch)   == 0:
            self.Start()
        elif GPIO.input(self.stop_switch)  == 0:
            self.Stop()
        elif GPIO.input(self.lap_switch)   == 0:
            self.Laptime()
        elif GPIO.input(self.Hours_switch) == 0:
            self.Hours()
        elif GPIO.input(self.Mins_switch)  == 0:
            self.Mins()
        elif GPIO.input(self.Secs_switch)  == 0:
            self.Secs()
        self.after(1, self.Check_GPIO)
        
    def Start(self):
        if self.run == 0:
            for x in range(0,11):
                self.Labels1[x].config(text = " ")
            self.start = time.time()
            if self.up == 1:
                self.old_timer = 0
            else:
                self.old_timer = self.down_timer
            self.l_time = 0
            self.s_time = 0
            self.pos    = 1
            self.num    = 1
            self.run    = 1
            self.Update()
                    
    def Stop(self):
        if self.run == 1 :
            self.s_time = time.time()
            self.run = 0
            if self.up == 0 and self.timer == 0:
                self.Disp_Stopwatch.config (text = "00:00:00.000", fg = "black")
                self.down_timer = 0
                self.up = 1
            elif self.up == 0:
                self.down_timer = 0
        elif time.time() - self.s_time > .5:
            for x in range(0,11):
                self.Labels1[x].config(text = " ")
            self.Disp_Stopwatch.config (text = "00:00:00.000", fg = "black")
            self.up         = 1
            self.down_timer = 0
            
        
    def Laptime(self):
        if self.run == 1 and time.time() - self.l_time > .2:
            self.l_time = time.time()
            if self.timer > self.old_timer:
                t = self.timer - self.old_timer
            else:
                t = self.old_timer - self.timer
            h = int(t/3600);m = int((t-(h*3600))/60);s = int((t-(h*3600)- (m*60)));p = ((t-(h*3600)- (m*60) - s))
            tmsg = "%02d:%02d:%02d" % (h,m,s)
            snum = str(self.num)
            if self.num < 10:
                snum = "0" + snum
            self.Labels1[self.pos - 1].config(text= snum + " - " + self.msg + "   " + str(tmsg) + str(p)[1:5])
            self.old_timer = self.timer
            self.pos +=1
            if self.pos > 10:
                self.pos = 1
            self.num +=1

    def Hours(self):
        if self.run == 0 and time.time() - self.h_time > .2:
            self.h_time = time.time()
            self.up = 0
            self.down_timer +=3600
            if self.down_timer > 359999:
                self.down_timer = 359999
            self.old_timer = self.down_timer
            m,s  = divmod(self.down_timer,60)
            h,m  = divmod(m,60)
            self.msg  = "%02d:%02d:%02d" % (h,m,s) + ".000"
            self.Disp_Stopwatch.config(text= self.msg, fg = "red")
            
    def Mins(self):
        if self.run == 0 and time.time() - self.h_time > .2:
            self.h_time = time.time()
            self.up = 0
            self.down_timer +=60
            if self.down_timer > 359999:
                self.down_timer = 359999
            self.old_timer = self.down_timer
            m,s  = divmod(self.down_timer,60)
            h,m  = divmod(m,60)
            self.msg  = "%02d:%02d:%02d" % (h,m,s) + ".000"
            self.Disp_Stopwatch.config(text= self.msg, fg = "red")
            
    def Secs(self):
        if self.run == 0 and time.time() - self.h_time > .2:
            self.h_time = time.time()
            self.up = 0
            self.down_timer +=1
            if self.down_timer > 359999:
                self.down_timer = 359999
            self.old_timer = self.down_timer
            m,s  = divmod(self.down_timer,60)
            h,m  = divmod(m,60)
            self.msg  = "%02d:%02d:%02d" % (h,m,s) + ".000"
            self.Disp_Stopwatch.config(text= self.msg, fg = "red")
            
    def Clear(self):
        if self.run == 0:
            self.up         = 1
            self.down_timer = 0
            self.old_timer  = 0
            m,s  = divmod(self.down_timer,60)
            h,m  = divmod(m,60)
            self.msg  = "%02d:%02d:%02d" % (h,m,s) + ".000"
            self.Disp_Stopwatch.config(text= self.msg, fg = "black")
        
    def Exit(self):
        self.master.destroy()

def main():
    root = Tk()
    root.title("Stopwatch")
    root.geometry("480x320")
    #root.wm_attributes('-fullscreen','true')
    ex = Stopwatch()
    root.mainloop() 

if __name__ == '__main__':
    main() 
