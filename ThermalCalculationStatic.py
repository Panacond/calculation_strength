# -*- coding: utf-8 -*-
# чтение из csv файла данных и расчет стальной прокатной балки
import os, fnmatch, csv, re
import string_calculation
# from ConcreteBeamReinforcing import read_file
def read_file(a):
    a = str(a)
    l=[]
    with open(a,'r',newline='',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return tabl_taxt(l)

def tabl_taxt(tabl):
    text_file = ''
    for i in tabl:
        text_file += i[0] + ' | ' + i[1] + ' | ' + i[2] + ' |\n'
    return text_file

def in_table(table):
    # перевод данных таблицы в нужный формат
    b= list(filter(lambda x:x[0]==' ', table))
    def fun(n):
        n = n[1:]
        return n
    text = ''
    for i in range(len(b)):
        b[i]=b[i][1:]
        if i%2:
            b[i]=b[i]+'\n'
            text +=b[i]
        else:
            b[i] = b[i].replace(',','.')
            b[i]= float(b[i])
            b[i]= round(b[i]/1000,4)
            b[i]= str(b[i])
            text +=b[i] + '\t'
    return text


def calculation(name, text_file):
    # функция основного расчета
    txt = string_calculation.Calc()
    start_text_replace='''**РАСЧЕТНЫЕ УСЛОВИЯ.**

**Климатические параметры.**

Расчетная температура внутреннего воздуха здания  $(t_в)$ :

Расчетная температура внутреннего воздуха для обследуемого здания в соответствии с ГОСТ 30494-96, ГОСТ Р 52539-2006, СанПиН 2.1.3.2630-10, СанПиН 2.1.3.2630-10, СП 44.13330.2011 принята  $t_в=$ +18°С.

Расчетная температура наружного воздуха в холодный период  $(t_н)$ :

Расчетная температура наружного воздуха для города Москва  $t_н$  -30°С принята по СП 131.13330.2012 «Строительная климатология», равной значению средней температуры наиболее холодной пятидневки, обеспеченностью 0,92.

Средняя температура наружного воздуха за отопительный период  $(t_{от})$ :

Средняя температура наружного воздуха за отопительный период для города Москва принята по СП 131.13330.2012 «Строительная климатология»  $t_{от}=$ -1,3°С (для периода со средней суточной температурой наружного воздуха не более 10°С – при проектировании жилых зданий).

Продолжительность отопительного периода  $(Z_{от})$ :

Продолжительность отопительного периода для города Москва принята по СП 131.13330.2012 «Строительная климатология»  $Z_{от}=214$  сут.

Градусо-сутки отопительного периода по формуле 5.2 СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»:

$ГСОП=(t_в–t_от) \\times Z_{от}=(18–(–1,3))×214=4130,2°С \\times сут.$

Зона влажности, согласно СП 131.13330.2012, – 2, нормальная; влажностный режим помещений, согласно СП 50.13330.2012, – нормальный, условия эксплуатации ограждающих конструкций – Б.

**Нормируемые теплоэнергетические параметры:**
Базовые значения требуемого сопротивления теплопередаче ограждающих конструкций  $R^{тр}_0.$ 

Градусо-сутки отопительного периода, ГСОП, °C×сут/год| Стен | Покрытий | Чердачных перекрытий |
:---:|:---:|:---:|:---:|
4130,2| 2.89 | 4,35 | - |

Нормируемое значение приведенного сопротивления теплопередаче ограждающей конструкции в соответствии 5.2 СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»:

$R^{норм}_0=R^{тр}_0 \\times m_p$, где $m_p=0.63$  – для стен;

$R^{норм}_0=R^{тр}_0 \\times m_p$, где $m_p=1$ – для остальных ограждающих конструкций.

Нормируемое значения требуемого сопротивления теплопередаче ограждающих конструкций  $R^{тр}_0.$ 

Градусо-сутки отопительного периода, ГСОП, °C×сут/год| Стен | Покрытий | Чердачных перекрытий |
:---:|:---:|:---:|:---:|
4130,2| 1,82 | 4,35 | - |

**ТЕПЛОТЕХНИЧЕСКИЕ РАСЧЕТЫ ОГРАЖДАЮЩИХ КОНСТРУКЦИЙ.**

**Приведенные сопротивления теплопередаче ограждающих конструкций:**

Сопротивления теплопередаче существующих ограждающих конструкций определены в зависимости от материалов и количества слоев при условиях эксплуатации Б по формулам 6-8 СП 23-101-2004 «Проектирование тепловой защиты зданий».
Сопротивление теплопередаче $R_0$, $м^2 \\times°С$/Вт многослойной ограждающей конструкции определяется в соответствии с п. 9.1.2, формула 8 СП 23-101-2004 «Проектирование тепловой защиты зданий»:

$R_0=\\frac{1}{\\alpha_b}+ \sum {R_s} + \\frac{1}{\\alpha_н}$

где $\\alpha_b$ – коэффициент теплоотдачи внутренней поверхности ограждающих конструкций, таблица 4 СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»;

$R_s$ – термическое сопротивление ограждающей конструкции с последовательно расположенными однородными слоями.

**Конструкции ограждающего элемента**

$\\alpha_b$ = 8,7 Вт/($м^2 \\times°С$) – коэффициент теплоотдачи внутренней поверхности ограждающих конструкций, таблица 4 СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»;

$\\alpha_н=23,0$ Вт/($м^2 \\times°С$) – коэффициент теплоотдачи наружной поверхности ограждающих конструкций для условий холодного периода, таблица 6 СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»;

$R_s$ – термическое сопротивление слоя однородной части фрагмента, ($м^2 \\times °С$)/Вт, определяемое для материальных слоев по формуле $R_s=\\frac{\delta_s}{\lambda_s}$  (E.7 Приложения Е СП 50.13330.2012 «Тепловая защита зданий. Актуализированная редакция СНиП 23-02-2003»).

В таблице ниже предоставлен состав стены (по направлению снаружи внутрь):
'''
    text_replace= 'Описательная часть добавить в конце после выполнения расчета\n'
    txt.c1(text_replace)
    t='''
Материал слоя | Толщина, мм | $\lambda_s$, Вт/($м \\times °С$) |
:---|:---:|:---:|'''
    txt.c1(t)
    find_text = text_file.split('теплопроводность  |')
    t=find_text[1]+ '\n'
    txt.c1(t)
    find_table = find_text[1].split(' |')
    table_temp = '\nR_tr={0}\nТермическое сопротивление отдельных элементов (м^2 \\times°C):\n'
    number = re.search('R_tr= ([^\d] (.*) [^0-9])\\nСлои',text_file).group(2)
    table_temp = table_temp.format(number)
    # перевод таблицы в нужный формат
    t = table_temp + in_table(find_table)
    t = t.replace('\t', '/')
    summ = '''Сумма сопротивлений составит (м^2 \\times °C):
\sum{R_s}='''
    text_list = t.split('\n')
    n = 1
    check = 'Термическое сопротивление отдельных элементов (м^2 \\times°C):'
    numer_i = len(text_list)
    for i in range(len(text_list)):
        
        if text_list[i] == check:
            numer_i = i
        if i > numer_i and i < len(text_list)-1:
            text_list[i]= 'R_s'+ str(n) +'=' + text_list[i]
            if n != 1:
                summ += '+'
            summ += 'R_s'+ str(n)
            n +=1
    t = '\n'.join(text_list)
    t += summ
    txt.c1(t, 80)

    t = '''
Общее термическое сопротивление составит (м^2 \\times°C):
R_0=1/8.7+\sum{R_s}+1/23
k=R_tr/R_0
'''
    txt.c1(t)
    if txt.numer['k'] < 1:
        text_i='''R_0={0} > R_0^тр = {1} (м^2 \\times °С)/Вт
Условие выполняется.
ВЫВОД. Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k={2}'''
    else:
        text_i='''R_0={0} < R_0^тр = {1} (м^2 \\times °С)/Вт
Условие не выполняется.
ВЫВОД. Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k={2}'''
    text_i = text_i.format(str(txt.numer['R_0']),str(txt.numer['R_tr']),str(txt.numer['k']))
    txt.rezult += text_i
    p = txt.finish(name = name)
    # print(p)
    text_print ='\n'.join( p.split('\n')[-6:])
    print(text_print)
    text_file = txt.rezult
    # замена данных для оформления
    text_file = re.sub(r'\tR_tr=[\d\.]*\n',r'', text_file)    
    text_file = text_file.replace(text_replace, start_text_replace)
    return text_file

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*TCS.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        print(text_file)
        from string_calculation import write_file
        write_file(name,text_file)

if __name__ == '__main__':
    main()
    
def CBR(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file