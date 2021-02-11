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
Расчет внецентренно сжатых (сжато-изгибаемых) элементов (9.2.1):
'''+t
    txt.c1(t, 60)
    t='''Определение геометрических характеристик сечения
Вспомогательные размеры:
a=b-t_s=18.0-1.0=17.0
h_1=h_0-2*t_p=34.0-2*1.0=32.0
Площадь сечения (см^2):
A_s=b*t_p*2+h_1*t_s
Момент инерции в плоскости x (см^4):
I_x=(b*h_0^3-a*h_1^3)/12
Момент сопротивления в вертикальной плоскости x(см^3):
W_x=(b*h_0^3-a*h_1^3)/(6*h_0)
Радиус инерции в плоскости x(см):
i_x= \sqrt (I_x/A_s)= \sqrt (12534.67/68.0)=13.58
Момент инерции в плоскости у (см^4):
I_y=2*t_p*b^3/12+h_1*t_s^3/12
Момент сопротивления в плоскости у (см^3):
W_y=2*t_p*b^2/6+h_1*t_s^2/6
Радиус инерции в плоскости у (см):
i_y= \sqrt (I_y/A_s)
'''
    txt.c1(t,50)
    t='''
Модуль упругости (кгс/см^2):
E=2000000
Коэффициент условий работы:
\gamma_c=0.95
9.2.1. Расчет на прочность элементов сплошного сечения 
Коэффициент для расчета элементов конструкций с учетом развития
пластических деформаций (приложение Е Таблица Е.1 тип сечения1)
Площадь полки (см^2):
A_f=b*t_p
Площадь стенки (см^2):
A_w=t_s*(h_0-2*t_p)
k_sect=A_f/A_w
'''
    txt.c1(t,50)
    import numpy
    number = numpy.interp(txt.numer['k_sect'],[0.25,0.5,1.0,2.0],[1.19,1.12,1.07,1.04])
    t='c_x=' + str(number)
    txt.c1(t)
    t='''
c_y=1.47
n_e1=1.5
9.1.1 Расчет на прочность внецентрено сжатых элементов (105):
k_1=(N/(A_s*R_y*\gamma_c))**(n_e1)+(M*100)/(c_x*W_x*R_y*\gamma_c)
9.2 Расчет на устойчивость внецентренно сжатых 
(сжато-изгибаемых) элементов в плоскости действия момента
Эксцентриситет буде равен (м):
e=M/N
Относительный эксцентриситет
m=(100*e*A_s)/W_x
Расчетная длина элемента:
l_e=L*\mu
Определение гибкости по оси x:
\lambda_x=l_e/i_x*100
Определение гибкости по оси y:
\lambda_y=l_e/i_y*100
Определение условной гибкости:
\lambda\\bar_x=\lambda_x*%(R_y/E)
Коэффициент \eta  определим по таблице Д.2
тип сечения 5
'''
    txt.c1(t,50)
    if txt.numer['m']>20:
        t='Расчет надо вести как изгибаемых элементов'
        txt.c1(t)
    if txt.numer['\lambda\\bar_x'] > 5:
        if txt.numer['k_sect'] < 0.25:
            t= "\eta=1.2"
        elif txt.numer['k_sect'] < 0.5:
            t= "\eta=1.25"
        else:
            t="\eta=1.3"
    else:
        if txt.numer['m'] < 5:
            if txt.numer['k_sect'] < 0.25:
                t= "\eta=(1.45-0.05*m)-0.01*(5-m)*\lambda\\bar_x"
            elif txt.numer['k_sect'] < 0.5:
                t= "\eta=(1.75-0.1*m)-0.02*(5-m)*\lambda\\bar_x"
            else:
                t="\eta=(1.9-0.1*m)-0.02*(6-m)*\lambda\\bar_x"
        else:
            if txt.numer['k_sect'] < 0.25:
                t= "\eta=1.2"
            elif txt.numer['k_sect'] < 0.5:
                t= "\eta=1.25"
            else:
                t="\eta=1.4-0.02*\lambda\\bar_x"
    txt.c1(t)
    t='''
Приведенный относительный эксцентриситет
m_ef=\eta*m
Коэффициент \phi_e  по таблице Д.3 в зависимости от значений \lambda\\bar_x, m_ef:
'''
    txt.c1(t)
    t='\lambda\\bar_x=\lambda\\bar_x\nm_ef=m_ef\n' 
    txt.c1(t)
    import tableD3
    t = '\phi_e=' + str(tableD3.func_interpoly(txt.numer['m_ef'],txt.numer['\lambda\\bar_x']))+'/1000'
    txt.c1(t)
    t='''
9.2.2 Расчет на устойчивость внецентренно сжатых (сжато-изгибаемых) элементов
при действии момента, совпадающей с плоскостью симметрии по формуле (109):
''' 
    txt.c1(t,50)
    t='k_2=N/(\phi_e*A_s*R_y*' + str(txt.numer['\gamma_c']) + ')'
    txt.c1(t)
    t='''
Расчет по устойчивости из плоскости действия момента п. 9.2.5
m_x=((100*M)/N)*(A_s/W_x)
'''
    txt.c1(t,50)
    t='''
7.1.3. Условная гибкость стрежня в плоскости x:
l\\bar_y=\lambda_y*%(R_y/E)=73.73*(2350.0/2000000.0)^0.5=2.53
'''
    txt.c1(t,40)
    if txt.numer['\lambda\\bar_x'] > 0.6:
        t='''
Коэффициенты условий работы (таблица 7):
a1=0.04
b1=0.09
7.1.3. Определение коэффициента (9):
d=9.87*(1-a1+b1*l\\bar_y)+l\\bar_y^2=9.87*(1-19.01+0.09*2.53)+2.53^2=18.12
7.1.3. Значение коэффициента \phi  при l\\bar   > 0.6 следует определять по формуле  (8):
\phi=0.5*(d-%(d^2-39.48*l\\bar_y^2))/(l\\bar_y^2)=0.5*(18.12-(18.12^2-39.48*2.53^2)^0.5)/(2.53^2)=0.74
'''
        txt.c1(t,40)
        if txt.numer['\phi']> 7.6/txt.numer['l\\bar_y']**2:
            t='''
При значениях  условной гибкости выше
l\\bar_ymax=7.6/l\\bar_y**2
\phi=7.6/l\\bar_y**2
'''
            txt.c1(t,50)
    else:
        t='''
7.1.3. При значениях l\\bar_y > 0.6 для сечения типа а и b
\phi=1'''
        txt.c1(t,50)
    t='''
Определение коэффициентов \\alpha  и \\beta  (таблица 21)
'''
    txt.c1(t,50)
    if txt.numer['m_x']<=1:
        t='\\alpha=0.7'
    else:
        t='\\alpha=0.65+0.05*m_x'
    txt.c1(t)
    txt.c1('\n\n')
    if txt.numer['l\\bar_y'] >=3.14:
        t='\\beta=2'
    else:
        t='\\beta=1'
    txt.c1(t)
    t='''
7.1.3. Условная гибкость стрежня в плоскости y:
l\\bar_y=\lambda_y*%(R_y/E)
'''
    txt.c1(t)
    if txt.numer['m_x']<5:
        t ='''
9.2.5 Коэффициент с в формуле (111) при значениях m_x < 5 по формуле (112):
c=\\beta/(1+\\alpha*m_x)
'''
        txt.c1(t,50)
        if txt.numer['c']>1:
            t='''
    Но не более 1
    c=1
    '''
            txt.c1(t,50)
    elif txt.numer['m_x']>=10:
        t='''
9.2.5. Коэффициент c в формуле (111) при значениях m_x >10
\\varphi_b  определяемый согласно требований 8.4.1 и приложения Ж, как балки с двумя
и более закреплениями сжатого пояса
n_z=2
'''
        txt.c1(t,50)
        # вставка расчета по приложению Ж.1
        input_list='L,h_0,b,t_p,t_s,R_y,n_z,E,I_x,I_y'
        list_number=application_G.list_input(input_list, txt)
        t,tn=application_G.function(list_number)
        txt.c1(t,50)
        t='''
9.2.5. Коэффициент c в формуле (111) при значениях m_x >10 по формуле (113):
c=1/(1+m_x*\phi/\\varphi_b)      
'''
        txt.c1(t,50)
    else:
        t='''
9.2.5. Коэффициент c в формуле (111) при значениях 5 < m_x < 10 по формуле (113):
c_5  определяется по формуле (112) при значении
m_x5=5
c_5=\\beta/(1+\\alpha*m_x5)
c_10  по формуле (113) при
m_x10=10
\\varphi_b  определяемый согласно требований 8.4.1 и приложения Ж, как балки с двумя
и более закреплениями сжатого пояса
n_z=2
'''
        txt.c1(t,80)
        # вставка расчета по приложению Ж.1
        input_list='L,h_0,b,t_p,t_s,R_y,n_z,E,I_x,I_y'
        list_number=application_G.list_input(input_list, txt)
        t,tn=application_G.function(list_number)
        txt.c1(t,50)
        t='''
9.2.5. Коэффициент c_10  по формуле (113):
c_10=1/(1+m_x10*\phi/\\varphi_b)
9.2.5. Коэффициент c в формуле (111)  при значениях 5 < m_x  < 10 по формуле (114)
c=c_5*(2-0.2*m_x)+c_10*(0.2*m_x-1)
'''
        txt.c1(t,50)

    t='''
9.2.4 Расчет на устойчивость внецентренно сжатых (сжато-изгибаемых) стержней
сплошного сечения, кроме коробчатого, из плоскости действия момента
при изгибе их в плоскости наибольшей жесткости, совпадающей с плоскостью
симметрии, а также швеллеров стоит выполнять по формуле (111)
'''
    txt.c1(t,50)
    t='k_5=N/(c*\phi*A_s*R_y*' + str(txt.numer['\gamma_c']) + ')'
    txt.c1(t)

    t='''    
10.4 Предельная гибкость элементов
10.4.1 Гибкости элементов \lambda  (l_e/i) не должны превышать
предельных значений \lambda_u, приведенных в таблице 32 для сжатых элементов 
'''
    txt.c1(t)
    t='''
Коэффициент альфа (таблица 32):
'''
    t='a_2=N/('+ str(txt.numer['\phi_e']) + '*A_s*R_y*' + str(txt.numer['\gamma_c']) + ')'
    txt.c1(t)
    if txt.numer['a_2'] < 0.5:
        t = ('\nПринимаем значение коэффициента альфа не менее 0.5:\n' +
        'a_2=0.5\n')
        txt.c1(t)
    t ='''
Предельная гибкость сжатого элемента (таблица 32):
l_u=180-60*a_2
Коэффициент использования по прочности
k_1=k_1
Коэффициент использования по устойчивости в плоскости действия момента
k_2=k_2
Коэффициент использования по устойчивости из плоскости действия момента
k_5=k_5
Коэффициент предельной гибкости по оси х:
k_3=\lambda_x/l_u
Коэффициент предельной гибкости по оси y:
k_4=\lambda_y/l_u'''
    txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-10:])
    print(text_print)
    text_file = txt.rezult
    # замена текста
    a ='(N/(A_s \\times R_y \\times \\gamma_c))^n_e1+M/(c_x \\times W_x \\times R_y \\times \\gamma_c)='
    text_file = text_file.replace(a, a + '\n=')
    text_file = text_file.replace('\tc_y=1.47\tn_e1=1.5','    c_y=1.47    n_e1=1.5')
    a=") \\times \lambda\\bar_x="
    text_file = text_file.replace(a,a +'\n=')
    a ='a=8 \\times ((L_ef \\times 100 \\times t_p)/(h_0 \\times b))^2 \\times (1+(0.5 \\times (h_0-2 \\times t_p) \\times t_s^3)/(b \\times t_p^3))='
    text_file = text_file.replace(a, a + '\n=')
    a ='k_1=(N/(A_s \\times R_y \\times \gamma_c))^(n_e1)+(M \\times 100)/(c_x \\times W_x \\times R_y \\times \gamma_c)='
    text_file = text_file.replace(a, a + '\n=')
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*SBM.csv'):
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