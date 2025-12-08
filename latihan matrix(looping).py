# rekursi:______________________________________
# def faktorial(n):
#         if (n == 0):
#               return 1
#         else:
#               return n * faktorial(n - 1)

# angka = int(input('masukkan angka: '))
# print(f'faktorial {angka}= {faktorial(angka)}')


# loop for:______________________________________________
# 

angka= int(input('masuk angka: '))

if angka <= 3:
    print('salah input')

    if angka % 2 == 1:
        for i in range(angka):
            for j in range(angka):
                
                if j < i:
                    print('0', end='')
                else:
                    print(i+1, end='')
            else:
                if j <= i:
                    print(i+1, end='')
                else:
                    print('0', end='')

        print()