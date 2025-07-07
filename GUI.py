import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from macro import AutoClicker
import pyautogui
from random import randint
import pynput
import threading
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Interface:
    def __init__(self):
        
        # -- SETTINGS FOR INTERFACE --
        self.window = ctk.CTk()
        self.window.geometry("625x575")
        self.window.title("Oink Macro")
        self.window.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(resource_path("themes/rime.json"))
        self.window.bind_all("<Button-1>", self.handleClick)

        bgImage = CTkImage(light_image=Image.open(resource_path("assets/backgroundImage.jpg")), size=(625, 575))
        bgLabel = ctk.CTkLabel(self.window, image=bgImage, text="")
        bgLabel.place(relx=0, rely=0, anchor="nw")
        self.pickPopup = None

         # --- CREATES THE AUTO CLICKER ---
        self.autoClicker = AutoClicker()
        self.hotkey = None
        self.hotkeyListener = None

        # --- TEXT VARIABLES ---
        self.intervalText = ctk.IntVar(value=0)
        self.hoursText = ctk.StringVar(value="0")
        self.minutesText = ctk.StringVar(value="0")
        self.secondsText = ctk.StringVar(value="1")
        self.millisecondsText = ctk.StringVar(value="0")
        self.randomSecondsText = ctk.StringVar(value="0")
        self.randomSecondsText2 = ctk.StringVar(value="5")
        self.positionText = ctk.IntVar(value=0)
        self.positionXText = ctk.StringVar(value="0")
        self.positionYText = ctk.StringVar(value="0")
        self.repeatOptionText = ctk.IntVar(value=0)
        self.repeatText = ctk.StringVar(value="1")
        self.mouseButtonText = ctk.StringVar(value="Left")
        self.clickTypeText = ctk.StringVar(value="Single Click")

        # --- STORE OLD ENTRY VALUES USED TO RESTORE ENTRIES WHEN INVALID ---
        self.entryValues = {"hoursText": self.hoursText.get(), "minutesText": self.minutesText.get(), "secondsText": self.secondsText.get(), "millisecondsText": self.millisecondsText.get(), "randomSecondsText": self.randomSecondsText.get(), "randomSecondsText2": self.randomSecondsText2.get(), "positionXText": self.positionXText.get(), "positionYText": self.positionYText.get(), "repeatText": self.repeatText.get()}

        # --- VALIDATE COMMANDS ---
        self.validateEntryCommand = (self.window.register(self.validateEntry), '%P', '%W')
        self.validateRandom1EntryCommand = (self.window.register(self.validateRandom1Entry), '%P')
        self.validateRandom2EntryCommand = (self.window.register(self.validateRandom2Entry), '%P')
        self.validatePositionXEntryCommand = (self.window.register(self.validatePositionXEntry), '%P')
        self.validatePositionYEntryCommand = (self.window.register(self.validatePositionYEntry), '%P')

        # --- INTERVAL HEADER ---
        headerFrame = ctk.CTkFrame(self.window, height=45, fg_color="#9989B6", width=545, corner_radius=8, border_width=0, background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        headerFrame.place(relx=0.5, rely=0.075, anchor="center")
        intervalIcon = CTkImage(light_image=Image.open(resource_path("assets/timeIntervalIcon.png")), size=(24, 24))
        ctk.CTkLabel(headerFrame, text=" Click Interval", image=intervalIcon, compound="left", text_color="white", font=("Courier New", 15, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # --- INTERVAL BODY ---
        intervalFrame = ctk.CTkFrame(self.window, height=120, width=545, border_width=2, border_color="#C7C3D4", corner_radius=0, fg_color="#d6cdde", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        intervalFrame.place(relx=0.5, rely=0.2075, anchor="center")

        # SPECIFIED INTERVAL RADIO BUTTON
        specifiedRadio = ctk.CTkRadioButton(intervalFrame, text="Specified Interval", font=("Courier New", 14, "bold"), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.intervalText, value=0)
        specifiedRadio.place(relx=0.05, rely=0.25, anchor="w")

        # RANDOM INTERVAL RADIO BUTTON
        randomRadio = ctk.CTkRadioButton(intervalFrame, text="Random Interval", font=("Courier New", 14, "bold"), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.intervalText, value=1)
        randomRadio.place(relx=0.65, rely=0.25, anchor="w")

        # INITIALIZE VARIABLES INSIDE OF INTERVAL FRAME
        entryWidth = 50
        entryRelY = 0.6
        labelRelY = 0.83
        spacing = 0.13
        labelAbsX= 0.125
        randomAbsX = 0.725

        # HOURS
        self.hoursEntry = ctk.CTkEntry(intervalFrame, textvariable=self.hoursText, placeholder_text="0", width=entryWidth, validate="focusout", validatecommand=self.validateEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.hoursEntry.place(relx=labelAbsX, rely=entryRelY, anchor="center")
        self.hoursEntry.bind("<FocusOut>", self.entryFocusOut)
        self.hoursEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Hours", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=labelAbsX, rely=labelRelY, anchor="center")
        
        # MINUTES
        self.minutesEntry = ctk.CTkEntry(intervalFrame, textvariable=self.minutesText, placeholder_text="0", width=entryWidth, validate="focusout", validatecommand=self.validateEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.minutesEntry.place(relx=labelAbsX+spacing, rely=entryRelY, anchor="center")
        self.minutesEntry.bind("<FocusOut>", self.entryFocusOut)
        self.minutesEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Mins", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=labelAbsX+spacing, rely=labelRelY, anchor="center")
       
        # SECONDS
        self.secondsEntry = ctk.CTkEntry(intervalFrame, textvariable=self.secondsText, placeholder_text="1", width=entryWidth, validate="focusout", validatecommand=self.validateEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.secondsEntry.place(relx=labelAbsX+2*spacing, rely=entryRelY, anchor="center")
        self.secondsEntry.bind("<FocusOut>", self.entryFocusOut)
        self.secondsEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Secs", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=labelAbsX+2*spacing, rely=labelRelY, anchor="center")
        
        # MILLISECONDS
        self.millisecondsEntry = ctk.CTkEntry(intervalFrame, textvariable=self.millisecondsText, placeholder_text="0", width=entryWidth, validate="focusout", validatecommand=self.validateEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.millisecondsEntry.place(relx=labelAbsX+3*spacing, rely=entryRelY, anchor="center")
        self.millisecondsEntry.bind("<FocusOut>", self.entryFocusOut)
        self.millisecondsEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Millis", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=labelAbsX+3*spacing, rely=labelRelY, anchor="center")

        # RANDOM INTERVAL
        self.randomEntryBox1 = ctk.CTkEntry(intervalFrame, textvariable=self.randomSecondsText, placeholder_text="0", width=entryWidth, validate="focusout", validatecommand=self.validateRandom1EntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.randomEntryBox1.place(relx=randomAbsX, rely=entryRelY, anchor="center")
        self.randomEntryBox1.bind("<FocusOut>", self.randomEntry1FocusOut)
        self.randomEntryBox1.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Secs", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=randomAbsX, rely=labelRelY, anchor="center")
        self.randomEntryBox2 = ctk.CTkEntry(intervalFrame, textvariable=self.randomSecondsText2, placeholder_text="5", width=entryWidth, validate="focusout", validatecommand=self.validateRandom2EntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.randomEntryBox2.place(relx=randomAbsX+0.12, rely=entryRelY, anchor="center")
        self.randomEntryBox2.bind("<FocusOut>", self.randomEntry2FocusOut)
        self.randomEntryBox2.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(intervalFrame, text="Secs", text_color="#585858", font=("Courier New", 13), fg_color="transparent").place(relx=randomAbsX+0.12, rely=labelRelY, anchor="center")

        # --- POSITION HEADER ---
        positionHeaderFrame = ctk.CTkFrame(self.window, height=45, fg_color="#9989B6", width=545, corner_radius=8, border_width=0, background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        positionHeaderFrame.place(relx=0.5, rely=0.37, anchor="center")
        positionIcon = CTkImage(light_image=Image.open(resource_path("assets/positionIcon.png")), size=(24, 24))
        ctk.CTkLabel(positionHeaderFrame, text=" Click Position", image=positionIcon, compound="left", text_color="white", font=("Courier New", 15, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # --- POSITION BODY---
        positionFrame = ctk.CTkFrame(self.window, height=40, width=545, border_width=2, border_color="#C7C3D4", corner_radius=0, fg_color="#d6cdde", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        positionFrame.place(relx=0.5, rely=0.4325, anchor="center")

        # FOLLOW MOUSE RADIO BUTTON
        followRadio = ctk.CTkRadioButton(positionFrame, text="Follow Mouse", font=("Courier New", 14), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.positionText, value=0)
        followRadio.place(relx=0.045, rely=0.5, anchor="w")

        # COORDINATE RADIO BUTTON
        coordinateRadio = ctk.CTkRadioButton(positionFrame, text="", font=("Courier New", 14), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.positionText, value=1)
        coordinateRadio.place(relx=0.33, rely=0.5, anchor="w")
        ctk.CTkLabel(positionFrame, text="X:", text_color="#858585", font=("Courier New", 14)).place(relx=0.39, rely=0.5, anchor="w")
        self.positionXEntry = ctk.CTkEntry(positionFrame, width=50, height=22, textvariable=self.positionXText, validate="focusout", validatecommand=self.validatePositionXEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.positionXEntry.place(relx=0.44, rely=0.5, anchor="w")
        self.positionXEntry.bind("<FocusOut>", self.positionXFocusOut)
        self.positionXEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(positionFrame, text="Y:", text_color="#858585", font=("Courier New", 13)).place(relx=0.55, rely=0.5, anchor="w")
        self.positionYEntry = ctk.CTkEntry(positionFrame, width=50, height=22, textvariable=self.positionYText, validate="focusout", validatecommand=self.validatePositionYEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.positionYEntry.place(relx=0.6, rely=0.5, anchor="w")
        self.positionYEntry.bind("<FocusOut>", self.positionYFocusOut)
        self.positionYEntry.bind("<Key>", self.validateKeyPress)

        # PICK COORDINATES BUTTON
        ctk.CTkButton(positionFrame, text="Pick", width=60, font=("Courier New", 14), fg_color="#9989B6", text_color="white", hover_color="#C7C3D4", command=self.pickPosition).place(relx=0.775, rely=0.5, anchor="w")

        # INITIALIZE VARIABLES INSIDE OF OPTIONS FRAME
        optionsRelX = 0.5 - (545/(2*625))
        optionsRelY = 0.485
        optionsFrameWidth = 260
        optionsFrameHeight = 160

        # --- OPTIONS HEADER---
        optionsHeader = ctk.CTkFrame(self.window, height=45, fg_color="#9989B6", width=optionsFrameWidth, corner_radius=8, border_width=0, background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        optionsHeader.place(relx=optionsRelX, rely=optionsRelY, anchor="nw")
        optionsIcon = CTkImage(light_image=Image.open(resource_path("assets/mouseOptionsIcon.png")), size=(24, 24))
        ctk.CTkLabel(optionsHeader, text=" Click Options", image=optionsIcon, compound="left", text_color="white", font=("Courier New", 15, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        
        # --- OPTIONS BODY ---
        optionsFrame = ctk.CTkFrame(self.window, height=optionsFrameHeight, width=optionsFrameWidth, border_width=2, border_color="#C7C3D4", corner_radius=0, fg_color="#d6cdde", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        optionsFrame.place(relx=optionsRelX, rely=optionsRelY+0.0695, anchor="nw")

        # MOUSE BUTTON TYPE OPTIONS
        ctk.CTkLabel(optionsFrame, text="Mouse Button", text_color="#858585", font=("Courier New", 14, "bold")).place(relx=0.08, y=10, anchor="nw")
        mouse_button = ctk.CTkSegmentedButton(optionsFrame, values=["Left", "Middle", "Right"], variable=self.mouseButtonText, width=200, font=("Courier New", 14), unselected_color="#9989B6", fg_color="#9989B6", selected_color='#C7C3D4', selected_hover_color='#C7C3D4', unselected_hover_color='#9989B6')
        mouse_button.place(relx=0.08, y=40, anchor="nw")

        # CLICK TYPE OPTIONS
        ctk.CTkLabel(optionsFrame, text="Click Type", text_color="#858585", font=("Courier New", 14, "bold")).place(relx=0.08, y=80, anchor="nw")
        click_type = ctk.CTkSegmentedButton(optionsFrame, values=["Single Click", "Double Click"], variable=self.clickTypeText, width=150, font=("Courier New", 14), unselected_color="#9989B6", fg_color="#9989B6", selected_color='#C7C3D4', selected_hover_color='#C7C3D4', unselected_hover_color='#9989B6')
        click_type.place(relx=0.08, y=110, anchor="nw")

        # INITIALIZE VARIABLES INSIDE OF REPEAT FRAME
        repeatRelX = 0.52  
        repeatRelY = optionsRelY

        # --- REPEAT HEADER ---
        repeatHeader = ctk.CTkFrame(self.window, height=45, fg_color="#9989B6", width=optionsFrameWidth, corner_radius=8, border_width=0, background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        repeatHeader.place(relx=repeatRelX, rely=repeatRelY, anchor="nw")
        repeatIcon = CTkImage(light_image=Image.open(resource_path("assets/repeatIcon.png")), size=(24, 24))
        ctk.CTkLabel(repeatHeader, text=" Click Repeat", image=repeatIcon, compound="left", text_color="white", font=("Courier New", 15, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        
        # --- REPEAT BODY ---
        repeatFrame = ctk.CTkFrame(self.window, height=optionsFrameHeight, width=optionsFrameWidth, border_width=2, border_color="#C7C3D4", corner_radius=0, fg_color="#d6cdde", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'])
        repeatFrame.place(relx=repeatRelX, rely=repeatRelY+0.0695, anchor="nw")

        # REPEAT RADIO BUTTON
        repeatRadio = ctk.CTkRadioButton(repeatFrame, text="Repeat", font=("Courier New", 14), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.repeatOptionText, value=0)
        repeatRadio.place(relx=0.08, rely=0.25, anchor="w")
        self.repeatEntry = ctk.CTkEntry(repeatFrame, width=80, textvariable=self.repeatText, validate="focusout", validatecommand=self.validateEntryCommand, border_color="#DDDDDD", font=("Courier New", 13))
        self.repeatEntry.place(relx=0.4, rely=0.25, anchor="w")
        self.repeatEntry.bind("<FocusOut>", self.entryFocusOut)
        self.repeatEntry.bind("<Key>", self.validateKeyPress)
        ctk.CTkLabel(repeatFrame, text="times", text_color="#858585", font=("Courier New", 14)).place(relx=0.77, rely=0.25, anchor="w")

        # INFINITE REPEAT RADIO BUTTON
        infinityRadio = ctk.CTkRadioButton(repeatFrame, text="Infinite until Stopped", font=("Courier New", 14), text_color="#858585", fg_color="#9989B6", hover_color="#858585", variable=self.repeatOptionText, value=1)
        infinityRadio.place(relx=0.08, rely=0.65, anchor="w")

        # --- BOTTOM BUTTONS FRAME ---
        bottomFrame = ctk.CTkFrame(self.window, fg_color="#d6cdde", width=545, height=60, background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'], border_width=0, border_color="#d6cdde")
        bottomFrame.pack(side="bottom", pady=20)
        bottomFrame.place(relx=0.5, rely=0.96, anchor="s")

        buttonWidth = int(545 / 3) - 10

        self.startButton = ctk.CTkButton(bottomFrame, text="Start", width=buttonWidth, height=45, font=("Courier New", 16, "bold"), fg_color="#9989B6", hover_color="#C7C3D4", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'], command=self.startClicker)
        self.startButton.pack(side="left", padx=(0, 5), pady=5, fill="both", expand=True)

        self.hotkeyButton = ctk.CTkButton(bottomFrame, text="Set Hotkey", width=buttonWidth, height=45, font=("Courier New", 16, "bold"), fg_color="#9989B6", hover_color="#C7C3D4", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'], command=self.setHotkey)
        self.hotkeyButton.pack(side="left", padx=(5, 0), pady=5, fill="both", expand=True)

        self.stopButton = ctk.CTkButton(bottomFrame, text="Stop", width=buttonWidth, height=45, font=("Courier New", 16, "bold"), fg_color="#9989B6", hover_color="#C7C3D4", background_corner_colors=['#d6cdde', '#d6cdde', '#d6cdde', '#d6cdde'], border_width=0, command=self.autoClicker.stop)
        self.stopButton.pack(side="left", padx=5, pady=5, fill="both", expand=True)


    # --- START CLICKER FUNCTION ---
    def startClicker(self):
        self.autoClicker = AutoClicker()

        if self.intervalText.get() == 0:
            interval = self.timeToSeconds()
        else:
            interval = randint(int(self.randomSecondsText.get()), int(self.randomSecondsText2.get()))

        if self.positionText.get() == 0:
            positionType = "Follow Mouse"
            position = None
        else:
            positionType = "Fixed"
            position = (int(self.positionXText.get()), int(self.positionYText.get()))
        
        if self.repeatOptionText.get() == 0:
            repeatType = "Finite"
            repeatCount = int(self.repeatText.get())
        else:
            repeatType = "Infinite"
            repeatCount = 0
        
        if self.clickTypeText.get() == 0:
            clickType = "Single"
        else:
            clickType = "Double"
        
        if not self.autoClicker.started:
            self.autoClicker.start(interval=interval, positionType=positionType, repeatType=repeatType, repeatCount=repeatCount, clickType=clickType, position=position, button=self.mouseButtonText.get())

    # --- SET HOTKEY FUNCTION ---
    def setHotkey(self):
        if self.hotkeyListener:
            self.hotkeyListener.stop()

        self.hotkeyButton.configure(text="Press any key...")
        self.window.bind("<Key>", self.setHotkeyPress)
    

    def setHotkeyPress(self, event):
        self.hotkey = pynput.keyboard.KeyCode.from_char(event.char)
        self.hotkeyButton.configure(text=f"Hotkey: {self.keycodeToString(self.hotkey)}")
        self.window.unbind("<Key>")
    
    # --- TOGGLE AUTO CLICKER BASED ON HOTKEY FUNCTION ---
    def onHotkeyPress(self, key):
        if key == self.hotkey:
            if self.autoClicker.clicking:
                self.autoClicker.stop()
            else:
                self.startClicker()
    
    # --- HANDLE CLICK FUNCTION ---
    def handleClick(self, event):
        try:
            if hasattr(event.widget, 'focus_set'):
                event.widget.focus_set()
        except:
            pass
    
    # --- PICK POSITION FUNCTION ---
    def pickPosition(self):
        width, height = pyautogui.size()
        self.pickPopup = ctk.CTkToplevel(self.window)
        self.pickPopup.geometry(f"{width}x{height}")
        self.pickPopup.resizable(False, False)
        self.pickPopup.attributes("-alpha", 0.5)
        self.pickPopup.bind("<Button-1>", self.setLocation)
        self.window.withdraw()
    
    # --- SET LOCATION FUNCTION ---
    def setLocation(self, event):
        self.positionXText.set(event.x)
        self.positionYText.set(event.y)
        self.pickPopup.destroy()
        self.pickPopup = None
        self.window.deiconify()
    
    # --- CONVERT PYNPUT KEYCODE OBJECT TO STRING FUNCTION ---
    def keycodeToString(self, key):
        if hasattr(key, 'char') and key.char:
            return key.char
        elif hasattr(key, 'name'):
            return key.name
        else:
            return str(key).replace("'", "")

    # --- VALIDATE FUNCTION FOR MOST ENTRIES ---
    def validateEntry(self, value, name):
        if value.isdigit() and int(value) >= 0:
            if name == ".!ctkframe2.!ctkentry.!entry":
                self.entryValues["hoursText"] = value
            elif name == ".!ctkframe2.!ctkentry2.!entry":
                self.entryValues["minutesText"] = value
            elif name == ".!ctkframe2.!ctkentry3.!entry":
                self.entryValues["secondsText"] = value
            elif name == ".!ctkframe2.!ctkentry4.!entry":
                self.entryValues["millisecondsText"] = value
            else:
                self.entryValues["repeatText"] = value
            return True
        return False

    # --- FOCUS OUT FUNCTION TO REVERT ENTRY TO OLD VALUE ---
    def entryFocusOut(self, event):
        if (event.widget.cget("textvariable")) == "PY_VAR1":
            self.hoursText.set(self.entryValues["hoursText"])
        elif (event.widget.cget("textvariable")) == "PY_VAR2":
            self.minutesText.set(self.entryValues["minutesText"])
        elif (event.widget.cget("textvariable")) == "PY_VAR3":
            self.secondsText.set(self.entryValues["secondsText"])
        elif (event.widget.cget("textvariable")) == "PY_VAR4":
            self.millisecondsText.set(self.entryValues["millisecondsText"])
        else:
            self.repeatText.set(self.entryValues["repeatText"])
    
    # --- VALIDATE KEY PRESS FUNCTION ---
    def validateKeyPress(self, event):
        allowed_keys = ['BackSpace', 'Delete', 'Return', 'Left', 'Right', 'Up', 'Down']
        
        if event.keysym in allowed_keys:
            if event.keysym == "Return":
                self.window.focus_set()
            return
        
        if event.char and event.char.isdigit():
            return
        
        self.window.after(100, lambda: self.window.focus_set())
        return "break"

    
    # --- VALIDATE FUNCTION FOR RANDOM INTERVAL ENTRY 1 ---
    def validateRandom1Entry(self, value):
        if value.isdigit() and int(value) >= 0:
            if int(value) < int(self.randomSecondsText2.get()):
                self.entryValues["randomSecondsText"] = value
                return True
        return False

    # --- FOCUS OUT FUNCTION TO REVERT RANDOM ENTRY 1 TO OLD VALUE ---
    def randomEntry1FocusOut(self, event):
        value = self.entryValues["randomSecondsText"]
        self.randomSecondsText.set(value)
    
    # --- VALIDATE FUNCTION FOR RANDOM INTERVAL ENTRY 2---
    def validateRandom2Entry(self, value):
        if value.isdigit() and int(value) >= 0:
            if int(value) > int(self.randomSecondsText.get()):
                self.entryValues["randomSecondsText2"] = value
                return True
        return False
    
    # --- FOCUS OUT FUNCTION TO REVERT RANDOM ENTRY 2 TO OLD VALUE ---
    def randomEntry2FocusOut(self, event):
        value = self.entryValues["randomSecondsText2"]
        self.randomSecondsText2.set(value)

    # --- VALIDATE FUNCTION FOR X POSITION COORDINATE ENTRY ---
    def validatePositionXEntry(self, value):
        screenWidth, screenHeight = pyautogui.size()
        if value.isdigit() and int(value) >= 0:
            if int(value) <= screenWidth-1:
                self.entryValues["positionXText"] = value
                return True
        return False
    
    # --- FOCUS OUT FUNCTION TO REVERT X POSITION COORDINATE ENTRY TO OLD VALUE ---
    def positionXFocusOut(self, event):
        value = self.entryValues["positionXText"]
        self.positionXText.set(value)
    
    # --- VALIDATE FUNCTION FOR Y POSITION COORDINATE ENTRY ---
    def validatePositionYEntry(self, value):
        screenWidth, screenHeight = pyautogui.size()
        if value.isdigit() and int(value) >= 0:
            if int(value) <= screenHeight-1:
                self.entryValues["positionYText"] = value
                return True
        return False
    
    # --- FOCUS OUT FUNCTION TO REVERT Y POSITION COORDINATE ENTRY TO OLD VALUE ---
    def positionYFocusOut(self, event):
        value = self.entryValues["positionYText"]
        self.positionYText.set(value)

    # --- TIME FUNCTION TO CONVERT TIME TO SECONDS ---
    def timeToSeconds(self):
        return int(self.hoursText.get()) * 3600 + int(self.minutesText.get()) * 60 + int(self.secondsText.get()) + int(self.millisecondsText.get()) / 1000


if __name__ == "__main__":
    gui = Interface()
    hotkeyListener = pynput.keyboard.Listener(on_press=gui.onHotkeyPress)
    threading.Thread(target=hotkeyListener.start, daemon=True).start()
    gui.window.mainloop()

"""
CREDITS:
- <a target="_blank" href="https://icons8.com/icon/OoEj25UTztmI/session-timeout">Session Timeout</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/113264/location-off">Location Off</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/TVppPfbzSk3y/select-cursor">Select Cursor</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/83216/synchronize">Repeat</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
"""
