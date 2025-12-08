import tkinter as tk
# import subprocess
# import os
import krisna_create
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Vending Machine")
root.geometry("600x700")
root.config(bg="orange")

# ======================= DATA PRODUK =======================
produk = {
    "01": {"nama": "Mineral Water", "harga": 3000, "img": "img/mineral.png", "stok": 99},
    "02": {"nama": "Milk", "harga": 15000, "img": "img/milk.png", "stok": 99},
    "03": {"nama": "Coca Cola", "harga": 5000, "img": "img/cola.png", "stok": 99},
    "04": {"nama": "Orange Juice", "harga": 6000, "img": "img/orange.png", "stok": 99},
    "05": {"nama": "Coffee", "harga": 4000, "img": "img/coffe.png", "stok": 99},
    "06": {"nama": "Pepsi", "harga": 25000, "img": "img/pepsi.png", "stok": 99},
    "07": {"nama": "Yoghurt", "harga": 10000, "img": "img/yogurt.png", "stok": 99},
    "08": {"nama": "Yakult", "harga": 5000, "img": "img/yakult.png", "stok": 99},
    "09": {"nama": "Potato Chips", "harga": 8000, "img": "img/potato.png", "stok": 99},
    "10": {"nama": "Popcorn", "harga": 14000, "img": "img/popcorn.png", "stok": 99},
    "11": {"nama": "Doritos", "harga": 12000, "img": "img/doritos.png", "stok": 99},
    "12": {"nama": "Chiki Balls", "harga": 10000, "img": "img/chiki.png", "stok": 99},
    "13": {"nama": "Crackers", "harga": 12000, "img": "img/crackers.png", "stok": 99},
    "14": {"nama": "Oreo", "harga": 8000, "img": "img/oreo.png", "stok": 99},
    "15": {"nama": "Chocopie", "harga": 5000, "img": "img/chocopie.png", "stok": 99},
}

ADMIN_PASS = "1234"

# ======================= CLEAR =======================
def clear():
    for w in root.winfo_children():
        w.destroy()

# ======================= MAIN MENU =======================
def main_menu():
    clear()
    tk.Label(root, text="VENDING MACHINE",
             font=("Arial",20,"bold"),
             bg="orange", fg="white").pack(pady=20)

    tk.Button(root, text="BELANJA", font=("Arial",16),
              bg="white", width=20, command=menu_belanja).pack(pady=10)

    tk.Button(root, text="ADMIN", font=("Arial",16),
              bg="white", width=20, command=login_admin).pack(pady=10)

# ======================= LOGIN ADMIN =======================
def login_admin():
    clear()
    tk.Label(root, text="LOGIN ADMIN", font=("Arial",18,"bold"),
             bg="orange", fg="white").pack(pady=20)

    entry = tk.Entry(root, show="*", font=("Arial",16))
    entry.pack(pady=10)

    def cek():
        if entry.get() == ADMIN_PASS:
            menu_admin()
        else:
            messagebox.showerror("Error", "Password salah!")

    tk.Button(root, text="LOGIN", bg="white", command=cek).pack(pady=10)
    tk.Button(root, text="Kembali", command=main_menu).pack()

# ======================= MENU ADMIN =======================
def menu_admin():
    clear()
    tk.Label(root, text="MENU ADMIN", font=("Arial",18,"bold"),
             bg="orange", fg="white").pack(pady=20)

    tk.Button(root, text="Tambah Produk", width=20, command=tambah_produk).pack(pady=5)
    tk.Button(root, text="Update Produk", width=20, command=update_produk).pack(pady=5)
    tk.Button(root, text="Hapus Produk", width=20, command=hapus_produk).pack(pady=5)
    tk.Button(root, text="Kembali", command=main_menu).pack(pady=10)

# ======================= TAMBAH PRODUK =======================
def tambah_produk():
    clear()
    tk.Label(root, text="Tambah Produk", font=("Arial",18,"bold"),
             bg="orange", fg="white").pack(pady=10)
    
    krisna_create.create_window()

    tk.Button(root, text="Kembali", command=menu_admin).pack()
    
    # ======================= UPDATE PRODUK =======================
def update_produk():
    clear()
    tk.Label(root, text="Update Produk", font=("Arial",18,"bold"),
             bg="orange", fg="white").pack(pady=10)
    
    # LANGSUNG BUKA WINDOW UPDATE.PY
    import update
    update.create_window()
    
    tk.Button(root, text="Kembali", command=menu_admin).pack(pady=20)
    
    # ======================= HAPUS =======================
def hapus_produk():
    clear()
    tk.Label(root, text="Hapus Produk", font=("Arial",18)).pack(pady=10)

    e_kode = tk.Entry(root); e_kode.pack()

    def hapus():
        if e_kode.get() in produk:
            del produk[e_kode.get()]
            messagebox.showinfo("Sukses", "Produk dihapus")
            menu_admin()
        else:
            messagebox.showerror("Error", "Kode tidak ada")

    tk.Button(root, text="Hapus", command=hapus).pack(pady=10)
    tk.Button(root, text="Kembali", command=menu_admin).pack()

# ======================= MENU BELANJA =======================
def menu_belanja():
    clear()

    tk.Label(root, text="BELANJA", font=("Arial", 18, "bold"),
             bg="orange", fg="white").pack(pady=5)

    # ================= CONTAINER =================
    container = tk.Frame(root, bg="orange")
    container.pack(fill="both", expand=True)

    # ========== KIRI (PRODUK) ==========
    frame_kiri = tk.Frame(container, bg="orange")
    frame_kiri.pack(side="left", padx=10, anchor="n")

    global img_cache
    img_cache = []

    row = col = 0
    for kode, data in produk.items():
        item = tk.Frame(frame_kiri, bg="orange", padx=5, pady=5)
        item.grid(row=row, column=col)

        try:
            img = Image.open(data["img"]).resize((60, 60))
            img = ImageTk.PhotoImage(img)
            img_cache.append(img)
            tk.Label(item, image=img).pack()
        except:
            tk.Label(item, text="(No Image)").pack()

        tk.Label(item, text=f"{kode}\n{data['nama']}\nRp{data['harga']}",
                 bg="orange", font=("Arial", 8)).pack()

        col += 1
        if col == 4:
            col = 0
            row += 1

    # ========== KANAN (PANEL) ==========
    frame_kanan = tk.Frame(container, bg="orange")
    frame_kanan.pack(side="right", padx=10, anchor="n")

    # Tombol mode
    mode = tk.StringVar(value="uang")

    def set_uang():
        nonlocal mode_var
        mode_var = "uang"
        info_label.config(text="Mode: Masukkan Uang")

    def set_kode():
        nonlocal mode_var
        mode_var = "kode"
        info_label.config(text="Mode: Masukkan Kode")

    mode_var = "uang"
    tk.Button(frame_kanan, text="Masukkan Uang", width=20,
              command=set_uang).pack(pady=2)

    tk.Button(frame_kanan, text="Masukkan Kode Produk", width=20,
              command=set_kode).pack(pady=2)

    # Monitor
    info_label = tk.Label(frame_kanan, text="Mode: Masukkan Uang",
                          bg="white", width=22, height=2)
    info_label.pack(pady=5)

    display = tk.Label(frame_kanan, text="", font=("Arial", 18, "bold"),
                       bg="black", fg="lime", width=16, height=2)
    display.pack(pady=5)

    input_value = ""

    def tekan(angka):
        nonlocal input_value
        input_value += angka
        display.config(text=input_value)

    def clear_input():
        nonlocal input_value
        input_value = ""
        display.config(text="")

    def ok():
        nonlocal input_value
        if mode_var == "uang":
            info_label.config(text=f"Uang: Rp {input_value}")
        else:
            if input_value in produk:
                info_label.config(text=f"Pilih: {produk[input_value]['nama']}")
            else:
                info_label.config(text="Kode tidak ditemukan")
        input_value = ""
        display.config(text="")

    # ================= KEYPAD =================
    panel = tk.Frame(frame_kanan, bg="orange")
    panel.pack(pady=5)

    btns = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2)
    ]

    for (text, r, c) in btns:
        tk.Button(panel, text=text, width=5, height=2,
                  command=lambda v=text: tekan(v)).grid(row=r, column=c, padx=2, pady=2)

    tk.Button(panel, text="Clear", bg="yellow", width=5, height=2,
              command=clear_input).grid(row=3, column=0, padx=2, pady=2)

    tk.Button(panel, text="0", width=5, height=2,
              command=lambda: tekan("0")).grid(row=3, column=1, padx=2, pady=2)

    tk.Button(panel, text="OK", bg="green", fg="white", width=5, height=2,
              command=ok).grid(row=3, column=2, padx=2, pady=2)

main_menu()
root.mainloop()