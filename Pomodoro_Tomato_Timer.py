#Pomodoro-Tomato Timer     - by -    Dr.M-Dev
#============================================

from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#ffffff"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
####
time_min = 25
time_sec = 59 #(60sec => 1min => 1 time_min)
#
rest_min = 4
long_rest_min = 30
####
check = "✔"
check_count = 0
####
# state_of_operation:
main_count_down = False
break_time = False
restart = False
####update-v2
reactivate_signal = True #default = true

#######UPDATE-3
just_did_reset = False

############################################################################
# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer_system():
    global time_min
    global time_sec
    #
    global rest_min
    #
    global check_count
    #
    global main_count_down
    global break_time
    global restart
    ####
    global reactivate_signal #default = true
    #--------------
    #--------------
    #DEBUG
    if break_time:
        #DEBUG
        print("ACTIVE1")
        main_count_down = True
        break_time = False
        restart = False
        #--------------
        global just_did_reset
        #--------------
        time_min = 25
        time_sec = 59
        rest_min = 4
        #
        check_count = 0 #<------IMPORTANT!!!
        laps_check_marks.config(text=f"{check * check_count}", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
        ####
        reactivate_signal = False
        if not reactivate_signal:
            # DEBUG
            print("ACTIVE2")
            start_button.focus()
            break_time = False
            main_count_down = False
            ####
            tomato_canvas.itemconfig(tomato_time_text, text="00:00", fill=WHITE)
            #
            # note2:
            note2.config(text="YOU FINISHED A CYCLE! press \"Start\" to start over", fg=GREEN, bg=YELLOW,
                          font=(FONT_NAME, 9, "bold"))
            note2.place(x=-12, y=7)
            #
            no_pause_allowed_note.config(text="",font=("grey", 8, "bold"), bg=YELLOW, fg="grey")
            no_pause_allowed_note.place(x=40, y=300)
            # --------------
            break_time = False  # NEW
            just_did_reset = True


# ---------------------------- TIMER MECHANISM ------------------------------- #
def restart_counter():
    global time_min
    global time_sec
    #
    global rest_min
    #
    global main_count_down
    global break_time
    global restart
    # --------------
    # --------------
    time_min = 25
    time_sec = 59
    rest_min = 4
    # --------------
    main_count_down = True
    break_time = False
    restart = False
    #{}==============={}
    countdown(1)  # 10-seconds

#---------------------------------------------------------------
#---------------------------------------------------------------
def long_break(rest_sec):
    global long_rest_min
    #
    global check_count
    #
    global main_count_down
    global break_time
    global restart
    # --------------
    # --------------
    #adding the last check :)
    if check_count < 4:
        if not just_did_reset: #NEW2
            check_count += 1
            laps_check_marks.config(text=f"{check * check_count}", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
    #
    # --------------
    # --------------
    if break_time:
        # DEBUG
        # print("YES")
        tomato_canvas.itemconfig(tomato_time_text, text=f"{long_rest_min}:{rest_sec}", fill=GREEN)
        # --------------
        if rest_sec > 0:
            window.after(1000, long_break, rest_sec-1)
            #----
        elif rest_sec <= 0 and long_rest_min <= 0:
            main_count_down = False
            reset_timer_system()
            #----
        else:
            long_rest_min -= 1
            long_break(time_sec) #<------use time_sec NOT rest_sec



#---------------------------------------------------------------
def five_min_rest(rest_sec):
    global rest_min
    #
    global main_count_down
    global break_time
    global restart
    # --------------
    # --------------
    if break_time and not main_count_down:
        #DEBUG
        # print("YES")
        tomato_canvas.itemconfig(tomato_time_text, text=f"{rest_min}:{rest_sec}",fill=GREEN)
        main_count_down = False
        # --------------
        if rest_sec < 10:
            tomato_canvas.itemconfig(tomato_time_text, text=f"{rest_min}:0{rest_sec}", fill=GREEN)
        # --------------
        if rest_sec > 0:
            window.after(1000, five_min_rest, rest_sec-1)
        # -------------
        elif rest_sec <= 0 and rest_min <= 0:
            restart_counter()
            #DEBUG
            print("ACTIVATE!")
        else:
            rest_min-=1
            five_min_rest(time_sec) #<------use time_sec NOT rest_sec


#---------------------------------------------------------------------


#laps:
def lap_check():
    global time_min
    global time_sec
    #
    global check
    global check_count
    #--------------
    global main_count_down
    global break_time
    global restart
    # --------------
    time_min = 25
    time_sec = 59
    #
    check_count += 1
    laps_check_marks.config(text=f"{check * check_count}", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
    #
    break_time = True
    main_count_down = False
    restart = True
    five_min_rest(time_sec)





# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    global time_min #25
    global check_count
    ####
    global break_time
    ####
    global long_rest_min
    ####
    global reactivate_signal
    ####
    if reactivate_signal:
        #--------------
        tomato_canvas.itemconfig(tomato_time_text, text=f"{time_min}:{count}",fill=WHITE)
        #update4:
        if count < 10:
            # --------------
            tomato_canvas.itemconfig(tomato_time_text, text=f"{time_min}:0{count}", fill=WHITE)
        #--------------
        # ----#
        no_pause_allowed_note.config(text="NOTE: you can't restart now!\nfinish your 25min of work session FIRST",
                                      font=("grey", 8, "bold"), bg=YELLOW, fg="grey")
        no_pause_allowed_note.place(x=40, y=300)
        #--------------
        if count > 0:
            window.after(1000, countdown, count-1)
                         #time       #function      #then you can add any other arguments "after" time is done and "fun" is activated
                     #millisecond
        elif check_count < 3 and time_min <=0:
            lap_check()
        #---------------------------------------30MIN-break timer
        elif check_count >= 3 and time_min <=0:
            break_time = True
            ####
            long_rest_min = 30
            long_break(time_sec)
        else:
            time_min -= 1
            countdown(time_sec)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro-Tomato Timer")
window.config(pady=50,padx=50, bg=YELLOW)
window.minsize(420,450)
window.maxsize(430,450)

#TEXT
timer_text = Label(text="Productivity Timer",fg=PINK ,bg=YELLOW ,font=(FONT_NAME,20,"bold"))
timer_text.place(x=19,y=-35)

#Canvas
tomato_canvas = Canvas(width=200,height=224,bg=YELLOW, highlightthickness=0)
#----
#adding image:
tomato_image = PhotoImage(file="tomato.png")
tomato_canvas.create_image(100,112, image=tomato_image) #x & y cor are the 1/2 amount of the canvas TO CENTER IT!
#----
#adding timer_text:
tomato_time_text = tomato_canvas.create_text(101.5,125,text="00:00",fill="white",font=(FONT_NAME,30,"bold"))
####
tomato_canvas.place(x=57,y=30) #<-----------pack is really good for initial build-up of widgets!!


#_____________________________________________check-counter
#check_count -> contains -> check ✔
laps_check_marks = Label(text=f"{check*check_count}", fg=GREEN, bg=YELLOW ,font=(FONT_NAME,30,"bold"))
laps_check_marks.place(x=75,y=260)


#_____________________________________________buttons
def start_timer():
    global main_count_down
    global break_time
    ####
    global reactivate_signal
    reactivate_signal = True
    # finishing cycle-note reset:
    note2.config(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 9, "bold"))
    # --------------
    # --------------
    if not break_time and not main_count_down:
        main_count_down = True
        countdown(0) #10-seconds


#------------------
start_button = Button(text="START", fg=RED, bg=YELLOW ,font=(FONT_NAME,10,"bold"), command=start_timer)
start_button.place(x=10,y=270)

# reset_button
reset_button = Button(text="RESET", fg=RED, bg=YELLOW ,font=(FONT_NAME,10,"bold"), command=reset_timer_system)
reset_button.place(x=255,y=270)

#_____________________________________misalliance-stuff:
# logo
logo_canvas = Canvas(width=100,height=100,bg=YELLOW, highlightthickness=0)
#
logo_image = PhotoImage(file="logo_ico.png")
logo_canvas.create_image(50,50, image=logo_image)
logo_canvas.place(x=-60,y=320)


font_size = 7
#info
#-----#

info = Label(text="productivity system:",font=("grey", font_size, "bold"), bg=YELLOW, fg="grey")
info.place(x=40, y=340)
#######################
#######################
info = Label(text="25min\nwork",font=("grey", font_size, "bold"), bg=YELLOW, fg=RED)
info.place(x=40, y=360)
######
info = Label(text=">>5min\n break-1",font=("grey", font_size, "bold"), bg=YELLOW, fg=GREEN)
info.place(x=40*2-10, y=360)
######
info = Label(text=">>25min\nwork",font=("grey", font_size, "bold"), bg=YELLOW, fg=RED)
info.place(x=40*3-10, y=360)
######
info = Label(text=">>5min\n break-2",font=("grey", font_size, "bold"), bg=YELLOW, fg=GREEN)
info.place(x=40*4-10, y=360)
######
info = Label(text=">>25min\nwork",font=("grey", font_size, "bold"), bg=YELLOW, fg=RED)
info.place(x=40*5-10, y=360)
######
info = Label(text=">>5min\n break-3",font=("grey", font_size, "bold"), bg=YELLOW, fg=GREEN)
info.place(x=40*6-10, y=360)
######
info = Label(text=">>25min\nwork",font=("grey", font_size, "bold"), bg=YELLOW, fg=RED)
info.place(x=40*7-10, y=360)
######
info = Label(text=">>30min<<\n break-4",font=("grey", font_size, "bold"), bg=YELLOW, fg=GREEN)
info.place(x=40*8-10, y=360)

#############################
#no reset note:
no_pause_allowed_note = Label(text="",font=("grey", 8, "bold"), bg=YELLOW, fg="grey")
no_pause_allowed_note.place(x=40, y=300)

#finihing a whole cycle note:
note2 = Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 9, "bold"))
note2.place(x=-12, y=7)

#==================end
window.mainloop()

