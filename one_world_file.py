# создание 1 общего world file и подчистка всего имеющегося
import os, re, pypandoc, fnmatch, pandas
import all_word_file

def read_file_md(a):
    #функция открытия одним целым
    # a= a + '.txt'
    with open(a, 'rb') as f:
        t = f.read().decode('utf-8')
    return t

def list_file(format='txt'):
    # создание списка файлов в папке заданного формата
    # отбор нужных файлов
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.' + format):
            f += [file]
    return f

def word_1():
    # os.chdir('..')
    # создание общего файла и удаление лишних файлов
    import read_exel, one_file, pandoc_md_in_world_class
    # создание списка файлов
    read_exel.create()
    # выполнение расчетов и сохранение картинок
    one_file.main2()
    # отбор нужных файлов
    f = list_file(format='md')
    # получение списка xlsx
    f_ex = list_file(format='xlsx')
    # получение списка только главных xlsx файлов
    f_ex1=[]
    for name in f_ex:
        xl = pandas.ExcelFile(name)
        i = xl.sheet_names[0]
        # Load a sheet into a DataFrame by name: df1
        df1 = xl.parse(i)
        # получение значения из первой ячейки
        df1.iat[0,0]
        if df1.iat[0,0] != '1':
            f_ex1.append(name)
        xl.close()
    # print(f_ex1)
    # print(f)
    for name_excel in f_ex1:
        name_under=name_excel.replace(" ", '_')
        # all_text=''
        paragraph = all_word_file.Result_text()
        for name_md in f:
            if name_under[:-5] in name_md[:-3]:
                # добавление расчетов в формат
                text = read_file_md(name_md)
                # paragraph = all_word_file.Result_text()
                paragraph.add_text(text=text)
                paragraph.data_search()
        all_text = paragraph.result()
        pypandoc.convert_text(all_text, format='md', to='md', outputfile = name_excel[:-5] +".md")
        # версия для windows 
        pypandoc.convert_text(all_text, format='md', to='docx', outputfile = name_excel[:-5] +".docx")
        # version for linux
        pypandoc.convert_text(all_text, format='md', to='odt', outputfile = name_excel[:-5] +".odt")
    # отбор файлов csv для удаления лишних файлов
    list_csv = list_file(format='csv')
    for file_csv in list_csv:
        name = file_csv[:-4]
        doc = pandoc_md_in_world_class.Doc(name=name)
        doc.del_image()
        for file_exrl in f_ex1:
            if file_exrl[:-5] in name:
                os.remove(name +'.csv')
                try:
                    os.remove(name +'.xlsx')
                except:
                    pass

def main():
    word_1()   

if __name__ == '__main__':
    main()
