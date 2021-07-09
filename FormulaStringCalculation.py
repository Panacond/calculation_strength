# чтение из csv файла данных и расчет балки
import os, fnmatch, csv
import string_calculation

def read_file(a):
    a = str(a)
    l=[]
    with open(a,'r',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return tabl_taxt(l)

def tabl_taxt(tabl):
    text_file = ''
    for i in tabl:
        if len(i)==1:
            text_file += i[0] + '\n'
        else:
            try:
                text_file += i[0] + '\t' + i[1] + i[2] + '\n'
            except:
                text_file += i[0] + '\n' + i[1] + '\n'
    return text_file

def calculation(name, text_file):
    txt = string_calculation.Calc()
    t = text_file
    print(t)
    txt.c1(text=t, n_letter=60)
    p = txt.finish(name = name)
    print(p)
    text_file = txt.rezult
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*SCA.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        print(text_file)
        string_calculation.write_file(name, str(text_file))
    pass

if __name__ == '__main__':
    main()
    
def CBR(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file