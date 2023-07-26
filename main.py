import database
import sqlite3
import customtkinter
import tkinter as tk
import userauth, homepage
from PIL import Image
from datetime import datetime, timedelta

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        loadingscreen = customtkinter.CTkFrame(self, width=1000, height=700, fg_color="#EFE6D5")
        loadingscreen.pack()
        
        g = customtkinter.CTkFrame(loadingscreen, fg_color="#EFE6D5", width=700, height=500)
        g.place(relx=.5, rely=.5,anchor= "center")
        
        my_image = customtkinter.CTkImage(light_image=Image.open("./images/logo.png"),
            size=(900, 300))
        image_label = customtkinter.CTkLabel(g, image=my_image, text="")  # display image with a CTkLabel
        image_label.pack(pady=20)
        #font= font3,command = login, text_color = "#D7EAF3",text="LOGIN",width=300,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35
        
        proceedbutton= customtkinter.CTkButton(g,font = font2,text="Proceed",command=lambda: controller.show_frame(userauth.LoginPage), width=300, hover_color="#E73213", text_color="#000000", fg_color="#EFE6D5", border_width=2, border_color="#000000",cursor="hand2", height = 35)
        proceedbutton.pack(pady = 40)

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #the title
        self.wm_title("I-SCHED")
        width =1000
        height = 700
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        x = (screenwidth/2) - (width/2)
        y = (screenheight/2) - (height/2)
        self.config(background="#EFE6D5")
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.resizable(0,0)
        container = customtkinter.CTkFrame(self, fg_color="#EFE6D5")
        container.place(relx=.5, rely=.5,anchor= "center")
        self.discUserInfo = {}
        ## required to make window show before the program gets to the mainloop
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (userauth.LoginPage, userauth.SignupPage, userauth.WelcomePage, MainPage, homepage.HomePage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)

        self.iconbitmap("./images/icon.ico")
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
    
    def get_page(self, page_class):
        return self.frames[page_class]

if __name__ == "__main__":
    font1 = ('Helvetica', 25, 'bold')
    font2 = ('Helvetica', 17, 'bold')
    font3 = ('Helvetica', 13, 'bold')
    font4 = ('Helvetica', 13, 'bold', 'underline') 

    database.createdatabase()
    
    App = windows()
    App.mainloop()
