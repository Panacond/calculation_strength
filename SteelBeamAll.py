# чтение из csv файла данных и расчет стальной прокатной балки
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
        text_file += i[0] + '\t' + i[1] + i[2] + '\n'
    return text_file

def calculation(name, text_file):
    txt = string_calculation.Calc()
    t = text_file
    t='''Расчет по СП 16.13330.2011 Стальные конструкции
Расчет изгибаемых элементов сплошного сечения:
'''+t
    txt.c1(t,60)
    t='''
Момент от нормативных нагрузок (кг м):
M_n=q_n*L^2/8=1800.0*5.5^2/8=4
Коэффициент условий работы (таблица 1):
\gamma_с=0.9
Модуль упругости (кгс/см^2):
E=2060000
Требуемый момент сопротивления (см^3):
W_t=M_r/(R_y*\gamma_с)*100=7800.0/(2450.0*0.9)*100=4
Прогиб составит (мм):
f_p=(f*10**7)/(E*I_x)
Нормативный прогиб составит (мм):
f_n=L/200*1000=5.5/200*1000=4
'''
    txt.c1(t,50)
    t='''
Коэффициент использования по прочности:
k_1=W_t/W_x
Коэффициент использования по прогибам:
k_2=f_p/f_n
'''
    txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-6:])
    print(text_print)
    text_file = txt.rezult
    # замена данных для оформления
    a ='Момент инерции сечения в горизонтальной плоскости (см^4):\nI_y='
    b = "Момент инерции сечения в горизонтальной плоскости (см^4): I_y="
    text_file = text_file.replace(a, b)
    a = 'Коэффициент условий работы (таблица 1):\n\\gamma_с='
    b = 'Коэффициент условий работы (таблица 1): \\gamma_с='
    text_file = text_file.replace(a, b)
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*SBA.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        print(text_file)
    pass

if __name__ == '__main__':
    main()
    
def SBR(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file