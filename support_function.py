# -*- coding: utf-8 -*-
# вспомогательные функции для оформления файлов
import os, fnmatch, csv

def tabl_taxt(tabl):
    # функция чтения csv файлов
    # для функции read_file_csv чтение таблиц
    text_file = ''
    for i in tabl:
        text_file += i[0] + '\t' + i[1] + i[2] + '\n'
    return text_file

def read_file_csv(a):
    # функция чтения csv файлов
    a = str(a)
    l=[]
    with open(a,'r',newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return tabl_taxt(l)


def write_filesAnd_calc(end_of_file_name, calculation):
    # указать концовку файлов которого нужно прочитать '*CBR.csv'
    # функция прочитает все файлы с подобными концовками выполнит над ними
    # вычисления и сохранит текстовые файлы вычислений
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, end_of_file_name):
            f += [file]
    for i in f:
        text_file = read_file_csv(i)
        name = i[:-7]
        text_file = calculation(name, text_file)
        from string_calculation import write_file
        write_file(name,text_file)