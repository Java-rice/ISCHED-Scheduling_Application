import tkinter as tk
import customtkinter
import sqlite3
import homepage, command
from tkinter import messagebox
from PIL import Image

font1 = ('Helvetica', 25, 'bold')
font2 = ('Helvetica', 17, 'bold')
font3 = ('Helvetica', 13, 'bold')
font4 = ('Helvetica', 13, 'bold', 'underline') 

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        def signpage(username_entry, password_entry):
            username_entry.delete(0,"end")
            password_entry.delete(0,"end")
            controller.show_frame(SignupPage)
        
        def login(username_entry, password_entry):
            username = username_entry.get()
            password = password_entry.get()
            if username != '' and password != '':
                conn = sqlite3.connect(r"database.db")
                cursor = conn.cursor()
                cursor.execute('SELECT password FROM users WHERE username=?', [username])
                result = cursor.fetchone()
                if result:
                    #if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                    if password == result[0]:
                        messagebox.showinfo('Success', 'Logged in Successfully.')
                        username_entry.delete(0, "end")
                        password_entry.delete(0, "end")
                        controller.discUserInfo['username'] = username
                        controller.show_frame(homepage.HomePage)
                    else:
                        messagebox.showerror('Error', 'Invalid Password')
                        conn.close()
                else:
                    messagebox.showerror('Error', 'Invalid Username')
                    conn.close()
            else:
                messagebox.showerror('Error', 'All Fields Are Required')
        
        
        tk.Frame.__init__(self, parent)
        #mainstorage for elements
        mainlogin = customtkinter.CTkFrame(self, width=1000, height=700, fg_color="#EFE6D5")
        mainlogin.pack()
        
        frame = customtkinter.CTkFrame(mainlogin, fg_color="#F2EEE7", width=700, height=500)
        frame.place(relx=.5, rely=.5,anchor= "center")
        
        #widgets
        login_label = customtkinter.CTkLabel(frame, font=font1, text_color="#000000", text="LOGIN")
        login_label.pack(padx=150,pady=50)
        username_label = customtkinter.CTkLabel(frame, font=font2, text_color="#000000", text="USERNAME:")
        username_label.pack(padx=(0,195))
        username_entry = customtkinter.CTkEntry(frame, font=font3, text_color="#000000", bg_color="#9DBEB7", fg_color="#9DBEB7",border_color="#000000", border_width=1, placeholder_text="Username", placeholder_text_color="#a3a3a3", width=300,height=30)
        username_entry.pack(pady=5, expand="False")
        password_label = customtkinter.CTkLabel(frame, font=font2, text_color="#000000", text="PASSWORD:")
        password_label.pack(padx=(0,195), pady=(20,0))
        password_entry = customtkinter.CTkEntry(frame, show="*", font=font3, text_color="#000000", bg_color="#9DBEB7", fg_color="#9DBEB7",border_color="#000000", border_width=1, placeholder_text="Password", placeholder_text_color="#a3a3a3", width=300,height=30)
        password_entry.pack(pady=5, expand="False")
        #loginbutton
        login_button = customtkinter.CTkButton(frame, font= font3,command = lambda:login(username_entry, password_entry), hover_color="#000000",  text_color = "#D7EAF3",text="LOGIN",width=300,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        login_button.pack(pady=(50), expand="False")
        #if no account yet
        noaccount = customtkinter.CTkLabel(frame, font=font3, text="Don't have an account?", text_color="#000000")
        noaccount.pack(pady=(0,0))
        sign = customtkinter.CTkButton(frame, font= font4, text_color = "#E73213", fg_color="transparent",hover_color="#F2EEE7", bg_color="transparent", text="Create Account",cursor="hand2",command=lambda:signpage(username_entry, password_entry))
        sign.pack(pady=(0,50))
        
class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        
        def back():
            reg_username_entry.delete(0, "end")
            reg_password_entry.delete(0, "end")
            confirm_password_entry.delete(0, "end")
            controller.show_frame(LoginPage)
        
        def signup():
            global regusername
            global regpassword
            regusername = reg_username_entry.get()
            regpassword = reg_password_entry.get()
            confirm = confirm_password_entry.get()
            if regusername != '' and regpassword != '':
                if confirm != regpassword:
                    messagebox.showerror('Error', 'Password didnt match')
                else:
                    if len(regpassword) < 8:
                        messagebox.showerror('Error','Password should be 8 to 15 characters')
                    else:
                        conn = sqlite3.connect(r"database.db")
                        cursor = conn.cursor()
                        cursor.execute('SELECT username FROM users WHERE username=?', [regusername])
                        if cursor.fetchone() is not None:
                            messagebox.showerror('Error', 'Username already exists.')
                            conn.close()
                        else:
                            #encoded_password = password.encode('utf-8')
                            #hashed_passsword = bcrypt.haspw(encoded_password, bcrypt.gensalt())
                            #print(hashed_passsword)
                            cursor.execute('INSERT INTO users VALUES (?, ?)', [regusername,regpassword])
                            conn.commit()
                            messagebox.showinfo('Success', 'Account has been created.')
                            regpassword = ''
                            regusername = ''
                            reg_username_entry.delete(0, "end")
                            reg_password_entry.delete(0, "end")
                            confirm_password_entry.delete(0, "end")
                            controller.show_frame(WelcomePage)
                            conn.close()
                            
            else:
                messagebox.showerror('Error', 'Enter all data.')
        
        tk.Frame.__init__(self, parent)
        #mainstorage for elements
        mainsignup = customtkinter.CTkFrame(self, width=1000, height=700, fg_color="#EFE6D5")
        mainsignup.pack()
        
        frame = customtkinter.CTkFrame(mainsignup, fg_color="#F2EEE7", width=900, height=500)
        frame.place(relx=.5, rely=.5,anchor= "center")
        
        #widgets
        login_label = customtkinter.CTkLabel(frame, font=font1, text_color="#000000", text="SIGN UP")
        login_label.pack(padx=150,pady=50)
        reg_username_label = customtkinter.CTkLabel(frame, font=font2, text_color="#000000", text="USERNAME:")
        reg_username_label.pack(padx=(0,195))
        reg_username_entry = customtkinter.CTkEntry(frame, font=font3, text_color="#000000", bg_color="#9DBEB7", fg_color="#9DBEB7",border_color="#000000", border_width=1, placeholder_text="Username", placeholder_text_color="#a3a3a3", width=300,height=30)
        reg_username_entry.pack(pady=5, expand="False")
        reg_password_label = customtkinter.CTkLabel(frame, font=font2, text_color="#000000", text="PASSWORD:")
        reg_password_label.pack(padx=(0,195), pady=(20,0))
        reg_password_entry = customtkinter.CTkEntry(frame, show="*", font=font3, text_color="#000000", bg_color="#9DBEB7", fg_color="#9DBEB7",border_color="#000000", border_width=1, placeholder_text="Password", placeholder_text_color="#a3a3a3", width=300,height=30)
        reg_password_entry.pack(pady=5, expand="False")
        confirm_password_label = customtkinter.CTkLabel(frame, font=font2, text_color="#000000", text="CONFIRM PASSWORD:")
        confirm_password_label.pack(padx=(0,123), pady=(20,0))
        confirm_password_entry = customtkinter.CTkEntry(frame, show="*", font=font3, text_color="#000000", bg_color="#9DBEB7", fg_color="#9DBEB7",border_color="#000000", border_width=1, placeholder_text="Password", placeholder_text_color="#a3a3a3", width=300,height=30)
        confirm_password_entry.pack(pady=5, expand="False")
        
        #buttons
        regret = customtkinter.CTkFrame(frame, fg_color="#F2EEE7", width=200, height=200)
        regret.pack(pady=50, expand="False")
        
        
        return_button = customtkinter.CTkButton(regret, font= font3 , hover_color="#000000", text_color = "#D7EAF3",text="RETURN",width=140,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35,
                                                command=back)
        return_button.pack(side = "left", padx=10, expand="False")
        
        register_button = customtkinter.CTkButton(regret, font= font3,hover_color="#000000", command = signup, text_color = "#D7EAF3",text="REGISTER",width=140,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35)
        register_button.pack(side = "left", padx=10, expand="False")

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        
        def go_to_login():
            controller.show_frame(LoginPage)

        tk.Frame.__init__(self, parent)
        
        mainprofile = customtkinter.CTkFrame(self, width=1000, height=700, fg_color="#EFE6D5")
        mainprofile.pack()
        
        frame = customtkinter.CTkFrame(mainprofile, fg_color="#EFE6D5", width=900, height=500)
        frame.place(relx=.5, rely=.5,anchor= "center")

        my_image = customtkinter.CTkImage(light_image=Image.open("./images/welcome.png"),
            size=(900, 250))

        image_label = customtkinter.CTkLabel(frame, image=my_image, text="")  # display image with a CTkLabel
        image_label.pack(pady=50)
        #font= font3,command = login, text_color = "#D7EAF3",text="LOGIN",width=300,fg_color="#E73213",cursor="hand2",corner_radius=5,border_color="#000000", border_width=1, height=35
        
        ccontinue = customtkinter.CTkButton(frame, font= font4, hover_color="#EFE6D5", text_color = "#E73213", fg_color="transparent", bg_color="transparent", text="CLICK TO CONTINUE",cursor="hand2",command=go_to_login)
        ccontinue.pack(pady=(160,0))
