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
    ung = {10: 19000, 15: 24000, 20: 27500, 25: 30000, 30: 32500, 35: 34500, 40: 36000, 45: 37000, 50: 38000, 55: 39000, 60: 39500}
    #name = "Плита"
    # Исходные данные бетон, просто поменять первый все остальные значения заменяться
    t = text_file
    # поиск и замена с помощью регулярных выражений
    import re
    find_concrete = re.search('В\d\d', t).group()
    t = re.sub('В\d\d',find_concrete, t)
    number_concrete = int(find_concrete[1:])
    t += 'R_b='+ str(concrete[number_concrete]) +'\n'
    t += 'E_b='+ str(ung[number_concrete])+'\n'
    t='''Расчет железобетонного элемента на действие вертикальных нагрузок
Расчет по СП 52-101-2007 Бетонные и железобетонные конструкции без предварительного напряжения
'''+t
    txt.c1(t,120)
    t = '''Расстояние от сжатой грани до арматуры (мм):
h_0=h_c-a
Площадь арматуры (см^2):
A_s=(n_s*3.14*d_s**2)/(4*100)
'''
    txt.c1(t)
    t='''Модуль упругости стали (МПа):
E_s=200000'''
    txt.c1(t,60)
    t='''
Момент инерции сечения (см^4):
I_c=(h_c^3*t_c)/(12*10**4)
Площадь сечения (см^2):
F_c=h_c*t_c/100
Радиус инерции сечения(см):
i_c=%(I_c/F_c)
Проверка конструктивных требований для колонн зданий:
k_g=L_0/i_c*100
'''
    txt.c1(t)
    if txt.numer['k_g'] < 120:
        t = '''Конструктивные требования выполняются {0} < 120
'''
    else:
        t = '''Конструктивные требования не выполняются {0} < 120
'''
    t = t.format(txt.numer['k_g'])
    txt.c1(t)
    t='''Эксцентриситет от момента будет (мм):
e_m=(M_0*1000)/N_0'''
    txt.c1(t)
    t='''
Определим случайный эксцентриситет, он должен быть не менее (мм):
e_a=(L_0*1000)/600
e_b=h_c/30
e_c=10'''
    txt.c1(t,1)
    t='''\nПримем значение случайного эксцентриситета (мм):'''
    t += '\ne_p='+ str(max([txt.numer['e_a'],txt.numer['e_b'],txt.numer['e_c']]))+ '\n'
    txt.c1(t,60)
    t='''Расчетный эксцентриситет определим как сумму случайного и заданного в нагрузках(мм):
e_0=e_m+e_p'''
    txt.c1(t)
    t='''
Момент от всех нагрузок (кгс \\times м):
M_a=M_0+N_0*(h_0-a)/(2*1000)
Момент от постоянных и длительных нагрузок (кгс \\times м):
M_b=M_1+N_1*(h_0-a)/(2*1000)
\\varphi=1+M_b/M_a
При этом \\varphi  должна быть не менее 0,15 и не более 2
'''
    txt.c1(t)
    t='''Окончательно примем'''
    if txt.numer['\\varphi'] < 0.15:
        t += '\n\\varphi=0.15\n'
    elif txt.numer['\\varphi'] > 2:
        t += '\n\\varphi=2\n'
    else:
        t += '\n\\varphi=' + str(txt.numer['\\varphi']) + '\n'
    txt.c1(t,60)
    t='''\delta=e_0/h_c
При этом значение эксцентриситета не должно быть менее 0,15 и более 1,5 п.8.1.15
'''
    txt.c1(t)
    t='''Окончательно примем'''
    if txt.numer['\delta'] <0.15:
        t +='''\delta=0.15'''
    elif txt.numer['\delta'] >1.5:
        t +='''\delta=1.5'''
    else:
        t +='''\nПолученное в расчете'''
    txt.c1(t,60)
    t ='''
\mu_a=(2*A_s)/(h_c*t_c*10)*E_s/E_b
Жесткость сечения составит:
D=(E_b*t_c*h_c**3)/10**10*(0.0125/(\\varphi*(0.3+\delta))+0.175*\mu_a*((h_0-a)/h_c)**2)
Критическая сила по формуле 7.7 (кгс):
N_cr=3.14^2*D/L_0^2*10^6
По формуле 7.6 СП получим:
\eta_h=1/(1-N_0/N_cr)
Определим эксцентриситет для продольной силы (мм):
e_n=e_p*\eta_h+(h_0-a)/2
Расчетный момент от продольной силы составит (кгс \\times м):
M_cN=(N_0*e_n)/1000
Расчетный момент от моментов с учетом прогиба составит (кгс \\times м):
M_cM=M_0+(M_0-M_1)*\eta_h
'''
    txt.c1(t)
    if txt.numer['M_cN'] >txt.numer['M_cM']:
        t='''Расчетный момент примем от продольной силы с эксцентриситетом (кгс \\times м):
M_c=M_cN
'''
    else:
        t= '''Расчетный момент примем от моментов с учетом прогиба (кгс \\times м):
M_c=M_cM
'''
    txt.c1(t)
    t='''Проверяем прочность сечения согласно п. 3.56
a_n=N_0/(R_b*t_c*h_0*100)
Значение по формуле (3.15):
\\xi_R=0.8/(1+R_s/700)
'''
    txt.c1(t)
    if txt.numer['a_n'] < txt.numer['\\xi_R']:
        t='''Высота сжатой зоны составит (мм):
x=a_n*h_0
Момент который может воспринять сечение по формуле 3.91 (кгс \\times м):
M_r=(R_b*t_c*x)/10*(h_0-x/2)+(R_s*A_s*10)*(h_0-a)*1/10**3
'''
    else:
        t='''a_s=(R_s*A_s)/(R_b*t_c*h_0*10)
\\xi=(a_n*(1-\\xi_R)+2*a_s*\\xi_R)/(1-\\xi_R+2*a_s)
x=h_0*\\xi
Момент который может воспринять сечение по формуле 3.91 (кгс*м):
M_r=(R_b*t_c*x)/10*(h_0-x/2)+(R_s*A_s*10)*(h_0-a)*1/10**3
'''
    txt.c1(t)
    t='''Коэффициент использования по гибкости
k_1=k_g/120
Коэффициент по прочности от действия изгибающего момента составит:
k_2=M_c/M_r'''

    txt.c1(t)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-4:])
    print(text_print)
    text_file = txt.rezult
    # замена не удобных данных
    a ='класса\nВ'
    b = 'класса В'
    text_file = text_file.replace(a, b)
    a = 'D=(E_b \\times t_c \\times h_c^3)/10^10 \\times (0.0125/(\\varphi \\times (0.3+\\delta))+0.175 \\times \\mu_a \\times ((h_0-a)/h_c)^2)='
    text_file = text_file.replace(a, a + '\n=')
    a = 'M_r=(R_b \\times t_c \\times x)/10 \\times (h_0-x/2)+(R_s \\times A_s \\times 10) \\times (h_0-a) \\times 1/10^3='
    text_file = text_file.replace(a, a + '\n=')
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*CCR.csv'):
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