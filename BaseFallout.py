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
    # добавление номеров слоев
    n = 1
    while 'h=' in t:
        t=t.replace('h=','h_'+str(n) +'=',1)
        t=t.replace('g=','g_'+str(n) +'=',1)
        t=t.replace('\\nu=','\\nu_'+str(n) +'=',1)
        t=t.replace('E=','E_'+str(n) +'=',1)
        n +=1
    # поиск и замена с помощью регулярных выражений
    t='''Определение расчетного сопротивление под подошвой фундамента
расчет по СП 22.13330.2011 ОСНОВАНИЯ ЗДАНИЙ И СООРУЖЕНИЙ
Исходные данные:
'''+t
    #txt.c1(t,60)
    t0='''Коэффициенты определенные по таблице 5.4. СП
g_c1=1.1
g_c2=1
Коэффициенты принимаемые по таблице 5.5 СП
m_y=0.36
m_g=2.43
m_o=4.99
Коэффициент принимаемый равным 1 при ширине фундамента меньше 10 м:
k_s=1
'''
    import re
    find_angle = re.search('arphi = \d\d', t).group()
    txt_inp = int(find_angle.split('=')[1])#извлечение нужной части строки
    K1 = {0: 0, 1: 0.01, 2: 0.03, 3: 0.04, 4: 0.06, 5: 0.08, 6: 0.1, 7: 0.12, 8: 0.14, 9: 0.16, 10: 0.18, 11: 0.21, 12: 0.23, 13: 0.26, 14: 0.29, 15: 0.32, 16: 0.36, 17: 0.39, 18: 0.43, 19: 0.47, 20: 0.51, 21: 0.56, 22: 0.61, 23: 0.66, 24: 0.72, 25: 0.78, 26: 0.84, 27: 0.91, 28: 0.98, 29: 1.06, 30: 1.15, 31: 1.24, 32: 1.34, 33: 1.44, 34: 1.55, 35: 1.68, 36: 1.81, 37: 1.95, 38: 2.11, 39: 2.28, 40: 2.46, 41: 2.66, 42: 2.88, 43: 3.12, 44: 3.38, 45: 3.66}
    K2 = {0: 1.0, 1: 1.06, 2: 1.12, 3: 1.18, 4: 1.25, 5: 1.32, 6: 1.39, 7: 1.47, 8: 1.55, 9: 1.64, 10: 1.73, 11: 1.83, 12: 1.94, 13: 2.05, 14: 2.17, 15: 2.3, 16: 2.43, 17: 2.57, 18: 2.73, 19: 2.89, 20: 3.06, 21: 3.24, 22: 3.44, 23: 3.65, 24: 3.87, 25: 4.11, 26: 4.37, 27: 4.64, 28: 4.93, 29: 5.25, 30: 5.59, 31: 5.95, 32: 6.34, 33: 6.76, 34: 7.22, 35: 7.71, 36: 8.24, 37: 8.81, 38: 9.44, 39: 10.11, 40: 10.85, 41: 11.64, 42: 12.51, 43: 13.46, 44: 14.5, 45: 15.64}
    K3 = {0: 3.14, 1: 3.14, 2: 3.32, 3: 3.41, 4: 3.51, 5: 3.61, 6: 3.71, 7: 3.82, 8: 3.93, 9: 4.05, 10: 4.17, 11: 4.29, 12: 4.42, 13: 4.55, 14: 4.69, 15: 4.84, 16: 4.99, 17: 5.15, 18: 5.31, 19: 5.48, 20: 5.66, 21: 5.84, 22: 6.04, 23: 6.24, 24: 6.45, 25: 6.67, 26: 6.9, 27: 7.14, 28: 7.4, 29: 7.67, 30: 7.95, 31: 8.24, 32: 8.55, 33: 8.88, 34: 9.22, 35: 9.58, 36: 9.97, 37: 10.37, 38: 10.8, 39: 11.25, 40: 11.73, 41: 12.24, 42: 12.79, 43: 13.37, 44: 13.98, 45: 14.64}

    t0 = t0.replace('m_y=0.36','m_y='+ str(K1[txt_inp]))
    t0 = t0.replace('m_g=2.43','m_g='+ str(K2[txt_inp]))
    t0 = t0.replace('m_o=4.99','m_o='+ str(K3[txt_inp]))
    t = t + t0
    txt.c1(text = t, n_letter = 90, charge = '\t')
    t = '''Допустимые напряжения составят (тс/м^2):
R_f=(g_c1*g_c2)/k_0*(m_y*k_s*B_f*G_2+m_g*d_1*G_1+(m_g-1)*d_b*G_2+m_o*c_2*100)
Давление под подошвой фундамента (тс/м^2):
P_r=P_0/(B_f*L_f)*1/10**3
Коэффициент использования составит:
k_1=P_r/R_f
'''
    txt.c1(text = t, n_letter = 90,charge='    ')

    t = '''Расчет осадки фундамента выполним методом эквивалентного слоя
'''
    txt.c1(text = t, n_letter = 90, charge = '  ')
    t='''
Определим дополнительные характеристики'''
    txt.c1(text = t, n_letter = 60, charge = '  ')
    tp='''\\beta_i=(1-(2*\\nu_i**2)/(1-\\nu_i))
Коэффициент относительной сжимаемости слоя (1/МПа):
a_i=\\beta_i/E_i'''
    def new_variable(input_x = 'h', output = ['\\beta', '\\nu','E', 'a'], text = tp, variable_list = txt.kef):
        '''Замена  _i на _1, _2 и т.д. здать перемнную, по которой брать заначения
        задать список значений, задать текст подстановки и список значений переменных откуда смотреть перменные
        также возвращает число слоев грунта'''
        text0 = ''
        n = []
        for x in variable_list:
            if input_x in x and x !='\\varphi ':
                text1 = text
                n.append(x.split('_')[1])#получение  номера слоя
                for j in output:
                    j_new = j +'_' + x.split('_')[1]
                    text1 = text1.replace( j + '_i', j_new)
                    a = ( j + '_i')
                # добавление глубины слоя
                S_sl = 0
                for i in n:
                    S_sl +=  txt.numer['h_'+ str(i)]
                    S_sl = round(S_sl,2)
                    text2 = 'Глубина нижней границы слоя составит (м):\n'
                    text2 += 'H_'+ str(i) + '=' + str(S_sl) + '\n'
                text0 += text1 + '\n' + text2
        return text0, n #t - новые текст с коэффициентами n - число слоев
    t, n = new_variable()
    txt.c1(text = t, n_letter = 60, charge = '  ')

    def deep_ground(d = txt.numer['d_1'], n = n ):
        '''Определение давления на уровне подошвы фундамента с учетом наличия разных слоев'''
        h = d # остаточная глубина
        '\\sigma_zg0'
        a = 0
        ti = ''
        for i_n in n:
            if h < txt.numer['h_' + i_n]:
                a = txt.numer['g_' + i_n]
                ti += 'g_'+ i_n +'*d_o'
                break
            else:
                ti += 'g_'+ i_n + '*h_' + i_n + '+'
                h -= txt.numer['h_' + i_n]
        t = 'Глубина от границы последнего слоя или поверхности, до подошвы фундамента(м): \n'
        h = round(h,2)
        t += 'd_o=' + str(h) + '\n'
        t += 'Давление на уровне подошвы фундамента (МПа):\n'
        t += '\\sigma_zg0=(' + ti +')*1/100'
        t += '\n'
        return t
    t = deep_ground()
    txt.c1(text = t, n_letter = 90, charge = '  ')
    t = '''Среднее давление под подошвой фундамента (МПа):
p_s=P_0/(B_f*L_f*10**5)
Дополнительное давление на уровне подошвы фундамента (МПа):
p_d=p_s-\\sigma_zg0
'''
    txt.c1(text = t, n_letter = 90, charge = '  ')
    import table_aw
    Aw = table_aw.all(txt.numer['n_s'],txt.numer['\\nu_1'])
    #print(Aw)
    t = 'Значение коэффициента эквивалентного слоя для жестких фундаментов по таблице 4.3:\n'
    t += 'A_w=' + str(Aw) + '\n'
    txt.c1(text = t, n_letter = 30, charge = '  ')
    t ='''Определим мощность эквивалентного слоя (м):
h_a=A_w*B_f
Высота сжимающей толщи влияющей на осадку фундамента составляет (м):
H=2*h_a'''
    txt.c1(text = t, n_letter = 90, charge = '  ')
    t='''
Отметка низа сжимающей толщи (м):
H_0s=H+d_1
Общая толщина слоев(м):
'''
    txt.c1(text = t)
    string_cal='H_sl='
    for i in n:
        if i =='1':
            string_cal +='h_' + str(i)
        else:
            string_cal +='+h_' + str(i)
    t = string_cal
    txt.c1(text = t)
    if txt.numer['H_0s'] < txt.numer['H_sl']:
        t='''\nГлубина геологических слоев достаточна для определения осадок'''
    else:
        t='''\nНеобходимо задать более слои ниже'''
    txt.c1(text = t)
    t = '\nРасчет слоев\n'
    txt.c1(text = t)
    t = ''
    formyla_text = ''
    do = txt.numer['d_1'] + txt.numer['H'] # вычисление низа глубины сжимаемой толщи
    t += 'Отметка нижней границы сжимаемой толщи (м):\n' 
    t += 'H_sg=d_1+H\n'
    txt.c1(text = t, n_letter = 90, charge = '  ')
    t=''
    for i in n:        
        H_n = txt.numer['H_' + str(i)] - txt.numer['h_' + str(i)] # ближайшая к поверхности граница грунта
        # первая схема глубина в 1 слое
        if txt.numer['H_sg'] <= txt.numer['H_1']:
            t = '!Слой ' + str(i) + '\n'
            t += 'Мощность слоя (м):\n'
            t += 'h_f1=' + str(txt.numer['H']) + '\n' # глубина
            t += 'Расстояние до нижней границы сжимаемой толщи (м):\n'
            middle = txt.numer['H']/2 + do - txt.numer['H_' + str(i)]
            t += 'f1=' + str(round(middle,2)) + '\n'# расстояние до низа
            # текст описывающий верхнюю часть формулы коэффициента относительной сжимаемости
            formyla_text = 'h_f1*a_' + str(i) + '*f1'
        else:
            # вторая схема через несколько слоев
            if (txt.numer['d_1'] >= (txt.numer['H_' + str(i)] - txt.numer['h_' + str(i)]) 
                and txt.numer['H_sg'] >  txt.numer['H_' + str(i)]
                and txt.numer['d_1'] <= txt.numer['H_' + str(i)]):
                # подошва фундамента попадает в данный слой
                t += 'Слой ' + str(i) + '\n'
                t += 'Мощность слоя (м):\n'
                middle = round(txt.numer['H_' + str(i)] - txt.numer['d_1' ],2)
                t += 'h_f' + str(i) + '=' + str(middle) + '\n' # мощность
                t += 'Расстояние до нижней границы сжимаемой толщи (м):\n'
                middle = ((txt.numer['H_' + str(i)] - txt.numer['d_1' ])/2
                        + do - txt.numer['H_' + str(i)])
                t += 'f' + str(i) + '=' + str( round(middle,2))  + '\n'# расстояние до низа
                formyla_text += 'h_f' + str(i) + '*a_' + str(i) + '*f' + str(i) +'+'
            if txt.numer['d_1'] < (txt.numer['H_' + str(i)] - txt.numer['h_' + str(i)]) and txt.numer['H_sg'] >  txt.numer['H_' + str(i)]:
                # весь слой в жимаемой толще
                t += 'Слой ' + str(i) + '\n'
                t += 'Мощность слоя (м):\n'
                t += 'h_f' + str(i) + '=' + str(txt.numer['h_' + str(i)]) + '\n' # мощность
                t += 'Расстояние до нижней границы сжимаемой толщи (м):\n'
                middle = txt.numer['h_' + str(i)]/2 + do - txt.numer['H_' + str(i) ]
                t += 'f' + str(i) + '=' + str(round(middle,2) )  + '\n'# расстояние до низа
                formyla_text += 'h_f' + str(i) + '*a_' + str(i) + '*f' + str(i) + '+'
            if txt.numer['H_sg'] <=  txt.numer['H_' + str(i)] and txt.numer['H_sg'] >= txt.numer['H_' + str(i)] - txt.numer['h_' + str(i)]:
                # нижняя граница грунта лежит в сжимаемой толще
                t += 'Слой ' + str(i) + '\n'
                t += 'Мощность слоя (м):\n'
                if txt.numer['d_1'] < (txt.numer['H_' + str(i)] - txt.numer['h_' + str(i)]):
                    t += 'h_f' + str(i) + '=' + str(round(txt.numer['H_sg'] - txt.numer['H_'+ str(i)]+txt.numer['h_'+ str(i)],2)) + '\n' # мощность
                else:
                    t += 'h_f' + str(i) + '=' + str(round(txt.numer['H_sg'] - txt.numer['d_1'],2)) + '\n' # мощность
                txt.c1(text = t, n_letter=1 )
                t = 'Расстояние до нижней границы сжимаемой толщи (м):\n'
                # txt.c1(text = t )
                t += 'f' + str(i) + '=' + str(txt.numer['h_f'+ str(i)]/2)  + '\n'# расстояние до низа
                # txt.c1(text = t)
                formyla_text += 'h_f' + str(i) + '*a_' + str(i) + '*f' + str(i)+ '+'
    if formyla_text[-1] =='+':
        formyla_text = formyla_text[:-1]
    txt.c1(text = t, n_letter = 90, charge = '  ')
    t = 'Коэффициент относительной сжимаемости составит (10/МПа):\n'
    t += 'a_ot=10*(' + formyla_text + ')/(2*h_a**2)\n'
    t += 'Средняя осадка составит (см):\n'
    t += 's=h_a*a_ot*p_d*10'
    txt.c1(t)
    t= '''
Коэффициент использования составит:
k_1=P_r/R_f'''
    txt.c1(t)
    if txt.numer['s'] < 10:
        t = '\nОсадки не превышают допустимые 10см'
    else:
        t = '\nОсадки превышают допустимые'
    #txt_inp = t.split('\n')[7]#извлечение строки из текста
    #txt_inp = int(txt_inp.split('=')[1])#извлечение нужной части строки
    txt.c1(text = t, n_letter = 90, charge = '  ')

    p = txt.finish(name = name)
    text_print ='\n'.join( p.split('\n')[-5:-1])
    print(text_print)
    text_file = txt.rezult
    text_file = text_file.replace('''Коэффициент Пуассона для Крупнообломочных 0,27, Пески и супеси 0,3

Суглинки 0,35, Глины 0,41\t\\nu''', '''Коэффициент Пуассона  \\nu''')
    text_file = text_file.replace('''СП\tg_c1''', '''СП\ng_c1''')
    text_file = text_file.replace('''СП\tm_''', '''СП\nm_''')
    text_file = text_file.replace('''Мощность слоя (м):\nh_f''', '''Мощность слоя (м):    h_f''')
    text_file = text_file.replace('''сжимаемой толщи (м):\nf''', '''сжимаемой толщи (м):    f''')
    a = '''R_f=(g_c1 \\times g_c2)/k_0 \\times (m_y \\times k_s \\times B_f \\times G_2+m_g \\times d_1 \\times G_1+(m_g-1) \\times d_b \\times G_2+m_o \\times c_2 \\times 100)='''
    text_file = text_file.replace(a, a +'''\n=''')
    return text_file


def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*BFG.csv'):
            f += [file]
    for i in f:
        text_file = read_file(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        # text_print ='\n'.join( text_file.split('\n')[-4:])
        # print(text_print)
    pass

if __name__ == '__main__':
    main()
    
def BRG(name, tabl):
    text_file = tabl_taxt(tabl)
    text_file = calculation(name, text_file)
    return text_file