import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Файл для хранения истории
        self.history_file = "password_history.json"
        self.history = self.load_history()
        
        # Переменные для параметров
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка истории в таблицу
        self.update_history_table()
    
    def create_widgets(self):
        # Рамка настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Ползунок длины пароля
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        
        ttk.Label(length_frame, text="Длина пароля:").pack(side="left", padx=5)
        self.length_scale = ttk.Scale(length_frame, from_=4, to=50, variable=self.password_length, orient="horizontal")
        self.length_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.length_label = ttk.Label(length_frame, textvariable=self.password_length, width=5)
        self.length_label.pack(side="right", padx=5)
        
        # Чекбоксы
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill="x", pady=5)
        
        ttk.Checkbutton(options_frame, text="Цифры (0-9)", variable=self.use_digits).pack(side="left", padx=10)
        ttk.Checkbutton(options_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).pack(side="left", padx=10)
        ttk.Checkbutton(options_frame, text="Спецсимволы (!@#$...)", variable=self.use_symbols).pack(side="left", padx=10)
        
        # Кнопка генерации
        generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=10)
        
        # Поле для отображения пароля
        result_frame = ttk.LabelFrame(self.root, text="Сгенерированный пароль", padding=10)
        result_frame.pack(fill="x", padx=10, pady=5)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(result_frame, textvariable=self.password_var, font=("Courier", 12), state="readonly")
        password_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        copy_btn = ttk.Button(result_frame, text="Копировать", command=self.copy_to_clipboard)
        copy_btn.pack(side="right", padx=5)
        
        # Таблица истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview с прокруткой
        columns = ("datetime", "length", "params", "password")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("datetime", text="Дата/время")
        self.tree.heading("length", text="Длина")
        self.tree.heading("params", text="Использованные символы")
        self.tree.heading("password", text="Пароль")
        
        self.tree.column("datetime", width=140)
        self.tree.column("length", width=50)
        self.tree.column("params", width=150)
        self.tree.column("password", width=200)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка очистки истории
        clear_btn = ttk.Button(history_frame, text="Очистить историю", command=self.clear_history)
        clear_btn.pack(pady=5)
    
    def generate_password(self):
        # Проверка, что выбран хотя бы один набор символов
        if not (self.use_digits.get() or self.use_letters.get() or self.use_symbols.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        length = self.password_length.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Длина пароля не может быть меньше 4!")
            return
        if length > 50:
            messagebox.showerror("Ошибка", "Длина пароля не может быть больше 50!")
            return
        
        # Формируем пул символов
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
        
        if not chars:
            return
        
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Сохраняем в историю
        params = []
        if self.use_digits.get():
            params.append("цифры")
        if self.use_letters.get():
            params.append("буквы")
        if self.use_symbols.get():
            params.append("спецсимволы")
        params_str = ", ".join(params)
        
        history_entry = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "length": length,
            "params": params_str,
            "password": password
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history_table()
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Нет сгенерированного пароля для копирования.")
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def update_history_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Вставляем записи из истории (последние сверху)
        for entry in reversed(self.history):
            self.tree.insert("", "end", values=(
                entry["datetime"],
                entry["length"],
                entry["params"],
                entry["password"]
            ))
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы действительно хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Готово", "История очищена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
