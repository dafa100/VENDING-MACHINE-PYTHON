angka = int(input('masukkan angka: '))

if angka <= 3:
    print('Salah Input')
else:
    for i in range(angka):
        for j in range(angka):
            if angka % 2 == 0:
                if j < i:
                    print('O', end='')
                else:
                    print('X', end='')

            else:
                if j < i:
                    print('X', end='')
                else:
                    print('O', end='')
            
        print()
        