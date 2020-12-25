import csv


def read_file(a):
    a = str(a) + '.csv'
    l=[]
    with open(a,'r',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return l

MT = read_file('ЖБ балка файл')

print(MT)


