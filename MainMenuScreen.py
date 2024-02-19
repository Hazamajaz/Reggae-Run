from tkinter import *
import os


def RunCreateMainMenuScreen():
  CreateMainMenuScreen = Tk()
  CreateMainMenuScreen.title("Opening Screen")
  CreateMainMenuScreen.geometry("600x420")
  CreateMainMenuScreen.configure(background="#272736")
  CreateMainMenuScreen.resizable(width=False, height=False)
  CreateMainMenuScreen.overrideredirect(1)
    
  titleImg = PhotoImage(file = "Main Menu Title.png")
  howToPlayImg = PhotoImage(file = "How To Play Button.png")
  playGameImg = PhotoImage(file = "Play Game Button.png")
  leaderboardImg = PhotoImage(file = "Leaderboard Button.png")

  def howToPlay():
    CreateMainMenuScreen.destroy()
    os.system('python HowToPlayScreen.py')  

  def playGame():
    CreateMainMenuScreen.destroy()
    os.system('python GameScreen.py')

  def leaderboard():
    CreateMainMenuScreen.destroy()
    os.system('python LeaderboardScreen.py')  
  
  lblPageTitle = Label(CreateMainMenuScreen, image=titleImg, borderwidth=0, bg="#272736")
  btnHowToPlayButton = Button(CreateMainMenuScreen, image=howToPlayImg, command=howToPlay, borderwidth=0, bg="#272736", highlightbackground="#272736", activebackground="#8FDE5D")
  btnPlayGameButton = Button(CreateMainMenuScreen, image=playGameImg, command=playGame, borderwidth=0, bg="#272736", highlightbackground="#272736", activebackground="#8FDE5D")
  btnLeaderboardButton = Button(CreateMainMenuScreen, image=leaderboardImg, command=leaderboard, borderwidth=0, bg="#272736", highlightbackground="#272736", activebackground="#8FDE5D")

  lblPageTitle.place(relx=0.5, rely=0.38, anchor=CENTER)
  btnHowToPlayButton.place(relx=0.38, rely=0.55, anchor=E)
  btnPlayGameButton.place(relx=0.5, rely=0.55, anchor=CENTER)
  btnLeaderboardButton.place(relx=0.62, rely=0.55, anchor=W)

  CreateMainMenuScreen.mainloop()

RunCreateMainMenuScreen()

