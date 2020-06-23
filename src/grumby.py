from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import simpleaudio as sa
import os
import keyboard
import random
import mouse

activated_sound = sa.WaveObject.from_wave_file("../audio/activated.wav")
deactivated_sound = sa.WaveObject.from_wave_file("../audio/deactivated.wav")

# Used to simply modify the bool and change background
def toggle_grumby():
    global is_on, sound_ChkBtn_state, background_label, style, activated_sound, deactivated_sound
    is_on = not is_on
    if is_on:
        if not sound_ChkBtn_state.get():
            try:
                activated_sound.play()
            except Exception as e:
                messagebox.showerror("Get Grian",f"There was an issue playing happy Grumby noises. Muting Grumby should hide this error.\n\n{str(e)}")
        change_background("activated")
    else:
        if not sound_ChkBtn_state.get():
            try:
                deactivated_sound.play()
            except Exception as e:
                messagebox.showerror("Get Grian",f"There was an issue playing sad Grumby noises. Muting Grumby should hide this error.\n\n{str(e)}")
        change_background("deactivated")

# Save the mute state of Grumby
def save_grumby_state():
    global hoteky, randmin, randmax, sound_ChkBtn_state
    _sound_ChkBtn_state = "True" if sound_ChkBtn_state else "False"
    saveFile = open('../config/hotkey.txt', "w")
    saveFile.write(f"{hotkey}\n{randmin}\n{randmax}\n{str(_sound_ChkBtn_state)}")
    saveFile.close()

# If grumby is actuive and this function is called by mouse click, then this function will press a key between the selected range of keys
def press_random_num_key():
    global is_on, randmin, randmax
    if is_on:
        randKey = str(random.randrange(randmin,randmax+1))
        keyboard.write(randKey)

# Change background function called by other functions
def change_background(background_type):
    global background_label, style
    if background_type == "activated":
        background = PhotoImage(file = "../images/activated.png")
        style.configure('W.TButton', background="#009933", foreground="white", font=('Source Code Pro', 11))
        style.configure('TCheckbutton', background="#009933", foreground="white", font=('Source Code Pro', 11))
        style.configure('TCombobox', background="white", foreground="black", font=('Source Code Pro', 11))
        style.configure('TFrame',background ="#009933", foreground="white")
        style.configure('TLabel', background="#009933", foreground="white", font=('Source Code Pro', 11))
    else:
        if background_type == "deactivated":
            background = PhotoImage(file = "../images/deactivated.png")
        elif background_type == "recording":
            background = PhotoImage(file = "../images/recording.png")
        style.configure('W.TButton', background="black", foreground="white", font=('Source Code Pro', 11))
        style.configure('TCheckbutton', background="black", foreground="white", font=('Source Code Pro', 11))
        style.configure('TCombobox', background="white", foreground="black", font=('Source Code Pro', 11))
        style.configure('TFrame',background ="black", foreground="white")
        style.configure('TLabel', background="black", foreground="white", font=('Source Code Pro', 11))
    try:
        background_label.configure(image=background)
    except:
        background_label = Label(window, image=background)
    background_label.image = background

# This function is called by the "change hotkey" button. This manages changeing the background, disables grumby, and parses recorded keys so that they can be input to the keyboard library
def toggle_record_new_hotkey():
    global window, recording, hotkey, keyboard_recording, new_hotkey_btn, show_hotkey, toggle_hotkey, is_on
    is_on = False
    # If grumby is in recoring mode
    if recording:
        recording = False
        keyboard_recording = keyboard.stop_recording()
        new_hotkey_btn['text'] = "Change Hotkey"
        change_background("deactivated")
        modifiers = []
        # The keyboard library records all keys pressed while grumby is in recording mode
        # This loop parses for any modifier keys that have been pressed (excluding the windows key)
        # As well as the last char charachter pressed. All other key presses are disguarded.
        for keypress in keyboard_recording:
            for modifier in keypress.modifiers:
                if modifier not in (modifiers):
                    modifiers.append(modifier)
            if keypress.name not in ('shift','ctrl','alt', 'windows', 'esc', 'unknown'):
                pressed_key = keypress.name
        if len(modifiers) > 0:
            new_hotkey = "+".join(modifiers) + "+" + pressed_key
        else:
            # If no keypresses were entered while grumby was in recording mode
            try:
                new_hotkey = pressed_key
            except:
                pass
        keyboard_recording = None
        # If the pressed keys were valid then modify the hotkey an ui, else reset to previously set hotkey
        try:
            toggle_hotkey = keyboard.add_hotkey(new_hotkey, toggle_grumby)
            hotkey = new_hotkey
            new_show_hotkey_text = f"Toggle Grumby with '{hotkey}'"
            if len(new_show_hotkey_text) < 30:
                show_hotkey['text'] = new_show_hotkey_text
            else:
                show_hotkey['text'] = f"Toggle Grumby with\n'{hotkey}'"
        except:
            messagebox.showinfo("*Wiggles Mustache*", "No keypresses were recorded.\nNo changes were made.\n\nPress multiple keys at the same time. For example: 'ctrl+shift+m' or 'alt+a'")
            toggle_hotkey = keyboard.add_hotkey(hotkey, toggle_grumby)
        save_grumby_state()
    # If grumby is not in recording mode, then change ui and start recording
    else:
        recording = True
        keyboard.remove_hotkey(toggle_hotkey)
        new_hotkey_btn['text'] = "Press To Stop"
        change_background("recording")
        keyboard.start_recording()

# Update the global randmax variable for what range of keys are to be pressed by grumby
# As well If the Random Max is set to be less than the random min, random min will be set to be random max -1
def change_randmax(event):
    global randmin, randmax
    view_randmin = int(randmin_combo.get())
    view_randmax = int(randmax_combo.get())
    if view_randmax <= view_randmin:
        view_randmin = view_randmax-1
        randmin_combo.set(view_randmin)
    randmax = view_randmax
    randmin = view_randmin
    save_grumby_state()

# Same as change_randmax but for randmin
def change_randmin(event):
    global randmin, randmax
    view_randmin = int(randmin_combo.get())
    view_randmax = int(randmax_combo.get())
    if view_randmax <= view_randmin:
        view_randmax = view_randmin+1
        randmax_combo.set(view_randmax)
    randmax = view_randmax
    randmin = view_randmin
    save_grumby_state()

# Initialize some variables and read from the config file.
is_on = False
recording = False
saveFile = open('../config/hotkey.txt','r')
hotkey, randmin, randmax, muteGrumby = saveFile.read().splitlines()
saveFile.close()

# Validate the config file. If there is an error, then reset all to default.
try:
    randmin = int(randmin)
    randmax = int(randmax)
    toggle_hotkey = keyboard.add_hotkey(hotkey, toggle_grumby)
except:
    messagebox.showerror("MOYORAL RESERVOIR ERROR", "There was an error loading settings. All settings were reset to default")
    saveFile = open('../config/hotkey.txt', "w")
    saveFile.write("ctrl+g\n1\n9\nFalse")
    saveFile.close()
    toggle_hotkey = keyboard.add_hotkey(hotkey, toggle_grumby)

# Calls the press_random_num_key function for every mouse click. The function does nothing if Grumby is deactivated, but it is called every mouse click if grumby is open
mouse.on_click(press_random_num_key)


########## - Create the GUI - ##########
# Create window
window = Tk()
window.title("Grumby v0.1")
window.geometry('407x308')
window.resizable(width=False, height=False)

# Set the default background
style = Style()
change_background("deactivated")

# Create the frame used in the settings
mainFrame = Frame(window)
hotkeyFrame = Frame(mainFrame, style='TFrame')
randFrame = Frame(mainFrame, style='TFrame')
settingsFrame = Frame(mainFrame, style='TFrame')

# Create and organize the hotkeyFrame (Shows hotkey and gives record new buttton)
show_hotkey = Label(hotkeyFrame, text=f"Toggle Grumby with '{hotkey}'", style="TLabel", justify="center")
show_hotkey.grid(column=0, row=0)

#Create and organize the randFrame
randmin_txt = Label(randFrame, text="Random min:", font=("Source Code Pro", 12))
randmin_combo = Combobox(randFrame,values=(1,2,3,4,5,6,7,8), width =2, state="readonly")
randmin_combo.set(randmin)
randmin_combo.bind("<<ComboboxSelected>>", change_randmin)
randmax_txt = Label(randFrame, text=" Random max:", font=("Source Code Pro", 12))
randmax_combo = Combobox(randFrame,values=(2,3,4,5,6,7,8,9), width=2, state="readonly")
randmax_combo.set(randmax)
randmax_combo.bind("<<ComboboxSelected>>", change_randmax)

randmin_txt.grid(column=0, row=0)
randmin_combo.grid(column=1, row=0)
randmax_txt.grid(column=2, row=0)
randmax_combo.grid(column=3, row=0)

# Create and organize settings frame (change hotkey button and toggle sound)
# These next 3 lines create a special object fro the check button, because it does not accept simple bool values
sound_ChkBtn_state = BooleanVar()
muteGrumby = True if muteGrumby == "True" else False
sound_ChkBtn_state.set(muteGrumby)

new_hotkey_btn = Button(settingsFrame, text="Change Hotkey", style='W.TButton', command=toggle_record_new_hotkey)
sound_ChkBtn = Checkbutton(settingsFrame, text="Mute Grumby", style='TCheckbutton', variable=sound_ChkBtn_state, onvalue=True, offvalue=False, command=save_grumby_state)

new_hotkey_btn.grid(column=0, row=1, padx=(5,5))
sound_ChkBtn.grid(column=1, row=1)

# Add the frames to the screen
hotkeyFrame.grid(column=0, row=0, pady=(5,5))
randFrame.grid(column=0, row=1, pady=(5,5))
settingsFrame.grid(column=0, row=2, pady=(5,5))
background_label.grid(column=0,row=0)
mainFrame.grid(column=0,row=0)

# Display the Grumby window
window.mainloop()