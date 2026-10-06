import tkinter as tk
from tkinter import messagebox
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


USERS = {
    "admin": hash_password("1234"),
    "user": hash_password("qwerty"),
}

MAX_ATTEMPTS = 3
attempts_left = MAX_ATTEMPTS


def toggle_password_visibility():
    if show_password_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")


def check_login(event=None):
    global attempts_left

    login = entry_login.get().strip()
    password = entry_password.get()

    if not login or not password:
        messagebox.showwarning("Внимание", "Заполните все поля!")
        return

    password_hash = hash_password(password)

    if login in USERS and USERS[login] == password_hash:
        messagebox.showinfo("Успех", f"Добро пожаловать, {login}!")
    else:
        attempts_left -= 1

        if attempts_left > 0:
            messagebox.showerror(
                "Ошибка",
                f"Неверный логин или пароль,\nОсталось попыток: {attempts_left}"
            )
        else:
            messagebox.showerror(
                "Блокировка",
                "Превышено число попыток. Приложение будет закрыто."
            )
            root.destroy()
            return

    entry_password.delete(0, tk.END)
    entry_password.focus()


root = tk.Tk()
root.title("Авторизация")
root.geometry("360x320")
root.resizable(False, False)

label_title = tk.Label(root, text="Вход в систему", font=("Arial", 16, "bold"))
label_title.pack(pady=15)

label_login = tk.Label(root, text="Логин:")
label_login.pack(anchor="w", padx=40)

entry_login = tk.Entry(root, width=30)
entry_login.pack(pady=5)
entry_login.focus()

label_password = tk.Label(root, text="Пароль:")
label_password.pack(anchor="w", padx=40)

entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack(pady=5)

show_password_var = tk.BooleanVar(value=False)
check_show = tk.Checkbutton(
    root,
    text="Показать пароль",
    variable=show_password_var,
    command=toggle_password_visibility
)
check_show.pack(anchor="w", padx=40)

btn_login = tk.Button(
    root,
    text="Войти",
    width=15,
    command=check_login,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    cursor="hand2"
)
btn_login.pack(pady=20)

root.bind("<Return>", check_login)

root.mainloop()