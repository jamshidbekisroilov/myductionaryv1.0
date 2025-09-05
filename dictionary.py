import tkinter as tk
from tkinter import messagebox
from database import get_connection

class DictionaryManager:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

    def show_create_dictionary(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        entry_font = ("Arial", 20)
        button_font = ("Arial", 18, "bold")

        tk.Label(self.frame, text="Lug'at nomi:", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.frame, font=entry_font, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="O'rganilayotgan til:", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.language_entry = tk.Entry(self.frame, font=entry_font, width=25)
        self.language_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame, text="Yaratish", font=button_font,
                  bg="#4CAF50", fg="white", command=self.create_dictionary).grid(row=2, columnspan=2, pady=20)
        tk.Button(self.frame, text="← Orqaga", font=button_font,
                  bg="#f44336", fg="white", command=self.back_to_main_menu).grid(row=3, columnspan=2, pady=10)

    def create_dictionary(self):
        name = self.name_entry.get().strip()
        target_language = self.language_entry.get().strip()

        if not name or not target_language:
            messagebox.showerror("Xatolik", "Iltimos, barcha maydonlarni to'ldiring.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                target_language TEXT NOT NULL
            )
        """)

        cursor.execute("INSERT INTO dictionaries (user_id, name, target_language) VALUES (?, ?, ?)",
                       (self.user_id, name, target_language))
        conn.commit()
        conn.close()

        messagebox.showinfo("Yaratildi", f"'{name}' lug'ati yaratildi!")
        self.frame.destroy()
        self.show_my_dictionaries()

    def show_my_dictionaries(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        button_font = ("Arial", 16, "bold")

        tk.Label(self.frame, text="Mening lug'atlarim:", font=label_font).pack(pady=10)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, target_language FROM dictionaries WHERE user_id = ?", (self.user_id,))
        dictionaries = cursor.fetchall()
        conn.close()

        if not dictionaries:
            tk.Label(self.frame, text="Hozircha lug'at yo'q. Yangi lug'at yarating.", font=("Arial", 16)).pack(pady=10)
            tk.Button(self.frame, text="Yangi lug'at yaratish", font=button_font,
                     bg="#4CAF50", fg="white", command=self.show_create_dictionary).pack(pady=5)
        else:
            for dic in dictionaries:
                dic_id, name, lang = dic
                btn_text = f"{name} ({lang})"
                tk.Button(self.frame, text=btn_text, font=button_font, width=30,
                         bg="#133FDF", fg="white", command=lambda d_id=dic_id: self.open_dictionary(d_id)).pack(pady=5)

            tk.Button(self.frame, text="Yangi lug'at yaratish", font=button_font,
                      bg="#4CAF50", fg="white",command=self.show_create_dictionary).pack(pady=20)

        tk.Button(self.frame, text="← Orqaga", font=button_font,
                  bg="#f44336", fg="white", command=self.back_to_main_menu).pack(pady=10)

    def open_dictionary(self, dictionary_id):
        self.frame.destroy()
        from word_entry import WordEntry
        word_entry = WordEntry(self.root, dictionary_id, self.user_id)
        word_entry.show_options()


    def back_to_main_menu(self):
        self.frame.destroy()
        from user import UserManager
        user_manager = UserManager(self.root, on_success=lambda: self.show_my_dictionaries())
        user_manager.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
