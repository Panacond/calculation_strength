# чтение из csv файла данных и расчет балки
import os, fnmatch, csv
import string_calculation, application_G

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
    # поиск и замена с помощью регулярных выражений
    t='''Расчет по СП 16.13330.2017 Стальные конструкции
8.2 Расчет на прочность изгибаемых элементов сплошного сечения:
'''+t
    txt.c1(t, 60)
    t='''
Коэффициент условий работы (таблица 1):
\gamma_с=0.9
Модуль упругости (кгс/см^2):
E=2060000
Определение геометрических характеристик сечения:
Вспомогательные размеры:
a=b-t_s=18.0-1.0=17.0
h_1=h_0-2*t_p=34.0-2*1.0=32.0
Площадь сечения (см^2):
A_s=b*t_p*2+h_1*t_s
Момент сопротивления в вертикальной плоскости (см^3):
W_x=(b*h_0^3-a*h_1^3)/(6*h_0)
Момент инерции в вертикальной плоскости(см^4):
I_x=(b*h_0^3-a*h_1^3)/12
Радиус инерции в горизонтальной плоскости (см):
i_x=\sqrt(I_x/A_s)=\sqrt(12534.67/68.0)=13.58
Момент инерции в горизонтальной плоскости (см^4):
I_y=2*t_p*b^3/12+h_1*t_s^3/12
Момент сопротивления в горизонтальной (см^3):
W_y=2*t_p*b^2/6+h_1*t_s^2/6
Радиус инерции в горизонтальной плоскости (см):
i_y= \sqrt (I_y/A_s)
Статический момент инерции полусечения (см^3):
S_x=b*t_p*(h_0-t_p)/2+(h_0/2-t_p)*t_s*1.5
8.2.1. Расчет на прочность балок 1-го класса при действии момента 
в одной из главных плоскостей (41)
Требуемый момент сопротивления (см^3):
W_t=M_r/(R_y*\gamma_с)*100=7800.0/(2450.0*0.9)*100=4
Сопротивление сдвигу составит (кгс/см^2):
R_s=0.58*R_y
'''
    txt.c1(t,50)
    # вставка расчета по приложению Ж.1
    input_list='L,h_0,b,t_p,t_s,R_y,n_z,E,I_x,I_y'
    list_number=application_G.list_input(input_list, txt)
    t,tn=application_G.function(list_number)
    txt.c1(t,50)
    if 'f'in txt.kef:
        t='''
Прогиб составит (мм):
f_p=q_n/q_r*(f*10**7)/(E*I_x)
Нормативный прогиб составит (мм):
f_n=L/200*1000
Коэффициент использования по прогибам:
k_3=f_p/(f_n*\gamma_с)'''
        txt.c1(t)
    t='''
8.2.1 Расчет на прочность балок 1 - го класса при действии изгибающего момента (42)
Коэффициент использования:
k_1=W_t/W_x
8.2.1 Расчет на прочность балок 1 - го класса при действии поперечной силы (42)
Коэффициент использования:
k_2=(Q_r*S_x)/(I_x*t_s*R_s*\gamma_с)
8.4.1 Расчет на устойчивость двутавровых балок 1 - го класса, при изгибе 
в плоскости стенки, совпадающей с плоскостью симметрии сечения (69)
Коэффициент использования:
k_4=(M_r*100)/(\\varphi_b*W_x*R_y*\gamma_с)'''
    txt.c1(t)
    p = txt.finish(name = name)
    text_print ='\n'.join( p.split('\n')[-8:])
    print(text_print)
    text_file = txt.rezult
    # замена данных для оформления
    a ='a=8 \\times ((L \\times 100 \\times t_p)/(h_0 \\times b))^2 \\times (1+(0.5 \\times (h_0-2 \\times t_p) \\times t_s^3)/(b \\times t_p^3))='
    text_file = text_file.replace(a, a + '\n=')
    a = 'Коэффициент условий работы (таблица 1):\n\\gamma_с='
    b = 'Коэффициент условий работы (таблица 1): \\gamma_с='
    text_file = text_file.replace(a, b)
    a='Прогиб балки ( (10^9 \\times  кгс \\times  мм^3)/EI  ):\nf='
    b='Прогиб балки ( (10^9 \\times  кгс \\times  мм^3)/EI  ): f='
    text_file = text_file.replace(a, b)
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*SBS.csv'):
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
    
def SBS(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file