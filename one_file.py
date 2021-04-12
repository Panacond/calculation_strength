#!C:\Users\ivashkevich\Desktop\01_вычисления по формулам\11_все и сразу\.venv\Scripts python
# будем читать один общий файл и по данным из него выполнять расчеты сохраняя в итоге в world
import os, csv, fnmatch, re
import pandoc_md_in_world_class, load12, matplotlib_moment_beam_PQ2
'''функции'''
def last_2_lines(list1):
    # возвращает 2 последние строчки таблциы
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
    
def read_file(a):
    # чтение файла
    a = str(a)
    l=[]
    with open(a,'r',newline='',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return l

def table_all(table):
    # создание списка из отдельных элементов исходного файла
    table_list = [] # общий список таблиц
    table_1 = [] # одна таблица
    for i in range(len(table)):
        if table[i][0] == '':
            table_list.append(table_1)
            table_1 =[]
        else:
            table_1 += [table[i]]
    table_list.append(table_1)
    return table_list

def replace_in_table(table, text1, text2):
    # поиск и замена в таблице значения ячейки
    for y in range(len(table)):
        for x in range(len(table[y])):
            if table[y][x] == text1:
                table[y][x] = str(text2)
    return table

def substituting_dictionary_values(dictionary, table):
    # Замена значений в таблице на значения из словаря
    key_text = list(dictionary)
    for i in key_text:
        table = replace_in_table(table=table, text1=i, text2=dictionary[i])
    return table

def read_save(text, dictionarity, expression):
    '''поиск из текста нужных цифр и извлечение их в изначально заданный словарь
    регулярное выражение должно содержать 3 группы
    r'(K[0-9])(=)([0-9.]*)'(K[0-9])
    (F[0-9])(.*=)([0-9.]*)
    '''
    find_list = re.findall(expression , text)
    key_text = list(dictionarity)
    for i in find_list:
        if i[0] in key_text:
            dictionarity[i[0]] = i[2]
    return dictionarity

'''классы'''
class ListCalc(object):
    # создаем расчет с одного файла csv
    def __init__(self, name):
        # подается имя файла полное
        self.original_name = name
        # обрезание названия
        self.name = name[:-4] # имя
        # чтение файла
        file = read_file(self.original_name)
        # создание общего списка всех данных
        self.table_all = table_all(file)
        # создание значений передаваемых в следующий расчет
        self.title = 'title'
        self.describle = 'describle'
        # рисунок оформления
        self.image = 'image'
        # таблица нагрузок
        self.loads = 'loads'
        # данные расчета значений
        self.text_calc = {'F1':0,'F2':0,'F3':0,'F4':0, 'F5':0, 'F6':0, 'F7':0, 'F8':0, 'F9':0}
        # 4 значения из таблицы нагрузок
        self.tabl_load = {'Q1':0,'Q2':0,'Q3':0,'Q4':0}
        # моменты из расчета эпюр
        self.tabl_moment = {'S1':0,'S2':0,'S3':0,'S4':0, 'S5':0, 'S6':0}
        # результаты расчетов
        self.tabl_calc = 'tabl_calc'
        # создание документа
        self.document = pandoc_md_in_world_class.Doc(name=self.name)
        # текст выводящийся в меню приложения
        self.final_text = self.name
    def read_table_all(self):
        # чтение общего списка и выполнение операций по нему
        dictionary_functions = {'title':'self.add_title(self.table_now)','describle':'self.add_describle(self.table_now)',
                                'image':'self.add_image(self.table_now)','Наименование нагрузки':'self.add_load(self.table_now)',
                                'Усилия':'self.add_epur(self.table_now)'}
        list_key = list(dictionary_functions)
        for i  in self.table_all:
            self.table_now = i
            first_cell = i[0][0]
            if len(first_cell) >3:
                exec(dictionary_functions[first_cell])
            elif len(first_cell) == 3:
                self.add_calc(table=self.table_now)
            else:
                print('ошибка чтения 1 ячейки таблицы')
    def add_title(self, table):
        # создание заголовка
        self.title = table[1][0]
        self.document.addTitle(title=self.title)
    def add_describle(self, table):
        # создание описания если оно в несколько строк
        text = ''
        for i in range(len(table)):
            if i !=0:
                text += table[i][0] + ' '
        self.describle = text
        self.document.addDescrible(describle=self.describle)
    def add_image(self, table):
        # добавление картинки
        self.image = [table[1][0],table[1][1]]
        self.document.addImage(image=self.image)
    def add_load(self, table):
        # вычисление таблицы нагрузок и добавление
        '''Замена значений в таблице значениями из расчета ранее'''
        table = substituting_dictionary_values(dictionary = self.text_calc, table = table)
        list_load, self.loads = load12.load_donload(l = table, name_file = self.original_name )
        # Убираем последнюю строку с общими выводами
        self.loads = self.loads[:-1]
        self.document.addTableLoads(loads=self.loads)
        # передача отдельных значений
        self.tabl_load = {'Q1':list_load[0],'Q2':list_load[1],'Q3':list_load[2],'Q4':list_load[3]}
        # добавляем нагрузки в вывод результатов в меню
        self.final_text +=  last_2_lines(self.loads)
    def add_epur(self, table):
        # Создание картинок эпюр
        graph = matplotlib_moment_beam_PQ2.plot_csv_file
        stress = graph(f = table, name = self.name, dict_load = self.tabl_load)
        # передача значений в словарь
        key = list(self.tabl_moment)
        for i, x in enumerate(stress):
            self.tabl_moment[key[i]] = x
        # добавление эпюр в документ
        self.document.addEpurImage()
    def add_calc(self, table):
        # замена значений в таблице исходных данных
        table = substituting_dictionary_values(dictionary = self.tabl_load, table = table)
        table = substituting_dictionary_values(dictionary = self.tabl_moment, table = table)
        # добавление вычислений
        tabl_stress = table
        name = self.name
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
        if tabl_stress[0][0]=='SBM':
            import SteelColumnMoment
            text_rezult = SteelColumnMoment.SBS(name = name, tabl = tabl_stress[1:] )
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
        if tabl_stress[0][0]=='HDP':
            import hangingDrillingPile
            text_rezult = hangingDrillingPile.FIN(name = name, tabl = tabl_stress[1:] )
        if tabl_stress[0][0]=='FSB':
            import FoundationStrengthBase
            text_rezult = FoundationStrengthBase.FIN(name = name, tabl = tabl_stress[1:] )
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
        # теплотехнический расчет для Москвы
        if tabl_stress[0][0]=='TCS':
            import ThermalCalculationStatic
            text_rezult = ThermalCalculationStatic.CBR(name = name, tabl = tabl_stress[1:] )
        # запись в текстовые файлы, для проверок поставить 1 для печати, и 0 для выключения
        switch = 0
        if switch == 1:
            with open( self.name + tabl_stress[0][0]+ '.txt', 'w', encoding='utf-8') as f:
                # метод write записывает в файл, ассоцированный с переменной f, заданную строку
                f.write(text_rezult)
        self.tabl_calc = text_rezult
        # print(text_rezult)
        # получение и передача данных для последующего расчета и удаление их из результатов
        self.text_calc = read_save(text=self.tabl_calc, dictionarity=self.text_calc, expression=r'(F[0-9])(.*=)([0-9.]*)')
        self.tabl_calc = re.sub(r'(F[0-9])(=)(.*)', '', self.tabl_calc)
        # добавление вычислений в документ
        self.document.addText_calc(text_calc=self.tabl_calc)
        # добавляем коэффициент использования в результат из расчета
        K = pandoc_md_in_world_class.find_max_K(self.tabl_calc)
        self.final_text += '\nКоэффициент использования К=' + str(K)
    def Save(self):
        # сохранение результатов всего расчета
        # self.document.addSave()
        self.document.save()
        print(self.final_text)
        return self.final_text


def main2():
    # для расчета общих файлов рисунки и md не удаляются
    # отбор нужных файлов
    import one_world_file   
    f = one_world_file.list_file(format='csv')
    fin = '' #выводящий текст
    for i in f:
        # работа с одним файлом создание таблицы, рисунки, текст ворлд
        name = i[:-4]
        count = ListCalc(name = i)
        count.read_table_all()
        count.document.save_md()
        fin += '\n\n'+ count.final_text
    return fin

def main1():
    # отбор нужных файлов
    import one_world_file   
    f = one_world_file.list_file(format='csv')
    fin = '' #выводящий текст
    for i in f:
        # работа с одним файлом создание таблицы, рисунки, текст ворлд
        name = i[:-4]
        count = ListCalc(name = i)
        count.read_table_all()
        fin += '\n\n'+ count.Save()
        # удаление картинок и md
        count.document.del_image()
    return fin

def main():
    main1()

if __name__ == '__main__':
    main()






