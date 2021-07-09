# -*- coding: utf-8 -*-
# чтение из csv файла данных и расчет металлических узлов
import string_calculation

def calcSVR(name, text_file):
    txt = string_calculation.Calc()
    t = text_file
    t=('''Расчет по СП 16.13330.2017 Стальные конструкции
14.1 Сварные соединения
14.1.16 Расчет сварного соединения с угловыми швами при действии силы N,
проходящей через центр тяжести соединения, следует выполнять на срез (условный) по одному из двух сечений (рисунок 20)
'''
    +t)
    txt.c1(t,60)
    t = '''Определение расчетного сопротивления по границе сплавления Таблица 4 (кгс/см^2):
R_wz=0.45*R_un
Коэффициенты принимаются по таблице 39 для ручной или механизированной сварки:
\\beta_f=0.7
\\beta_z=1.0
Коэффициент условий работы (таблица 1):
\gamma_с=0.9
S=(\\beta_f*R_wf)/(\\beta_z*R_wz)
'''
    txt.c1(t)
    if txt.numer['S'] <= 1:
        t = '''При S меньше или равно 1 расчет ведем по металлу шва формула (176):
k_1=N/(\\beta_f*k_f*l_w*R_wf*\gamma_с)*10**2
'''
    else:
        t = '''При S меньше или равно 1 расчет ведем по металлу границы сплавления формула (177):
k_1=N/(\\beta_z*k_f*l_w*R_wz*\gamma_с)*10**2
'''
    txt.c1(t)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    # замена текста
    text_file = text_file.replace('\n\\beta_z=','    \\beta_z=')
    text_file = text_file.replace('\nR_un=','    R_un=')
    text_file = text_file.replace('\n\gamma_с=','    \gamma_с=')
    return text_file

def SVR(name, tabl):
    from support_function import tabl_taxt
    text_file = tabl_taxt(tabl)
    text_file = calcSVR(name, text_file)
    return text_file

def calcBSR(name, text_file):
    # болтовой узел на срез
    txt = string_calculation.Calc()
    t = text_file
    t=('''Расчет по СП 16.13330.2017 Стальные конструкции
14.2 Болтовые соединения
14.2.1 Для болтовых соединений элементов стальных конструкций следует
применять болты согласно приложению Г.
Коэффициент условий работы, определяемый по таблице 1
\gamma_с=0.9
Коэффициент условий работы болтового соединения, определяемый по таблице 41
\gamma_b=0.9
Число расчетных срезов одного болта:
n_s=1
'''
    +t)
    txt.c1(t,60)
    from tableD3 import tableG5
    R_bs, R_bt = tableG5(txt.numer['k_b'])
    t = '''Расчетные сопротивления приняты по таблице Г5:
R_bs={0}
R_bt={1}
'''
    t=t.format(R_bs,R_bt)
    txt.c1(t)
    from tableD3 import tableG9
    A_b, A_bn = tableG9(txt.numer['d_b'])
    t = '''Площади сечений болтов приняты по таблице Г9:
A_b={0}
A_bn={1}
Расчетное сопротивление смятию (кгс/см^2):
R_bp=4750
'''
    t=t.format(A_b, A_bn)
    txt.c1(t)
    t='''14.2.9 Расчетное усилие, которое может быть воспринято одним болтом, в зависимости от вида напряженного состояния следует определять по формулам:
При срезе одного болта (186) (кгс):
N_bs=R_bs*A_b*n_s*\gamma_b*\gamma_с
Коэффициент использования по прочности при срезе:
k_1=N/(N_bs*n)
При смятии одного болта (187) (кгс):
N_bp=R_bt*d_b*t*\gamma_b*\gamma_с*1/10**2
Коэффициент использования по прочности при смятии:
k_2=N/(N_bp*n)
'''
    txt.c1(t)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    # замена текста
    text_file = text_file.replace('\n\gamma_с=','    \gamma_с=')
    text_file = text_file.replace('\n\gamma_b=','    \gamma_b=')
    text_file = text_file.replace('\nR_bs=','    R_bs=')
    text_file = text_file.replace('\nR_bt=','    R_bt=')
    text_file = text_file.replace('\nA_b=','    A_b=')
    text_file = text_file.replace('\nA_bn=','    A_bn=')
    text_file = text_file.replace('\nR_bp=','    R_bp=')
    return text_file

def BSR(name, tabl):
    from support_function import tabl_taxt
    text_file = tabl_taxt(tabl)
    text_file = calcBSR(name, text_file)
    return text_file

def calcBSM(name, text_file):
    # болтовой узел на момент
    txt = string_calculation.Calc()
    t = text_file
    t=('''Расчет по СП 16.13330.2017 Стальные конструкции
14.2 Болтовые соединения
14.2.1 Для болтовых соединений элементов стальных конструкций следует
применять болты согласно приложению Г.
Коэффициент условий работы, определяемый по таблице 1
\gamma_с=0.9
'''
    +t)
    txt.c1(t,60)
    from tableD3 import tableG5
    R_bs, R_bt = tableG5(txt.numer['k_b'])
    t = '''Расчетные сопротивления приняты по таблице Г5:
R_bs={0}
R_bt={1}
'''
    t=t.format(R_bs,R_bt)
    txt.c1(t)
    from tableD3 import tableG9
    A_b, A_bn = tableG9(txt.numer['d_b'])
    t = '''Площади сечений болтов приняты по таблице Г9:
A_b={0}
A_bn={1}
'''
    t=t.format(A_b, A_bn)
    txt.c1(t)
    t='''
14.2.9 Расчетное усилие, которое может быть воспринято одним болтом, в зависимости от вида напряженного состояния следует определять по формулам:
При растяжении одного болта (188) (кгс):
N_bt=R_bt*A_bn*\gamma_с
Усилие от растяжения и изгибающего момента на наиболее удаленный болт от центра тяжести (кгс):
P=N/n+(M*y)/y_s*1000
Коэффициент использования по прочности при растяжении:
k_2=P/N_bt
'''
    txt.c1(t)
    p = txt.finish(name = name)
    text_print = '\n'.join(p.split('\n')[-2:])
    print(text_print)
    text_file = txt.rezult
    # замена текста
    text_file = text_file.replace('\n\gamma_с=','    \gamma_с=')
    text_file = text_file.replace('\nR_bs=','    R_bs=')
    text_file = text_file.replace('\nR_bt=','    R_bt=')
    text_file = text_file.replace('\nA_b=','    A_b=')
    text_file = text_file.replace('\nA_bn=','    A_bn=')
    return text_file

def BSM(name, tabl):
    from support_function import tabl_taxt
    text_file = tabl_taxt(tabl)
    text_file = calcBSM(name, text_file)
    return text_file

def main():
    # вычисление всех файлов в папке
    from support_function import write_filesAnd_calc
    write_filesAnd_calc(end_of_file_name='*SVR.csv', calculation = calcSVR)
    write_filesAnd_calc(end_of_file_name='*BSR.csv', calculation = calcBSR)
    write_filesAnd_calc(end_of_file_name='*BSM.csv', calculation = calcBSM)

if __name__ == '__main__':
    main()
    