
import sqlite3
import tkinter as tk 
import customtkinter
from tkinter import ttk
import command
from tkinter import messagebox
from tktimepicker import AnalogPicker,AnalogThemes, constants
from tkcalendar import *
from PIL import Image

font1 = ('Helvetica', 25, 'bold')
font2 = ('Helvetica', 17, 'bold')
font3 = ('Helvetica', 13, 'bold')
font4 = ('Helvetica', 13, 'bold', 'underline') 

#controller.discUserInfo
class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        def update(idletree, scheduletree, tree, historytree):
            command.add_to_idletree(self, idletree)
            command.add_to_scheduletree(self, scheduletree)
            command.add_to_treeview(self, tree)
            command.add_to_historytree(self, historytree)
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        homeframe = customtkinter.CTkFrame(self, width=1000, height=700, fg_color="#EFE6D5")
        homeframe.pack()
        
            #tabs
        tabview = customtkinter.CTkTabview(homeframe, fg_color="#F2EEE7", width=1000, height=650, command= lambda: update(idletree, scheduletree, tree, historytree))
        tabview.pack(expand="True")
        tabview.add("TASKS") 
        tabview.add("SCHEDULE")  
        tabview.add("HISTORY")  
        tabview.add("ACCOUNT")  
        tabview.set("TASKS")  # set currently visible tab
        
        #################################### Schedule Tab ####################################################
        
        scheduletree = ttk.Treeview(tabview.tab("SCHEDULE"), height = 15)
        scheduletree['columns'] = ('ID','Name', 'Duration', 'Deadline(Date)', 'Deadline(Time)', 'Value','Schedule(Date)')
        scheduletree.column('#0', width=0, stretch=True)
        scheduletree.column('ID', anchor="center", width=120)
        scheduletree.column('Name', anchor="center", width=120)
        scheduletree.column('Duration', anchor="center", width=120)
        scheduletree.column('Deadline(Date)', anchor="center", width=120)
        scheduletree.column('Deadline(Time)', anchor="center", width=120)
        scheduletree.column('Value', anchor="center", width=120)
        scheduletree.column('Schedule(Date)', anchor="center", width=120)
        scheduletree.heading('ID', text="ID")
        scheduletree.heading('Name', text="Name")
        scheduletree.heading('Duration', text="Duration")
        scheduletree.heading('Deadline(Date)', text="Deadline(Date)")
        scheduletree.heading('Deadline(Time)', text="Deadline(Time)")
        scheduletree.heading('Value', text="Value")
        scheduletree.heading('Schedule(Date)', text="Schedule(Date)")
        scheduletree.pack(pady=20)
        #################################### Schedule Tab #################################################### 

        #################################### Task Tab ####################################################
        global tree
        tree = ttk.Treeview(tabview.tab("TASKS"), height = 15)
        tree['columns'] = ('ID','Name', 'Duration', 'Deadline(Date)', 'Deadline(Time)', 'Importance','Status')

        tree.column('#0', width=0, stretch=True)
        tree.column('ID', anchor="center", width=120)
        tree.column('Name', anchor="center", width=120)
        tree.column('Duration', anchor="center", width=120)
        tree.column('Deadline(Date)', anchor="center", width=120)
        tree.column('Deadline(Time)', anchor="center", width=120)
        tree.column('Importance', anchor="center", width=120)
        tree.column('Status', anchor="center", width=120)
        tree.heading('ID', text="ID")
        tree.heading('Name', text="Name")
        tree.heading('Duration', text="Duration")
        tree.heading('Deadline(Date)', text="Deadline(Date)")
        tree.heading('Deadline(Time)', text="Deadline(Time)")
        tree.heading('Importance', text="Importance")
        tree.heading('Status', text="Status")
        tree.pack(pady=20)
            
        #################################### History Tab ####################################################
        global historytree
        historytree = ttk.Treeview(tabview.tab("HISTORY"), height = 15)
        historytree['columns'] = ('ID','Name', 'Time Finished', 'Date Finished', 'Status')
            
        historytree.column('#0', width=0, stretch=True)
        historytree.column('ID', anchor="center", width=120)
        historytree.column('Name', anchor="center", width=120)
        historytree.column('Time Finished', anchor="center", width=120)
        historytree.column('Date Finished', anchor="center", width=120)
        historytree.column('Status', anchor="center", width=120)
        historytree.heading('ID', text="ID")
        historytree.heading('Name', text="Name")
        historytree.heading('Time Finished', text="Time Finished")
        historytree.heading('Date Finished', text="Date Finished")
        historytree.heading('Status', text="Status")
        historytree.pack(pady=20)
        
        #################################### History Tab ####################################################
        taskname_label = customtkinter.CTkLabel(tabview.tab("TASKS"), font=font2, text_color="#000000", text="TASK ACTION")
        taskname_label.pack(anchor="center", pady=(20,0))
            
        buttonframe = customtkinter.CTkFrame(tabview.tab("TASKS"), width=1000, height=700, fg_color="#EFE6D5")
        buttonframe.pack(padx=20, pady = 20)
        addtask = customtkinter.CTkButton(buttonframe, font= font3,command = lambda:command.addtask(self, tree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="ADD TASK",width=170,fg_color="#14397D",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        addtask.pack(side="left",expand=False, padx=10)
        updatetask = customtkinter.CTkButton(buttonframe, font= font3,command = lambda:command.updatetask(self, tree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="MODIFY TASK",width=170,fg_color="#14397D",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        updatetask.pack(side = "left",expand=False, padx=10)
        donetask = customtkinter.CTkButton(buttonframe, font= font3,command = lambda:command.donetask(self, tree, historytree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="DONE TASK",width=170,fg_color="#14397D",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        donetask.pack(side = "left", expand=False, padx=10)  
        deletetask = customtkinter.CTkButton(buttonframe, font= font3,command = lambda:command.deletetask(self, tree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="DELETE TASK",width=170,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        deletetask.pack(side = "left", expand=False, padx=10)
        #################################### Task Tab ####################################################
        
                    
        
        #################################### Account Tab ####################################################
            
        taskname_label = customtkinter.CTkLabel(tabview.tab("ACCOUNT"), font=font2, text_color="#000000", text="IDLE TIME")
        taskname_label.pack(anchor="center", pady=(20,0))
        
        idletree = ttk.Treeview(tabview.tab("ACCOUNT"), height = 15)
        idletree['columns'] = ('idleID','starttime', 'endtime', 'date') 
        idletree.column('#0', width=0, stretch=True)
        idletree.column('idleID', anchor="center", width=120)
        idletree.column('starttime', anchor="center", width=120)
        idletree.column('endtime', anchor="center", width=120)
        idletree.column('date', anchor="center", width=120)
        idletree.heading('idleID', text="ID")
        idletree.heading('starttime', text="Start Time")
        idletree.heading('endtime', text="End Time")
        idletree.heading('date', text="Date")
        idletree.pack(pady=20)
            
        dlebuttonframe = customtkinter.CTkFrame(tabview.tab("ACCOUNT"), width=1000, height=700, fg_color="#EFE6D5")
        dlebuttonframe.pack(padx=20, pady = 20) 
        addidle = customtkinter.CTkButton(dlebuttonframe, font= font3,command = lambda:command.addidle(self, idletree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="ADD IDLE TIME",width=250,fg_color="#14397D",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        addidle.pack(side="left",expand=False, padx=10)  
        removeidle = customtkinter.CTkButton(dlebuttonframe, font= font3,command = lambda:command.reidle(self, idletree, scheduletree), hover_color="#000000", text_color = "#D7EAF3",text="REMOVE IDLE TIME",width=250,fg_color="#14397D",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        removeidle.pack(side="left",expand=False, padx=10)   
        button_1 = customtkinter.CTkButton(tabview.tab("ACCOUNT"), text="LOGOUT", command=lambda: command.logout(self, parent, controller, tree, idletree, scheduletree, historytree), font= font3,hover_color="#000000", text_color = "#D7EAF3",width=250,cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        button_1.pack(padx=20, pady=20)

        if len(self.controller.discUserInfo) > 0:
            update(idletree, scheduletree, tree, historytree)
           #################################### Account Tab ###################################################
        