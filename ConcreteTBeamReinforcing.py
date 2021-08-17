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
    t='''Расчет железобетонного элемента на изгиб по СП 52-101-2003
Бетонные и железобетонные конструкции без предварительного натяжения арматуры
'''+t
    txt.c1(t,60)
    t = '''Определение несущей способности элемента по прочности.
Определение h_0:
h_0=h_b-a_1
Площадь установленной арматуры составит (см^2):
A_i=(3.14*(D_s*0.1)^2*n_b)/4
Площадь сечения свесов полки(мм^2):
A_ov=(b_1-b_t)*h_f
'''
    txt.c1(t)
    def koefT32(RS):
        if RS < 242:
            t = '''
Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.425
e_r=0.612
'''
        elif RS > 242 and RS <= 312  :
            t = '''
Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.411
e_r=0.577
'''
        elif RS > 312 and RS <= 395  :
            t = '''
Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.390
e_r=0.531
'''
        else:
            t = '''
Принимаем значения коэффициентов по табл.3.2 пособия
a_r=0.372
e_r=0.493
''' 
        return txt.c1(t)
# Конструктивные требования по свесам
    if txt.numer['h_f'] <= txt.numer['h_b']*0.05:
        t= '''
Расчет ведем как прямоугольного сечения т. к. h_f < h_b \\times 0.05
Принимаем ширину сечения по ширине нижней полки тавра
b_1=b_t'''
    elif txt.numer['h_f'] > txt.numer['h_b']*0.05 and txt.numer['h_f'] <= txt.numer['h_b']*0.1:
        t= '''Расчет ведем как тавровго сечения т. к. h_b \\times 0.05 < h_f < h_b \\times 0.1
Принимаем ширину сечения по ширине нижней полки тавра
b_1=h_f*3*2+b_t'''
    elif txt.numer['h_f'] > txt.numer['h_b']*0.1:
        t= '''Расчет ведем как таврового сечения т. к. h_b \\times 0.1 < h_f
Ширина должна быть не более:
b_n=h_f*6*2+b_t'''
        txt.c1(t)
        if txt.numer['b_1'] < txt.numer['b_n']:
            t= '''
Оставляем ширину сечения без изменений т.к. b_1 меньше или равно b_n'''
        else:
            t= '''
Принимаем ширину сечения по требованиям ограничения ширины
b_1=b_n'''
    txt.c1(t)
    t = '''
Если граница сжатой зоны проходит в полке то соблюдается условие (3.27) K_1<K_2 
К_1 и К_2 (кН):
K_1=R_s*A_i/10
K_2=R_b*b_1*h_f/1000
Проверим условие (3.32)
M_t=(M_r*10000)/(R_b*b_1*h_f*(h_0-0.5*h_f))
'''
    txt.c1(t)
    if txt.numer['M_t'] <= 1:
# расчет прямоугольного сечения
        t = '''
Расчет ведем как для прямоугольного сечения
Определение коэффициента a_m:
a_m=(M_r*10000)/(R_b*b_1*h_0^2)'''
        txt.c1(t)
        koefT32(txt.numer['R_s'])
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
# Расчет как для таврового сечения
    else:
        t = '''
Расчет как для таврового сечения
Определение коэффициента a_m:
a_m=((M_r*10000)-R_b*A_ov*(h_0-0.5*h_f))/(R_b*b_t*h_0^2)'''
        txt.c1(t)
        koefT32(txt.numer['R_s'])
        if txt.numer['a_m'] < txt.numer['a_r']:
            t = '''
Расчет ведем из условия, что верхняя арматура не требуется a_m < a_r
Необходимая площадь армирования составит (см^2):
A_s=(R_b*b_t*h_0*(1-\sqrt(1-2*a_m))+R_b*A_ov)/(R_s*100)'''
        else:
            t = '''
Расчет ведем из условия,что верхняя арматура требуется a_m > a_r
Необходимая площадь армирования составит (см^2):
A_v=(M_r-a_r*R_b*b_1*h_0^2/10000-a_r*R_b*A_ov/10000)*100/(R_s*(h_0-a_1))
A_s=(R_b*b_t*h_0*(1-\sqrt(1-2*a_m))+R_b*A_ov)/(R_s*100)+A_v'''
        txt.c1(t)
    t='''
Коэффициент использования по прочности составит:
k_1=A_s/A_i'''
    txt.c1(t)
    if txt.numer['K_1'] > txt.numer['K_2']:
        t='''Граница проходит в полке расчет пересмотреть!'''
        txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    text_file = text_file.replace('класса\nВ','класса В')
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*CBT.csv'):
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