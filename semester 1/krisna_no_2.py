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



