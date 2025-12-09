from tkinter import *
from tkinter import messagebox

def create_window():
    """Fungsi untuk membuat window create produk"""
    window = Toplevel()  # <-- BUAT DI DALAM FUNGSI
    window.title("Input Barang")
    window.geometry("300x500")
    window.configure(bg="#FF7F00")
    window.resizable(0,0)
    
    # Posisi window di tengah layar
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    def kirim_data():
        nama = entry_nama.get() 
        harga = entry_harga.get()
        
        print(f"Data Berhasil Dibuat:")
        print(f"Nama Barang: {nama}")
        print(f"Harga Barang: {harga}")
    
    # Frame utama untuk judul 
    frame_judul = Frame(window, bg="#FF7F00")
    frame_judul.pack()
    
    # Judul
    label_judul = Label(frame_judul, text="FORM INPUT BARANG", 
                       fg="black",  
                       bg="#FF7F00",
                       padx=10,       
                       font=("Arial", 16, "bold"))
    label_judul.pack()
    
    # FRAME PERSEGI PUTIH DI TENGAH 
    frame_persegi = Frame(window, 
                          bd=5, 
                          padx=20,
                          pady=70)
    frame_persegi.pack(padx=20, pady=50)
    
    # Nama Barang
    label_nama = Label(frame_persegi, 
                       text="Nama Barang:",
                       font=("Arial", 10))
    label_nama.grid(row=1, column=0, pady=5)
    
    entry_nama = Entry(frame_persegi, 
                       width=15,
                       font=("Arial", 10))
    entry_nama.grid(row=1, column=1, pady=5, padx=(0, 200))
    
    # Harga Barang
    label_harga = Label(frame_persegi, 
                        text="Harga Barang:",
                        font=("Arial", 10))
    label_harga.grid(row=2, column=0, pady=5)
    
    entry_harga = Entry(frame_persegi, 
                        width=15,
                        font=("Arial", 10))
    entry_harga.grid(row=2, column=1, pady=5, padx=(0, 200))
    
    # Input Gambar
    label_gambar = Label(frame_persegi, 
                         text="Gambar Barang:",
                         font=("Arial", 10))
    label_gambar.grid(row=3, column=0, pady=5)
    
    # Frame untuk tombol gambar
    frame_gambar = Frame(frame_persegi, bg='red')
    frame_gambar.grid(row=3, column=1, pady=2, padx=(0, 200))
    
    tombol_gambar = Button(frame_gambar, 
                           text="Pilih Gambar",
                           width=15)
    tombol_gambar.pack()
    
    # Frame untuk tombol KIRIM
    frame_tombol = Frame(window, bg="#FF7F00")
    frame_tombol.pack()
    
    tombol_kirim = Button(frame_tombol, 
                          text="KIRIM", 
                          command=kirim_data,
                          fg="black",
                          font=("Arial", 10, "bold"),
                          width=10)
    tombol_kirim.pack()
    
    return window
