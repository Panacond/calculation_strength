#будем читать один общий файл и по данным из него выполнять расчеты
import os, csv, fnmatch

def read_file(a):
    a = str(a)
    l=[]
    with open(a,'r',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return l

def tabl_3(l):
    # 3 списка для разных таблиц
    button_replace = 0
    tabl_load = []
    tabl_moment = []
    tabl_stress=[]
    for i in range(len(l)):
        if l[i][0]=='':
            button_replace +=1
        if l[i][0]!='' and button_replace == 0:
            tabl_load +=[l[i]]
        if l[i][0]!='' and button_replace == 1:
            tabl_moment +=[l[i]]
        if l[i][0]!='' and button_replace == 2:
            tabl_stress +=[l[i]]
    all_tabl = [tabl_load, tabl_moment, tabl_stress]
    # проверка на наличие данных
    tabl_load = []
    tabl_moment = []
    tabl_stress=[]
    for i in all_tabl:
        try:
            b = i[0][0]
        except:
            b = ''
        if b == 'Наименование нагрузки':
            tabl_load = i
        if b == 'Усилия':
            tabl_moment = i
        if len(b) == 3:
            tabl_stress = i
    return tabl_load, tabl_moment, tabl_stress

def last_2_lines(list1):
    # возвращает 2 последние строчки
    if type(list1) == str:
        list1 = list1.split('\n')
        list1 = '\n' + list1[-2] + '\n' + list1[-1]
    elif type(list1) == list:
        # list1 = list1[-2]
        if len(list1)>=2:
            list1 ='\n' + str(list1[-2]) + '\n' + str(list1[-1])
        else:
            list1=""
    return list1

def main():
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    fin = '' #выводящий текст
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*файл.csv'):
            f += [file]
    for i in f:
        # работа с одним файлом создание таблицы, рисунки, текст ворлд
        name = i[:-4]
        l = read_file(i)
        # Получил 3 списка для разных таблиц
        tabl_load, tabl_moment, tabl_stress = tabl_3(l)
        # запись файла нагрузок в ексель файл
        # Q, MT = finish_load(l = tabl_load, name_file = i )
        import load12
        Q, MT = load12.load_donload(l = tabl_load, name_file = i )
        # Убираем последнюю сторку с общими выводами
        MT=MT[:-1]
        # добавляем нагрузки в вывод результатов в меню
        fin += '\n\n'+ name + last_2_lines(MT)
        dict_load = {'Q1':Q[0],'Q2':Q[1],'Q3':Q[2],'Q4':Q[3]}
        dict_all = {'Q1':Q[0],'Q2':Q[1],'Q3':Q[2],'Q4':Q[3],'S1':0,'S2':0,'S3':0,'S4':0, 'S5':0}
        # создание эпюр
        import matplotlib_moment_beam_PQ2
        graph = matplotlib_moment_beam_PQ2.plot_csv_file
        if tabl_moment != []:
            stress = graph(f = tabl_moment, name = name, dict_load = dict_load )
            dict_all ={'Q1':Q[0],'Q2':Q[1],'Q3':Q[2],'Q4':Q[3],'S1':stress[0],'S2':stress[1],'S3':stress[2],'S4':stress[3], 'S5':stress[4]}
        len_stress = len(tabl_stress)
        for i in range(len_stress):
            if tabl_stress[i][2] in ['Q1', 'Q2', 'Q3', 'Q4','S1', 'S2', 'S3', 'S4', 'S5']:
                nx = tabl_stress[i][2]
                a = str(dict_all[nx])
                tabl_stress[i][2] = a
        # выполнение расчета на усилия !
        if tabl_stress != []:
            # бетонные и жб балки
            if tabl_stress[0][0]=='CBR':
                import ConcreteBeamReinforcing
                text_rezult = ConcreteBeamReinforcing.CBR(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='CBT':
                import ConcreteTBeamReinforcing
                text_rezult = ConcreteTBeamReinforcing.CBR(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='CBP':
                import ConcreteBeamPretense
                text_rezult = ConcreteBeamPretense.CBP(name = name, tabl = tabl_stress[1:] )
            # стальные балки и колонны
            if tabl_stress[0][0]=='SBR':
                import SteelBeamRol
                text_rezult = SteelBeamRol.SBR(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='SBS':
                import SteelBeamSection
                text_rezult = SteelBeamSection.SBS(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='SCS':
                import SteelColumnSection
                text_rezult = SteelColumnSection.SBS(name = name, tabl = tabl_stress[1:] )
            # деревянные конструкции
            if tabl_stress[0][0]=='WBS':
                import WoodBeamSection
                text_rezult = WoodBeamSection.WBS(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='WCS':
                import WoodColumnSection
                text_rezult = WoodColumnSection.WBS(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='WCC':
                import WoodColumnCircle
                text_rezult = WoodColumnCircle.WBS(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='WBL':
                import WoodBeamSectionLVL
                text_rezult = WoodBeamSectionLVL.WBS(name = name, tabl = tabl_stress[1:] )
            # фундаменты
            if tabl_stress[0][0]=='BRG':
                import BaseResistanceGround
                text_rezult = BaseResistanceGround.BRG(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='BFG':
                import BaseFallout
                text_rezult = BaseFallout.BRG(name = name, tabl = tabl_stress[1:] )
            # бетонные и жб колонны
            if tabl_stress[0][0]=='CCN':
                import ConcreteColumnNoArm
                text_rezult = ConcreteColumnNoArm.CBR(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='CCR':
                import ConcreteColumnReinforced
                text_rezult = ConcreteColumnReinforced.CBR(name = name, tabl = tabl_stress[1:] )
            if tabl_stress[0][0]=='SCA':
                import FormulaStringCalculation
                text_rezult = FormulaStringCalculation.CBR(name = name, tabl = tabl_stress[1:] )
            # запись в ворлд файл
            import do1
            do1.world(name = name, text_calc = text_rezult, loads= MT)
        # добавляем результаты расчета вывод результатов в меню 
        try:
            fin +=  last_2_lines(text_rezult)
        except:
            pass
    return fin

if __name__ == '__main__':
    main()

def main1():
    fin = main()
    return fin 

