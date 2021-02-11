import csv


def read_file(a):
    a = str(a) + '.csv'
    l=[]
    with open(a,'r',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            l = l + [row]
    return l

MT = read_file('фундамент')

print(MT)
table = MT

# def in_number(table):
#     '''Перевод списка текстового в список значений'''
#     new_table = []
#     for i in table:
#             if i != '':
#                 i = i.replace(',', '.')
#                 new_table.append(float(i))
#     return new_table
# # выбор нужных частей функции
# table_x = in_number(table[0])

# table_y = in_number(table[-1])

# table_Q=[]
# for i in table[1:-1]:
#     i = in_number(i)
#     table_Q.append(i)
# print(table_x)
# print(table_y)
# print(table_Q)

