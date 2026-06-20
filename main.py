import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import string

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.history = load_history()

        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        self.build_ui()
        self.update_history_display()

    def build_ui(self):
        # Настройки
        settings_frame = tk.LabelFrame(self.root, text="Настройки пароля", padx=10, pady=10)
        settings_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(settings_frame, text="Длина:").grid(row=0, column=0, sticky="w")
        self.length_scale = tk.Scale(settings_frame, from_=4, to=30, orient="horizontal",
                                     variable=self.length_var, length=200)
        self.length_scale.grid(row=0, column=1, padx=10)
        self.length_label = tk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2)
        self.length_scale.config(command=lambda v: self.length_label.config(text=str(int(float(v)))))

        cb_frame = tk.Frame(settings_frame)
        cb_frame.grid(row=1, column=0, columnspan=3, pady=5)
        tk.Checkbutton(cb_frame, text="Цифры", variable=self.use_digits).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(cb_frame, text="Заглавные (A-Z)", variable=self.use_uppercase).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(cb_frame, text="Строчные (a-z)", variable=self.use_lowercase).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(cb_frame, text="Спецсимволы", variable=self.use_special).pack(side=tk.LEFT, padx=5)

        # Кнопка генерации
        btn_generate = tk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password,
                                 bg="#4CAF50", fg="white", font=("Arial", 12))
        btn_generate.pack(pady=10)

        # Поле для пароля
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(self.root, textvariable=self.password_var, font=("Arial", 14),
                                  justify="center", state="readonly", width=40)
        password_entry.pack(pady=5)
        btn_copy = tk.Button(self.root, text="Копировать в буфер", command=self.copy_to_clipboard)
        btn_copy.pack(pady=5)

        # История
        history_frame = tk.LabelFrame(self.root, text="История паролей", padx=10, pady=10)
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(history_frame, columns=("password",), show="headings", height=8)
        self.tree.heading("password", text="Сгенерированные пароли")
        self.tree.column("password", width=480, anchor="center")
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_clear = tk.Button(self.root, text="Очистить историю", command=self.clear_history, bg="#f44336", fg="white")
        btn_clear.pack(pady=5)

    def generate_password(self):
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_special.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
            return

        length = self.length_var.get()
        password = ''.join(random.choices(chars, k=length))
        self.password_var.set(password)

        self.history.append(password)
        save_history(self.history)
        self.update_history_display()

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена.")
        else:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте пароль.")

    def update_history_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pwd in self.history:
            self.tree.insert("", tk.END, values=(pwd,))

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            save_history(self.history)
            self.update_history_display()
            self.password_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
