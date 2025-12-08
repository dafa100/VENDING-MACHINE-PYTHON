# update.py - VERSI DIPERBAIKI
import tkinter as tk

def create_window():
    def kirim_data():
        id_barang = entry_id.get()
        harga_barang = entry_harga.get()
        gambar_barang = entry_gambar.get()

        print(f"Data Update Dikirim:")
        print(f"Id Barang: {id_barang}")
        print(f"Harga Barang: {harga_barang}")
        print(f"Gambar Barang: {gambar_barang}")

    # BUAT TOPLEVEL, BUKAN TK()
    window = tk.Toplevel()
    window.title("Update Barang Vending Machine")
    
    window_width = 320
    window_height = 500
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(False, False)
    window.configure(bg='#1E1E1E')

    # Warna
    color_orange = '#FF7F00'
    color_gray = '#D9D9D9'
    color_button_bg = 'white'
    color_button_fg = 'black'

    # Panel Oranye
    panel_orange = tk.Frame(window, bg=color_orange, width=window_width - 20, height=window_height - 20, relief="flat", bd=0)
    panel_orange.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Kotak Formulir Abu-abu
    form_frame = tk.Frame(panel_orange, bg=color_gray, padx=10, pady=10, relief="flat", bd=0)
    form_frame.place(relx=0.5, rely=0.40, anchor=tk.CENTER, relwidth=0.88, relheight=0.55)

    # Label dan Input Fields
    label_style = {'bg': color_gray, 'font': ('Arial', 11), 'fg': 'black'}

    INPUT_PADX = 10
    INPUT_PADY = 20
    ENTRY_WIDTH = 15

    form_frame.grid_rowconfigure(0, weight=1)
    form_frame.grid_rowconfigure(4, weight=1)

    # Id Barang
    label_id = tk.Label(form_frame, text="Id Barang:", **label_style)
    label_id.grid(row=1, column=0, sticky='w', pady=INPUT_PADY, padx=INPUT_PADX)
    entry_id = tk.Entry(form_frame, width=ENTRY_WIDTH, bd=1, relief="solid")
    entry_id.grid(row=1, column=1, pady=INPUT_PADY, padx=INPUT_PADX, sticky='e')

    # Harga Barang
    label_harga = tk.Label(form_frame, text="Harga Barang:", **label_style)
    label_harga.grid(row=2, column=0, sticky='w', pady=INPUT_PADY, padx=INPUT_PADX)
    entry_harga = tk.Entry(form_frame, width=ENTRY_WIDTH, bd=1, relief="solid")
    entry_harga.grid(row=2, column=1, pady=INPUT_PADY, padx=INPUT_PADX, sticky='e')

    # Gambar Barang
    label_gambar = tk.Label(form_frame, text="Gambar Barang:", **label_style)
    label_gambar.grid(row=3, column=0, sticky='w', pady=INPUT_PADY, padx=INPUT_PADX)
    entry_gambar = tk.Entry(form_frame, width=ENTRY_WIDTH, bd=1, relief="solid")
    entry_gambar.grid(row=3, column=1, pady=INPUT_PADY, padx=INPUT_PADX, sticky='e')

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    # Tombol Kirim
    button_kirim = tk.Button(panel_orange, text="KIRIM", command=kirim_data, bg=color_button_bg, fg=color_button_fg, relief="raised", bd=1, font=('Arial', 10), width=8)
    button_kirim.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    return window