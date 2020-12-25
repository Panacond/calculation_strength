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
        text_file += i[0] + '\t' + i[1] + i[2] + '\n'
    return text_file

def calculation(name, text_file):
    txt = string_calculation.Calc()
    # словарь характеристик бетона
    concrete ={10: 6, 15: 8.5, 20: 11.5, 25: 14.5, 30: 17, 35: 19.5, 40: 22, 45: 25, 50: 27.5, 55: 30, 60: 33}
    #name = "Плита"
    # Исходные данные бетон, просто поменять первый все остальные значения заменяться
    t = text_file
    # поиск и замена с помощью регулярных выражений
    import re
    find_concrete = re.search('В\d\d', t).group()
    t = re.sub('В\d\d',find_concrete, t)
    number_concrete = int(find_concrete[1:])
    t += 'R_b='+ str(concrete[number_concrete]) +'\n'
    t=('Расчет железобетонного элемента на изгиб по СП 52-101-2003'
    'Бетонные и железобетонные конструкции без предварительного натяжения арматуры\n'
    +t)
    t=t.replace('класса\t','класса ')
    txt.c1(t,60)
    t = ('Определение несущей способности элемента по прочности.\n'
    'Определение h_0:\n'
    'h_0=h_b-a_1\n'
    'Ширина железобетонного элемента (мм):\n'
    'Определение коэффициента a_m:\n'
    'a_m=(M_r*10000)/(R_b*b_1*h_0^2)\n')
    txt.c1(t)
    if txt.numer['R_s'] < 242:
        t = '''Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.425
e_r=0.612'''
    elif txt.numer['R_s'] > 242 and txt.numer['R_s'] <= 312  :
        t = '''Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.411
e_r=0.577'''
    elif txt.numer['R_s'] > 312 and txt.numer['R_s'] <= 395  :
        t = '''Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.390
e_r=0.531'''
    else:
        t = '''Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.372
e_r=0.493'''
    txt.c1(t)
    if txt.numer['a_m'] < txt.numer['a_r']:
        t = '''
Расчет ведем из условия, что верхняя арматура не требуется a_m < a_r
Необходимая площадь армирования составит (см^2):
A_s=(R_b*b_1*h_0*(1-\sqrt(1-2*a_m)))/(R_s*100)'''
    else:
        t = '''
Расчет ведем из условия,что верхняя арматура требуется a_m > a_r
Необходимая площадь армирования составит (см^2):
A_v=(M_r-a_r*R_b*b_1*h_0^2/10000)*100/(R_s*(h_0-a_1))
A_s=e_r*R_b*b_1*h_0/R_s/100+A_v'''
    txt.c1(t)
    t='''
Площадь установленной арматуры составит (см^2):
A_i=(3.14*(D_s*0.1)^2*n_b)/4
Коэффициент использования по прочности составит:
k=A_s/A_i'''
    txt.c1(t)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    text_file = text_file.replace('класса\nВ','класса В')    
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*CBR.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
    pass

if __name__ == '__main__':
    main()
def CBR(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file