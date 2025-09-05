import tkinter as tk
from tkinter import messagebox
from database import get_connection
import random

class WordEntry:
    def __init__(self, root, dictionary_id, user_id):
        self.root = root
        self.dictionary_id = dictionary_id
        self.user_id = user_id
    def get_user_id(self):
        return self.user_id
    def show_word_list(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        tk.Label(self.frame, text="📋 Kiritilgan so'zlar", font=label_font).pack(pady=10)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT native_word, target_word FROM words WHERE dictionary_id = ?", (self.dictionary_id,))
        words = cursor.fetchall()
        conn.close()

        if not words:
            tk.Label(self.frame, text="Hozircha so'zlar yo'q.", font=("Arial", 16)).pack(pady=10)
        else:
            for native, target in words:
                tk.Label(self.frame, text=f"{native} → {target}", font=("Arial", 16)).pack()

        tk.Button(self.frame, text="← Orqaga", font=("Arial", 16, "bold"),
                 bg="#f44336", fg="white", command=self.show_options).pack(pady=20)
    def show_mistakes(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        tk.Label(self.frame, text="❌ Noto'g'ri javoblar", font=label_font).pack(pady=10)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictionary_id INTEGER,
                native_word TEXT,
                correct_answer TEXT,
                user_answer TEXT
            )
        """)
        cursor.execute("SELECT native_word, correct_answer, user_answer FROM mistakes WHERE dictionary_id = ?", (self.dictionary_id,))
        mistakes = cursor.fetchall()
        conn.close()

        if not mistakes:
            tk.Label(self.frame, text="Hozircha xatolar yo'q.", font=("Arial", 16)).pack(pady=10)
        else:
            for native, correct, user in mistakes:
                text = f"{native} → Siz: '{user}' | To'g'ri: '{correct}'"
                tk.Label(self.frame, text=text, font=("Arial", 16), fg="red").pack(anchor="w", padx=20)

        tk.Button(self.frame, text="← Orqaga", font=("Arial", 16, "bold"),
              bg="#f44336", fg="white", command=self.show_options).pack(pady=20)



    def show_options(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        button_font = ("Arial", 16, "bold")

        tk.Label(self.frame, text="Lug'at menyusi", font=label_font).pack(pady=10)

        tk.Button(self.frame, text="Yangi so'z qo'shish", font=button_font, width=25,
                 bg="#4CAF50", fg="white", command=self.add_words).pack(pady=5)

        tk.Button(self.frame, text="Takrorlash", font=button_font, width=25,
                 bg="#4CAF50", fg="white", command=self.start_quiz).pack(pady=5)
        tk.Button(self.frame, text="← Mening lug'atlarimga qaytish", font=button_font,
                 bg="#f44336", fg="white", command=self.back_to_dictionary_list).pack(pady=10)
        tk.Button(self.frame, text="📋 So'zlar ro'yxati", font=button_font,
          bg="#2196F3", fg="white", command=self.show_word_list).pack(pady=5)
        tk.Button(self.frame, text="❌ Xatolar ro'yxati", font=button_font,
          bg="#FF9800", fg="white", command=self.show_mistakes).pack(pady=5)



    def add_words(self):
        self.clear_window()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        label_font = ("Arial", 20)
        entry_font = ("Arial", 20)
        button_font = ("Arial", 16, "bold")

        tk.Label(self.frame, text="Ona tilidagi so'z:", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.native_entry = tk.Entry(self.frame, font=entry_font, width=25)
        self.native_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Tarjimasi:", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.target_entry = tk.Entry(self.frame, font=entry_font, width=25)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame, text="Qo'shish", font=button_font,
                  bg="#4CAF50", fg="white", command=self.save_word).grid(row=2, columnspan=2, pady=20)
        tk.Button(self.frame, text="← Orqaga", font=button_font,
                 bg="#f44336", fg="white", command=self.back_to_menu).grid(row=3, columnspan=2, pady=10)

    def save_word(self):
        native_word = self.native_entry.get().strip()
        target_word = self.target_entry.get().strip()

        if not native_word or not target_word:
            messagebox.showerror("Xatolik", "Iltimos, har ikki so'zni kiriting.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictionary_id INTEGER,
                native_word TEXT,
                target_word TEXT
            )
        """)

        cursor.execute("""
            SELECT id FROM words
            WHERE dictionary_id = ? AND native_word = ? AND target_word = ?
        """, (self.dictionary_id, native_word, target_word))
        existing = cursor.fetchone()

        if existing:
            messagebox.showwarning("Eslatma", f"'{native_word}' → '{target_word}' so'zi allaqachon mavjud.")
            return

        # ✅ Yangi so'zni qo'shish
        cursor.execute("INSERT INTO words (dictionary_id, native_word, target_word) VALUES (?, ?, ?)",
                        (self.dictionary_id, native_word, target_word))

        messagebox.showinfo("Qo'shildi", f"'{native_word}' → '{target_word}' so'zi saqlandi.")
        self.native_entry.delete(0, tk.END)
        self.target_entry.delete(0, tk.END)

    def start_quiz(self):
        self.clear_window()

        self.correct_count = 0
        self.incorrect_count = 0
        self.total_questions = 0
        self.max_questions = 20

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        self.label_font = ("Arial", 20)
        self.entry_font = ("Arial", 20)
        self.button_font = ("Arial", 16, "bold")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT native_word, target_word FROM words WHERE dictionary_id = ?", (self.dictionary_id,))
        self.words = cursor.fetchall()
        conn.close()

        if not self.words:
            tk.Label(self.frame, text="Bu lug'atda hali so'zlar yo'q.", font=self.label_font).pack(pady=10)
            tk.Button(self.frame, text="← Orqaga", font=self.button_font,
                      bg="#f44336", fg="white", command=self.show_options).pack(pady=10)
            return

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 18), fg="blue")
        self.status_label.pack(pady=10)

        self.show_next_question()
    def show_next_question(self):
        if self.total_questions >= self.max_questions:
            self.show_summary()
            return

        self.total_questions += 1
        self.current_word = random.choice(self.words)
        native = self.current_word[0]

        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text=f"{self.total_questions}. '{native}' so'zining tarjimasini kiriting:", font=self.label_font).pack(pady=10)
        self.answer_entry = tk.Entry(self.frame, font=self.entry_font, width=25)
        self.answer_entry.pack(pady=10)

        tk.Button(self.frame, text="Tekshirish", font=self.button_font,
                  bg="#4CAF50", fg="white", command=self.check_answer).pack(pady=5)

        tk.Button(self.frame, text="← Orqaga", font=self.button_font,
                  bg="#f44336", fg="white", command=self.show_options).pack(pady=5)

        # 🆕 Har bir savolda status_label qayta yaratiladi
        self.status_label = tk.Label(self.frame, text="", font=("Arial", 18), fg="blue")
        self.status_label.pack(pady=10)



    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_word[1].lower()
        native_word = self.current_word[0]

        conn = get_connection()
        cursor = conn.cursor()

        # Xatolar jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictionary_id INTEGER,
                native_word TEXT,
                correct_answer TEXT,
                user_answer TEXT
            )
        """)

        if user_answer == correct_answer:
            self.correct_count += 1
            self.status_label.config(text=f"✅ To'g'ri javob: {correct_answer}", fg="green")
        else:
            self.incorrect_count += 1
            self.status_label.config(text=f"❌ Noto'g'ri. To'g'ri javob: {correct_answer}", fg="red")

            # ❌ Xatoni saqlaymiz
            cursor.execute("INSERT INTO mistakes (dictionary_id, native_word, correct_answer, user_answer) VALUES (?, ?, ?, ?)",
                       (self.dictionary_id, native_word, correct_answer, user_answer))

        conn.commit()
        conn.close()

        self.answer_entry.delete(0, tk.END)
        self.root.after(1000, self.show_next_question)
    def show_summary(self):
        self.clear_window()

        summary_frame = tk.Frame(self.root)
        summary_frame.pack(pady=50)

        total = self.correct_count + self.incorrect_count
        percent = round((self.correct_count / total) * 100, 1) if total > 0 else 0

        tk.Label(summary_frame, text="📊 Test yakuni", font=("Arial", 22, "bold")).pack(pady=10)
        tk.Label(summary_frame, text=f"To'g'ri javoblar: {self.correct_count}", font=("Arial", 18), fg="green").pack(pady=5)
        tk.Label(summary_frame, text=f"Noto'g'ri javoblar: {self.incorrect_count}", font=("Arial", 18), fg="red").pack(pady=5)
        tk.Label(summary_frame, text=f"Eslab qolish darajasi: {percent}%", font=("Arial", 18), fg="blue").pack(pady=5)

        tk.Button(summary_frame, text="← Bosh menyuga qaytish", font=("Arial", 16, "bold"),
                 bg="#f0f0f0", fg="black", command=self.show_options).pack(pady=20)



    def back_to_menu(self):
        self.frame.destroy()
        self.show_options()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def back_to_dictionary_list(self):
        self.frame.destroy()
        from dictionary import DictionaryManager
        dictionary_manager = DictionaryManager(self.root, user_id=self.get_user_id())
        dictionary_manager.show_my_dictionaries()

