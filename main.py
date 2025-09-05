import tkinter as tk
from database import init_db
from user import UserManager
from dictionary import DictionaryManager

def main():
    init_db()

    root = tk.Tk()
    root.title("MyDuctionary")
    root.geometry("800x600")

    def after_login():
        user_id = 1  # Hozircha statik, keyinchalik dinamik bo'ladi
        dictionary_manager = DictionaryManager(root, user_id)
        dictionary_manager.show_my_dictionaries()

    user_manager = UserManager(root, on_success=after_login)
    user_manager.show_login()

    root.mainloop()

if __name__ == "__main__":
    main()
