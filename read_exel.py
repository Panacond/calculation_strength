# Чтение ексель файлов и создание csv файлов от каждой страницы
import os, fnmatch, pandas

def create_csv(name):
    # создание таблиц csv
    # Load spreadsheet
    xl = pandas.ExcelFile(name)
    # # Print the sheet names
    # print(xl.sheet_names)
    for i in xl.sheet_names:
        # Load a sheet into a DataFrame by name: df1
        df1 = xl.parse(i)
        try:
            # получение значения из первой ячейки
            df1.iat[0,0]
            # Write the DataFrame to csv
            if df1.iat[0,0] != '1':
                df1.to_csv(name[:-5]+i+".csv", encoding='utf-8', index=False)
            # df1.to_csv(name[:-5]+i+".csv", encoding='utf-8', index=False, header=None)
        except:
            pass

def create():
    # отбор нужных файлов
    import one_world_file
    f = one_world_file.list_file('xlsx')
    for i in f:
        # работа с одним файлом создание таблицы, рисунки, текст ворлд
        create_csv(name = i)

def main():
    create()

if __name__ == '__main__':
    main()
