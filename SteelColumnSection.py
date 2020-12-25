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
    t = text_file
    # поиск и замена с помощью регулярных выражений
    t='''Расчет по СП 16.13330.2017 Стальные конструкции
Расчет центрально сжатых элементов:
'''+t
    txt.c1(t, 60)
    if txt.numer['S_v']==1:
        t='''
Вспомогательные размеры:
a=b-t_s=18.0-1.0=17.0
h_1=h_0-2*t_p=34.0-2*1.0=32.0
Площадь сечения (см^2):
A_s=b*t_p*2+h_1*t_s
Момент инерции в плоскости x (см^3):
I_x=(b*h_0^3-a*h_1^3)/12
Момент сопротивления в вертикальной плоскости x(см^4):
W_x=(b*h_0^3-a*h_1^3)/(6*h_0)
Радиус инерции в плоскости x(см):
i_x= \sqrt (I_x/A_s)= \sqrt (12534.67/68.0)=13.58
Момент инерции в плоскости у (см^4):
I_y=2*t_p*b^3/12+h_1*t_s^3/12
Момент сопротивления в плоскости у (см куб):
W_y=2*t_p*b^2/6+h_1*t_s^2/6
Радиус инерции в плоскости у (см):
i_y= \sqrt (I_y/A_s)
Минимальный радиус инерции (см):
i_0=1*i_y=1*4.34=4.34'''
    elif txt.numer['S_v']==2:
        t='''
Вспомогательные размеры:
a=b-2*t_s
h_1=h_0-2*t_p
Площадь сечения (см^2):
A_s=b*h_0-a*h_1
Момент инерции в плоскости x (см^3):
I_x=(b*h_0^3-a*h_1^3)/12
Момент сопротивления в вертикальной плоскости x(см^4):
W_x=(b*h_0^3-a*h_1^3)/(6*h_0)
Минимальный радиус инерции (см):
i_0= \sqrt (I_x/A_s)'''
    else:
        t='''
Радиус инерции в плоскости (см):
i_0= \sqrt (I_x/A_s)='''
    txt.c1(t,50)
    t='''
Проверка устойчивости элемента.
Модуль упругости (кгс/см^2):
E=2000000
Коэффициент условий работы:
\gamma_c=0.95
Проверка элемента прочность (кгс/см^2):
\sigma=N/(A_s*\gamma_c)
Коэффициенты условий работы по СП16.13330.2017 Стальные конструкции таблица 7:
a1=0.04
b=0.09
Расчетная длина элемента:
l_e=L*m=3.2*1.0=3.2
Определение гибкости:
l_x=l_e/i_0*100=3.2/4.34*100=73.73
Определение условной гибкости:
l_y=l_x*%(R_y/E)=73.73*(2350.0/2000000.0)^0.5=2.53
Определение коэффициента:
d=9.87*(1-a1+b*l_y)+l_y^2=9.87*(1-19.01+0.09*2.53)+2.53^2=18.12
Вычисление \phi:
\phi=0.5*(d-%(d^2-39.48*l_y^2))/(l_y^2)=0.5*(18.12-(18.12^2-39.48*2.53^2)^0.5)/(2.53^2)=0.74
'''
    txt.c1(t,50)
    if txt.numer['\phi']>1:
        txt.numer['\phi']=1
    t = ('Принимаем значение коэффициента \phi:\n'+
'\phi='+str(txt.numer['\phi'])+'\n')
    txt.c1(t)
    t='''Использование по прочности составит:
K_1=\sigma/R_y
Проверка устойчивости:
K_2=N/(\phi*A_s*R_y*\gamma_c)=71.0/(0.74*71.0*2350.0*0.95)*1000=0.61
Коэффициент альфа:
a_2=N/(\phi*A_s*R_y*\gamma_c)=71.0/(0.74*71.0*2350.0*0.95)*1000=0.61
'''
    txt.c1(t)
    if txt.numer['a_2']<0.5:
        txt.numer['a_2']=0.5
    t = ('Принимаем значение коэффициента альфа:\n'+
    'a_2='+str(txt.numer['a_2'])+'\n')
    txt.c1(t)
    t ='''Предельная гибкость:
l_u=180-60*a_2=180-60*19.02=143.4
Коэффициент предельной гибкости:
K_3=l_x/l_u=73.73/143.4=0.51'''
    txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-12:])
    print(text_print)
    text_file = txt.rezult
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