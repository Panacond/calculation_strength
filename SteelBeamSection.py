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
Расчет изгибаемых элементов сплошного сечения:
'''+t
    txt.c1(t, 60)
    t='''
Коэффициент условий работы (таблица 1):
\gamma_с=0.9
Модуль упругости (кгс/см^2):
E=2060000
Вспомогательные размеры:
a=b-t_s=18.0-1.0=17.0
h_1=h_0-2*t_p=34.0-2*1.0=32.0
Площадь (см^2):
A_s=b*t_p*2+h_1*t_s
Момент сопротивления в вертикальной плоскости (см^3):
I_x=(b*h_0^3-a*h_1^3)/12
Момент инерции в вертикальной плоскости(см^4):
W_x=(b*h_0^3-a*h_1^3)/(6*h_0)
Радиус инерции в горизонтальной плоскости (см):
i_x= \sqrt (I_x/A_s)= \sqrt (12534.67/68.0)=13.58
Момент инерции в горизонтальной плоскости (см^4):
I_y=2*t_p*b^3/12+h_1*t_s^3/12
Момент сопротивления в горизонтальной (см^3):
W_y=2*t_p*b^2/6+h_1*t_s^2/6
Радиус инерции в горизонтальной плоскости (см):
i_y= \sqrt (I_y/A_s)
Статический момент инерции полусечения (см^3):
S_x=b*t_p*(h_0-t_p)/2+(h_0/2-t_p)*t_s*1.5
Требуемый момент сопротивления (см^3):
W_t=M_r/(R_y*\gamma_с)*100=7800.0/(2450.0*0.9)*100=4
Сопротивление сдвигу составит (кгс/см^2):
R_s=0.58*R_y
Прогиб составит (мм):
f_p=5/384*q_n*L^4/(E*I_x)*10**7
Нормативный прогиб составит (мм):
f_n=L/200*1000=5.5/200*1000=4
Проверка на общую устойчивость
a=8*((L*100*t_p)/(h_0*b))**2*(1+(0.5*(h_0-2*t_p)*t_s**3)/(b*t_p**3))
Расчетную длину пролета принимаем (м):
L_ef=L/(n_z+1)
'''
    txt.c1(t,50)
    if txt.numer['n_z']==0:
        if txt.numer['a']>40:
            t='''При значениях а больших 40 и нагрузке приложенной к сжатому поясу коэффициент составит:
\Psi=3.15+0.04*a-2.7*10**(-5)*a**2'''
        else:
            t='''При значениях а меньших 40 и нагрузке приложенной к сжатому поясу коэффициент составит:
\Psi=1.6+0.08*a'''
    else:
        if txt.numer['a']>40:
            t='''При значениях а больших 40 и нагрузке приложенной к сжатому поясу коэффициент составит:
\Psi=3.6+0.04*a-3.5*10**(-5)*a**2'''
        else:
            t='''При значениях а меньших 40 и нагрузке приложенной к сжатому поясу коэффициент составит:
\Psi=2.25+0.07*a'''
    txt.c1(t)
    t='''\nЗначение коэффициента вычисляются по формуле (Ж.3):
\\varphi_1=\Psi*I_y/I_x*(h_0/(L_ef*100))**2*E/R_y'''
    txt.c1(t)
    if txt.numer['\\varphi_1']>0.85:
        t='''
При значениях  \\varphi_1 > 0.85:
\\varphi_b=0.68+0.21*\\varphi_1'''
    else:
        t='''
При значениях  \\varphi_1 < 0.85:
\\varphi_b=\\varphi_1'''
    txt.c1(t, 60)
    if txt.numer['\\varphi_1'] > 1:
        t ='''При значениях \\varphi_1 > 1:
\\varphi_b=1'''
        txt.c1(t)
    t='''
Коэффициент использования по прочности от изгибающего момента:
k_1=W_t/W_x
Коэффициент использования по прочности от поперечной силы:
k_2=(Q_r*S_x)/(I_x*t_s*R_s*\gamma_с)
Коэффициент использования по прогибам:
k_3=f_p/(f_n*\gamma_с)
Коэффициент использования по устойчивости:
k_4=(M_r*100)/(\\varphi_b*W_x*R_y*\gamma_с)'''
    txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-8:])
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