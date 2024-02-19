from tkinter import *
from tkinter import font
from tkinter import messagebox
import os
import sqlite3
from re import search

formGroups = ["LR", "JP", "MP", "BD", "JBA", "OR", "MW", "KTA"]
specialChars = ["!", "@", "#", "$", "%", "*", "&", "?"]

def RunCreateSignUpScreen():
  CreateSignUpScreen = Tk()
  CreateSignUpScreen.title("Sign Up Screen")
  CreateSignUpScreen.geometry("600x420")
  CreateSignUpScreen.configure(background="#272736")
  CreateSignUpScreen.resizable(width=False, height=False)

  checkInt = IntVar(value=0)

  def showPassword():
    if(checkInt.get()==1):
      #when check box is enabled
      entPassword.config(show='')
    else:
      #when checkbox is not enabled
      entPassword.config(show='*')

  def login():
    CreateSignUpScreen.destroy()
    os.system("python LoginScreen.py")      

  def validForm():
    form = entForm.get()
    if form[0] in ["7", "8", "9"]:
      form = form[1:]
      if form in formGroups:
        return True
      else: 
        return False
    elif (form[0] == "1" and (form[1] in ["0", "1", "2", "3"])):
      form = form[2:]
      if form in formGroups:
        return True
      else: 
        return False
    else:
      return False

  def validPassword():
    password = entPassword.get()
    #checks password is longer than 8 characters
    if not (len(password) >= 8):
      messagebox.showerror("Error", "Password must be at least 8 characters long")
      return False
    #checks if password contains a letter
    elif (search('[A-Z]', password) is None) and (search('[a-z]', password) is None):
      messagebox.showerror("Error", "Password must contain at least one letter")
      return False
    #checks if password contains a number
    elif search('[0-9]', password) is None:
      messagebox.showerror("Error", "Password must contain at least one number")
      return False
    #checks if passowrd contains a special character
    elif not any(char in specialChars for char in password):
      messagebox.showerror("Error", "Password must contain at least one special character (!, @, #, $, %, *, &, ?)")
      return False
    else:
      return True
  
  def signUp():
    #check for empty entry fields
    if (entUsername.get() == "" or entPassword.get() == "" or entFirstName.get()=="" or entSurname.get()=="" or entForm.get()==""):
      messagebox.showerror("Error", "All fields are required")
    else:
      #checks that first and last names are alphabetic strings
      if not (entFirstName.get().isalpha() and entSurname.get().isalpha()):
        messagebox.showerror("Error", "First name and surname must be alphabetic")
      else:
        #checks if form group is valid
        if not validForm():
          messagebox.showerror("Error", "Form group is invalid")
        else:
          #checks is username already exists
          database = sqlite3.connect("ReggaeRun.db")
          cursor = database.cursor()
          cursor.execute('''SELECT username FROM user_table WHERE username=?''', [entUsername.get()])
          checkUsername = cursor.fetchone()
          if checkUsername:
            messagebox.showerror("Error", "Username already exists")
          else:
            if validPassword():
              cursor.execute("""INSERT INTO user_table VALUES (?,?,?,?,?)""", [entUsername.get(), entPassword.get(), entFirstName.get(), entSurname.get(), entForm.get()])
              database.commit()
              database.close()
              CreateSignUpScreen.destroy()
              os.system("python LoginScreen.py")
  
  CreateSignUpScreen.bind('<Return>', lambda event: signUp())

  titleImg = PhotoImage(file="Login Title.png")
  loginImg = PhotoImage(file="Login Btn 1.png")
  signUpImg = PhotoImage(file="Sign Up Button.png")

  font1 = font.Font(family="Times New Roman", size=15, weight="bold")

  lblPageTitle = Label(CreateSignUpScreen, image=titleImg, bg="#272736")
  lblUsername = Label(CreateSignUpScreen, text="Username:", font=font1, bg="#272736", fg="#8FDE5D")
  lblFirstName = Label(CreateSignUpScreen, text="First Name:", font=font1, bg="#272736", fg="#8FDE5D")
  lblSurname = Label(CreateSignUpScreen, text="Surname:", font=font1, bg="#272736", fg="#8FDE5D")
  lblForm = Label(CreateSignUpScreen, text="Form:", font=font1, bg="#272736", fg="#8FDE5D")
  lblPassword = Label(CreateSignUpScreen, text="Password:", font=font1, bg="#272736", fg= "#8FDE5D")
  entUsername = Entry(CreateSignUpScreen)
  entUsername.focus_set()
  entFirstName = Entry(CreateSignUpScreen)
  entSurname = Entry(CreateSignUpScreen)
  entForm = Entry(CreateSignUpScreen)
  entPassword = Entry(CreateSignUpScreen, show="*")
  checkboxPassword = Checkbutton(CreateSignUpScreen, variable=checkInt,
    onvalue=1,offvalue=0,command=showPassword, bg="#272736", borderwidth=0, activebackground="#272736", highlightthickness=0)
  btnSignUp = Button(CreateSignUpScreen, image=signUpImg, bg="#272736", activebackground="#8FDE5D", highlightbackground="#272736", borderwidth=0, command=signUp)
  btnLogin = Button(CreateSignUpScreen, image=loginImg, command=login, bg="#272736", activebackground="#8FDE5D", highlightbackground="#272736", borderwidth=0)

  lblPageTitle.place(relx = 0.5, rely = 0.15, anchor = CENTER)
  lblUsername.place(relx = 0.49, rely = 0.27, anchor = E)
  entUsername.place(relx = 0.5, rely = 0.27, anchor = W)
  lblFirstName.place(relx = 0.49, rely = 0.345, anchor = E)
  entFirstName.place(relx = 0.5, rely = 0.345, anchor = W)
  lblSurname.place(relx = 0.49, rely = 0.42, anchor = E)
  entSurname.place(relx = 0.5, rely = 0.42, anchor = W)
  lblForm.place(relx = 0.49, rely = 0.495, anchor = E)
  entForm.place(relx = 0.5, rely = 0.495, anchor = W)
  lblPassword.place(relx = 0.49, rely = 0.57, anchor = E)
  entPassword.place(relx = 0.5, rely = 0.57, anchor = W)
  checkboxPassword.place(relx = 0.78, rely = 0.57, anchor = W)
  btnSignUp.place(relx = 0.5, rely = 0.7, anchor = S)
  btnLogin.place(relx = 0.5, rely = 0.71, anchor = N)



  CreateSignUpScreen.mainloop()
RunCreateSignUpScreen()