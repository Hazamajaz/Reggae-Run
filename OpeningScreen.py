from tkinter import *
import os


def RunCreateOpeningScreen():
  CreateOpeningScreen = Tk()
  CreateOpeningScreen.title("Opening Screen")
  CreateOpeningScreen.geometry("600x420")
  CreateOpeningScreen.configure(background="#272736")
  CreateOpeningScreen.resizable(width=False, height=False)
  CreateOpeningScreen.overrideredirect(1)
  
  def login():
    CreateOpeningScreen.destroy()
    os.system('python LoginScreen.py')   
  
  loginImg = PhotoImage(file = "Login Button.png")
  titleImg = PhotoImage(file = "Opening Title.png")
  
  lblPageTitle = Label(CreateOpeningScreen, image=titleImg, borderwidth=0, bg="#272736")
  btnLoginButton = Button(CreateOpeningScreen, image=loginImg, command=login, borderwidth=0, bg="#272736", highlightbackground="#272736", activebackground="#8FDE5D")
  
  lblPageTitle.place(relx=0.5, rely=0.38, anchor=CENTER)
  btnLoginButton.place(relx=0.5, rely=0.55, anchor=CENTER)

  CreateOpeningScreen.mainloop()
  
RunCreateOpeningScreen()
  
  

