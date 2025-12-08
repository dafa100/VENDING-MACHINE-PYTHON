def cek_bonus():
    print("=== Program Cek Bonus ===")
    total_belanja = int(input('Masukkan total pembelian= '))

    if total_belanja >= 100000:
        print("Selamat anda mendapatkan BONUS")

        print('Terimakasih telah berbelanja')

cek_bonus()

def operasi_aritmatika():
    print('Operasi Aritmatika')
    angka1= float(input('Masukkan angka pertama= '))    
    angka2= float(input('Masukkan angka kedua= '))   

    operasi= input('Masukkan operasi (+, -, *, /)= ')

    if operasi == "+":
        print('Hasil: ', angka1, '+', angka2, '=', angka1 + angka2)
    elif operasi == "-":
        print('Hasil: ', angka1, '-', angka2, '=', angka1 - angka2)
    elif operasi == "*":
        print('Hasil: ', angka1, '*', angka2, '=', angka1 * angka2)
    elif operasi == "/" and angka2 == 0:
        print('Error tidak bisa dibagi 0')
    elif operasi == "/":
        print('Hasil: ', angka1, '/', angka2, '=', angka1 / angka2)

operasi_aritmatika()

def vending_machine():
    print('=== Vending Machine ===')

    print(1, 'Es Teh: 4000')
    print(2, 'Es Jeruk: 5000')
    print(3, 'Kopi: 6000')

    nomor= int(input('Masukkan nomor minuman= '))
    uang= int(input('Masukkan uang= '))

    if nomor == 1:
        harga= 4000
        if uang < harga:
            print('Uang kamu kurang')
        elif uang == harga:
            print('uang kamu pass')
        else: 
            kembalian= uang - harga
            print('kembailan= ', kembalian)
    elif nomor == 2:
        harga= 5000
        if uang < harga:
            print('Uang kamu kurang')
        elif uang == harga:
            print('uang kamu pass')
        else: 
            kembalian= uang - harga
            print('kembailan= ', kembalian)
    elif nomor == 3:
        harga= 6000
        if uang < harga:
            print('Uang kamu kurang')
        elif uang == harga:
            print('uang kamu pass')
        else: 
            kembalian= uang - harga
            print('kembailan= ', kembalian)
    else:
        print('minuman tidak ada')

vending_machine()




