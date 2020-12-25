# версия 10
# Чтение формул из текстового файла вычисление их и запись в текстовый файл файл
# чтение содержимого папок и выбор необходимых элементов
#!!!Функции
# печать в файл
def write_file(name_file, text):
    f = open(name_file +'.txt', 'w')
    f.write(text)
    f.close()

# добавление в словарь коментарий и формул
#выбор нужных симоволов
def sele(a):
    l=len(a)
    b='1234567890.'
    c=0
    for y in b:
        for x in a:
            if x==y:
                c=c+1
            else:
                c=c
    d=False
    if l == c:
        d=True
    return(d)

class Calc (object):
    '''класс выполнения вычислений добавляем текстовую строку из кода программы'''
    def __init__(self):
    # созданные переменные
        self.list_string = [] # список всех строк
        self.numer = dict()#словарь исходных данных
        self.kef = []    # список ключей исходных данных
        self.rezult = '' # результаты
    def true_rep(self, a):
        'Проверка, а есть ли переменные в строке'
        c=None
        for x in self.kef:
            if x in a:
                c=True
        return(c)
    def rep(self, a):
        # замена переменных
        b = self.kef[:]
        def cmp_min(a1):
            return max(a1)
        b.sort(key = cmp_min)
        b.reverse()
        for x in b:
            a = a.replace(str(x),str(self.numer[x]))
        return(a)
    def evaluate(self, t):
        'функция выполнения арифметических операций'
        import math
        t = t.replace('%','math.sqrt')
        try:
            r = eval(t)
            return round(r,2)
        except:
            pass       
    def dictionary(self, original_string, n):
        # текст, значение переменной, вычисления
        if  not '=' in original_string:
            rez = original_string
        else:
            a = original_string.split('=')
            a[1] = str(a[1]).replace('^','**')# замена знаков в формулах
            a[1] = str(a[1]).replace(',','.')
            a[1] = str(a[1]).replace(' ','')
            a[1] = str(a[1]).replace('\\times','*')
            a[1] = str(a[1]).replace('\\sqrt','%')
            a[1] = str(a[1]).replace(' ','')
            a[1] = a[1].split('=')[0]
            if sele(a[1]):# если в правой части число, добавление его в переменные
                self.kef.append(a[0])
                self.numer [a[0]] = float(a[1])
                rez = a[0] + '=' + a[1]
            elif self.true_rep(a[1]): # если есть переменные, подстановка и вычисления
                b = self.rep(a[1])
                c1 = self.evaluate(b)
                if c1 == None:
                    rez = None
                    pass
                else:
                    self.kef.append(a[0])
                    self.numer [a[0]] = c1
                    rez = a[0] + '=' + a[1] + '=' + b + '=' + str(c1)
            else: # в правой части одни цифры, вычисление
                c2 = self.evaluate(a[1])
                if c2 == None:
                    rez = None
                    pass
                else:
                    self.kef.append(a[0])
                    self.numer [a[0]] = c2
                    rez = a[0] + '=' + a[1] +  '=' + str(c2)
            if rez != None:
                rez = rez.replace('**', '^')
                rez = rez.replace('*',' \\times ' ) #' \\times ')
                rez = rez.replace('%', ' \\sqrt ')
        return rez
    def c1(self, text, n_letter = 1, charge = '\t'):
        # выполнение подстановка строки и выполнение вычислений
        text = text.replace(charge, '\n')
        l = text.split('\n')
        string_middle = ''
        for n in range(len(l)):
            a = l[n]
            string_rez = self.dictionary(a, n)
            if string_rez == None:
                string_rez = 'error string' + str(l[n])
                print('не указаны неизвестные cтрока формулы', n+1,
                      '\n', str(l[n]))

            string_middle += string_rez + '\n'
        self.rezult += self.string_split(t = string_middle, n = n_letter, charge = charge)
    def string_split(self, t, n = 1, charge = '\t'):
        # выполнение разделения строки
        t = t.replace(charge, '\n')
        list1 = t.split('\n')
        list2 = [list1[0]]
        for i  in range(len(list1)):
            if len(list2[-1] + '\t' + list1[i]) < n and '=' in list1[i]:
                list2[-1] += charge + list1[i]
            else:
                list2.append(list1[i])
        txt = ''
        list2 = list2[1:]
        for i in list2:
            txt += i + '\n'
        return txt[:-2]
    def finish(self, name):
        #запись готовых результатов полного расчета
        return self.rezult
#расчет текстовых файлов
# открытие файла с формулами
def read_file(a):
    f = open(a +'.txt', 'r')
    l = f.read()
    f.close()
    return l
# Функция чтения файлов из папки
def read_folder():
    import os, fnmatch
    f = []# создание списка файлов и чтение из текущей папки списка файлов
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.txt'):
            f += [file]
    need_f = [] # создание списка названий файлов
    for i in f:
        need_f += [i[:-4]]
    return need_f
#основная программа
def main():
    for i in read_folder():
        print('*-'*5)
        txt = Calc()
        print(i)
        text1 = read_file(i)
        txt.c1(text1, 27)# число символов в одной строке
        p = txt.finish(name = i)
        write_file(i, p)
        #вывод на экран 2 последних строк
        fin = p.split('\n')
        fin = fin[-2] + '\n' + fin[-1]
        print(fin)

if __name__ == '__main__':
    main()

# запуск из другого файла и вывод результатов в него
def main1():
    fin1 = ""
    for i in read_folder():
        txt = Calc()
        text1 = read_file(i)
        txt.c1(text1, 27)# число символов в одной строке
        p = txt.finish(name = i)
        write_file(i, p)
        #вывод на экран 2 последних строк
        fin = p.split('\n')
        fin = fin[-2] + '\n' + fin[-1]
        fin1 += '\n' + str(i) + '\n' + fin
    print(fin1)
    return(fin1)

