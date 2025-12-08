def vending_machine():
    print('=== Vending Machine ===')
    
    # Menu minuman
    print("1. Es Teh    - 4000")
    print("2. Es Jeruk  - 5000") 
    print("3. Kopi      - 6000")
    print("4. BATAL")
    
    # Input pilihan
    nomor = int(input('Masukkan nomor minuman (1-4): '))
    
    # Cek jika memilih batal
    if nomor == 4:
        print("Transaksi dibatalkan")
        return
    
    # Cek pilihan valid
    if nomor not in [1, 2, 3]:
        print("Pilihan tidak valid!")
        return
    
    # Input koin
    koin = int(input('Masukkan koin: Rp '))
    
    # Tentukan harga berdasarkan pilihan
    if nomor == 1:
        harga = 4000
        nama_minuman = "Es Teh"
    elif nomor == 2:
        harga = 5000
        nama_minuman = "Es Jeruk"
    else:  # nomor == 3
        harga = 6000
        nama_minuman = "Kopi"
    
    # Proses transaksi
    if koin < harga:
        print(f"❌ Jumlah koin kurang! Kurang: Rp {harga - uang}")
        
    elif koin == harga:
        print(f"✅ Keluarkan {nama_minuman} melalui produk dispenser")
        print("✅ Transaksi berhasil!")

    elif koin > harga:  
        kembalian = koin - harga
        print(f"✅ Keluarkan {nama_minuman} melalui produk dispenser")
        print(f"✅ Keluarkan koin kembalian Rp {kembalian} melalui koin dispenser")
        print("✅ Transaksi berhasil!")
        
    else:
        print('Transaksi Gagal❌')
# Jalankan program
vending_machine()