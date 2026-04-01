import tkinter as tk
from tkinter import ttk
import threading  
import pyautogui
import pynput
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

mouse = Controller()

class MyGui():

    

    def __init__(self):
        self.go = False
        self.delay = .1

        self.root = tk.Tk()
        self.root.title("Nates Auto")
        self.root.geometry("600x400")

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        self.printFlag = tk.BooleanVar(value=False)
            
        self.lab = ttk.Label(self.root, text="Nate's Auto Clicker")
        self.lab.pack(padx=20,pady=20)
        
        self.instruc = tk.Text(self.root, height=3, width=30)
        self.instruc.insert(tk.END, "[ is used to end program\n] is used to start or stop\nBox below is used for new time")
        self.instruc.pack()

        self.numval = ttk.Entry(self.root)
        self.numval.pack()

        self.buttonfram = ttk.Frame(self.root)
        self.but1 = ttk.Button(self.buttonfram, text="Change Time", command=self.change)
        self.but1.grid(row=0,column=0)
        self.but3 = ttk.Button(self.buttonfram, text="Start", command=self.swap)
        self.but3.grid(row=1,column=0)
        self.but2 = ttk.Button(self.buttonfram, text="End Program", command=self.root.destroy)
        self.but2.grid(row=2,column=0)
        self.buttonfram.pack(padx=0, pady=0)

        

        self.root.mainloop()

    def change(self):
        try:
           new = self.numval.get()
           self.delay = float(new)
           print(f'new delay of {self.delay}')
        except:
          print("bad delay")

    def on_press(self, key):
        if key == KeyCode.from_char(']'):
          self.swap()
        if key == KeyCode.from_char('['):
          self.root.destroy()

    def swap(self):
        self.go = not self.go
        if self.go:
            threading.Thread(target=self.worker, daemon=True).start()
        else:
            print("off")

    def worker(self):
        try:
            while(self.go):
                mouse.click(Button.left)
                time.sleep(self.delay)
        except KeyboardInterrupt:
            print("ended")

MyGui()