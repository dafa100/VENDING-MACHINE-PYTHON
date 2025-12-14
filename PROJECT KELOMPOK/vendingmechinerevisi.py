import tkinter as tk
import mysql.connector
import time,os
# buat ngimpor gambar dari folder UAS_ALGORITMA di laptop ini
IMAGE_DIR = "gambar_produk"
MULTITAP = {
    "1": ["1", "a", "b", "c"],
    "2": ["2", "d", "e", "f"],
    "3": ["3", "g", "h", "i"],
    "4": ["4", "j", "k", "l"],
    "5": ["5", "m", "n", "o"],
    "6": ["6", "p", "q", "r"],
    "7": ["7", "s", "t", "u"],
    "8": ["8", "v", "w", "x"],
    "9": ["9", "x", "y", "z"],
    "0": ["0"],
}
def load_products_from_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="",          
            database="db_vending"
        )
        cur = conn.cursor()
        cur.execute("SELECT id_produk, nama_barang, harga_barang, gambar_produk FROM produk ORDER BY id_produk")
        rows = cur.fetchall()
        conn.close()

        products = []
        for idp, nama, harga, gambar in rows:
            # bersihkan gambar jika masih ada path lama
            if gambar.startswith(IMAGE_DIR + "/") or gambar.startswith(IMAGE_DIR + "\\"):
                gambar = os.path.basename(gambar)
            # gabungkan path lengkap untuk gambar
            full_path = os.path.join(IMAGE_DIR, gambar)
            products.append((idp, nama, harga, full_path))
        return products

    except Exception as e:
        print("Gagal load dari MySQL:", e)
        return []
    
def insert_product_to_mysql(nama, harga, gambar):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_vending"
        )
        cur = conn.cursor()

        # simpan nama file saja, bukan path lengkap
        filename = os.path.basename(gambar)

        # kalau id_produk auto increment, jangan diisi.
        sql = "INSERT INTO produk (nama_barang, harga_barang, gambar_produk) VALUES (%s, %s, %s)"
        cur.execute(sql, (nama, harga, filename))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Gagal INSERT:", e)
        return False
PRODUCTS = []
db_products = load_products_from_mysql()
if db_products:
    PRODUCTS = db_products
HAS_PRODUCTS = bool(PRODUCTS)

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self, bg="#123953", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#123953")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # aktifkan scroll pakai scrollwheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesin Penjualan Otomatis KELOMPOK 3")

        self.text = tk.StringVar()
        self.msg = tk.StringVar()
        self.last_key = None
        self.last_time = 0
        self.tap = 0
        self.timeout = 0.8

        # mode: menu pilih admin/belanja, pass = layar password, shop = belanja
        self.mode = "menu"
        self.admin_pass = "1234"   # password admin
        self.pass_buf = ""         # penampung input password

        # untuk fitur tambah barang (admin_add)
        self.admin_add_step = 0   # 0 = belum, 1 = isi nama, 2 = isi harga
        self.new_name = ""
        self.new_price = 0
        self.new_image = ""   # untuk menyimpan nama file gambar

        self.items = {}
        self.images = []

        main = tk.Frame(root, bg="#0b2b3f")
        main.pack(fill="both", expand=True)

        scroll = ScrollFrame(main)
        scroll.pack(side="left", fill="both", expand=True)
        self.products_parent = scroll.scrollable_frame
        right = tk.Frame(main, bg="#0b2b3f", padx=40, pady=40)
        right.pack(side="right", fill="y")

        self.build_products(self.products_parent)
        self.build_panel(right)
    def refresh_products(self):
        global PRODUCTS, HAS_PRODUCTS

        # hapus semua widget produk lama
        for w in self.products_parent.winfo_children():
            w.destroy()

        # load ulang dari DB
        PRODUCTS = load_products_from_mysql()
        HAS_PRODUCTS = bool(PRODUCTS)

        # reset cache images & items
        self.items = {}
        self.images = []

        # bangun ulang kartu produk
        self.build_products(self.products_parent)

    def build_products(self, parent):
        if not HAS_PRODUCTS:
            lbl = tk.Label(parent,
                        text="Tidak ada produk",
                        font=("Arial", 14, "bold"),
                        bg="#123953",
                        fg="white")
            lbl.pack(pady=50)
            return
        for i, (code, name, price, imgfile) in enumerate(PRODUCTS):
            r, c = divmod(i, 3)
            card = tk.Frame(parent, bg="#f0f0f0", bd=2, relief="ridge", padx=8, pady=8)
            card.grid(row=r, column=c, padx=10, pady=10)

            img = None
            if os.path.exists(imgfile):
                try:
                    img = tk.PhotoImage(file=imgfile).subsample(6, 8)
                except:  # file rusak dll
                    img = None
            if img:
                self.images.append(img)
                tk.Label(card, image=img, bg="#f0f0f0",wraplength=90,
                justify="center").pack()
            else:
                tk.Label(card, text="No Image", width=12, height=6, bg="#ccc").pack()

            tk.Label(card, text=code, font=("Arial", 9, "bold"), bg="#f0f0f0").pack()
            tk.Label(card, text=name, font=("Arial", 9), bg="#f0f0f0").pack()
            tk.Label(card, text=f"{price:,}".replace(",", "."),
                     font=("Arial", 9), bg="#f0f0f0").pack()

            stok_var = tk.StringVar(value="99")
            tk.Label(card, textvariable=stok_var, font=("Arial", 9), bg="#f0f0f0").pack()

            self.items[code] = {"name": name, "price": price, "stock": 99, "stok_var": stok_var}

    def build_panel(self, parent):
        monitor = tk.Frame(parent, bg="black", padx=20, pady=20)
        monitor.pack(fill="x", pady=(0, 30))
           
        # >>> Tambahan penting supaya monitor TIDAK mengecil
        monitor.config(height=250, width=200)        # tinggi bisa kamu sesuaikan: 180, 220, dll
        monitor.pack_propagate(False)     # jangan sesuaikan ukuran ke isi di dalam

        # FRAME UTAMA UNTUK CONTENT NORMAL (tambah barang, menu, dll)
        self.monitor_content = tk.Frame(monitor, bg="black")
        self.monitor_content.pack(fill="both", expand=True)

        # FRAME KHUSUS UNTUK TULISAN BERHASIL (TENGAH LAYAR)
        self.monitor_center = tk.Frame(monitor, bg="black")
        # Tidak di-pack sekarang → hanya saat dipakai

        # ==== ISI MONITOR NORMAL (DI DALAM monitor_content) ====
        self.label1 = tk.Label(self.monitor_content, text="SELAMAT DATANG",
                            fg="white", bg="black", font=("Arial", 12, "bold"))
        self.label1.pack(anchor="w")

        self.label2 = tk.Label(self.monitor_content, text="1. ADMIN",
                            fg="white", bg="black", font=("Arial", 10))
        self.label2.pack(anchor="w")

        self.label3 = tk.Label(self.monitor_content, text="2. BELANJA",
                            fg="white", bg="black", font=("Arial", 10))
        self.label3.pack(anchor="w")

        self.label4 = tk.Label(self.monitor_content, text="",
                            fg="white", bg="black", font=("Arial", 10))
        self.label4.pack(anchor="w")

        self.label_batal = tk.Label(
        self.monitor_content,text="",fg="white",bg="black",font=("Arial", 10))
        self.label_batal.pack(anchor="w")

        # spasi
        tk.Label(self.monitor_content, text=" ", bg="black").pack()

        # INPUT + nilai input + pesan
        tk.Label(self.monitor_content, text="INPUT:", fg="white", bg="black",
                font=("Arial", 10)).pack(anchor="w")

        tk.Label(self.monitor_content, textvariable=self.text, fg="white", bg="black",
                font=("Consolas", 13)).pack(anchor="w")

        # ==== LAYAR TENGAH UNTUK "BERHASIL" ====
        self.center_label = tk.Label(self.monitor_center,
                                    text="",
                                    fg="white",
                                    bg="black",
                                    font=("Arial", 20, "bold"))
        self.center_label.pack(expand=True)

        outer = tk.Frame(parent, bg="#d9d9d9", padx=10, pady=10)
        outer.pack()
        pad = tk.Frame(outer, bg="#d9d9d9")
        pad.pack()

        keys = [
            ("1", "abc"), ("2", "def"), ("3", "ghi"),
            ("4", "jkl"), ("5", "mno"), ("6", "pqr"),
            ("7", "stu"), ("8", "vwx"), ("9", "xyz"),
            ("X", ""),    ("0", ""),    ("OK", "")
        ]

        r = c = 0
        for key, letters in keys:
            if key in MULTITAP:
                text = f"{key}\n{letters}"
                bg, fg = "#222", "white"
            elif key == "X":
                text, bg, fg = "X", "#f33", "white"
            else:
                text, bg, fg = "OK", "#f8a52b", "white"

            tk.Button(
                pad, text=text, width=4, height=2, bg=bg, fg=fg,
                font=("Arial", 10, "bold"), relief="flat",
                command=lambda k=key: self.handle_key(k)
            ).grid(row=r, column=c, padx=4, pady=4)

            c += 1
            if c > 2:
                c = 0
                r += 1
    def show_menu(self):
        self.mode = "menu"
        self.text.set("")
        self.msg.set("")
        self.reset_label_colors()
        self.label_batal.config(text="")
        self.label1.config(text="SELAMAT DATANG", font=("Arial", 12, "bold"))
        self.label2.config(text="1. ADMIN", font=("Arial", 10, "normal"))
        self.label3.config(text="2. BELANJA", font=("Arial", 10, "normal"))
        self.label4.config(text="", font=("Arial", 10, "normal"))
    def show_pass_screen(self):
        self.mode = "pass"
        self.pass_buf = ""
        self.text.set("")
        self.msg.set("")
        self.reset_label_colors()
        self.label1.config(text="PASSWORD", font=("Arial", 14, "bold"))
        self.label2.config(text="", font=("Arial", 10))
        self.label3.config(text="0 - BATAL", font=("Arial", 10))
        self.label4.config(text="", font=("Arial", 10))
    def highlight_step(self, step):
        # reset semua jadi putih dulu
        self.label2.config(fg="white")
        self.label3.config(fg="white")
        self.label4.config(fg="white")

        # yang aktif jadi hijau
        if step == 1:
            self.label2.config(fg="lime")
        elif step == 2:
            self.label3.config(fg="lime")
        elif step == 3:
            self.label4.config(fg="lime")

    def show_admin_add(self):
        self.mode = "admin_add"
        self.text.set("")
        self.msg.set("")
        self.admin_add_step = 1  # mulai dari nama

        self.label1.config(text="=TAMBAH BARANG=", font=("Arial", 12, "bold"))
        self.label2.config(text="- NAMA BARANG", font=("Arial", 10, "bold"))
        self.label3.config(text="- HARGA BARANG", font=("Arial", 10, "bold"))
        self.label4.config(text="- GAMBAR BARANG", font=("Arial", 10, "bold"))
        self.label_batal.config(text="0 - BATAL", font=("Arial", 10))

        # highlight langkah 1
        self.highlight_step(1)

    def after_add_success(self):
        # sembunyikan layar tengah
        self.monitor_center.pack_forget()

        # tampilkan kembali tampilan tambah barang
        self.monitor_content.pack(fill="both", expand=True)

        self.show_admin_add()   # ← balik ke mode tambah barang

    def show_success_center(self, text="BERHASIL"):
        # sembunyikan konten normal
        self.monitor_content.pack_forget()

        # tampilkan layar tengah
        self.center_label.config(text=text)
        self.monitor_center.pack(fill="both", expand=True)
    def reset_label_batal(self):
        self.label_batal.config(text="")
    def reset_label_colors(self):
        self.label1.config(fg="white")
        self.label2.config(fg="white")
        self.label3.config(fg="white")
        self.label4.config(fg="white")
        self.label_batal.config(fg="white")
    def show_admin_menu(self):
        self.mode = "admin_menu"
        self.text.set("")
        self.msg.set("")
        self.reset_label_colors()
        self.reset_label_batal()
        self.label1.config(text="1. MENAMBAHKAN", font=("Arial", 10, "bold"))
        self.label2.config(text="2. MEMPERBARUI", font=("Arial", 10, "bold"))
        self.label3.config(text="3. MENGHAPUS",   font=("Arial", 10, "bold"))
        self.label4.config(text="4. KELUAR",      font=("Arial", 10, "bold"))
    def handle_key(self, key):
        self.msg.set("")


            # ================= MODE MENU: ketik 1 lalu OK =================
        if self.mode == "menu":
            if key == "OK":
                val = self.text.get()
                if val == "1":
                    self.show_pass_screen()
                #elif val == "2":
                    #self.mode = "shop"   # << MASUK MODE BELANJA
                    #self.text.set("")
                return

        # ================= MODE PASSWORD =================
        if self.mode == "pass":
            if key == "X":              # backspace password
                self.pass_buf = self.pass_buf[:-1]
                self.text.set("*" * len(self.pass_buf))
                return

            if key == "OK":
                # 0 + OK = batal → kembali ke menu
                if self.pass_buf == "0":
                    self.show_menu()
                elif self.pass_buf == self.admin_pass:
                    self.show_admin_menu()
                else:
                    self.msg.set("password salah")
                return

            if key in "0123456789":     # hanya angka, tanpa multi-tap
                self.pass_buf += key
                self.text.set("*" * len(self.pass_buf))
            return
    # ================= MODE MENU ADMIN =================
        if self.mode == "admin_menu":
            if key == "X":
                # backspace input menu admin
                cur = self.text.get()
                self.text.set(cur[:-1])
                return

            if key == "OK":
                pilihan = self.text.get().strip()
                if pilihan == "1":        # 1. MENAMBAHKAN
                    self.show_admin_add()
                elif pilihan == "4":      # 4. KELUAR
                    self.show_menu()
                # 2 dan 3 nanti bisa ditambah di sini
                return

            if key.isdigit():
                self.text.set(self.text.get() + key)
            return

    # ================= MODE TAMBAH BARANG (ADMIN ADD) =================
        if self.mode == "admin_add":
            # 0 + OK = batal → kembali ke menu admin
            if key == "OK":
                teks = self.text.get().strip()

                # batal
                if teks == "0":
                    self.show_admin_menu()
                    return

                # langkah 1: simpan nama barang
                if self.admin_add_step == 1:
                    if teks == "":
                        self.msg.set("Nama tidak boleh kosong")
                        return
                    self.new_name = teks
                    self.admin_add_step = 2
                    self.text.set("")
                    # pesan pendek supaya pas di monitor 200x250
                    self.msg.set("Masukkan harga\n(angka), lalu OK")
                    self.highlight_step(2)
                    return

                # langkah 2: simpan harga barang
                if self.admin_add_step == 2:
                    if not teks.isdigit():
                        self.msg.set("Harga harus angka")
                        return
                    self.new_price = int(teks)

                    # lanjut ke langkah 3: gambar barang
                    self.admin_add_step = 3
                    self.text.set("")
                    self.msg.set("Nama gambar\n(tanpa .png), OK")
                    self.highlight_step(3)
                    return
                
                # langkah 3: simpan gambar barang
                if self.admin_add_step == 3:
                    if teks == "":
                        self.msg.set("Tidak boleh kosong")
                        return

                    # kalau user cuma ketik "01" atau "aqua",
                    # otomatis dibikin "01.png" atau "aqua.png"

                    filename = teks if teks.lower().endswith(".png") else teks + ".png"
                    self.new_image = os.path.join(IMAGE_DIR, filename)

                    # ====== INSERT KE DATABASE ======
                    ok = insert_product_to_mysql(self.new_name, self.new_price, self.new_image)
                    if not ok:
                        self.msg.set("Gagal simpan DB")
                        return
                    # refresh tampilan produk
                    self.refresh_products()
                    # kosongkan judul-judul di monitor
                    self.label1.config(text="")
                    self.label2.config(text="")
                    self.label3.config(text="")
                    self.label4.config(text="")

                    # kosongkan input, reset step
                    self.text.set("")
                    self.admin_add_step = 1

                    # tampilkan tulisan BERHASIL di tengah monitor
                    self.show_success_center("BERHASIL")

                    # setelah 3 detik kembali ke tampilan TAMBAH BARANG
                    self.root.after(3000, self.after_add_success)
                    return

            # tombol backspace
            if key == "X":
                cur = self.text.get()
                self.text.set(cur[:-1])
                return

            # langkah 1: nama barang → pakai multi-tap huruf
            if self.admin_add_step == 1 and key in MULTITAP:
                now = time.time()
                same = (key == self.last_key and now - self.last_time < self.timeout)
                self.tap = self.tap + 1 if same else 0
                self.last_key, self.last_time = key, now

                chars = MULTITAP[key]
                ch = chars[self.tap % len(chars)]
                cur = self.text.get()
                if same and cur:
                    cur = cur[:-1]
                self.text.set(cur + ch)
                return

            # langkah 2: harga barang → hanya angka biasa
            if self.admin_add_step == 2 and key in "0123456789":
                self.text.set(self.text.get() + key)
                return
            
            # langkah 3: nama file gambar → pakai multi-tap juga
            if self.admin_add_step == 3 and key in MULTITAP:
                now = time.time()
                same = (key == self.last_key and now - self.last_time < self.timeout)
                self.tap = self.tap + 1 if same else 0
                self.last_key, self.last_time = key, now

                chars = MULTITAP[key]
                ch = chars[self.tap % len(chars)]
                cur = self.text.get()
                if same and cur:
                    cur = cur[:-1]
                self.text.set(cur + ch)
                return

        # ================= MODE SHOP / BELANJA (logika lama, dipersingkat) =================
        if key == "OK":
            self.buy()
            return

        if key == "X":                  # backspace di input kode produk
            cur = self.text.get()
            if cur:
                self.text.set(cur[:-1])
            self.last_key = None
            self.tap = 0
            return

        if key not in MULTITAP:         # tombol lain (kalau ada) ditambah mentah
            self.text.set(self.text.get() + key)
            return

        # multi-tap angka → huruf (mode belanja)
        now = time.time()
        same = (key == self.last_key and now - self.last_time < self.timeout)
        self.tap = self.tap + 1 if same else 0
        self.last_key, self.last_time = key, now

        chars = MULTITAP[key]
        ch = chars[self.tap % len(chars)]
        cur = self.text.get()
        if same and cur:
            cur = cur[:-1]
        self.text.set(cur + ch)

    def buy(self):
        code = self.text.get().strip()
        if code not in self.items:
            self.msg.set("Kode tidak valid.")
            return
        item = self.items[code]
        if item["stock"] <= 0:
            self.msg.set("Stok habis.")
            return
        item["stock"] -= 1
        item["stok_var"].set(f"Stok : {item['stock']}")
        self.msg.set(f"Anda membeli {item['name']} (Rp {item['price']:,})".replace(",", "."))
        self.text.set("")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()