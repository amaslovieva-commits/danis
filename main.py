import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("650x500")

        self.books = self.load_data()

        # Интерфейс ввода
        input_frame = tk.LabelFrame(root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(input_frame)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2)
        self.author_entry = tk.Entry(input_frame)
        self.author_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, pady=5)
        self.genre_entry = tk.Entry(input_frame)
        self.genre_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2)
        self.pages_entry = tk.Entry(input_frame)
        self.pages_entry.grid(row=1, column=3, padx=5)

        tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="green", fg="white").grid(row=2, column=0, columnspan=4, pady=10)

        # Интерфейс фильтрации
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre_entry = tk.Entry(filter_frame)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)

        tk.Button(filter_frame, text="Фильтр по жанру", command=self.filter_by_genre).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="Больше 200 стр.", command=self.filter_long_books).grid(row=0, column=3, padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.refresh_table).grid(row=0, column=4, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страницы")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Валидация
        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
        self.books.append(new_book)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        for entry in (self.title_entry, self.author_entry, self.genre_entry, self.pages_entry):
            entry.delete(0, tk.END)

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_data = data if data is not None else self.books
        for b in display_data:
            self.tree.insert("", tk.END, values=(b["title"], b["author"], b["genre"], b["pages"]))

    def filter_by_genre(self):
        query = self.filter_genre_entry.get().strip().lower()
        results = [b for b in self.books if query in b["genre"].lower()]
        self.refresh_table(results)

    def filter_long_books(self):
        results = [b for b in self.books if b["pages"] > 200]
        self.refresh_table(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
