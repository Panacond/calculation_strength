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
    # print(t)
    # поиск и замена с помощью регулярных выражений
    import re
    find_concrete = re.search('В\d\d', t).group()
    t = re.sub('В\d\d',find_concrete, t)
    number_concrete = int(find_concrete[1:])
    t = re.sub('R_b= 17','R_b='+ str(concrete[number_concrete]) +'', t)
    t='''Расчет железобетонного элемента на изгиб по СП 52-103-2003
Предварительно напряженные бетонные и железобетонные конструкции 
'''+ t
    txt.c1(t,60)
    t = '''Изгибающий момент от постоянных нагрузок (кН \\times м): 
M_sh=M_sh/100
Изгибающий момент от всех нагрузок (кН \\times м): 
M_p=M_sh/Q_a*Q_p
Тогда расчетное значение будет:
R_s1=R_n/1.2=1400.0/1.2=1166.67
Площадь сечения в растянутой зоне (мм^2):
A_sp1=3.14*(D_sp1/10)^2/4*n_bsp1*100=3.14*(5.0/10)^2/4*80.0*100=1570.0
Площадь сечения в сжатой зоне (мм^2):
A_sg1=3.14*(D_sg1/10)^2/4*n_bsg1*100=3.14*(5.0/10)^2/4*20.0*100=392.5
Площадь сечения в растянутой зоне (мм^2):
A_sp2=3.14*(D_sp2/10)^2/4*n_bsp2*100=3.14*(10.0/10)^2/4*0.0*100=0.0
Предварительное напряжение с учетом всех потерь
для арматуры в растянутой зоне (МПа):
\sigma_sp1=R_n*0.4=1400.0*0.4=560.0
для арматуры в сжатой зоне (МПа):
\sigma_sp2=R_n*0.3=1400.0*0.3=420.0
Проверить прочность сечения
Высота сечения до центра тяжести арматуры (мм):
h_0=h_1-a_1=700.0-60.0=640.0
Коэффициент примем по п.3.10:
\gamma_sp=1.1
Напряжение в напрягаемой арматуре сжатой зоны (МПа):
\sigma_sp3=400-\gamma_sp*\sigma_sp2=400-1.1*800.0=-480.0
По формуле 3.3 определим \\xi_1:
\\xi_1=(R_s1*A_sp1+R_s2*A_sp2-\sigma_sp3*A_sg1)/(R_b*b_1*h_0)=(1170.0*1570.0+355.0*0.0--480.0*392.5)/(17.0*300.0*640.0)=0.62
Предварительное напряжение арматуры растянутой зоны принимаем с учетом коэф. \gamma_sp:
\gamma_sp=0.9
Предварительное напряжение в (МПа):
\sigma_sp4=\gamma_sp*\sigma_sp1=0.9*700.0=630.0
По таблице 3.1 при классе арматуры В_р 1400 и при
k=\sigma_sp4/R_s1=630.0/1170.0=0.54
находим
\\xi_R=0.341'''
    txt.c1(t,60)
    if txt.numer['\\xi_1'] > txt.numer['\\xi_R']:
        t = '''Поскольку \\xi_1 > \\xi_R прочность сечения проверяем из условия (3.7), принимая
a_m=\\xi_1*(1-\\xi_1/2)=0.62*(1-0.62/2)=0.43
a_R=\\xi_R*(1-\\xi_R/2)=0.341*(1-0.341/2)=0.28
Несущая способность сечения кН \\times м):
M_m=((2*a_m+a_R)/3*R_b*b_1*h_0^2+\sigma_sp3*A_sg1*(h_0-a_p))/10^6=((2*0.43+0.28)/3*17.0*300.0*640.0^2+-480.0*392.5*(640.0-30.0))/10^6=678.88
Прочность на действие всех нагрузок обеспечена, с коэффициентом:
K_1=M_p/M_m=45.0/678.88=0.07
Проверим прочность на действие постоянных и длительных нагрузок
При этом коэффициент \gamma_b2:
\gamma_b2=0.9
Расчетное сопротивление бетона (МПа):
R_1=R_b*\gamma_b2=17.0*0.9=15.3
\\xi_1=(R_s1*A_sp1+R_s2*A_sp2+\sigma_sp3*A_sg1)/(R_1*b_1*h_0)=(1170.0*1570.0+355.0*0.0+-480.0*392.5)/(15.3*300.0*640.0)=0.56
Поскольку \\xi_1 > \\xi_R прочность сечения проверяем из условия (3.7), принимая
a_m=\\xi_1*(1-\\xi_1/2)=0.56*(1-0.56/2)=0.4
Несущая способность сечения кН \\times м):
M_m=((2*a_m+a_R)/3*R_b*b_1*h_0^2+\sigma_sp3*A_sg1*(h_0-a_p))/10^6=((2*0.4+0.28)/3*17.0*300.0*640.0^2+-480.0*392.5*(640.0-30.0))/10^6=637.1
Прочность на действие всех нагрузок обеспечена, с коэффициентом:
K_2=M_sh/M_m=22.5/637.1=0.04
'''
    else:
        t = '''
Поскольку \\xi_1 < \\xi_R прочность сечения проверяем из условия (3.2), принимая
\gamma_s3=1.25-0.25*\\xi_R/\\xi_1=1.25-0.25*0.341/0.12=0.54
x=(\gamma_s3*R_s1*A_sp1+R_s2*A_sp2)/(R_b*b_1)=(0.54*1166.67*471.0+1166.67*235.5)/(17.0*1500.0)=22.41
Несущая способность сечения кН \\times м):
M_m=R_b*b_1*x*(h_0-0.5*x)/10^6=17.0*1500.0*22.41*(190.0-0.5*22.41)/10^6=102.17
Прочность на действие всех нагрузок обеспечена, с коэффициентом:
K_1=M_p/M_m=72.43/102.17=0.71'''
    txt.c1(t)
    p = txt.finish(name = name)
    print(p[-10:])
    text_file = txt.rezult
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*CBP.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
    pass

if __name__ == '__main__':
    main()

def CBP(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file