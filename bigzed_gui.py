
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

default_mapping = {
    "A": "#", "B": "$", "C": "%", "D": "&", "E": "*", "F": "1", "G": "2", "H": "3",
    "I": "4", "J": "5", "K": "6", "L": "7", "M": "8", "N": "9", "O": "0", "P": "@",
    "Q": "!", "R": "^", "S": "~", "T": "`", "U": "+", "V": "-", "W": "=", "X": "{",
    "Y": "}", "Z": ":"
}

mapping_file = "bigzed_klavye.json"

def load_mapping():
    if os.path.exists(mapping_file):
        with open(mapping_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_mapping.copy()

def save_mapping(mapping):
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

def encrypt(text, mapping):
    return "".join([mapping.get(c.upper(), c) for c in text])

def decrypt(text, mapping):
    reverse = {v: k for k, v in mapping.items()}
    return "".join([reverse.get(c, c) for c in text])

def edit_mapping():
    mapping = load_mapping()
    for harf in sorted(default_mapping.keys()):
        val = simpledialog.askstring("Eşle", f"{harf} harfi için karakter:", initialvalue=mapping.get(harf, ""))
        if val:
            mapping[harf] = val
    save_mapping(mapping)
    messagebox.showinfo("BİGZED", "Yeni eşleşmeler kaydedildi!")

def open_translator():
    mapping = load_mapping()

    def convert():
        encrypted = input_text.get("1.0", "end").strip()
        decrypted = decrypt(encrypted, mapping)
        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", decrypted)
        output_text.config(state="disabled")

    trans_win = tk.Toplevel()
    trans_win.title("🧾 Şifreyi Çöz / Göster")
    trans_win.geometry("400x300")

    tk.Label(trans_win, text="Şifreli Metin:", font=("Arial", 10)).pack()
    input_text = tk.Text(trans_win, height=5)
    input_text.pack()

    tk.Button(trans_win, text="Çevir", command=convert).pack(pady=5)

    tk.Label(trans_win, text="Çözülmüş Metin:", font=("Arial", 10)).pack()
    output_text = tk.Text(trans_win, height=5, state="disabled")
    output_text.pack()

def show_result(title, content):
    result_win = tk.Toplevel()
    result_win.title(title)
    result_win.geometry("400x200")
    tk.Label(result_win, text=title, font=("Arial", 12, "bold")).pack(pady=5)
    result_box = tk.Text(result_win, height=6)
    result_box.pack(padx=10, pady=10)
    result_box.insert("1.0", content)
    result_box.config(state="normal")

def main():
    mapping = load_mapping()

    def run_encrypt():
        metin = simpledialog.askstring("Şifrele", "Şifrelenecek metni gir:")
        if metin:
            sonuc = encrypt(metin, mapping)
            show_result("🔐 Şifrelenmiş Metin", sonuc)

    def run_decrypt():
        metin = simpledialog.askstring("Çöz", "Çözülecek metni gir:")
        if metin:
            sonuc = decrypt(metin, mapping)
            show_result("🔓 Çözülmüş Metin", sonuc)

    root = tk.Tk()
    root.title("🛡️ BİGZED ŞİFRELEME")
    root.geometry("300x350")
    tk.Label(root, text="BİGZED ŞİFRELEME", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(root, text="🧠 Tuş Eşlemesini Ayarla", command=edit_mapping).pack(pady=5)
    tk.Button(root, text="🔐 Şifrele", command=run_encrypt).pack(pady=5)
    tk.Button(root, text="🔓 Çöz", command=run_decrypt).pack(pady=5)
    tk.Button(root, text="🧾 Şifreyi Çöz / Göster", command=open_translator).pack(pady=5)
    tk.Button(root, text="🚪 Çık", command=root.destroy).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
