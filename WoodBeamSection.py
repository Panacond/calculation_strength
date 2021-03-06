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
    t='''Расчет выполним по СП 64.13330.2011 Деревянные конструкции
'''+t
    txt.c1(t)
    if txt.numer['b_0']!=0:
        t='''Определяем момент сопротивления (см^3):
W_tr=b_0*(h_0^2)/6=5.0*(17.0^2)/6=240.83
Определяем статический момент инерции(см^3):
S_br=b_0*h_0/2*h_0/4=5.0*17.0/2*17.0/4=180.62
Определяем момент инерции(см^4):
I_tr=b_0*(h_0^3)/12=5.0*(17.0^3)/12=2047.08
'''
        txt.c1(t)
    else:
        t='''Определяем момент сопротивления (см^3):
W_tr=3,14*h_0**3/32
Определяем статический момент инерции(см^3):
S_br=h_0**3/12
Определяем момент инерции относительно оси х(см^4):
I_tr=3,14*h_0**4/64
Ширина сечения (см):
b_0=h_0
'''
        txt.c1(t)        
    t='''
5.1 Расчетные сопротивления древесины сосны, ели и лиственницы европейской влажностью 12 % для основного сочетания нагрузок (режим В согласно таблице В.1)в сооружениях нормального (2-го согласно приложению Г) уровня ответственности при сроке эксплуатации до 50 лет приведены в таблице 3. Расчетные сопротивления для других пород древесины устанавливают путем умножения величин, приведенных в таблице 3, на переходные коэффициенты, указанные в таблице 5. Расчетные сопротивления LVL из однонаправленного шпона приведены в таблице 4:
а) элементы прямоугольного сечения (за исключением указанных в подпунктах «б», «в») высотой до 50 см:
R_i=14
а) для различных условий эксплуатации конструкций — коэффициент указанный в таблице 7 (По таблице 1 принимаем класс эксплуатации 3):
m_b=1
б) для конструкций, эксплуатируемых при установившейся температуре воздуха до +35 °С коэффициент:
m_t=1
в) для конструкций, в которых напряжения в элементах, возникающие от постоянных и временных длительных нагрузок, превышают 80 % суммарного напряжения от всех нагрузок, — коэффициент:
m_d=1
Расчетные сопротивления, приведенные в таблицах 3,4 и 6,следует разделить на коэффициенты надежности по сроку службы (таблица 12):
\gamma_h=1
Расчетное сопротивление составит (МПа):
R_u=R_i*m_b*m_t*m_d/\gamma_h=14.0*0.9*1.0*1.0/1.0=12.6
6.9 Расчет изгибаемых элементов, обеспеченных от потери устойчивости плоской формы деформирования (см.6.14 и 6.15), на прочность по нормальным напряжениям следует производить по формуле (МПа):
\sigma_r=M_y*10/W_tr=259.14*10/240.83=10.76
Коэффициент использования составит:
k_1=\sigma_r/R_u=10.76/12.6=0.85

5 Скалывание вдоль волокон:
а) при изгибе элементов из цельной древесины (МПа):
R_s0=1.6
Расчетное сопротивление  скалыванию составит (МПа):
R_sk=R_s0*m_b*m_t*m_d/\gamma_h=1.6*0.9*1.0*1.0/1.0=1.44
Расчетное сопротивление скалыванию в (МПа):
6.10 Расчет изгибаемых элементов на прочность по скалыванию следует выполнять по формуле (МПа):
\\tau_r=Q_0/10*S_br/(I_tr*b_0)=511.88/10*180.62/(2047.08*5.0)=0.9
Коэффициент использования составит:
k_2=\\tau_r/R_sk=0.9/1.44=0.62

Определение расчетных характеристик материалов сопротивлению смятия:
в) элементы прямоугольного сечения шириной свыше 13 см при высоте сечения свыше 13 до 50 см (МПа):
R_s1=10
Расчетное сопротивление  скалыванию составит (МПа):
R_sm=R_s1*m_b*m_t*m_d/\gamma_h=10.0*0.9*1.0*1.0/1.0=9.0
7.2 Расчетную несущую способность соединений, работающих на смятие и скалывание, следует определять по формулам:
Ширина площадки смятия (см):
b_1=b_0
Высота сечения (см):
h_1=b_0
а) из условия смятия древесины (МПа):
T_r=Q_0/10*S_br/(I_tr*b_0)=511.88/10*180.62/(2047.08*5.0)=0.9
Коэффициент использования составит:
k_3=T_r/R_sm=0.9/9.0=0.1
6.14 Расчет на устойчивость плоской формы деформирования изгибаемых элементов
Коэффициент, зависящий от формы эпюры изгибающих моментов на участке, определяемый по таблице Е.2 приложения Е настоящих норм:
k_f=1.13
Коэффициент \\varphi_m для изгибаемых элементов прямоугольного постоянного поперечного сечения, шарнирно закрепленных от смещения из плоскости изгиба и закрепленных от поворота вокруг продольной оси в опорных сечениях, следует определять по формуле (25):
\\varphi_m=140*b_0**2/(L_r*h_0*100)*k_f
Расчет на устойчивость плоской формы деформирования изгибаемых элементов прямоугольного постоянного сечения следует производить по формуле (24):
\sigma_r=M_y*10/(W_tr*\\varphi_m)
Коэффициент использования составит:
k_4=\sigma_r/R_u
'''
    txt.c1(t)
    if 'f' in txt.numer:
        t='''5.3 Модуль упругости древесины и LVL при расчете по предельным состояниям 
второй группы следует принимать равным: вдоль волокон (кгс/см^2):
E=10**5
Прогиб составит (мм):
f_0=q_n/q_r*(f*10**7)/(E*I_tr)
Коэффициент учитывающий изменение высоты сечения балки по длине (таблица Е.2):
\\beta=1
Значения коэффициентов k_a и с для основных расчетных схем балок приведены в таблице Е.3 приложения Е:
k_a=0,15+0,85*\\beta
c=15,4+3,8*\\beta
Наибольший прогиб шарнирно-опертых и консольных изгибаемых элементов постоянного и переменного сечений f следует определять по формуле (55) (мм):
f_p=f_0/k_a*(1+c*(h_0/(L_r*100))**2)
Нормативный прогиб составит (мм):
f_n=L_r/200*1000=5.5/200*1000=4
Коэффициент использования по прогибам:
k_5=f_p/f_n
'''
    txt.c1(t)
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-5:])
    # print(text_print)
    text_file = txt.rezult
    # замена не удобных данных
    list_a = [
        'коэффициенты надежности по сроку службы (таблица 12):',
        '80 % суммарного напряжения от всех нагрузок, — коэффициент:',
        'температуре воздуха до +35 °С коэффициент:',
        '(По таблице 1 принимаем класс эксплуатации 3):',
        '«б», «в») высотой до 50 см:',
        'Высота сечения или диаметр для круга (см): ',
        'Ширина сечения (для круга 0) (см): ',
        'Длина балки м:',
        'Прогиб балки ( (10^9 \\times  кгс \\times  мм^3)/EI ):',
        'Нормативная нагрузка (кг/м^2):',
        'Расчетная нагрузка (кг/м^2):',
        'свыше 13 см при высоте сечения свыше 13 до 50 см (МПа):',
        'таблице Е.2 приложения Е настоящих норм:',
        'а) при изгибе элементов из цельной древесины (МПа):']
    for a in list_a:
        text_file = text_file.replace(a+"\n", a+" ")
    text_file = text_file.replace("составит (кгс  \\times м):\nM_y=", "составит (кгс  \\times м): M_y=")
    text_file = text_file.replace("нагрузок (кг):\nQ_0=", "нагрузок (кг): Q_0=")
    text_file = text_file.replace("сечения (см): \nb_0=", "сечения (см): b_0=")
    text_file = text_file.replace("сечения (см): \nh_0=", "сечения (см): h_0=")
    text_file = text_file.replace("смятия (см):\nb_1=", "смятия (см): b_1=")
    text_file = text_file.replace("сечения (см):\nh_1=", "сечения (см): h_1=")
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*WBR.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        # print(text_file)
    pass

if __name__ == '__main__':
    main()
    
def WBS(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file