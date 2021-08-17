
# python3
import numpy

def SP15Table19(x,y):
    'Выбор значений из таблицы 19 сп 15'
    # задание нужных таблиц
    table_x = [1500, 1000, 750, 500, 350, 200, 100]
    table_Q = [[1, 1, 1, 0.98, 0.94, 0.9, 0.82],
            [0.98, 0.96, 0.95, 0.91, 0.88, 0.81, 0.68],
            [0.95, 0.92, 0.9, 0.85, 0.8, 0.7, 0.54],
            [0.92, 0.88, 0.84, 0.79, 0.72, 0.6, 0.43],
            [0.88, 0.84, 0.79, 0.72, 0.64, 0.51, 0.34],
            [0.85, 0.79, 0.73, 0.66, 0.57, 0.43, 0.28],
            [0.81, 0.74, 0.68, 0.59, 0.5, 0.37, 0.23],
            [0.77, 0.7, 0.63, 0.53, 0.45, 0.32, 0.23],
            [0.69, 0.61, 0.53, 0.43, 0.35, 0.24, 0.23],
            [0.61, 0.52, 0.45, 0.36, 0.29, 0.2, 0.2],
            [0.53, 0.45, 0.39, 0.32, 0.25, 0.17, 0.17],
            [0.44, 0.38, 0.32, 0.26, 0.21, 0.14, 0.14],
            [0.36, 0.31, 0.26, 0.21, 0.17, 0.12, 0.12],
            [0.29, 0.25, 0.21, 0.17, 0.14, 0.09, 0.09],
            [0.21, 0.18, 0.16, 0.13, 0.1, 0.07, 0.07],
            [0.17, 0.15, 0.13, 0.1, 0.08, 0.05, 0.05],
            [0.13, 0.12, 0.1, 0.08, 0.06, 0.04, 0.04]]
    table_y = [4, 6, 8, 10, 12, 14, 16, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54]
    table_x.reverse()
    # table_y.reverse()
    table_Q.reverse()
    # cначала создаем список значений у
    table_Y = []
    for i in table_Q:
        interpoly=numpy.interp(x,table_x,i)
        table_Y.append(interpoly)
    table_Y.reverse()
    f = numpy.interp(y,table_y,table_Y)
    return round(f,2)
# print(SP15Table19(500,5.7))

def SP15Table21(x):
    # Таблица 15 СП 15 каменные и армокаменные конструкции
    # Значения выбраны для неармированной кладки из керамического кирпича
    X=[10, 12, 14, 16, 18, 20, 22, 24, 26]
    Y=[0, 0.04, 0.08, 0.12, 0.15, 0.2, 0.24, 0.27, 0.31]
    m_g = numpy.interp(x,X,Y)
    return m_g
print(SP15Table21(15))