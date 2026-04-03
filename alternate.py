import os
import sys
import tkinter as tk
from tkinter import ttk
import threading  
import pyautogui
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

# Required for EXE to find your images
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

mouse = Controller()

class MyGui():
    def __init__(self):
        self.go = False
        self.case = False
        self.delay = .1

        self.root = tk.Tk()
        self.root.title("Nate's Auto")
        self.root.geometry("600x450")

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        self.lab = ttk.Label(self.root, text="Nate's Auto Bot", font=("Arial", 16, "bold"))
        self.lab.pack(padx=20, pady=15)
        
        self.instruc = tk.Text(self.root, height=6, width=45)
        self.instruc.insert(tk.END, "HOTKEYS:\n[ : Close Entire Program\n] : Toggle Standard Clicker\n; : Toggle Case Opener\n\nSETTINGS:\nType speed (seconds) in box then 'Change Time'")
        self.instruc.pack(pady=5)

        self.numval = ttk.Entry(self.root)
        self.numval.insert(0, "0.1")
        self.numval.pack(pady=5)

        self.buttonfram = ttk.Frame(self.root)
        ttk.Button(self.buttonfram, text="Change Time", command=self.change).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.buttonfram, text="Start/Stop (])", command=self.swap).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.buttonfram, text="Case Opener (;)", command=self.caseopen).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.buttonfram, text="EXIT ([)", command=self.root.destroy).grid(row=1, column=1, padx=5, pady=5)
        self.buttonfram.pack(pady=10)

        self.root.mainloop()

    def change(self):
        try:
            self.delay = float(self.numval.get())
            print(f'Speed set to {self.delay}s')
        except:
            print("Invalid input! Use numbers like 0.5")

    def on_press(self, key):
        if key == KeyCode.from_char(']'): self.swap()
        if key == KeyCode.from_char('['): self.root.destroy()
        if key == KeyCode.from_char(';'): self.caseopen()

    def swap(self):
        self.go = not self.go
        if self.go:
            print("Clicker: STARTED")
            threading.Thread(target=self.worker, daemon=True).start()
        else:
            print("Clicker: STOPPED")

    def caseopen(self):
        self.case = not self.case
        if self.case:
            print("Case Opener: STARTED")
            threading.Thread(target=self.caseworker, daemon=True).start()
        else:
            print("Case Opener: STOPPED")

    def caseworker(self):
        # Local paths for images
        img_open = resource_path('open.png')
        img_use = resource_path('use.png')

        while self.case:
            try:
                # Look for 'Open' button
                location = pyautogui.locateOnScreen(img_open, confidence=0.9)
                # This will throw a TypeError if location is None, 
                # jumping us straight to the 'except' block!
                x, y = pyautogui.center(location)
                pyautogui.click(x, y)
                time.sleep(0.3)

                # Look for 'Use' button
                location = pyautogui.locateOnScreen(img_use, confidence=0.9)
                x, y = pyautogui.center(location)
                pyautogui.click(x, y)
                
                # Rare animation wait time
                time.sleep(4.6)
                
                # Final click on the offset
                pyautogui.click(x, y + 30)

            except:
                # THE JUMPY THING:
                # If images aren't found, we wait a bit and 'blind click' 
                # to push through long animations or lag.
                time.sleep(0.5)
                mouse.click(Button.left)
                print("Image not found - performing blind click...")

    def worker(self):
        while self.go:
            mouse.click(Button.left)
            time.sleep(self.delay)

if __name__ == "__main__":
    MyGui()