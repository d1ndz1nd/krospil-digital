import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import hashlib
import webbrowser

root = tk.Tk()
root.title("Krospil Digital")
root.geometry("350x250")


# registration functions

def show_frame(frame):
    frame_login.pack_forget()
    frame_reg.pack_forget()
    frame_mainWindow.pack_forget()
    frame.pack(fill="both", expand=True, padx=10, pady=10)

def registration():
    login = entryRegLogin.get().strip()
    password = entryRegPassword.get().strip()
    passwordHashing = hashlib.md5(password.encode())
    passwordHash = passwordHashing.hexdigest()
    if login and password:
        with open("registration.txt", "w") as file:
            file.write(f"{login}:{passwordHash}")
        entryRegLogin.delete(0, 'end')
        entryRegPassword.delete(0, 'end')
        messagebox.showinfo("Успіх!", "Профіль створено! Тепер увійдіть.")
        show_frame(frame_login)
    else:
        messagebox.showwarning("Увага!", "Заповніть усі поля!")

def login():
    userLogin = entryLogLogin.get().strip()
    userPassword = entryLogPassword.get().strip()
    userPasswordHashing = hashlib.md5(userPassword.encode())
    userPasswordHash = userPasswordHashing.hexdigest()

    if not userLogin or not userPassword:
        messagebox.showwarning("Увага!", "Заповніть усі поля!")
        return

    try:
        with open("registration.txt", "r") as file:
            content = file.read().strip()
            if not content: 
                show_frame(frame_reg)
                return
                
            stored_login, stored_password = content.split(":")
            
            if userLogin == stored_login and userPasswordHash == stored_password:
                with open("session.txt", "w") as session_file:
                    session_file.write("True")
                entryLogLogin.delete(0, 'end')
                entryLogPassword.delete(0, 'end')
                messagebox.showinfo("Успіх!", "Ви увійшли в систему!")
                show_frame(frame_mainWindow)
            else:
                messagebox.showerror("Помилка", "Неправильний нік або пароль!")
    except ValueError:
        messagebox.showerror("Помилка", "Файл даних пошкоджено. Створіть новий профіль.")
        show_frame(frame_reg)

def logout():
    with open("session.txt", "w") as session_file:
        session_file.write("False")
    show_frame(frame_login)

def open_website(url):
    webbrowser.open(url)

def confirmationWindowOpenWebsiteID(url_to_open):
    confirmationWindow = tk.Toplevel(root)
    confirmationWindow.title("Перенаправлення")
    confirmationWindow.geometry("450x160")
    confirmationWindow.resizable(False, False)
    confirmationWindow.grab_set()
    
    confirmationLabel = Label(confirmationWindow, text="Ви залишаєте застосунок і перенаправляєтесь на вебсайт для отримання послуги.\n\nПідтвердити?", wraplength=350)
    confirmationLabel.pack(pady=10)
    
    frameButtonConfirm = Frame(confirmationWindow)
    frameButtonConfirm.pack(pady=10)
    buttonYes = Button(frameButtonConfirm, text="Так", bg="#43A047", fg="white", width=10, command=lambda: [open_website(url_to_open), confirmationWindow.destroy()])
    buttonYes.pack(side=LEFT, padx=10)
    buttonNo = Button(frameButtonConfirm, text="Ні", bg="#D32F2F", fg="white", width=10, command=confirmationWindow.destroy)
    buttonNo.pack(side=RIGHT, padx=10)

def checkAppState():
    is_logged_in = False
    if os.path.exists("session.txt"):
        with open("session.txt", "r") as session_file:
            if session_file.read().strip() == "True":
                is_logged_in = True

    if is_logged_in:
        show_frame(frame_mainWindow)
    elif os.path.exists("registration.txt") and os.path.getsize("registration.txt") > 1:
        show_frame(frame_login)
    else:
        show_frame(frame_reg)


# registration window

frame_reg = tk.Frame(root)
labelRegText = Label(frame_reg, text='СТВОРЕННЯ ПРОФІЛЮ')
labelRegText.pack(pady=10)

frameRegNick = Frame(frame_reg, bd=2, relief=RIDGE)
frameRegNick.pack(expand=1, fill=X, pady=10, padx=5)
labelRegLogin = Label(frameRegNick, text='Нік:')
labelRegLogin.pack(side=LEFT, padx=5)
entryRegLogin = Entry(frameRegNick)
entryRegLogin.pack(side=RIGHT, padx=5)

frameRegPassword = Frame(frame_reg, bd=2, relief=RIDGE)
frameRegPassword.pack(expand=1, fill=X, pady=10, padx=5)
labelRegPassword = Label(frameRegPassword, text='Пароль:')
labelRegPassword.pack(side=LEFT, padx=5)
entryRegPassword = Entry(frameRegPassword, show="*")
entryRegPassword.pack(side=RIGHT, padx=5)

buttonRegistration = Button(frame_reg, text='Зареєструвати', bg="#43A047", fg="white", command=registration)
buttonRegistration.pack(pady=15)
    
frame_login = tk.Frame(root)

labelLogText = Label(frame_login, text='АВТОРИЗАЦІЯ')
labelLogText.pack(pady=10)

frameLogNick = Frame(frame_login, bd=2, relief=RIDGE)
frameLogNick.pack(expand=1, fill=X, pady=10, padx=5)
labelLogLogin = Label(frameLogNick, text='Нік:')
labelLogLogin.pack(side=LEFT, padx=5)
entryLogLogin = Entry(frameLogNick)
entryLogLogin.pack(side=RIGHT, padx=5)

frameLogPassword = Frame(frame_login, bd=2, relief=RIDGE)
frameLogPassword.pack(expand=1, fill=X, pady=10, padx=5)
labelLogPassword = Label(frameLogPassword, text='Пароль:')
labelLogPassword.pack(side=LEFT, padx=5)
entryLogPassword = Entry(frameLogPassword, show="*")
entryLogPassword.pack(side=RIGHT, padx=5)

frameButtonLog = Frame(frame_login)
frameButtonLog.pack(pady=10)
buttonLogin = Button(frameButtonLog, text="Увійти", bg="#1E88E5", fg="white", command=login)
buttonLogin.pack(side=LEFT, padx=5)
buttonReset = Button(frameButtonLog, text="Скинути профіль", bg="#D32F2F", fg="white", command=lambda: show_frame(frame_reg))
buttonReset.pack(side=RIGHT, padx=5)

# main window

frame_mainWindow = tk.Frame(root)

buttonMyID = Button(frame_mainWindow, text="Оформити картку Кроспільця", width=30, command=lambda: confirmationWindowOpenWebsiteID("https://d1ndz1nd.github.io/krospil-card/"))
buttonMyID.pack()
buttonMyBankCard = Button(frame_mainWindow, text="Мій рахунок в КроспільБанк", width=30, state="disabled")
buttonMyBankCard.pack()
buttonEstateShop = Button(frame_mainWindow, text="Ринок нерухомості", width=30, state="disabled")
buttonEstateShop.pack()
buttonLogOut = Button(frame_mainWindow, text="Вийти", bg="#D32F2F", fg="white", command=logout, width=30)
buttonLogOut.pack(pady=10)

checkAppState()
root.mainloop()
