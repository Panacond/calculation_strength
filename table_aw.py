# Таблица интерполяции начальных значений
# Получение из таблицы коэффициента эквивалентного слоя
def choice_dictionary(x, dicty):
    'выбор значений из словаря'
    for i in dicty:
        n_min = dicty[i]
        break
    for i in dicty:
        i_min = i
        break
    for i in dicty:
        if x <= i:
            n_max = dicty[i]
            i_max = i
            break
        if x >= i:
            n_min = dicty[i]
            n_max = dicty[i]
            i_min = i
            i_max = i
    return i_min, i_max, n_min, n_max

def choice_list(x, list1):
    'выбор значений из словаря'
    n_min = list1[0]
    for i in list1:
        if x <= i:
            n_max = i
            break
        if x >= i:
            n_min = i
            n_max = i
    return n_min, n_max

def interpolation(x, i_min, i_max, n_min, n_max):
    'интерполяция'
    if i_min != i_max:
        n2 = n_min + (n_max - n_min)*(x-i_min)/(i_max - i_min)
        n2 = round(n2,3)
    else:
        n2 = n_max
    return n2

def all(n, i):
    nu = [0.1, 0.2, 0.25, 0.3, 0.35, 0.4]
    n0 = [1,1.5,2,3,4,5,10]
    d10 = {0.1: 0.89, 0.2: 0.94, 0.25: 0.99, 0.3: 1.08, 0.35: 1.24, 0.4: 1.58}
    d15 = {0.1: 1.09, 0.2: 1.15, 0.25: 1.21, 0.3: 1.32, 0.35: 1.52, 0.4: 1.94}
    d20 = {0.1: 1.23, 0.2: 1.3, 0.25: 1.37, 0.3: 1.49, 0.35: 1.72, 0.4: 2.2}
    d30 = {0.1: 1.46, 0.2: 1.54, 0.25: 1.62, 0.3: 1.76, 0.35: 2.01, 0.4: 2.59}
    d40 = {0.1: 1.62, 0.2: 1.72, 0.25: 1.81, 0.3: 1.97, 0.35: 2.26, 0.4: 2.9}
    d50 = {0.1: 1.74, 0.2: 1.84, 0.25: 1.94, 0.3: 2.11, 0.35: 2.42, 0.4: 3.1}
    d100 = {0.1: 2.15, 0.2: 2.26, 0.25: 2.38, 0.3: 2.6, 0.35: 2.98, 0.4: 3.82}
    n_isx = {1: d10, 1.5: d15, 2: d20, 3: d30, 4: d40, 5: d50, 10: d100}

    i_min, i_max, a, b = choice_dictionary(n, n_isx)
    i_min, i_max, a_min, a_max = choice_dictionary(i, a)
    a_s = interpolation(i, i_min, i_max, a_min, a_max)
    i_min, i_max, b_min, b_max = choice_dictionary(i, b)
    b_s = interpolation(i, i_min, i_max, b_min, b_max)
    n_min, n_max = choice_list(n, n0)
    n3 = interpolation(n, n_min, n_max, a_s, b_s)

    return n3