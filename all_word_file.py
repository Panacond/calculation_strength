# сбор общего отчета с коэффициентами использования и таблицами нагрузок
# это подгружаемый модуль в one_world_file
import re

def read_file_md(a):
    #функция открытия одним целым
    a= a + '.md'
    with open(a, 'rb') as f:
        t = f.read().decode('utf-8')
    return t

class Result_text(object):
    # документ который отбирает данные для выводов
    def __init__(self):
        # Задать имя файла, который будет читаться
        # порядковый номер в таблице
        self.number = 0
        # расчет нагрузок
        self.text_load = ''
        # таблицы нагрузок
        self.table_load = ''
        # начало файла 
        self.part1='''
# ТАБЛИЦА РЕЗУЛЬТАТОВ
|№      | Наименование рассчитываемого элемента  | Коэффициент использования  | Выводы |
|:---   |    :---:                               |                     :---:  |:---:   |
| *1*   |     *2*                                |            *3*             | *4*    |
'''

        self.part2='''
# СВЕДЕНИЯ О НАГРУЗКАХ И ВОЗДЕЙСТВИЯХ
**характеристика местности**

| Характеристика                                  | Значение |
|    :---                                         |   :---:  |
| Снеговой район                                  | III      | 
| Нормативное значение снегового покрова,  кПа    | 1,5      |
| Ветровой район                                  | I        | 
| Нормативное значение ветрового давления, кПа    | 0,23     |
| Глубина промерзания, м                          | 1,76     |


## Нагрузки на конструкции

Действующими нагрузками на несущие и ограждающие конструкции объекта
являются:


'''
        self.part3='# РАСЧЕТ КОНСТРУКЦИЙ'
        self.row_table1a = '''|{0}.|{1}| k={2} | Прочность элемента, под действием наиболее неблагоприятного сочетания полных постоянных и временных расчетных нагрузок обеспечена. Коэффициент использования по наиболее неблагоприятному критерию k={3} (недонапряжение {4}%).|
'''
        self.row_table1b = '''|{0}.|{1}| k={2}| Прочность элемента, под действием наиболее неблагоприятного сочетания полных постоянных и временных расчетных нагрузок не обеспечена. Коэффициент использования по наиболее неблагоприятному критерию k={3} (перенапряжение {4}%).|
'''
        self.row_table1c = '''|{0}.|{1}| k={2}| Состав теплоограждающих конструкций: {3} |
'''
    def add_text(self, text):
        # добавить текст
        self.text = text
        # добавить номер в таблице итогов
        self.number += 1
    
    def data_search(self):
        # выбор данных из текста и добавление
        # поиск заголовка
        try:
            title = re.search(r'(# (.*)\n)', self.text).group(2)
        except:
            title  = ''
        # поиск вычисления нагрузок
        try:
            load = re.search(r'png\)((.*\n)*.*)Таблица сбора нагрузок, действующих на элемент', self.text).group(1)
            if (('Снег' or 'снег' or 'Ветр' or 'Ветер' or 'ветр' or 'ветер') in load) and (not load in self.text_load):
                self.text_load += '\n\n' + load + '\n\n' 
        except:
            pass
        # поиск таблицы нагрузок        
        try:
            table = re.search(r'Таблица сбора нагрузок, действующих на элемент(.*\n)*.*\(нормативная нагрузка [\d\.]* кг/м\)', self.text).group()
            if not table in self.table_load:
                self.table_load += '\n\n' +'**' + title + '**\n\n' + table + '\n\n'
        except:
            pass
        # получение коэффициента использования и процента
        try:
            k = re.search(r'Коэффициент использования k=([\d\.,]*)', self.text).group(1)
            k = k.replace(',','.')
            k_number=float(k)
            pass
            if k_number < 1:
                percent= round(100-k_number*100)
            else:
                percent= round(k_number*100 - 100)
        except:
            k = 0
            percent = 0
            k_number = 0
        # добавление коэффициента использования в таблицу
        k=str(k).replace('.',',')
        percent_text = str(percent)
        percent_text = percent_text.replace('.',',')
        try:
            structure = re.search(r'(Состав теплоограждающих конструкций: )(.*)(\r\n)', self.text).group(2)
        except:
            structure = ' - '
        if "Теплотехнический расчет" in self.text:
            row_table = self.row_table1c.format(self.number, title, k, structure)
            # row_table = self.row_table1a.format(self.number, title, k, k, structure)
        elif k_number < 1:
            row_table = self.row_table1a.format(self.number, title, k, k, percent_text)
        else:
            row_table = self.row_table1b.format(self.number, title, k, k, percent_text)
        self.part1 += row_table
        # добавление расчета
        self.part3 += '\n\n' + self.text + '\n\n'

    def result(self):
        # общий итоговый отчет
        text_result = self.part1
        text_result += self.part2
        text_result += self.text_load
        text_result += self.table_load
        text_result += self.part3
        return text_result

def main():
    import pandoc_md_in_world_class
    dok = pandoc_md_in_world_class.Doc(name='Общий файл')
    text = read_file_md('1_все_расчетыЛист2')
    paragraph = Result_text()
    paragraph.add_text(text=text)
    paragraph.data_search()
    text2 = paragraph.result()
    dok.addText(text=text2)
    dok.save()
if __name__ == '__main__':
    main()



