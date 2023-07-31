#Name: Bhavya Patel id: 731654
"""
Description:
A program that displays math flashcards, ranging from a variety of difficulties.
It uses Tkinter to display a graphical user interface with many different
features.

Enhancements:
    - Negative Numbers
    - Division operator
    - Log of previous questions, answers and the user answer. 
    - Two different modes, timed and progress (also referred to as quantified mode).
    
"""
#***Import libraries***
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import *
import threading #Used to run the stopwatch on a different thread. 
import time
import random

#***Global Variables***
#There are a large number of global variables because many different functions
#need to access the same variables. 

#Counts 
count_right = 0
count_wrong = 0
total_questions = 0

#Initialize max_range to 3 if the user does not pick an option. 
max_range = 3 

#Initialize both equation and user answers
equation = ""
answer = 0

#Variable used to store the number of questions in the Progress Mode
int_question = 0

#Initialized mode to standard (endless amount of questions)
mode = "Standard"

#Variable used to store the total amounts of seconds on the timer
temp = 1

#Seconds and minutes are displayed to the user
second = 0
minute = 0

#Message answer
message_answer = "UNKNOWN"

#Variable used to stop timer/stopwatch when the options menu is open
callback = True

#***Define Functions***

#*Switching/Changing Frames*
#A function that changes the frame from the title to the notebook containing the 
#rest of the frames.
    #Inputs: None
    #Returns: None
def switch_to_notebook():
    tab_control.pack(expand = 1, fill = "both")
    #Forget removes the frame from view. 
    #Source: https://www.youtube.com/watch?v=e6ktaqlXaec
    title_frame.forget()
    #Expand the window for the main program
    main_window.geometry("1024x550")

#A function that switches to the options page from the notebook.
    #Inputs: None
    #Returns: None
def switch_to_options():
    global callback
    callback = False #Changes callback to false, which pauses the timers. 
    title_frame.pack(fill = "both", expand = 1)
    tab_control.pack_forget()
    main_window.geometry("500x650")

#A function that channges back to the title frame from the mode frame.
    #Inputs: None
    #Returns: None
def change_to_title():
    title_frame.pack(fill = "both", expand = 1)
    mode_frame.forget()
    #Change window size back to the default options screen
    main_window.geometry("500x650")

#A function that reuses the title page as an options page by switching the main
#title and configuring the button.
    #Inputs: None
    #Returns: None
def configure_options_page():
    main_title.configure(text = "Options Menu")
    #Changes the start now button so that it does not reset the counts. This 
    #is to improve the user experience, as they can continue where they left 
    #off.
    start_now_btn.configure(command = options_start)

#A function that changes the frame to the mode menu. For the Game Mode Button.
    #Inputs: None
    #Returns: None
def switch_to_mode():
    mode_frame.pack(fill = "both", expand = 1)
    title_frame.forget()
    #Reduce the size of the main window
    main_window.geometry("500x400")

#*Hiding specific widgets*
#A function designed to hide the timed mode selection. 
#Source: https://www.geeksforgeeks.org/how-to-hide-recover-and-delete-tkinter-widgets/
    #Inputs: None
    #Returns: None 
def hide_timed():
    global temp, second, minute
    temp = 0
    second = 1
    minute = 0

    #Grid_forget method removes the widget from the screen. 
    timed_lbl.grid_forget()
    min_entry.grid_forget()
    sec_entry.grid_forget()
    timer_label.grid_forget()

#A function that hides the quantified mode selection and widgets on the home screen.
    #Inputs: None
    #Returns: None
def hide_quantified():
    global second, minute
    reset_counts()
    questions_entry.grid_forget()
    num_of_questions_lbl.grid_forget()
    quantified_bar.grid_forget()
    stopwatch_label.grid_forget()

#A function that disables the reset buttons during timed or progress mode, to see
#the true capabilities of the user. 
    #Inputs: None
    #Returns: None
def hide_standard():
    reset_log.configure(state = DISABLED)
    reset_count_button.configure(state = DISABLED)
    
#*Deleting/Resetting Inputs*
#A function that clears the time selection when the user inputs invalid input.
    #Inputs: None
    #Returns: None
def clear_time():
    min_entry.delete(0, END)
    sec_entry.delete(0, END)
    mins.set("00")
    secs.set("01")

#A function that changes the global second and minute variables. 
    #Inputs: None
    #Returns: None
def reset_time():
    global second, minute
    second = 0
    minute = 0

#A function that clears the quantified selection when the user inputs invalid input.
    #Inputs: None
    #Returns: None
def clear_quantified():
    questions_entry.delete(0, END)
    questions.set(1)  

#A function that clears the counts. 
    #Inputs: None
    #Returns: None
def reset_counts():
    global count_right, count_wrong, total_questions, message_answer
    message_answer = "UNKNOWN"
    count_right = 0
    count_wrong = 0
    total_questions = 0
    configure_count_label(count_right, count_wrong, total_questions,\
        message_answer)

#A function that clears the entire log. If there are no entries, then it will
#display an error box. 
    #Inputs: None
    #Returns: None
#Source: https://stackoverflow.com/questions/27966626/how-to-clear-delete-the-contents-of-a-tkinter-text-widget
def delete_log():
    try:
        log.configure(state = NORMAL)
        log.delete(1.0, END)
        log.configure(state = DISABLED)
    
    except:
        messagebox.showerror("NOT ENOUGH ENTRIES", "Unable to delete entries.")

#A function that destroys the main window, which stops the game.
    #Inputs: None
    #Returns: None
def end_code():
    main_window.destroy()

#*Configuring Labels*
#A function that configures the count labels.
    #Inputs: Count of right, wrong and total questions.
    #Returns: None
def configure_count_label(count_right, count_wrong, total_questions, message_answer):
    last_answer.configure(text = message_answer)
    num_total_question.configure(text = total_questions)
    num_count_right.configure(text = count_right)
    num_count_wrong.configure(text = count_wrong)

    #Changes the colour based on if the user's answer was right or wrong.
    if message_answer == "Correct!":
        last_answer.configure(fg = "green")
    elif message_answer == "Incorrect!":
        last_answer.configure(fg = "red")
    else:
        last_answer.configure(fg = "white")
    
#A function that adds to the different counts based on user answer.
    #Inputs: User answer
    #Returns: None
def add_to_count(user_answer):
    global total_questions, count_right, count_wrong, answer, message_answer

    #Add one to the total questions each time
    total_questions += 1

    #If the answer equals the user's answer, add one to the counter. 
    if answer == user_answer:
        count_right += 1
    else:
        count_wrong += 1

    #Updates the count labels.
    configure_count_label(count_right, count_wrong, total_questions, message_answer)

#A function that places widgets on the home frame for Progress Mode
    #Inputs: None
    #Outputs: None
def quantified_widgets():
    #Progress Bar 
    quantified_bar.grid(row = 7, column = 0, columnspan = 4)
    quantified_bar["value"] = 0 #Reset value of the quantified bar
    stopwatch_label.grid(row = 1, column = 0)

#A function that places the timer label for the Timed Mode
    #Inputs: None
    #Outputs: None
def time_widgets():
    timer_label.grid(row = 1, column = 0)

#A function that resets the states of the reset buttons to normal again. 
    #Inputs: None
    #Returns: None
def standard_widgets():
    global mode
    #Place button
    reset_log.configure(state = NORMAL)
    reset_count_button.configure(state = NORMAL)
    reset_time()

#A function that adds to the progress bar.
    #Inputs: None
    #Returns: None
def add_to_progress_bar():
    global total_questions, int_question

    #Value added to progress bar each time (based on the number of questions)
    amount_added = 100/int_question

    #If the progress bar is less than 100, an increment will be added.
    if quantified_bar["value"] <= 100:
        quantified_bar["value"] += amount_added

        #When the bar is greater than or equal to 100, multiple functions will 
        #be performed
        if quantified_bar["value"] >= 100:
            time_end() #Create and display a message box
            selected_mode.set("Standard") #Set mode to standard
            update_mode() #Calls update mode function to remove other widgets.
            reset_counts() #Resets counts
            standard_widgets()#Enable Reset Buttons

#**Processing Functions**
#A function that updates the global max range value based on the selected level 
#from the radio buttons.
    #Inputs: None
    #Returns: None
def level_selection():
    global max_range
    #Since a value cannot be returned to a button, the value is added to a 
    #global variable named max_range 
    max_range = selected.get()

#A function that uses the global max range to generate two random numbers and an
#operator. It then updates the global equation and answer variables.
    #Inputs: None
    #Returns: None
def obtain_values():
    global answer, max_range, equation
    #Obtain displayed numbers
    num_1 = random.randint(1,max_range)
    num_2 = random.randint(1,max_range)
    #Obtain random operator
    #Note: X is used as the multiplication sign because that is what will be 
    #displayed
    operator = random.choice(["+","-","x", "/"])

    #If the user selects negative number, there is a 50% chance that the 
    #generated numbers are negative or positive.
    if isNegative.get() == True:
        num_1 *= random.choice([-1, 1])
        num_2 *= random.choice([-1, 1])

    #Obtain answer using randomly generated operator
    if operator == "+":
        answer = num_1 + num_2
    elif operator == "-":
        answer = num_1 - num_2
    elif operator == "x":
        answer = num_1 * num_2
    elif operator == "/":
        #In this case, num_1 is the product of the two random numbers, to prevent
        #the answer from being a float.
        num_1 *= num_2
        #Integer division to return an integer.
        answer = num_1//num_2

    #Create the displayed equation
    equation = str(num_1) + " " + operator + " " + str(num_2) + " =" 

    #Change the label to the new equation
    equation_label.configure(text = equation)

#A function that adds an entry to the scrolled text log. 
    #Inputs: User answer
    #Returns: None
def add_to_log(user_answer):
    global answer, equation, message_answer

    #Updates the value of message answer based on if it is correct or incorrect.
    message_answer = "Incorrect!"
    if user_answer == answer:
        message_answer = "Correct!"
    
    #Concatenate the different segments to form a cohesive log entry.
    log_entry = equation + " " + str(answer) + ". Your answer was: " \
        + str(user_answer) + ". " + message_answer +"\n\n"

    #Prevents user input in the log
    #Source: https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-
    #the-tkinter-text-widget-read-only
    log.configure(state= NORMAL)
    log.insert(INSERT, log_entry)
    log.configure(state=DISABLED) #Switches back to disabled right after entering
    #the eqaution.

#A function that runs a stopwatch. Source: https://copyassignment.com/stopwatch-using-python-tkinter/
#*Note: This source uses object oriented python but I used the same 
#mechanics without it.
    #Inputs: None
    #Returns: None
def stopwatch():
    global second, minute, callback
    running = True #A check that will turn false once the user is in the title
    #frame, exiting the loop and thus, killing the entire thread. When 
    #the start button is pressed again, a new thread is created, which calls
    #on the same minute and second variables. 

    #Continues running while the progress bar is less than 100, and the 
    #running check is true. 
    while quantified_bar["value"] < 100 and running:
        #If the second is == to 59, it will change second back to 0. This will
        #make it so the user never sees 60 seconds (as there is a 1 second delay)
        if second == 59:
            second = 0
            minute += 1

        #Add 1 second each iteration of the loop
        second += 1
        main_window.update() #Update the window
        change_time_label(second, minute) #Configure the time label
        time.sleep(1) #Delays the execution of the code for one second

        #Determines if the user is in the options using global callback.
        if not callback:
            running = False
     
#A function that runs a stopwatch.
#Source: https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/
    #Inputs: None
    #OutputS: None
def timer():
    global temp, second, minute, callback
    running = True #Extra check similar to stopwatch function

    #Continues decreasing the temp (amount of seconds) till it is 0 and while
    # the running check is True. 
    while temp > -1 and running:
        #Returns the quotient and the remainder (splits the minutes and the seconds)
        minute, second = divmod(temp, 60)
        time.sleep(1) #Delays the execution of the program for one second.
        main_window.update() #Update the main window
        change_time_label(second, minute) #Configure time label
        temp -= 1 #Subtract 1 from the number of seconds each iteration

        #Performs a check to exit out of the timer loop.
        if not callback:
           running = False

        if temp == 0:
            time_end()
            selected_mode.set("Standard") #Preselect standard mode
            update_mode() #Updates the widgets for the standard window
            #Clears the previous inputted time on the mode frame.
            clear_time()
            reset_counts() #Reset counts
            standard_widgets()

#A function that configures the message box after the game mode is completed.
    #Inputs: None
    #Outputs: None
def time_end():
    message_title, message_body = configure_message_box()
    messagebox.showinfo(message_title, message_body)

#A function that displays a different message in the message box using the 
#information from each mode. For the progress mode, it displays the number of 
#questions and the time it took. It also displays the number of right and wrong
#answers. For timed mode, it displays the number of questions answered in 
#the allocated time, as well as the number correct and incorrect.
    #Inputs: None
    #Returns: Message title and message body for the message box in time_end function.
def configure_message_box():
    global mode, total_questions, count_right, count_wrong, minute, second
    message_title = mode + " mode completed!"
    message_body = ""
    if mode == "Progress":
        message_body += "You completed " + str(total_questions) \
            + " questions in " + str(minute) + " min and  " + str(second) + " seconds.\n"
        message_body += "Number correct : " + str(count_right) + "\n"
        message_body += "Number wrong : " + str(count_wrong) 

    elif mode == "Timed":
        message_body += "You completed " + str(total_questions) \
            + " questions in the time you set for yourself.\n"
        message_body += "Number correct : " + str(count_right) + "\n"
        message_body += "Number wrong : " + str(count_wrong) 

    return message_title, message_body

#A function that starts the stopwatch in another thread. 
    #Inputs: None
    #Returns: None
def stopwatch_thread():
    #Threading essentially runs this command on a different part of the processor.
    #If it is not used,
    #the delay for the stopwatch function will apply to the
    #Entire program, making it appear laggy.
    #Args is a keyword used for a variable number of paremeters, but in this case,
    #no parameters are needed (args is still required however)
    stopwatch_threading = threading.Thread(target = stopwatch, args = [])

    #Starts the thread
    stopwatch_threading.start()

#A function that starts the stopwatch in another thread.
    #Inputs: None
    #Outputs: None
def timer_thread():
    timer_threading = threading.Thread(target = timer, args = [])
    #Starts the thread
    timer_threading.start()

#A function that configures the labels for either the stopwatch or timer label
    #Inputs: Seconds and Minutes
    #Outputs: None
def change_time_label(secs, mins):
    global mode
    #Adds a 0 if the number of seconds and minutes is less than 10, 
    #to keep a consistent length (polished finish)
    if secs < 10:
        secs = "0" + str(secs)
    
    if mins < 10:
        mins = "0" + str(mins)
    
    #Concatonates, t
    time = str(mins) + " : " + str(secs)

    #Changes either the stopwatch label or the timer label based on the mode.
    if mode == "Progress":
        stopwatch_label.configure(text = time)
    
    else:
        timer_label.configure(text = time)

#**Button Functions**
#A function that displays a message box containing the game description. For the 
#Game Description button.
    #Inputs: None
    #Returns: None
def display_description():
    #Indenting the other lines will cause tabs in the final message.
    description = "Test your math arithmetic skills in a fun, engaging way! \
Essentially, the program will output two randomly generated integers and an \
operator. Your job is to type the correct answer to the expression.\
 To get started, choose a level difficulty, which will change the max possible \
value. In addition, change the modes and options to suit your preferences."

    #display messagebox
    messagebox.showinfo("Game Description", description)

#A function that displays a message box containing the range for each level and
#how the negative number option works. for the Levels and Options button.
    #Inputs: None
    #Returns: None
def display_levels_and_options():
    description = "There are four levels to choose from. The range for the \
generated numbers in each level is as follows:\n- Level 1: 0-3\n- Level 2: 0-6 \
\n- Level 3: 0-9\n- Level 4: 0-12\nEnabling negative numbers means that there \
is a 50% chance that the generated number is negative."

    #display messagebox
    messagebox.showinfo("Levels and Negative Numbers", description)


#A function that displays different entry actions when mode is selected. For the
#Save Changes Button
    #Inputs: None
    #Outputs: None
def update_mode():
    global mode #Allow the mode variable to be used by the confirm button
    mode = selected_mode.get()

    if mode == "Timed":
        #Hide the other widgets for different modes
        hide_quantified()
        hide_standard()
        #Grid each label.
        timed_lbl.grid(row = 3, column = 0, columnspan = 4, pady=(20,5))
        min_entry.grid(row = 5, column = 1)
        sec_entry.grid(row = 5, column = 2)

    elif mode == "Progress":
        #Hide the other widgets for different modes
        hide_timed()
        hide_standard()
        #Grid each label.
        num_of_questions_lbl.grid(row = 3, column = 0, columnspan = 4, \
            rowspan = 2, pady = (20, 5))
        questions_entry.grid(row = 5, column = 1, columnspan = 2)
        questions_entry.focus()

    else:
        hide_timed()
        hide_quantified()

#A function that saves the level, obtains the random integers and operator, 
#and switches to the home frame. For the Start Now button. 
    #Inputs: None
    #Outputs: None
def start_now():
    global mode #Uses global mode variable to determine which thread is used.

    #Obtains selected level and generates the random integers and operators. It
    #then switches to the notebook, and changes the options page. 
    level_selection()
    obtain_values()
    switch_to_notebook()
    configure_options_page()

    #Reset counts and time
    reset_counts() 
    reset_time()

    #Starts a different thread based on the mode. 
    if mode == "Progress":
        stopwatch_thread()

    elif mode == "Timed":
        timer_thread()

#A function that configures the start_now button to perform the same functions
# except resetting the counts. 
    #Inputs: None
    #Returns: None
def options_start():
    global callback 
    level_selection()
    obtain_values()
    switch_to_notebook()
    callback = True #Will switch callback back to True to enable the timer/stopwatch once
    #again.

    #Starts the thread based on the mode. The global minute or second variables
    #are not updated, which means that the timer/stopwatch will stay at the same
    #time they were left at.
    if mode == "Progress":
        stopwatch_thread()

    elif mode == "Timed":
        timer_thread()

#A function that turns the user_answer into a string, adds an entry to the log
#and generates a new operator and set of integers. For the Confirm Answer Button
#(Home Frame)
    #Inputs: None
    #Returns: None
def obtain_answer():
    global mode
    try:
        #Obtain answer from input box and turn it into an integer.
        user_answer = int(string_answer.get())
        #Add the entry to the log
        add_to_log(user_answer)
        #Add to the count
        add_to_count(user_answer)
        #Randomly generate a new set of integers
        obtain_values()
        #Clear the user input from last time
        user_input.delete(0, END)

        #If the mode is progress, then the progress bar value will be changed.
        if mode == "Progress":
            add_to_progress_bar()
        
    except: #If there is invalid input, a message box is shown, and the 
        #current selection is deleted.
        messagebox.showerror("Error","Enter a valid integer")
        user_input.delete(0, END)


#A function that changes based on the mode selection. It takes the user input
#and turns it into usable integer data, which will then be passed to other 
#functions that show the different widgets on the home screen. For the Confirm 
#button (Mode Frame).
    #Inputs: None
    #Returns: None
def confirm_mode():
    global mode, int_question, temp
    try:
        #Perform different functions based on the mode. 
        if mode == "Timed":
            #Temp takes the user's inputted time and convert it into integers, as
            #well as converting the minutes to seconds.
            temp = int(mins.get())*60 + int(secs.get())

            #Check if the inputted time is less than 5 minutes
            if (temp <= 0) or (temp > 300):
                #Error Generator that prompts the except category if the integer
                #is notin the valid range 
                error_generator = 1 + "1"
                clear_time()
            
            #Place the time widgets
            time_widgets()

        elif mode == "Progress":
            #Converts question variable into integer.
            int_question = int(questions.get())

            #Check if the inputted question is less than 25. 
            if (int_question <= 0) or (int_question > 25):
                error_generator = 1 + "1"
                clear_quantified()
            
            quantified_widgets()
        
        elif mode == "Standard":
            standard_widgets()

        #Change to the title screen afterwards.
        change_to_title()

    except:
        #Displays an error box if an invalid integer is inputted
        messagebox.showerror("Error", "Please enter a valid integer")
        #Focus in the entry boxes
        questions_entry.focus()
        sec_entry.focus()
        #Clear the selection
        clear_quantified()
        clear_time()

#***Main Program***
#Creating main_window
main_window = Tk()
main_window.title("Math Flash Cards")
main_window.geometry("500x650")
#Icon in Window Display. Source: Lakindu

#Establish Style
style = ttk.Style()
style.theme_use("clam")

#Create Title Frame
title_frame = Frame(main_window)
title_frame.pack(fill = "both", expand = 1)
title_background = PhotoImage(file = "among_us_background.png")
title_background_label = Label(title_frame, image = title_background)
#Use place to make the background fill the entire frame.
title_background_label.place(x = 0, y = 0, relwidth= 1, relheight = 1) 

#Mode Frame
mode_frame = Frame(main_window, background = "black")
#Use PhotoImage to add an image
mode_background = PhotoImage(file = "mode_frame_background.png")
#Image is put into a label
mode_background_label = Label(mode_frame, image = mode_background)
#Use place to make the background fill the entire frame. Place essentially
#uses the relative width of the window, and can be a value from 0 - 1. 
mode_background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) 

#Create the Notebook that holds all the frames 
tab_control = ttk.Notebook(main_window)

#Create Home Frame
home_frame = Frame(tab_control, background = "black")
#Set a background
home_background = PhotoImage(file = "home_frame_background.png")
home_background_label = Label(home_frame, image = home_background)
home_background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

#Create Log Frame
log_frame = Frame(tab_control, background = "black")
#Set a background
log_background = PhotoImage(file = "log background.png")
log_background_label = Label(log_frame, image = log_background)
log_background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
tab_control.add(home_frame, text= "Home")
tab_control.add(log_frame, text = "Log")

#Count Frame 
count_frame = Frame(home_frame, highlightbackground = "red", highlightthickness = 3, \
    background = "black")
count_frame.grid(row = 1, column = 1, columnspan = 2, rowspan = 6, padx = (70, 25),\
    pady = 20)

#*Options/Title Frame Widgets*

#Title for the Initial Frame
main_title = Label(title_frame, text = "Astronaut Arithmetic", font = ("Amatic SC", \
    40), fg = "white", bg = "black")


#Grid row #1
#Padx and pady parameters can take a tuple, with information for the left and right
    #sides. Source: https://stackoverflow.com/questions/4174575/adding-padding-to-a-tkinter-widget-only-on-one-side
main_title.grid(row = 0, column = 0, columnspan = 6, padx = (10,0), pady= (20, 10))

#Name 
name = Label(title_frame, text = "Created by: Bhavya Patel 2023", \
    bg = "black", fg = "red", font = ("Amatic SC", 20))

#Grid row #2
name.grid(row = 1, column = 1, columnspan = 2, pady=(0, 10))

#Description Button
description = Button(title_frame, text = "Game Description"\
    , font = ("VCR OSD Mono", 12), command = display_description, \
        bg = "black", fg = "white", border = 3)

#Level range and negative number options information
level_and_negative = Button(title_frame, font = ("VCR OSD Mono", 12), \
        bg = "black", fg = "white", border = 3, text = "Learn More about Options",\
             command = display_levels_and_options)

#Grid row #3
description.grid(row = 2, column = 0, columnspan = 2, pady = (10, 15))
level_and_negative.grid(row = 2, column = 2, columnspan = 2)

#Level selection subtitle 
level_selector_subtitle = Label(title_frame, text = "Level Selection", \
    font= ("Amatic SC", 20), bg = "black", fg = "white")
#Radio buttons for the levels, with the value being the maximum of the
#integer range.

#Grid row #4
level_selector_subtitle.grid(row = 3, column = 0, columnspan=4, sticky= W, padx=(20,0))

selected = IntVar() #Obtains integer value of selected level button.
selected.set(3) #Preselects the level to #1
#Radio button for level. Active background parameter changes the background while
#the button is being clicked. In addition, active foreground does the same 
#with the foreground instead. 
level_1 = Radiobutton(title_frame, text = "Level 1", value = 3, \
    variable = selected, font = ("VCR OSD Mono", 11), fg = "red", bg = "black"\
        , activebackground= "black", activeforeground = "green")
level_2 = Radiobutton(title_frame, text = "Level 2", value = 6, \
    variable = selected, font = ("VCR OSD Mono", 11), fg = "red", bg = "black"\
        , activebackground= "black", activeforeground = "green")
level_3 = Radiobutton(title_frame, text = "Level 3", value = 9, \
    variable = selected, font = ("VCR OSD Mono", 11), fg = "red", bg = "black"\
        , activebackground= "black", activeforeground = "green")
level_4 = Radiobutton(title_frame, text = "Level 4", value = 12, \
    variable = selected, font = ("VCR OSD Mono", 11), fg = "red", bg = "black"\
        , activebackground= "black", activeforeground = "green")

#Grid row #5
level_1.grid(row = 4, column = 0, pady = 20)
level_2.grid(row = 4, column = 1)
level_3.grid(row = 4, column = 2)
level_4.grid(row = 4, column = 3, padx=(0,20))

#Weight essentially splits the space evenly between the specified columns, which 
#gives the radio buttons equal amounts of space (polished look)
#Source: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/grid-config.html
#:~:text=Tkinter%208.5%20reference%3A%20a%20GUI%20for%20Python&text=Unless%20you
#%20take%20certain%20measures,height%20of%20its%20tallest%20cell.
title_frame.columnconfigure((0,1,2,3), weight = 1)

#Negative number subtitle
negative_selector_subtitle = Label(title_frame, text="Enable Negative Numbers",\
    font=("Amatic SC", 20), bg = "black", fg = "white")

#Grid row #6
negative_selector_subtitle.grid(row = 5, column=0, columnspan = 4, sticky = W, \
    padx=(20,0))

#Initalize isNegative as a boolean value, which will be accessed in the 
#obtain values function. 
isNegative = BooleanVar()
isNegative.set(False) #Set the variable to false. 

#Checkbox to select negative numbers
negative_check = Checkbutton(title_frame, variable = isNegative,\
    text = "Negative Numbers", background = "black", foreground = "red",
    activebackground = "black", activeforeground = "green", font = ("VCR OSD Mono", 11))

#Grid row #7
negative_check.grid(row = 6, column = 1, columnspan = 2,  pady= 20)

#Game Mode Subtitle
game_mode_subtitle = Label(title_frame, text="Choose Your Game Mode",\
    font=("Amatic SC", 20), bg = "black", fg = "white")

#Grid row #8
game_mode_subtitle.grid(row = 7, column = 0, columnspan = 4, sticky = W, \
    padx=(20,0))

#Button that switches to the mode frame
game_mode = Button(title_frame, text = "Game Modes", command = switch_to_mode, \
     font = ("VCR OSD Mono", 12), bg = "black", fg = "white")

#Grid row #9
game_mode.grid(row = 8, column = 1, columnspan= 2, pady = 20)

#Button that switches from the title frame to the notebook. 
#Image to use on top of the start button
start_image = PhotoImage(file = "start_button.png")

#The image parameter is used to set the background of a button. 
start_now_btn = Button(title_frame, command = start_now, \
    image = start_image, bg = "black", borderwidth = 0, activebackground= "black")  
start_now_btn.grid(row = 10, column = 1, columnspan= 2)

#**Mode Frame Widgets**
#Title for the mode frame
mode_frame_title = Label(mode_frame, text = "Game Mode Menu",\
    font = ("Amatic SC", 40), fg = "white", bg = "#5f758c")

#Grid row #1
mode_frame_title.grid(row = 0, column = 1, columnspan = 2, pady= (20, 10))

#Radio Buttons to select a mode. Bg parameter can accept hexcodes
selected_mode = StringVar() #Obtains integer value of selected button.
selected_mode.set("Standard")
standard_mode = Radiobutton(mode_frame, text = "Standard", value = "Standard", \
    variable = selected_mode, font = ("VCR OSD Mono", 11), bg = "#5f758c", \
    fg = "orange", activebackground = "orange", activeforeground = "#5f758c")
timed_mode = Radiobutton(mode_frame, text = "Timed", value = "Timed", \
    variable = selected_mode, font = ("VCR OSD Mono", 11), bg = "#5f758c", \
    fg = "orange", activebackground = "orange", activeforeground = "#5f758c")
quantified_mode = Radiobutton(mode_frame, text = "Progress", value = "Progress", \
    variable = selected_mode, font = ("VCR OSD Mono", 11), bg = "#5f758c", \
    fg = "orange", activebackground = "orange", activeforeground = "#5f758c")

#This button will save the radio button choice and allow the user to perform
#actions based on the chosen mode. For example, set the clock for timed mode.
save_mode = Button(mode_frame, text = "Save Changes", command = update_mode, \
    font = ("VCR OSD Mono", 11), bg = "#5f758c", fg = "white")

#Grid row #2
standard_mode.grid(row = 2, column = 0, pady = 20)
timed_mode.grid(row = 2, column = 1)
quantified_mode.grid(row = 2, column = 2)
save_mode.grid(row = 2, column = 3)
mode_frame.columnconfigure((0,1,2,3), weight = 1)

#Initialize different entry actions based on mode. 
#*Setting the timer *
#Variables designed to take the user input in the form of a string.
mins = StringVar()
secs = StringVar()
#Set the minimum time of 1 second (Prevents user from inputting 0 seconds)
mins.set("0")
secs.set("01")
#Change the cursor colour with insert background parameter
#Source: https://stackoverflow.com/questions/14284492/how-to-change-text-cursor-color-in-tkinter
timed_lbl = Label(mode_frame,\
    text = "Enter the time you want to play for (max 5 min)", \
        font = ("Amatic SC", 20), fg = "white", bg = "#5f758c")
min_entry = Entry(mode_frame, width = 5, textvariable= mins, \
    font = ("VCR OSD Mono", 20), bg = "black", fg = "white", insertbackground = "white")
sec_entry = Entry(mode_frame, width = 5, textvariable = secs,\
    font = ("VCR OSD Mono", 20), bg = "black", fg = "white", insertbackground = "white")

sec_entry.focus()

#*Setting the Number of Questions*
#Variable designed to take the user input as a string.
questions = StringVar()
questions.set(1)
num_of_questions_lbl = Label(mode_frame,\
    text = "Enter the Number of Questions (max 25)", \
        font = ("Amatic SC", 20), fg = "white", bg = "#5f758c")
questions_entry = Entry(mode_frame, width = 10, textvariable = questions, \
    font = ("VCR OSD Mono", 20), bg = "black", fg = "white", insertbackground = "white")

#Button that will change its function based on the user choice for mode. For 
#example, displaying the clock on home screen for timed mode.
confirm_mode = Button(mode_frame, text = "Confirm", command = confirm_mode, \
    font = ("VCR OSD Mono", 11), bg = "#5f758c", fg = "white")
confirm_mode.grid(row = 6, column= 1, columnspan = 2, sticky = W+E, \
    pady = 20)

#**Home Frame Widgets**
equation_label = Label(home_frame, text = equation, font = ("VCR OSD Mono", 40), \
    bg = "black", fg = "white")
equation_label.grid(row = 0, column = 0, padx = (70, 0), pady = (40, 0))

#String_answer takes the user input as a string, which will later be converted
#into an integer
string_answer = StringVar()
#Entry for user_answer
user_input = Entry(home_frame, width= 10, textvariable = string_answer, \
    font = ("VCR OSD Mono", 30))
user_input.grid(row = 0, column= 1, padx = (25, 0), pady = (40, 0))

#Confirm answer button to submit the answer
confirm_answer = Button(home_frame, text = "Confirm Answer", \
    command = obtain_answer,  font = ("VCR OSD Mono", 20), bg = "black", fg = "white")
confirm_answer.grid(row = 0, column = 2, padx = (10, 0), pady = (40, 0))

user_input.focus()

#Count Frame Widgets
count_title = Label(count_frame, text = "Live Counter", \
    font = ("Amatic SC", 40), fg = "white", bg = "black")

#Grid row #1
count_title.grid(row = 0, column = 0, columnspan = 2)

#Shows if the last answer was correct or incorrect
last_answer_label = Label(count_frame, text = "Your last answer was ", \
    font = ("VCR OSD Mono", 15), fg = "white", bg = "black")
last_answer = Label(count_frame, text = message_answer, bg = "black", fg = "white", \
    font = ("Arial Bold", 15))

#Grid row #2
last_answer_label.grid(row = 1, column = 0)
last_answer.grid(row = 1, column = 1, padx = (0, 20))

#Total Questions count
total_questions_label = Label(count_frame, text = "Total Questions: ", \
    font = ("VCR OSD Mono", 15), fg = "white", bg = "black")
num_total_question = Label(count_frame, text = 0, bg = "black", fg = "cyan", \
    font = ("Arial Bold", 15))

#Grid row #3
total_questions_label.grid(row = 2, column = 0)
num_total_question.grid(row = 2, column = 1)

#Number of right questions
count_right_label = Label(count_frame, text = "Number of correct answers: ", \
    font = ("VCR OSD Mono", 15), fg = "white", bg = "black")
num_count_right = Label(count_frame, text = 0, bg = "black", fg = "green", \
    font = ("Arial Bold", 15))

#Grid row #4
count_right_label.grid(row = 3, column = 0)
num_count_right.grid(row = 3, column = 1)

#Number of wrong questions
count_wrong_label = Label(count_frame, text = "Number of wrong answers: ", \
    font = ("VCR OSD Mono", 15), fg = "white", bg = "black")
num_count_wrong = Label(count_frame, text = 0, bg = "black", fg = "red", \
    font = ("Arial Bold", 15))

#Grid row #5
count_wrong_label.grid(row = 4, column = 0)
num_count_wrong.grid(row = 4, column = 1)

#Reset counts button
reset_count_button = Button(count_frame, text = "Reset Counts", \
    command = reset_counts, font = ("VCR OSD Mono", 15), fg = "white", bg = "black")

#Grid row #5 
reset_count_button.grid(row = 5, column = 0, columnspan = 2, pady = 20)

#*Log Frame Widgets*
log = scrolledtext.ScrolledText(log_frame, width = 70, height = 10)
#Prevents user input in the log at the start
log.configure(state= DISABLED, font = ("VCR OSD Mono", 15))

#Grid row #1
log.grid(padx = 90, pady = (30, 0), sticky = W+E, columnspan = 2)

#Button to reset the log
reset_log = Button(log_frame, text = "Reset log", command = delete_log, \
    font = ("VCR OSD Mono", 15), fg = "white", bg = "black")

#Give each column even weight
log_frame.columnconfigure((0,1), weight = 1)

#Grid row #2
reset_log.grid(row = 1, column = 0, pady = 10, columnspan = 2)


#Grid row #3
#*Quantified Widgets*
#Initialize the quantified widgets, only placing in a grid and hiding in the 
#function. 

#Progress bar that will change after the user inputs an answer
progress_style = ttk.Style() #Create style
progress_style.theme_use("default")
style.configure("black.Horizontal.TProgressbar", background = "green")
quantified_bar = Progressbar(home_frame, length = 700, style = "black.Horizontal.TProgressbar")
stopwatch_label = Label(home_frame, text = "00 : 00", bg = "black", fg = "white", \
    font = ("VCR OSD MONO", 20))

#*Timed Widget*
timer_label = Label(home_frame, text = "00 : 00", bg = "black", fg = "white", \
    font = ("VCR OSD MONO", 20))

#Options button
options_button = Button(home_frame, text = "Options", command = switch_to_options, \
    font = ("VCR OSD MONO", 15), bg = "orange", activebackground = "black", \
        activeforeground = "orange")
options_button.grid(row = 4, column = 0, pady = (15, 0))

#Button that kills the program
end_program = Button(home_frame, text = "Exit Program", command = end_code, \
    font = ("VCR OSD MONO", 15), bg = "red", fg = "white", \
        activebackground = "white", activeforeground = "red")
end_program.grid(row = 5, column = 0)

main_window.mainloop()
