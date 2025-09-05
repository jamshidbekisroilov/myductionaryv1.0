import tkinter as tk
from tkinter import messagebox
from database import get_connection

class UserManager:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

    def show_login(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=50)

        label_font = ("Arial", 20)
        entry_font = ("Arial", 20)
        button_font = ("Arial", 20, "bold")

        tk.Label(self.frame, text="Ismingiz:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(self.frame, font=entry_font, width=20)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Familiyangiz:", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.surname_entry = tk.Entry(self.frame, font=entry_font, width=20)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Ona tilingiz:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.language_entry = tk.Entry(self.frame, font=entry_font, width=20)
        self.language_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Ro'yxatdan o'tish", font=button_font,
                  bg="#4CAF50", fg="white", command=self.register_user).grid(row=3, columnspan=2, pady=20)

    def register_user(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        language = self.language_entry.get().strip()

        if not name or not surname or not language:
            messagebox.showerror("Xatolik", "Iltimos, barcha maydonlarni to'ldiring.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, surname, native_language) VALUES (?, ?, ?)",
                       (name, surname, language))
        conn.commit()
        conn.close()

        messagebox.showinfo("Tabriklaymiz", f"Xush kelibsiz, {name}!")
        self.frame.destroy()
        self.on_success()
