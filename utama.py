import tkinter as tk
from tkinter import messagebox


class BelanjaAdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Belanja Admin")

        # Dapatkan ukuran layar
        lebar_layar = self.root.winfo_screenwidth()
        tinggi_layar = self.root.winfo_screenheight()
        # Hitung posisi x dan y untuk window di tengah
        x = (lebar_layar // 2) - (500 // 2)
        y = (tinggi_layar // 2) - (700 // 2)

        # Set geometry dengan posisi fixed
        self.root.geometry(f"500x650+{x}+{y}")

        # Nonaktifkan resize
        self.root.resizable(False, False)
        
        self.root.configure(bg='#0C2D48')  # Warna latar belakang

        # Data produk
        self.produk_list = [
            {"id": "P001", "nama": "Indomie Goreng", "harga": 3500},
            {"id": "P002", "nama": "Susu Ultra", "harga": 6000},
            {"id": "P003", "nama": "Kopi Kapal Api", "harga": 2000},
            {"id": "P004", "nama": "Teh Botol", "harga": 5000},
            {"id": "P005", "nama": "Roti Tawar", "harga": 12000},
            {"id": "P006", "nama": "Minyak Goreng", "harga": 25000},
            {"id": "P007", "nama": "Gula 1kg", "harga": 15000},
            {"id": "P008", "nama": "Telur 1kg", "harga": 28000},
            {"id": "P009", "nama": "Sabun Mandi", "harga": 5000},
            {"id": "P010", "nama": "Pasta Gigi", "harga": 8000},
            {"id": "P011", "nama": "Shampoo", "harga": 12000},
            {"id": "P012", "nama": "Air Mineral", "harga": 3000},
        ]
        
        # Variabel untuk input
        self.uang_var = tk.StringVar()
        self.id_produk_var = tk.StringVar()
        
        # Status mode
        self.mode_aktif = "awal"  # awal, belanja, admin
        
        # Frame untuk bagian kanan
        self.frame_kanan = None
        
        # Buat GUI lengkap
        self.buat_gui_lengkap()
    
    def buat_gui_lengkap(self):
        """Membuat GUI lengkap dengan produk di kiri dan panel kanan"""
        
        # Frame utama untuk konten
        konten_frame = tk.Frame(self.root, bg='#0C2D48')
        konten_frame.pack(fill=tk.BOTH, expand=True)
        
        # BAGIAN KIRI: PRODUK (selalu tampil)
        self.buat_bagian_produk(konten_frame)

        garis_pemisah = tk.Frame(konten_frame, bg='white', width=1)
        garis_pemisah.pack(side=tk.LEFT, fill=tk.Y)
        
        # BAGIAN KANAN: Panel dinamis (awalnya tampilkan pilihan)
        self.buat_panel_kanan(konten_frame)

        # Tampilkan mode awal (pilihan BELANJA/ADMIN)
        self.tampilkan_mode_awal()

    def buat_bagian_produk(self, parent):
        """Membuat bagian kiri untuk menampilkan produk (selalu tampil)"""
        # Frame untuk produk
        frame_produk = tk.Frame(parent, bg='#34495e')
        frame_produk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Judul produk
        tk.Label(frame_produk, text="DAFTAR PRODUK", 
                bg='#34495e', fg='white', 
                font=("Arial", 14, "bold")).pack(pady=8)
        
        # Frame untuk grid produk 3x4
        grid_produk = tk.Frame(frame_produk, bg='#34495e')
        grid_produk.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Buat 12 tombol produk
        for i in range(12):
            baris = i // 3  # Baris ke-0, 1, 2, 3
            kolom = i % 3   # Kolom ke-0, 1, 2
            
            if i < len(self.produk_list):
                produk = self.produk_list[i]
                # Format teks: ID, Nama, Harga
                teks_produk = f"{produk['id']}\n{produk['nama']}\nRp{produk['harga']:,}"
                
                # Buat tombol produk
                tk.Button(grid_produk, text=teks_produk,
                         font=("Arial", 7, "bold"),
                         bg='#3498db', fg='white',
                         relief=tk.RAISED, bd=1,
                         height=1,
                         wraplength=70,
                         command=lambda p=produk: self.pilih_produk(p)
                ).grid(row=baris, column=kolom, padx=2, pady=2, sticky='nsew')
        
        # Atur ukuran grid
        for i in range(4): grid_produk.grid_rowconfigure(i, weight=1)
        for i in range(3): grid_produk.grid_columnconfigure(i, weight=1)
    
    def buat_panel_kanan(self, parent):
        """Membuat panel kanan yang akan berubah isinya"""
        # Frame untuk panel kanan
        self.frame_kanan = tk.Frame(parent, bg='#34495e')
        self.frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Label judul panel (akan diupdate sesuai mode)
        self.label_judul = tk.Label(self.frame_kanan, text="", 
                                   bg='#34495e', fg='white', 
                                   font=("Arial", 16, "bold"))
        self.label_judul.pack(pady=10)
        
        # Frame untuk konten dinamis
        self.frame_konten = tk.Frame(self.frame_kanan, bg='#34495e')
        self.frame_konten.pack(fill=tk.BOTH, expand=True, padx=10)
    
    def tampilkan_mode_awal(self):
        """Menampilkan pilihan BELANJA dan ADMIN di panel kanan"""
        self.mode_aktif = "awal"
        self.label_judul.config(text="SELAMAT DATANG")
        
        # Hapus konten sebelumnya
        for widget in self.frame_konten.winfo_children():
            widget.destroy()
        
        # Frame untuk tombol pilihan
        frame_pilihan = tk.Frame(self.frame_konten, bg='#34495e')
        frame_pilihan.pack(expand=True)
        
        # Tombol BELANJA
        tk.Button(frame_pilihan, text="BELANJA", 
                 font=("Arial", 12, "bold"),
                 bg='#3498db', fg='white',
                 relief=tk.RAISED, bd=2,
                 width=8, height=1,
                 command=self.tampilkan_mode_belanja
        ).pack(pady=5)
        
        # Tombol ADMIN
        tk.Button(frame_pilihan, text="ADMIN", 
                 font=("Arial", 12, "bold"),
                 bg='#e74c3c', fg='white',
                 relief=tk.RAISED, bd=2,
                 width=8, height=1,
                 command=self.tampilkan_mode_admin
        ).pack(pady=5)
    
    def tampilkan_mode_belanja(self):
        """Menampilkan mode belanja (keypad transaksi)"""
        self.mode_aktif = "belanja"
        self.label_judul.config(text="TRANSAKSI BELANJA")
        
        # Hapus konten sebelumnya
        for widget in self.frame_konten.winfo_children():
            widget.destroy()
        
        # Tombol kembali ke menu utama
        frame_header = tk.Frame(self.frame_konten, bg='#34495e')
        frame_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(frame_header, text="← Kembali", 
                 font=("Arial", 10),
                 bg='#7f8c8d', fg='white',
                 relief=tk.RAISED, bd=1,
                 command=self.tampilkan_mode_awal
        ).pack(side=tk.LEFT)
        
        # Input ID Produk
        tk.Label(self.frame_konten, text="ID PRODUK:", 
                bg='#34495e', fg='white', 
                font=("Arial", 10, "bold")).pack(anchor='w', pady=(5, 2))
        
        tk.Entry(self.frame_konten, textvariable=self.id_produk_var, 
                font=("Arial", 10), width=12).pack(fill=tk.X, pady=(0, 8))
        
        # Input Uang
        tk.Label(self.frame_konten, text="MASUKKAN UANG:", 
                bg='#34495e', fg='white', 
                font=("Arial", 10, "bold")).pack(anchor='w', pady=(5, 2))
        
        tk.Entry(self.frame_konten, textvariable=self.uang_var, 
                font=("Arial", 10), width=12).pack(fill=tk.X, pady=(0, 15))
        
        # Label Keypad
        tk.Label(self.frame_konten, text="KEYPAD", 
                bg='#34495e', fg='white', 
                font=("Arial", 12, "bold")).pack(pady=(0, 8))
        
        # Buat keypad lengkap
        self.buat_keypad_lengkap()
    
    def tampilkan_mode_admin(self):
        """Menampilkan mode admin (placeholder)"""
        self.mode_aktif = "admin"
        self.label_judul.config(text="MODE ADMIN")
        
        # Hapus konten sebelumnya
        for widget in self.frame_konten.winfo_children():
            widget.destroy()
        
        # Frame untuk konten admin
        frame_admin = tk.Frame(self.frame_konten, bg='#34495e')
        frame_admin.pack(expand=True)
        
        # Tombol kembali ke menu utama
        tk.Button(frame_admin, text="← Kembali", 
                 font=("Arial", 10),
                 bg='#7f8c8d', fg='white',
                 relief=tk.RAISED, bd=1,
                 command=self.tampilkan_mode_awal
        ).pack(pady=(0, 15))
        
        # Pesan placeholder
        tk.Label(frame_admin, text="Fitur Admin\nakan segera hadir!", 
                bg='#34495e', fg='white', 
                font=("Arial", 14, "bold"),
                justify=tk.CENTER).pack(expand=True)
        
        # Informasi sederhana
        tk.Label(frame_admin, text=f"Jumlah Produk: {len(self.produk_list)}", 
                bg='#34495e', fg='#ecf0f1', 
                font=("Arial", 11)).pack(pady=8)
    
    def buat_keypad_lengkap(self):
        """Membuat keypad angka lengkap dengan BELI dan REFRESH"""
        frame_keypad = tk.Frame(self.frame_konten, bg='#34495e')
        frame_keypad.pack(fill=tk.BOTH, expand=True)
        
        # Susunan tombol keypad (4 baris angka)
        tombol_keypad = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', 'HAPUS', 'OK']
        ]
        
        # Buat tombol-tombol angka
        for baris, deret_tombol in enumerate(tombol_keypad):
            for kolom, teks in enumerate(deret_tombol):
                # Tentukan warna tombol
                if teks == 'OK':
                    warna = '#27ae60'  # Hijau
                    perintah = self.ok_pressed
                elif teks == 'HAPUS':
                    warna = '#e67e22'  # Oranye
                    perintah = self.hapus_pressed
                else:
                    warna = '#7f8c8d'  # Abu-abu
                    perintah = lambda t=teks: self.tombol_angka_ditekan(t)
                
                # Buat tombol
                tk.Button(frame_keypad, text=teks,
                         font=("Arial", 9, "bold"),
                         bg=warna, fg='white',
                         relief=tk.RAISED, bd=1,
                         width=3, height=1,
                         command=perintah
                ).grid(row=baris, column=kolom, padx=1, pady=1, sticky='nsew')
        
        # Frame untuk tombol BELI dan REFRESH (baris ke-5)
        frame_aksi = tk.Frame(frame_keypad, bg='#34495e')
        frame_aksi.grid(row=4, column=0, columnspan=3, pady=(5, 0), sticky='nsew')
        
        # Tombol BELI (kiri)
        tk.Button(frame_aksi, text="BELI", 
                 font=("Arial", 9, "bold"),
                 bg='#e74c3c', fg='white',
                 relief=tk.RAISED, bd=1,
                 width=5, height=1,
                 command=self.beli_pressed
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 1))
        
        # Tombol REFRESH (kanan)
        tk.Button(frame_aksi, text="REFRESH", 
                 font=("Arial", 9, "bold"),
                 bg='#3498db', fg='white',
                 relief=tk.RAISED, bd=1,
                 width=5, height=1,
                 command=self.refresh_pressed
        ).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(1, 0))
        
        # Konfigurasi grid untuk frame keypad
        for i in range(5):  # 4 baris angka + 1 baris aksi
            frame_keypad.grid_rowconfigure(i, weight=1)
        for i in range(3):  # 3 kolom
            frame_keypad.grid_columnconfigure(i, weight=1)
    
    # ========== FUNGSI-FUNGSI UTAMA ==========
    
    def tombol_angka_ditekan(self, angka):
        """Menambahkan angka ke input yang sedang aktif"""
        widget_aktif = self.root.focus_get()
        if isinstance(widget_aktif, tk.Entry):
            widget_aktif.insert(tk.END, angka)
    
    def hapus_pressed(self):
        """Menghapus karakter terakhir"""
        widget_aktif = self.root.focus_get()
        if isinstance(widget_aktif, tk.Entry):
            teks_sekarang = widget_aktif.get()
            widget_aktif.delete(0, tk.END)
            widget_aktif.insert(0, teks_sekarang[:-1])
    
    def pilih_produk(self, produk):
        """Mengisi ID produk saat produk dipilih"""
        self.id_produk_var.set(produk['id'])
        
        # Jika sedang di mode belanja, fokus ke input uang
        if self.mode_aktif == "belanja":
            # Cari entry uang dan fokuskan
            for widget in self.frame_konten.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Entry):
                            child.focus_set()
                            break
    
    def ok_pressed(self):
        """Memvalidasi input sebelum pembelian"""
        uang = self.uang_var.get()
        id_produk = self.id_produk_var.get()
        
        if not uang or not id_produk:
            messagebox.showwarning("Peringatan", "Harap isi uang dan ID produk!")
            return
        
        # Cari produk
        produk = self.cari_produk(id_produk)
        if not produk:
            messagebox.showwarning("Peringatan", f"ID {id_produk} tidak ditemukan!")
            return
        
        # Validasi uang
        try:
            uang_int = int(uang)
            if uang_int >= produk['harga']:
                kembalian = uang_int - produk['harga']
                pesan = f"Produk: {produk['nama']}\nHarga: Rp{produk['harga']:,}"
                pesan += f"\nUang: Rp{uang_int:,}\nKembalian: Rp{kembalian:,}"
                pesan += "\n\nTekan BELI untuk melanjutkan."
                messagebox.showinfo("Konfirmasi", pesan)
            else:
                kurang = produk['harga'] - uang_int
                messagebox.showwarning("Uang Kurang", f"Kurang Rp{kurang:,}")
        except:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
    
    def beli_pressed(self):
        """Memproses pembelian"""
        uang = self.uang_var.get()
        id_produk = self.id_produk_var.get()
        
        if not uang or not id_produk:
            messagebox.showwarning("Peringatan", "Harap isi uang dan ID produk!")
            return
        
        # Cari produk
        produk = self.cari_produk(id_produk)
        if not produk:
            messagebox.showwarning("Peringatan", f"ID {id_produk} tidak ditemukan!")
            return
        
        # Proses pembelian
        try:
            uang_int = int(uang)
            if uang_int >= produk['harga']:
                kembalian = uang_int - produk['harga']
                pesan = f"Terima kasih telah berbelanja!\n\n"
                pesan += f"Produk: {produk['nama']}\n"
                pesan += f"Harga: Rp{produk['harga']:,}\n"
                pesan += f"Uang: Rp{uang_int:,}\n"
                pesan += f"Kembalian: Rp{kembalian:,}"
                messagebox.showinfo("Berhasil", pesan)
                self.refresh_pressed()
            else:
                kurang = produk['harga'] - uang_int
                messagebox.showerror("Gagal", f"Uang kurang Rp{kurang:,}")
        except:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
    
    def refresh_pressed(self):
        """Mengosongkan input"""
        self.uang_var.set("")
        self.id_produk_var.set("")
    
    def cari_produk(self, id_produk):
        """Mencari produk berdasarkan ID"""
        for produk in self.produk_list:
            if produk['id'] == id_produk:
                return produk
        return None

# Program utama
if __name__ == "__main__":
    root = tk.Tk()
    app = BelanjaAdminGUI(root)
    root.mainloop()