import sqlite3
import tkinter as tk
import homepage, userauth, main
from tkinter import messagebox
import customtkinter
from datetime import date
from tktimepicker import AnalogPicker,AnalogThemes, constants
from tkcalendar import *
from tkinter import ttk
from datetime import datetime, timedelta
from datetime import date

font1 = ('Helvetica', 25, 'bold')
font2 = ('Helvetica', 17, 'bold')
font3 = ('Helvetica', 13, 'bold')
font4 = ('Helvetica', 13, 'bold', 'underline') 

def add_to_historytree(self, historytree):
    # Get the current username from the "currentuser" table
    current_username = self.controller.discUserInfo['username'] 

    # Fetch tasks that have a similar username to the current username
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT task_id, task_name, currenttime, currentdate, status FROM history WHERE username = ?''', (current_username,))
    historylist = cursor.fetchall()

    historytree.delete(*historytree.get_children())
    for hist in historylist:
        historytree.insert('', tk.END, values=hist)
    conn.close()

def taskname_exists(taskname_entry):
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE taskname = ?', (taskname_entry,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

def confirm(self, tree, taskname, datec, timel, duration_value, importance_value, top, scheduletree):
    if not (taskname and datec and timel and duration_value and importance_value):
        messagebox.showerror('Error', 'Enter all fields.')
    elif taskname_exists(taskname.get()):
        messagebox.showerror('Error', 'Taskname Already Exists')
    else:
        username = self.controller.discUserInfo['username'] 

        # Insert the new task into the database table
        status = 'pending'
        conn = sqlite3.connect(r"database.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO tasks (username, taskname, duedate, duetime, duration, importance, status) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (username, taskname.get(), datec.cget("text"), timel.cget("text"), duration_value.get(), importance_value.get(), status))
        conn.commit()
        conn.close()

        # Clear the entry fields after successful insertion
        taskname.delete(0, tk.END)
        datec.configure(text="")
        timel.configure(text="")
        duration_value.set(1)
        importance_value.set(1)

    # Update the Treeview with the new task
    add_to_treeview(self, tree)
    add_to_scheduletree(self, scheduletree)
    top.destroy()

def add_to_treeview(self, tree):
    # Get the current username from the "currentuser" table
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    current_username = self.controller.discUserInfo['username'] 

    # Fetch tasks that have a similar username to the current username
    cursor.execute('''SELECT task_id, taskname, duration, duedate, duetime, importance, status FROM tasks WHERE username = ?''', (current_username,))
    tasklist = cursor.fetchall()

    tree.delete(*tree.get_children())
    for task in tasklist:
        tree.insert('', tk.END, values=task)
    conn.close()

def updateTime(time, timel,newtop):
    timel.configure(text="{:02d}:{:02d}".format(*time)) # remove 3rd flower bracket in case of 24 hrs time
    newtop.destroy()
    
def get_time(self,timel,top):
    newtop = customtkinter.CTkToplevel(top)
    newtop.wm_attributes("-topmost",True)
    newtop.title("Select Time")
            
    time_picker = AnalogPicker(newtop, type=constants.HOURS24)
    time_picker.setHours(10) #set the hour to 10
    time_picker.setMinutes(45) #set the minutes to 45
    time_picker.pack(expand=True, fill="both")

    theme = AnalogThemes(time_picker)
    theme.setDracula()
    ok_btn = tk.Button(newtop, text="Confirm", command=lambda: updateTime(time_picker.time(), timel, newtop), width=20)
    ok_btn.pack(pady=4)

def grab_date(cal, datec, datetop):
    datec.configure(text=cal.get_date())
    datetop.destroy()

def get_date(self,datec,top):
    datetop = customtkinter.CTkToplevel(top)
    datetop.wm_attributes("-topmost", True)
    datetop.title("Select Time")
                     
    cal = Calendar(datetop, selectmode = "day")
    cal.pack(pady=20)
            
    select = customtkinter.CTkButton(datetop, text="Confirm", command=lambda:grab_date(cal, datec, datetop), width=20)
    select.pack(pady=4)

def addtask(self, tree, scheduletree):
    top = customtkinter.CTkToplevel(self, fg_color="#EFE6D5")
    top.geometry("800x600")
    top.wm_attributes("-topmost",True)
    top.title("Add Tasks")
            
    Mainlabel = customtkinter.CTkLabel(top, font=font1, text_color="#000000", text="ADD TASK")
    Mainlabel.pack(anchor = "center", pady=20)
        
    tasknamecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    tasknamecont.pack(padx=50, pady=10)
    tasknamelabel = customtkinter.CTkLabel(tasknamecont, font=font3, text_color="#000000", text="Task name:")
    tasknamelabel.pack(side = "left", padx=10, expand="False")
    taskname = customtkinter.CTkEntry(tasknamecont,font=font3, text_color="#000000", bg_color="transparent", fg_color="transparent",border_color="#000000", border_width=1, placeholder_text_color="#a3a3a3", width=300,height=30)
    taskname.pack(side = "left", padx=10, expand="False")
            
    datecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    datecont.pack(padx=50, pady=10)
    date_lbl = customtkinter.CTkLabel(datecont, font=font3, text_color="#000000", text="Deadline(Date):  ")
    date_lbl.pack(side = "left", padx=10, expand="False")
    currentdateframe = customtkinter.CTkFrame(datecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currentdateframe.pack(side = "left",padx=10, expand="False")
    datec = customtkinter.CTkLabel(currentdateframe, font=font3, text_color="#000000", text="")
    datec.pack(side = "left", padx=10, expand="False")
    date_btn = tk.Button(datecont, text="Select Date", command= lambda: get_date(self, datec, top))
    date_btn.pack(side = "left", padx=10, expand="False")

    timecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    timecont.pack(padx=50, pady=10)
    time_lbl = customtkinter.CTkLabel(timecont, font=font3, text_color="#000000", text="Deadline(Time):  ")
    time_lbl.pack(side = "left", padx=10, expand="False")
    currenttimeframe = customtkinter.CTkFrame(timecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currenttimeframe.pack(side = "left",padx=10, expand="False")
    timel = customtkinter.CTkLabel(currenttimeframe, font=font3, text_color="#000000", text="")
    timel.pack(side = "left", padx=10, expand="False")
    time_btn = tk.Button(timecont, text="Select Time", command=lambda: get_time(self,timel,top))
    time_btn.pack(side = "left", padx=10, expand="False")
            
    duration_value = tk.IntVar()
    durationcont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    durationcont.pack(padx=50, pady=10)
    durationlabel = customtkinter.CTkLabel(durationcont, font=font3, text_color="#000000", text="Duration:")
    durationlabel.pack(side = "left", padx=10, expand="False")
    durationspin_box = ttk.Spinbox(durationcont,from_=1,to=300, font=font3,  textvariable = duration_value)  
    durationspin_box.pack(side = "left", padx=10, expand="False")
            
    importance_value = tk.IntVar()
    importancecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    importancecont.pack(padx=50, pady=10)
    importancelabel = customtkinter.CTkLabel(importancecont, font=font3, text_color="#000000", text="Importance:")
    importancelabel.pack(side = "left", padx=10, expand="False")
    spin_box = ttk.Spinbox(importancecont,from_=1,to=10, font=font3,  textvariable = importance_value)  
    spin_box.pack(side = "left", padx=10, expand="False")
            
    donetask = customtkinter.CTkButton(top, font=font3,
                                       command=lambda: confirm(self, tree, taskname, datec, timel, duration_value, importance_value, top, scheduletree),
                                       hover_color="#000000", text_color="#D7EAF3", text="ADD TASK", width=300,
                                       fg_color="#14397D", cursor="hand2", corner_radius=5,
                                       border_color="#000000", border_width=1, height=35)
    donetask.pack(anchor="center", expand=False, padx=30, pady=40)

def deletetask(self,tree,scheduletree):  
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select a task to delete.')
        return

    task_values = tree.item(selected_item)['values']
    task_id = task_values[0]
    task_name = task_values[1]

    # Show a confirmation messagebox
    response = messagebox.askquestion('Confirmation', f'Do you want to delete the task "{task_name}"?')
    if response == 'no':
        return

    # Proceed with the deletion
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()

    # Delete the task with the same task id from the tasks table
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()

    # Refresh the treeview to reflect the changes
    add_to_treeview(self, tree)
    add_to_scheduletree(self, scheduletree)

    # Close the database connection
    conn.close()

def confirm_update(top, self, tree, task_id, updated_taskname, updated_datec, updated_timel, updated_duration, updated_importance,  taskname, datec, timel,duration_value, importance_value, scheduletree):
    # Update the task in the database
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE tasks SET taskname = ?, duedate = ?, duetime = ?, duration = ?, importance = ? WHERE task_id = ?''', 
                   (updated_taskname, updated_datec, updated_timel, updated_duration, updated_importance, task_id))
    conn.commit()

    # Update the Treeview with the updated task
    add_to_treeview(self, tree)
    add_to_scheduletree(self, scheduletree)
           
    # Clear the entry fields after successful update
    taskname.delete(0, "end")
    timel.configure(text="")
    datec.configure(text="")
    duration_value.set(1)
    importance_value.set(1)
    top.destroy()
    conn.close()

def updatetask(self, tree, scheduletree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select a task to update.')
        return

    task_values = tree.item(selected_item)['values']
    task_id = task_values[0]
    task_name = task_values[1]
    task_duration = task_values[2]
    task_deadline_date = task_values[3]
    task_deadline_time = task_values[4]
    task_importance = task_values[5]
    task_status = task_values[6]
    
    top = customtkinter.CTkToplevel(self, fg_color="#EFE6D5")
    top.geometry("800x600")
    top.wm_attributes("-topmost",True)
    top.title("Add Tasks")
            
    Mainlabel = customtkinter.CTkLabel(top, font=font1, text_color="#000000", text="ADD TASK")
    Mainlabel.pack(anchor = "center", pady=20)
        
    tasknamecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    tasknamecont.pack(padx=50, pady=10)
    tasknamelabel = customtkinter.CTkLabel(tasknamecont, font=font3, text_color="#000000", text="Task name:")
    tasknamelabel.pack(side = "left", padx=10, expand="False")
    taskname = customtkinter.CTkEntry(tasknamecont,font=font3, text_color="#000000", bg_color="transparent", fg_color="transparent",border_color="#000000", border_width=1, placeholder_text_color="#a3a3a3", width=300,height=30)
    taskname.pack(side = "left", padx=10, expand="False")
            
    datecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    datecont.pack(padx=50, pady=10)
    date_lbl = customtkinter.CTkLabel(datecont, font=font3, text_color="#000000", text="Deadline(Date):  ")
    date_lbl.pack(side = "left", padx=10, expand="False")
    currentdateframe = customtkinter.CTkFrame(datecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currentdateframe.pack(side = "left",padx=10, expand="False")
    datec = customtkinter.CTkLabel(currentdateframe, font=font3, text_color="#000000", text="")
    datec.pack(side = "left", padx=10, expand="False")
    date_btn = tk.Button(datecont, text="Select Date", command= lambda: get_date(self, datec, top))
    date_btn.pack(side = "left", padx=10, expand="False")

    timecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    timecont.pack(padx=50, pady=10)
    time_lbl = customtkinter.CTkLabel(timecont, font=font3, text_color="#000000", text="Deadline(Time):  ")
    time_lbl.pack(side = "left", padx=10, expand="False")
    currenttimeframe = customtkinter.CTkFrame(timecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currenttimeframe.pack(side = "left",padx=10, expand="False")
    timel = customtkinter.CTkLabel(currenttimeframe, font=font3, text_color="#000000", text="")
    timel.pack(side = "left", padx=10, expand="False")
    time_btn = tk.Button(timecont, text="Select Time", command=lambda: get_time(self,timel,top))
    time_btn.pack(side = "left", padx=10, expand="False")
            
    duration_value = tk.IntVar()
    durationcont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    durationcont.pack(padx=50, pady=10)
    durationlabel = customtkinter.CTkLabel(durationcont, font=font3, text_color="#000000", text="Duration:")
    durationlabel.pack(side = "left", padx=10, expand="False")
    durationspin_box = ttk.Spinbox(durationcont,from_=1,to=300, font=font3,  textvariable = duration_value)  
    durationspin_box.pack(side = "left", padx=10, expand="False")
            
    importance_value = tk.IntVar()
    importancecont = customtkinter.CTkFrame(top, fg_color="transparent", bg_color="transparent")
    importancecont.pack(padx=50, pady=10)
    importancelabel = customtkinter.CTkLabel(importancecont, font=font3, text_color="#000000", text="Importance:")
    importancelabel.pack(side = "left", padx=10, expand="False")
    spin_box = ttk.Spinbox(importancecont,from_=1,to=10, font=font3,  textvariable = importance_value)  
    spin_box.pack(side = "left", padx=10, expand="False")
            
    taskname.insert(0, task_name)
    datec.configure(text=task_deadline_date)
    timel.configure(text=task_deadline_time)
    duration_value.set(task_duration)
    importance_value.set(task_importance)

    # Create the "Update Task" button
    update_button = customtkinter.CTkButton(top, font=font3,command=lambda: confirm_update(top, self, tree, task_id, taskname.get(), datec.cget("text"), timel.cget("text"), duration_value.get(), importance_value.get(), taskname, datec, timel,duration_value, importance_value, scheduletree),
                                            hover_color="#000000", text_color="#D7EAF3", text="UPDATE TASK", width=300,
                                            fg_color="#14397D", cursor="hand2", corner_radius=5,
                                            border_color="#000000", border_width=1, height=35)
    update_button.pack(anchor="center", expand=False, padx=30, pady=40)

def donetask(self,tree,historytree, scheduletree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select a task to delete.')
        return        
    
    task_values = tree.item(selected_item)['values']
    task_id = task_values[0]
    task_name = task_values[1]
    
    response = messagebox.askquestion('Confirmation', f'Mark "{task_name}" as done?')
    if response == 'no':
        return

    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    current_username = self.controller.discUserInfo['username'] 
    
    timenow = datetime.now()
    currenttime = timenow.strftime("%H:%M")
    datetoday = date.today()
    currentdate = datetoday.strftime("%m/%d/%y")
    status = "Finished"
    
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    
    #addtodatabase
    cursor.execute('''INSERT INTO history (username, task_id, task_name, currenttime, currentdate, status) VALUES (?, ?, ?, ?, ?, ?)''',
                   (current_username, task_id, task_name, currenttime, currentdate, status))
    conn.commit()
    
    # Delete the task with the same task id from the tasks table
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()
    
    add_to_historytree(self, historytree)
    
    # Refresh the treeview to reflect the changes
    add_to_treeview(self, tree)
    add_to_scheduletree(self, scheduletree)

    # Close the database connection
    conn.close()
            
def add_to_idletree(self, idletree):
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()

    current_username = self.controller.discUserInfo['username'] 

    # Fetch tasks that have a similar username to the current username
    cursor.execute('''SELECT idleID, starttime, endtime, date FROM idletime WHERE username = ?''', (current_username,))
    idelist = cursor.fetchall()

    idletree.delete(*idletree.get_children())
    for idle in idelist:
        idletree.insert('', tk.END, values=idle)
    conn.close()

def confirm_idle(self, idletree, starttime, endtime, result, idle_top, scheduletree):
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()

    username = self.controller.discUserInfo['username'] 
    
    cursor.execute('''INSERT INTO idletime (username, starttime, endtime, date) VALUES (?, ?, ?, ?)''',
                       (username, starttime.cget("text"), endtime.cget("text"), result.get()))
    conn.commit()
    
    starttime.configure(text="")
    endtime.configure(text="")
    result.set("everyday")
    
    add_to_idletree(self, idletree)
    add_to_scheduletree(self, scheduletree)
    idle_top.destroy()

def grab_idle_date(idate, result, idledatetop):
    date = idate.get_date()
    result.set(date)
    idledatetop.destroy()

def get_idle_date(self, result, idledatecont):
    idledatetop = customtkinter.CTkToplevel(idledatecont)
    idledatetop.wm_attributes("-topmost", True)
    idledatetop.title("Select Date ")
                     
    idate = Calendar(idledatetop, selectmode = "day")
    idate.pack(pady=20)
            
    select = customtkinter.CTkButton(idledatetop, text="Confirm", command=lambda:grab_idle_date(idate, result, idledatetop), width=20)
    select.pack(pady=4)

def addidle(self, idletree, scheduletree):
    idletop = customtkinter.CTkToplevel(self, fg_color="#EFE6D5")
    idletop.geometry("800x600")
    idletop.wm_attributes("-topmost",True)
    idletop.title("Add Tasks")
            
    Mainlabel = customtkinter.CTkLabel(idletop, font=font1, text_color="#000000", text="ADD IDLE TIME")
    Mainlabel.pack(anchor = "center", pady=20)
    
    starttimecont = customtkinter.CTkFrame(idletop, fg_color="transparent", bg_color="transparent")
    starttimecont.pack(padx=50, pady=10)
    starttime_lbl = customtkinter.CTkLabel(starttimecont, font=font3, text_color="#000000", text="Start Time:  ")
    starttime_lbl.pack(side = "left", padx=10, expand="False")
    currentstarttimeframe = customtkinter.CTkFrame(starttimecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currentstarttimeframe.pack(side = "left",padx=10, expand="False")
    starttime = customtkinter.CTkLabel(currentstarttimeframe, font=font3, text_color="#000000", text="")
    starttime.pack(side = "left", padx=10, expand="False")
    starttime_btn = tk.Button(starttimecont, text="Select Time", command=lambda: get_time(self,starttime,idletop))
    starttime_btn.pack(side = "left", padx=10, expand="False")
    
    endtimecont = customtkinter.CTkFrame(idletop, fg_color="transparent", bg_color="transparent")
    endtimecont.pack(padx=50, pady=10)
    endtime_lbl = customtkinter.CTkLabel(endtimecont, font=font3, text_color="#000000", text="End Time:  ")
    endtime_lbl.pack(side = "left", padx=10, expand="False")
    currentendtimeframe = customtkinter.CTkFrame(endtimecont, fg_color="transparent", bg_color="transparent", width=350, height = 30, border_color="#000000", border_width=1)
    currentendtimeframe.pack(side = "left",padx=10, expand="False")
    endtime = customtkinter.CTkLabel(currentendtimeframe, font=font3, text_color="#000000", text="")
    endtime.pack(side = "left", padx=10, expand="False")
    endtime_btn = tk.Button(endtimecont, text="Select Time", command=lambda: get_time(self,endtime,idletop))
    endtime_btn.pack(side = "left", padx=10, expand="False")
    
    result = tk.StringVar()
    result.set("everyday")
    idledatecont = customtkinter.CTkFrame(idletop, fg_color="transparent", bg_color="transparent")
    idledatecont.pack(padx=50, pady=10)
    idledate_lbl = customtkinter.CTkLabel(idledatecont, font=font3, text_color="#000000", text="Date:  ")
    idledate_lbl.pack(side = "left", padx=10, expand="False")
    idledate = customtkinter.CTkEntry(idledatecont,font=font3, text_color="#000000",textvariable=result, bg_color="transparent", fg_color="transparent",border_color="#000000", border_width=1, placeholder_text_color="#a3a3a3", width=100,height=30)
    idledate.pack(side = "left", padx=10, expand="False")

    
    doneidle = customtkinter.CTkButton(idletop, font=font3,
                                       command=lambda: confirm_idle(self, idletree, starttime, endtime, result, idletop, scheduletree),
                                       hover_color="#000000", text_color="#D7EAF3", text="ADD IDLE TIME", width=300,
                                       fg_color="#14397D", cursor="hand2", corner_radius=5,
                                       border_color="#000000", border_width=1, height=35)
    doneidle.pack(anchor="center", expand=False, padx=30, pady=40)
    
def reidle(self, idletree, scheduletree):
    selected_item = idletree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select a task to delete.')
        return

    task_values = idletree.item(selected_item)['values']
    idle_id = task_values[0]
    

    # Show a confirmation messagebox
    response = messagebox.askquestion('Confirmation', f'Do you want to delete the task "{idle_id}"?')
    if response == 'no':
        return

    # Proceed with the deletion
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()

    # Delete the task with the same task id from the tasks table
    cursor.execute("DELETE FROM idletime WHERE idleID = ?", (idle_id,))
    conn.commit()

    # Refresh the treeview to reflect the changes
    add_to_idletree(self, idletree)
    add_to_scheduletree(self, scheduletree)
    
    # Close the database connection
    conn.close()

def logout(self, parent, controller, tree, idletree, scheduletree, historytree):
    if messagebox.askokcancel(title="Log Out", message="Are you sure you want to log out?") == True:
        tree.delete(*tree.get_children())
        idletree.delete(*idletree.get_children())
        scheduletree.delete(*scheduletree.get_children())
        historytree.delete(*historytree.get_children())
        controller.show_frame(userauth.LoginPage)

def checkidletime(current_username):
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT starttime, endtime FROM idletime WHERE username = ? AND date = 'everyday' ORDER BY starttime ASC''', (current_username,))
    idle_times = cursor.fetchall()
    conn.close()
    return idle_times

def timetoint(time):
    splittime = time.split(':')
    splithour = (int(splittime[0]))
    splitmin = (int(splittime[1])) / 60
    return splithour + splitmin

def time_to_float(time_str):
    # Convert a time string (e.g., '08:30') to a float (e.g., 8.5)
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

def check_if_due(taskid, task_due_date, tday):
    if task_due_date < tday:
        messagebox.showwarning('Warning', 'Task ' + taskid + ' will be overdue\nWe recommend modifying your \ntask duration and idle time')

def convert_to_datetime(time_str):
    return datetime.strptime(time_str, '%H:%M')

def calmaxbasedtime(current_time_str, list_of_idle_time):
    #conversion string array
    current_time = convert_to_datetime(current_time_str)

    total_working_time = 0.0
    idle_time_slots = []

    for idle_start_str, idle_end_str in list_of_idle_time:
        idle_start = convert_to_datetime(idle_start_str)
        idle_end = convert_to_datetime(idle_end_str)
        idle_time_slots.append((idle_start, idle_end))

    # Sort the idle time slots by start time
    idle_time_slots.sort()

    for idx, (start, end) in enumerate(idle_time_slots):
        if current_time < start:
            # Calculate the working time between the current time and the next idle start time
            diff = start - current_time
            total_working_time += diff.total_seconds() / 3600  # Convert seconds to hours
            current_time = end
        elif start <= current_time <= end:
            # Move the current time to the end of the current idle slot
            current_time = end

    # Calculate the working time from the last idle end time to the end of the day (23:59)
    end_of_day = convert_to_datetime('23:59')
    diff = end_of_day - current_time
    total_working_time += diff.total_seconds() / 3600  # Convert seconds to hours

    return total_working_time

def checktime(listofidletime):
    total = 0
    for i in listofidletime:
        total += timetoint(i[1]) - timetoint(i[0])
    return 24 - total

def fractional_knapsack(tasks, current_username):
    schedule = []
    unfinished_task = []
    #date today
    today = date.today()    
    datetoday = today.strftime("%m/%d/%y")
    datetoday = datetime.strptime(datetoday, "%m/%d/%y")
    #timenow
    timenow = datetime.now()
    currenttime = timenow.strftime("%H:%M")
    #hours tracker
    current_hours = 0
    #checking of idletime
    listofidletime = checkidletime(current_username)
    mg_hours = checktime(listofidletime)
    first_day = 0; #if its on the current day
    for task in tasks:
        max_hours = mg_hours
        if first_day == 0:
            max_hours = calmaxbasedtime(currenttime, listofidletime)
        if current_hours + task['duration'] <= max_hours:
            task['day'] = datetoday
            schedule.append(task)
            task_due_date = datetime.strptime(task['duedate'], "%m/%d/%y")
            tday = task['day']
            check_if_due(str(task['task_id']), task_due_date, tday)
            current_hours += task['duration']
            if current_hours == max_hours:
                datetoday +=  timedelta(days=1)
                first_day = 1
                current_hours = 0
        else:
            remaining_hours = max_hours - current_hours
            fraction = remaining_hours / task['duration']
            partial_task = {
                'task_id': task['task_id'],
                'taskname': task['taskname'],
                'duration': remaining_hours,
                'duedate': task['duedate'],
                'duetime': task['duetime'],
                'importance': task['importance'] * fraction,
                'deadlinebaseval': task['deadlinebaseval'],
                'hoursfromdeadline': task['hoursfromdeadline'],
                'day': datetoday
            }
            unfinished = {
                'task_id': task['task_id'],
                'taskname': task['taskname'],
                'duration': task['duration'] - partial_task['duration'],
                'duedate': task['duedate'],
                'duetime': task['duetime'],
                'importance': task['importance'] - partial_task['importance'],
                'deadlinebaseval': task['deadlinebaseval'],
                'hoursfromdeadline': task['hoursfromdeadline'],
                'day': datetoday + timedelta(days=1)
            }
            #messagebox #warning overdue
            task_due_date = datetime.strptime(partial_task['duedate'], "%m/%d/%y")
            tday = partial_task['day']
            check_if_due(str(partial_task['task_id']), task_due_date, tday)
            schedule.append(partial_task)
            unfinished_task.append(unfinished)
            datetoday +=  timedelta(days=1)
            current_hours = 0
            first_day = 1
        #when there is unfinished task    
        while len(unfinished_task) != 0:
            #if not the current day
            if first_day != 0:
                max_hours = mg_hours
            dur = unfinished_task[0]['duration']
            if dur < max_hours - current_hours:
                current_hours += unfinished_task[0]['duration']
                task_due_date = datetime.strptime(unfinished_task[0]['duedate'], "%m/%d/%y")
                tday = unfinished_task[0]['day']
                check_if_due(str(unfinished_task[0]['task_id']) , task_due_date, tday)
                schedule.append(unfinished_task[0])
                unfinished_task.clear()
            elif dur == max_hours - current_hours:
                current_hours += unfinished_task[0]['duration']
                task_due_date = datetime.strptime(unfinished_task[0]['duedate'], "%m/%d/%y")
                tday = unfinished_task['day']
                check_if_due(str(unfinished_task['task_id']) ,task_due_date, tday)
                schedule.append(unfinished_task[0])
                unfinished_task.clear()
                datetoday +=  timedelta(days=1)
                first_day = 1
                current_hours = 0
            elif dur > max_hours - current_hours:
                remaining_hours = max_hours - current_hours
                fraction = remaining_hours / dur
                partial_task = {
                    'task_id': unfinished_task[0]['task_id'],
                    'taskname': unfinished_task[0]['taskname'],
                    'duration': remaining_hours,
                    'duedate': unfinished_task[0]['duedate'],
                    'duetime': unfinished_task[0]['duetime'],
                    'importance': unfinished_task[0]['importance'] * fraction,
                    'deadlinebaseval': unfinished_task[0]['deadlinebaseval'],
                    'hoursfromdeadline': unfinished_task[0]['hoursfromdeadline'],
                    'day': datetoday
                }
                unfinished = {
                    'task_id': unfinished_task[0]['task_id'],
                    'taskname': unfinished_task[0]['taskname'],
                    'duration': unfinished_task[0]['duration'] - partial_task['duration'],
                    'duedate': unfinished_task[0]['duedate'],
                    'duetime': unfinished_task[0]['duetime'],
                    'importance': unfinished_task[0]['importance'] - partial_task['importance'],
                    'deadlinebaseval': unfinished_task[0]['deadlinebaseval'],
                    'hoursfromdeadline': unfinished_task[0]['hoursfromdeadline'],
                    'day': datetoday + timedelta(days=1)
                }
                unfinished_task.clear()
                task_due_date = datetime.strptime(partial_task['duedate'], "%m/%d/%y")
                tday = partial_task['day']
                check_if_due(str(partial_task['task_id']),task_due_date, tday)
                schedule.append(partial_task)
                unfinished_task.append(unfinished)
                datetoday +=  timedelta(days=1)
                first_day = 1
                current_hours = 0
    return schedule
        
def currentvalues(tasks):
    for i in tasks:
        #date & time
        today = date.today()    
        datetoday = today.strftime("%m/%d/%y")
        timenow = datetime.now()
        currenttime = timenow.strftime("%H:%M")
        #string separation
        datetoday_date = datetoday.split('/')
        datetoday_time = currenttime.split(':')
        taskdate_date = i['duedate'].split('/')
        taskdate_time = i['duetime'].split(':')
        year_diff = int(taskdate_date[0]) - int(datetoday_date[0])
        month_diff = int(taskdate_date[1]) - int(datetoday_date[1])
        day_diff = int(taskdate_date[2]) - int(datetoday_date[2])
        hour_diff = int(taskdate_time[0]) - int(datetoday_time[0])
        minute_diff = int(taskdate_time[1]) - int(datetoday_time[1])
        difference_in_hours = (year_diff * 365 * 24) + (month_diff * 30 * 24) + (day_diff * 24) + hour_diff + (minute_diff / 60)
        #formula (cost)
        val = i['importance'] / difference_in_hours
        i['hoursfromdeadline'] = difference_in_hours
        i['deadlinebaseval'] = round(val, 6)
        # value / hoursfromdeadline
    return tasks

def merge_sort(tasks):
    if len(tasks) <= 1:
        return tasks
    mid = len(tasks) // 2
    left_half = tasks[:mid]
    right_half = tasks[mid:]
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]['deadlinebaseval'] >= right[j]['deadlinebaseval']:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def add_to_scheduletree(self, scheduletree):
    #open the database
    conn = sqlite3.connect(r"database.db")
    cursor = conn.cursor()
    current_username = self.controller.discUserInfo['username'] 
    
    # Fetch tasks that have a similar username to the current username
    cursor.execute('''SELECT task_id, taskname, duration, duedate, duetime, importance FROM tasks WHERE username = ?''', (current_username,))
    schedule = cursor.fetchall()
    tasks_with_names = []
    for task in schedule:
        sched_dict = {
            "task_id": task[0],
            "taskname": task[1],
            "duration": task[2],
            "duedate": task[3],
            "duetime": task[4],
            "importance": task[5]
        }
        tasks_with_names.append(sched_dict)
    
    
    #calculation formula: value = importance/hoursfromdeadline
    taskwithvalues = currentvalues(tasks_with_names)
    #mergesort
    sorted_task = merge_sort(taskwithvalues)
    #fractional knapsack (assign based on idle time & current date and time)
    resulted = fractional_knapsack(sorted_task, current_username)
    
    #display on schedule tree
    scheduletree.delete(*scheduletree.get_children())
    for task in resulted:
        scheduletree.insert('', 'end',values=(task['task_id'], task['taskname'], str(round(task['duration'], 2)) + " hrs", task['duedate'], task['duetime'], round(task['importance'],2), task['day'].strftime("%m/%d/%y"), 'walapa'))
    conn.close()


#################################### SCHEDULE TREE  ####################################################
#################################### SCHEDULE TREE  ####################################################
#################################### SCHEDULE TREE  ####################################################
#################################### SCHEDULE TREE  ####################################################
