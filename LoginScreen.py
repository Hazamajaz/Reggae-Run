from tkinter import *
from tkinter import font
from tkinter import messagebox
import os
import sqlite3

attempts = 3

def RunCreateLoginScreen():
  CreateLoginScreen = Tk()
  CreateLoginScreen.title("Login Screen")
  CreateLoginScreen.geometry("600x420")
  CreateLoginScreen.configure(background="#272736")
  CreateLoginScreen.resizable(width=False, height=False)

  checkInt = IntVar(value=0)

  def showPassword():
    if(checkInt.get()==1):
      #when check box is enabled
      entPassword.config(show='')
    else:
      #when checkbox is not enabled
      entPassword.config(show='*')

  def login():
    global attempts
    #checks for empty input fields
    if (entUsername.get()=="" or entPassword.get()==""):
      #alerts user of empty input fields
      messagebox.showerror("Error", "Please enter both a username and a password")
    else:
      #checks for existence of username in database.py
      database = sqlite3.connect("ReggaeRun.db")
      cursor = database.cursor()
      cursor.execute('''SELECT username FROM user_table WHERE username=?''', [entUsername.get()])
      checkUsername = cursor.fetchone()
      if not checkUsername:
        messagebox.showerror("Error", "Username does not exist, sign up to create an account")
      else:
        #checks for matching password
        cursor.execute('''SELECT password FROM user_table WHERE username=?''', [entUsername.get()])
        checkPassword = cursor.fetchone()
        if attempts != 0:
          if checkPassword[0] != entPassword.get():
            attempts -= 1
            if attempts == 0:
              messagebox.showerror('Error', 'Incorrect password, 3 attempt limit has been reached')
            else:
              messagebox.showerror("Error", f"Incorrect password, {attempts} attempts left")
          else:
            CreateLoginScreen.destroy()
            os.system("python MainMenuScreen.py")
        else:
          messagebox.showerror("Error", "Attempt limit reached, sign up to create a new account") 
      database.close()

  def signUp():
    CreateLoginScreen.destroy()
    os.system("python SignUpScreen.py")            

  CreateLoginScreen.bind('<Return>', lambda event: login())
  
  titleImg = PhotoImage(file="Login Title.png")
  loginImg = PhotoImage(file="Login Button.png")
  signUpImg = PhotoImage(file="Sign Up Btn1.png")
  
  font1 = font.Font(family="Times New Roman", size=15, weight="bold")

  lblPageTitle = Label(CreateLoginScreen, image=titleImg, bg="#272736")
  lblUsername = Label(CreateLoginScreen, text="Username:", font=font1, bg="#272736", fg="#8FDE5D")
  lblPassword = Label(CreateLoginScreen, text="Password:", font=font1, bg="#272736", fg= "#8FDE5D")
  entUsername = Entry(CreateLoginScreen)
  entUsername.focus_set()
  entPassword = Entry(CreateLoginScreen, show="*")
  checkboxPassword = Checkbutton(CreateLoginScreen, variable=checkInt,
    onvalue=1,offvalue=0,command=showPassword, bg="#272736", borderwidth=0, activebackground="#272736", highlightthickness=0)
  btnLogin = Button(CreateLoginScreen, image=loginImg, bg="#272736", activebackground="#8FDE5D", highlightbackground="#272736", borderwidth=0, command=login)
  btnSignUp = Button(CreateLoginScreen, image=signUpImg, command=signUp, bg="#272736", activebackground="#8FDE5D", highlightbackground="#272736", borderwidth=0)

  lblPageTitle.place(relx = 0.5, rely = 0.15, anchor = CENTER)
  lblUsername.place(relx = 0.49, rely = 0.3, anchor = E)
  entUsername.place(relx = 0.5, rely = 0.3, anchor = W)
  lblPassword.place(relx = 0.49, rely = 0.4, anchor = E)
  entPassword.place(relx = 0.5, rely = 0.4, anchor = W)
  checkboxPassword.place(relx = 0.78, rely = 0.4, anchor = W)
  btnLogin.place(relx = 0.5, rely = 0.7, anchor = S)
  btnSignUp.place(relx = 0.5, rely = 0.71, anchor = N)
  


  CreateLoginScreen.mainloop()
RunCreateLoginScreen()