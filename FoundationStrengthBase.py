# чтение из csv файла данных и расчет висячей буровой сваи
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

import numpy

def table_512(corner):
    'таблица 5.12 определение коэффициентов N_y , N_q, N_c в зависимости от угла \varphi'
    table_corner=[0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0]
    table_k1= [0.0, 0.2, 0.6, 1.35, 2.88, 5.87, 12.39, 27.5, 66.01, 177.61]
    table_k2= [1.0, 1.57, 2.47, 3.94, 6.4, 10.66, 18.4, 33.3, 64.19, 134.87]
    table_k3= [5.14, 6.49, 8.34, 10.98, 14.84, 20.72, 30.14, 46.12, 75.31, 133.87]
    k1=numpy.interp(corner,table_corner,table_k1)
    k1 = round(k1,2)
    k2=numpy.interp(corner,table_corner,table_k2)
    k2 = round(k2,2)
    k3=numpy.interp(corner,table_corner,table_k3)
    k3 = round(k3,2)
    return k1, k2, k3


def calculation(name, text_file):
    txt = string_calculation.Calc()
    # расчет
    t = text_file
    t=('''СП 22.13330.2011 Основания зданий и сооружений
5.7 Расчет оснований по несущей способности 
5.7.2 Расчет оснований по несущей способности производят исходя из условия (5.27)
F<(\gamma_c \\times F_u)/(\gamma_n)
Исходные данные
'''
    +t)
    # словарь коэффициентов \gamma_c  п. 5.7.2
    concrete ={'g1:для песков, кроме пылеватых\n': 1.0, 
    'g1:для песков пылеватых, а также глинистых грунтов в стабилизированном состоянии\n': 0.9, 
    'g1:для глинистых грунтов в нестабилизированном состоянии\n':0.85,
    'g1:для скальных грунтов невыветрелых и слабовыветрелых\n': 1.0, 
    'g1:для скальных грунтов выветрелых\n': 0.9, 
    'g1:для скальных сильновыветрелых\n': 0.8}
    # поиск и замена с помощью регулярных выражений
    import re
    # поиск нужного выражение (не жадный)
    find_concrete = re.search(r'g1:.*\n?', t).group()
    # выбор нужного коэффициента
    k1 = concrete[find_concrete]
    text_replace = 'Коэффициент условий работы (п.5.7.2)\n' + find_concrete[3:] +'z1gamma_c=' + str(k1)
    # Замена фрагмента текста
    t = re.sub('выбрать нужный и подставить нужный\tg1:.*\nдля песков, кроме пылеватых\t\nдля песков пылеватых, а также глинистых грунтов в стабилизированном состоянии\t\nдля глинистых грунтов в нестабилизированном состоянии\t\nдля скальных грунтов невыветрелых и слабовыветрелых\t\nдля скальных грунтов выветрелых\t\nдля скальных сильновыветрелых\t',text_replace, t)
    t = t.replace('z1gamma_c','\gamma_c')
    txt.c1(t,50)
    t = '''
b_1  l_1  соответственно ширина и длин фундамента вычисляемые по формулам (5.29)(м):
b_1=B_f-2*e_b
l_1=L_f-2*e_l
5.7.11 Определение вертикальной составляющей силы предельного сопротивления 
\eta=L_f/B_f
Коэффициенты определим по формулам (5.33):
\\xi_y=1-0.25/\eta
\\xi_q=1+1.5/\eta
\\xi_c=1+0.3/\eta'''
    txt.c1(t,50)
    k1, k2, k3 =table_512(txt.numer['\\varphi'])
    t='''
Безразмерные коэффициенты несущей способности, определяемые по таблице 5.12 в 
зависимости от расчетного значения угла внутреннего трения грунта
N_y={0}
N_q={1}
N_c={2}
5.7.11 Вертикальную составляющую силы предельного сопротивления N_u, (кгс), 
основания, сложенного дисперсными грунтами в стабилизированном состоянии, 
допускается определять по формуле (5.32), если фундамент имеет плоскую 
подошву и грунты основания ниже подошвы однородны до глубины не менее ее 
ширины, а в случае различной вертикальной пригрузки с разных сторон фундамента 
интенсивность большей из них не превышает 0,5 \\times R (R – расчетное 
сопротивление грунта основания, определяемое в соответствии с 5.6.7 - 5.6.25)
N_u=b_1*l_1*(N_y*\\xi_y*b_1*\gamma_I+N_q*\\xi_q*\gamma_II*d+N_c*\\xi_c*c_I*10**2)*10**3
5.7.2 Расчет оснований по несущей способности производят исходя из условия (5.27)
F_u=(\gamma_c*N_u)/\gamma_n
Коэффициент использования фундамента по прочности:
k=P_0/N_u
'''
    t = t.format(k1,k2,k3)
    txt.c1(t,50)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    # замена текста
    text_file = text_file.replace('поперечном направлении (м):\n','поперечном направлении (м): ')
    text_file = text_file.replace('продольном направлении (м):\n','продольном направлении (м): ')
    text_file = text_file.replace('действия воды,  (гс/м^3): \n','действия воды,  (гс/м^3): ') 
    text_file = text_file.replace('подошвы фундамента  (гс/м^3): \n','подошвы фундамента  (гс/м^3): ')
    text_file = text_file.replace('в стабилизированном состоянии\n','в стабилизированном состоянии')
    text_file = text_file.replace('грунт в основании фундамента\n\n',' ')
    t='\\xi_c \\times c_I \\times 10^2) \\times 10^3='
    text_file = text_file.replace(t,t +'\n=')
    text_file = text_file.replace('уровней ответственности\n\\gamma_n','уровней ответственности \\gamma_n')
    text_file = text_file.replace('\gamma_c=',' \gamma_c=')
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*FSB.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        string_calculation.write_file(name, str(text_file))
    pass

if __name__ == '__main__':
    main()
def FIN(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file