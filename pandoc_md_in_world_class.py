# здесь создадим отдельный md файл на каждый расчет отдельно и его преобразуем в world
# для этого нам прийдется оставить картинки и создать md файл, чтоб в последующем его собирать в единый файл, чтоб иметь постоянно доступ к файлам
# будем все делать классами, чтоб можно было документ собирать из разных расчетов и файлов и в любой нужной последовательности, таблицы и картинки и расчеты
# так как нам будет надо
import os, re, pypandoc, fnmatch
'''отдельные функции'''
def read_file(a):
    #функция открытия одним целым
    a=a + '.txt'
    with open(a, 'rb') as f:
        t = f.read().decode('utf-8')
    return t

def replace_calc(i):
    # функция замены выражений в формулах для отображения в tex
    # подстановка степеней в скобках
    i = re.sub(r'\^\(([^)]*)\)',r'^{\g<1>}', i)

    # подстановка для дробей
    # старое выражение
    # ((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\\times|+|-|=|/]+)))(/)((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\|+|-|=|/]+)))
    i = re.sub(r'((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)| |+|-|=|/]+)))(/)((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\|+|-|=|/]+)))',r'\\frac{\g<1>}{\g<6>}', i)
    i = re.sub(r'((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)| |+|-|=|/]+)))(/)((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\|+|-|=|/]+)))',r'\\frac{\g<1>}{\g<6>}', i)
    i = re.sub(r'((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)| |+|-|=|/]+)))(/)((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\|+|-|=|/]+)))',r'\\frac{\g<1>}{\g<6>}', i)
    i = re.sub(r'((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)| |+|-|=|/]+)))(/)((?:(\([^(|)]*\([^(|)]*\)[^(|)]*\))|(\([^(|)]*\))|([^(|)|\\|+|-|=|/]+)))',r'\\frac{\g<1>}{\g<6>}', i)
    i = re.sub(r'([^(|)|\*|+|-|=|/]+)(/)([^(|)|\*|+|-|=|/]+)',r'\\frac{\g<1>}{\g<3>}', i)
    # подстановка квадратного корня
    i = re.sub(r'\\sqrt \((([^)|(]*(\([^)|(]*(\([^)|(]*\))*[^)|(]*\))*)*[^)|(]*)\)',r'\\sqrt{\g<1>}', i)
    # замена повторяющихся результатов
    i = re.sub(r'(=[^=]*)(?=\1)(=[^=|\n]*)',r'\g<1>', i)
    # Замена степени 0,5
    i = i.replace('^0.5','^{0.5}')
    i = i.replace('t_s\\frac{^','\\frac{t_s^')
    # i = re.sub(r'\^\(-(\d)\)', '^{-\g<1>}', i)
    i = i.replace(')}','}')
    i = i.replace('{(','{')
    if ':' in i:
        i = i.replace(':\t$', ':    $')
        i = i.replace(':\t', ':    $')
        i = re.sub(r'([ ]{3,})', ' \g<1>$', i)
    else:
        i = '$' + i
        i = i.replace('$\t','$')
    i = i + '$'
    i = i.replace('\t','    ') #;
    return i

def replace_text(text):
    # функция подстановки формул в строки без формул или ввода данных
    i = text
    if '=' in i:
        # замена a=1.24 на $a=1.24$
        i = re.sub(r'(([^ \t]*)(=)([0-9.]*))', ' $\g<1>$ ', i)
    else:
        # замена \varphi_1 на $\varphi_1$ 
        i = re.sub(r'([^ =\е\t\n]*_[^ =:]*)(?![=0-9a-zA-Z{}\(\)])', ' $\g<1>$ ', i)
    return i

def editing_conclusions(text):
    # удаление выводов из теплотехнического расчета
    plus_text ='ВЫВОД. Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k='
    no_text='ВЫВОД. Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k='
    if plus_text in text:
        text = re.sub(r'(ВЫВОД\. Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты\. Коэффициент использования[ $]*k=[\d\.$]*)',r'', text)
    elif no_text in text:
        text = re.sub(r'(ВЫВОД\. Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты\. Коэффициент использования[ $]*k=[\d\.$]*)',r'', text)
    return text

def replace_const(text):
    # Замена обозначений в тексте
    i_dict={'см^2':'{см}^2','см^3':'{см}^3','мм^2':'{мм}^2','м^2':'{м}^2','м^3':'{м}^3','см^4':'{см}^4','кгс/м^2':'{кгс}/м^2',
            'кгс/см^2':'{кгс}/{см}^2',
            'кгс  \\times м':'кгс  \\times м',
            'кгс  \\\\times м':'кгс  \\times м',
            '(10^9 \\times  кгс \\times  мм^3)/EI':'\\frac{10^9 \\times  кгс \\times  мм^3}{EI}',
            '(10^9 \\times  кгс \\times  м ${м}^3$ )/EI':'\\frac{10^9 \\times  кгс \\times  мм^3}{EI}'}
    key_dict = list(i_dict)
    for k in key_dict:
        new_k= ' $' + i_dict[k] + '$ '
        text = text.replace(k,new_k)
    return text

def replace_signs(text_file):
    # функция замены для оформления в формулы
    new_text_file=''
    # создание 2х уровневой таблицы, первая, с \t вторая \n
    table_file = text_file.split('\n')
    for i in table_file:
        # Замена выражений с верхним подчеркиванием
        i = i.replace('l\\bar_ymax','\\bar{l_y}_{max}')
        i = i.replace('\\lambda\\bar_x','\\bar{\\lambda_x}')
        i = i.replace('l\\bar_x','\\bar{l_x}')
        i = i.replace('l\\bar_y','\\bar{l_y}')
        i = i.replace('l\bar','\\bar{l}')
        # не проверять если там уже есть знаки оформления $
        if not '$' in i:
            # нижнее подчеркивание несколько знаков
            i = re.sub(r'_([a-zA-Z0-9]{2,})',r'_{\g<1>}', i)
            # поиск 2 знаков равно
            n1=i.find('=')
            n2=i.rfind('=')
            if n2 != n1:
                # правка по : и уделение после : пробела
                if ':' in i:
                    list_string=i.split(':')
                    list_string[0] = replace_text( text= list_string[0])
                    while list_string[1][0] ==' ':
                        list_string[1] = list_string[1][1:]
                    while list_string[1][0:2] == '\t':
                        list_string[1] = list_string[1][2:]
                    list_string[1] = replace_calc(list_string[1] )
                    i = ': '.join(list_string)
                else:
                    i = replace_calc(i)
            else:
                i
                i = re.sub(r'(^\t)', '', i)
                # если строка содержит : то разделить по этому символу и найти формулы
                if ':' in i:
                    list_string=i.split(':')
                    a=[]
                    for i in list_string:
                        a.append(replace_text( text= i))
                    i = ':'.join(a)
                else:
                    i = replace_text( text= i)
                # функция замены констант
                i = replace_const(i)
            i = i.replace('$$','$')
            i = i.replace('$ $','$')
            i = i.replace('\\ $', '$\\')
            i = i.replace('\r$','$')
            i = i.replace('    $','$')
            if '|' in i:
                new_text_file += i + '\n'
            else:
                i = i.replace('    ',';    ')
                new_text_file += i + '\n'*2
        else:
            new_text_file += i + '\n'
    return new_text_file

def find_max_K(text):
    # поиск максимального коэффициента
    find_concrete = re.findall(r'(k(_\d)?=)([^=]*=){0,2}([\d\.]*)', text)
    k = 0
    try:
        for i in find_concrete:
            try:
                i = float(i[3])
            except:
                i=0
            if i > k:
                k = i
    except:
        pass
    return k
'''объекты документа'''
class Doc(object):
    # создается документ в который можно добавлять разные элементы и в итоге сохранить все
    def __init__(self, name):
        # Задать имя файла, который будет читаться
        self.name = name # имя
        # начало файла (скрипт для просмотра файла в html)
        self.markdown = '<script type="text/javascript" src="ASCIIMathML.js"></script>\n' 

        try:
            self.new_name = self.name.replace(' ', '_')
        except:
            pass

    def addTitle(self, title):
        # добавление названия
        self.title = title
        self.markdown += '## ' + self.title[:1].capitalize() + title[1:] +'\n'

    def addDescrible(self, describle):
        # добавление описания
        self.describle = describle
        try:
            self.title
        except:
            self.title = '________ '
        self.describle = 'Рассматриваемый элемент - ' + self.title[:1].lower() + self.title[1:] +  ' '+ self.describle + '\n'
        self.markdown += self.describle
    
    def addImage(self, image):
        # добавление рисунка с общим видом
        self.image = image
        self.image = ''.join(self.image)
        self.markdown += '\n\n![](' + self.image + ')\n\n'

    def addTableLoads(self, loads):
        # добавление таблицы нагрузок
        self.loads = loads
        self.markdown += 'Таблица сбора нагрузок, действующих на элемент: \n\n'
        # преобразование и форматирование таблицы
        self.table_text = ''
        for i, cell_row in enumerate(self.loads):
            for j, cell_cow in enumerate(cell_row):
                # удаление начальных и конечных пробельных символов
                cell_cow = str(cell_cow)
                cell_cow = cell_cow.lstrip(' ')
                cell_cow = cell_cow.rstrip(' ') 
                if i == 0 :
                    self.table_text += '**' + cell_cow +'**|'
                elif i == 1:
                    self.table_text += '*' + cell_cow +'*|'
                elif (len(self.loads[i]) == 1 and len(self.loads[i+1]) ==1 and j!=1 ):
                    self.table_text += '**' + str(cell_cow) +'** |'
                elif (len(cell_row) != 1 and self.loads[i][3] == '' and j!=1) :
                    if cell_cow != '':
                        self.table_text += '**' + str(cell_cow) +'** |'
                    else:
                        self.table_text += '|'
                elif len(cell_row) == 1 :
                    self.table_text += '*' + str(cell_cow) +'*|'
                else:
                    self.table_text +=  str(cell_cow) +'|'
            if i==0:
                self.table_text += '\n:---:|:---:|:---:|:---:|:---:| \n'
            else:
                self.table_text += '\n'
        a, b = self.loads[-1][2], self.loads[-1][4]
        text ='Фактическая постоянная расчетная распределенная нагрузка от веса конструкций составляет {0} кг/м (нормативная нагрузка {1} кг/м)'
        self.table_text += '\n'+ text.format(a,b) + '\n'
        self.markdown += self.table_text +'\n'

    def addEpurImage(self):
        # правка названий
        try:
            os.rename(self.name +'1.png' , self.new_name +'1.png'  )
            os.rename(self.name +'2Q.png', self.new_name +'2Q.png')
            os.rename(self.name +'3M.png', self.new_name +'3M.png')
            os.rename(self.name +'4f.png', self.new_name +'4f.png')
        except:
            print('файлов для переименования нет')
        # добавление рисунков усилий
        try:
            file_list=[]
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*.png'):
                    file_list += [file]
            if self.new_name +'1.png' in file_list:
                    self.markdown += 'Напряжения в элементе: \n\n'
                    self.markdown += '![](' + self.new_name + '1.png'   + ')\n\n'
                    self.markdown += '![](' + self.new_name + '2Q.png' + ')\n\n'
                    self.markdown += '![](' + self.new_name + '3M.png' + ')\n\n'
                    self.markdown += '![](' + self.new_name + '4f.png' + ')\n\n'
                    self.markdown += '\n\n'
        except:
            print('not epur')
            pass

    def addText_calc(self, text_calc):
        # добавление расчета
        self.text_calc = text_calc
        text = editing_conclusions(self.text_calc)
        self.markdown += replace_signs(text) +'\n'

    def addText(self, text):
        # добавление просто текста
        text = editing_conclusions(text)
        self.markdown += text

    def save_md(self):
        # сохранение без удаления картинок только md
        try:
            # добавление выводов в конце файла
            self.describle = self.describle.replace('\n','')
            self.markdown += '**Вывод:**\n\n'
            self.markdown +='**' + self.describle + '**\n\n'
            # поиск максимального коэффициента
            k = find_max_K(self.text_calc)
            if k < 1:
                text1 ='''**На элемент приложены действующие нагрузки, по действующим нормативным документам. Определены внутренние усилия и напряжения от действующих нагрузок и возникающие напряжения в элементе. Условие прочности выполняется. Коэффициент использования k={0} < 1, что удовлетворяет требованиям к надежности конструкции.**'''
            else:
                text1 ='''**На элемент приложены действующие нагрузки, по действующим нормативным документам. Определены внутренние усилия и напряжения от действующих нагрузок и возникающие напряжения в элементе. Условие прочности не выполняется. Коэффициент использования k={0} > 1, что не удовлетворяет требованиям к надежности конструкции.**'''
            text_k= str(k)
            text_k= text_k.replace('.',',')
            text ='ВЫВОД. Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k='
            no_text='ВЫВОД. Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k='
            if text in self.text_calc:
                find_concrete = re.search(r'ВЫВОД\. (Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты. Коэффициент использования[ $]*k=[\d\.$]*)', self.text_calc).group(1)
                self.text_calc = re.sub(r'(ВЫВОД\. Наружные ограждающие конструкции удовлетворяют требованиям в части тепловой защиты\. Коэффициент использования[ $]*k=[\d\.$]*)',r'', self.text_calc)
                self.markdown += '**'+ find_concrete + '**'
            elif no_text in self.text_calc:
                find_concrete = re.search(r'ВЫВОД\. (Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты. Коэффициент использования k=[\d\.]*)', self.text_calc).group(1)
                self.text_calc = re.sub(r'(ВЫВОД\. Наружные ограждающие конструкции не удовлетворяют требованиям в части тепловой защиты\. Коэффициент использования[ $]*k=[\d\.$]*)',r'3.14', self.text_calc)
                self.markdown += '**'+ find_concrete + '**'
            else:
                text_conclusion = text1.replace('{0}', text_k)
                self.markdown += text_conclusion
        except:
            pass
        # сохранение всего файла
        try:
            # запись файла формата markdown
            with open( self.new_name + '.md', 'w', encoding='utf-8') as f:
                # метод write записывает в файл, ассоцированный с переменной f, заданную строку
                f.write(self.markdown)
        except:
            print('Not name file or not work world 1')    
    
    
    def save(self):
        # сохранение word
        try:
            self.save_md()
            # конвертирование в world
            pypandoc.convert_text(self.markdown, format='md', to='docx', outputfile = self.new_name +".docx")
        except:
            print('Not name file or not work world 2 ')

    def del_image(self):
        # удаление картинок и md
        try:
            os.remove(self.name +'1.png')
            os.remove(self.name +'2Q.png')
            os.remove(self.name +'3M.png')
            os.remove(self.name +'4f.png')
        except:
            pass
        try:
            os.remove(self.new_name +'1.png')
            os.remove(self.new_name +'2Q.png')
            os.remove(self.new_name +'3M.png')
            os.remove(self.new_name +'4f.png')
        except:
            pass
        try:
            pass
            os.remove(self.new_name +'.md')
        except:
            pass
    def addSave(self):
        # сохранение все сразу
        self.save()
        self.del_image()

def save_text():
    # сохранение текстовых файлов
    from one_world_file import list_file
    list = list_file()
    for name in list:
        name =name[:-4]
        document = Doc(name=name)
        text_calc = read_file(name)
        text_calc = text_calc.replace('*'," \\times ")
        document.addText_calc(text_calc=text_calc)
        document.addSave()   

def main():
    # тестовые данные
    name = 'Плита основное сочетание нагрузок'

    # text_rezult вместо text_calc
    loads =  [['Вид нагрузки', 'Ед. изм.', 'Нормативная нагрузка', 'Коэффициент надежности по нагрузке', 'Расчетная нагрузка'],
    ['1', '2', '3', '4', '5'], 
    ['Перекрытие'],
    ['Постоянные '], 
    ['Керамогранит G=2200 кг/м.куб t=12 мм', 'кг/м.кв', 26, 1.2, 32], 
    ['Стяжка G=1800 кг/м.куб t=130 мм', 'кг/м.кв', 234, 1.1, 257],
    ['ЖБ плита G=2500 кг/м.куб t=200 мм', 'кг/м.кв', 500, 1.1, 550],
    ['Итого', 'кг/м.кв', 760, '', 839],
    ['Временные'],
        ['Полезная G=300 кг/м.кв', 'кг/м.кв', 300, 1.2, 360], 
        ['Итого', 'кг/м.кв', 300, '', 360], 
    ['Всего', 'кг/м.кв', 1060, '', 1199],
    ['Перекрытие'],
    ['Постоянные '], 
    ['Керамогранит G=2200 кг/м.куб t=12 мм', 'кг/м.кв', 26, 1.2, 32], 
    ['Стяжка G=1800 кг/м.куб t=130 мм', 'кг/м.кв', 234, 1.1, 257],
    ['ЖБ плита G=2500 кг/м.куб t=200 мм', 'кг/м.кв', 500, 1.1, 550],
    ['Итого', 'кг/м.кв', 760, '', 839],
    ['Временные'],
        ['Полезная G=300 кг/м.кв', 'кг/м.кв', 300, 1.2, 360], 
        ['Итого', 'кг/м.кв', 300, '', 360], 
    ['Всего', 'кг/м.кв', 1060, '', 1199],
        ['Всего временные', 'кг/м.кв', 300, '', 360], 
        ['Всего постоянные ', 'кг/м.кв', 760, '', 839], 
        ['Сумма всех нагрузок', 'кг/м.кв', 1060, '', 1199]]

    title ='Монолитная ЖБ плита в осях «21-22/М-Н» на отм. +14,900. Расчет на прочность, основное сочетание нагрузок, без учета сейсмических нагрузок с учетом усиления плиты.'

    describle = 'Длина элемента 5,6 м. Толщина плиты 200 мм. Материал монолитный железобетон класса В20 W6 F150 ГОСТ 26633-2015. Плита снизу усилена металлическими накладками с шагом 1000 мм. Сечение накладки 200х10(h) мм. Марка стали накладок С245.'
 
    document = Doc(name=name)
    # document.addTitle(title=title)
    # document.addDescrible(describle=describle)
    # image= ['План_балки','.png']
    # document.addImage(image=image)
    
    # text_calc = read_file('теплотехника')
    # document.addText(text_calc)
   
    text_calc = read_file('теплотехника')
    document.addText_calc(text_calc=text_calc)

    # document.addTableLoads(loads=loads)

    # document.addEpurImage()
    
    document.save()
    # document.addSave()

def replace_in_table(table, text1, text2):
    # поиск и замена в таблице значения ячейки
    for y in range(len(table)):
        for x in range(len(table[y])):
            if table[y][x] == text1:
                table[y][x] = text2
    return table

if __name__ == '__main__':
    main()
    # save_text()