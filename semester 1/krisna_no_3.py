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




