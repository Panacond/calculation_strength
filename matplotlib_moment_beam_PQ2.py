# Построение эпюр от сосредоточенных сил

import matplotlib.pyplot as plt
# функции и классы
# исходные данные для эпюры поперечных сил и моментов от сил действующих на балку
# подавать значения, силы и их положение и длину балки
class Power(object):
    '''Сила принимает величину и положение'''
    def __init__(self, P, x):
        self.P = P
        self.x = x
    def __str__(self):
        return self.P, self.x
    def R1(self, beam):
        'определение опорной рекации 1'
        Ma, Mb = self.support_moment(beam)
        R1 = (self.P*(beam.L-self.x) - Ma + Mb)/beam.L
        return R1
    def R2(self, beam):
        'определение опорной рекации 2'
        Ma, Mb = self.support_moment(beam)
        R2 = (self.P*self.x - Ma + Mb )/beam.L
        return R2
    def support_moment(self, beam):
        # задание опорных моментов
        if beam.S == 0:
            Ma = 0
            Mb = 0
        if beam.S == 1:
            Ma = -1*self.P*self.x*(beam.L-self.x)/(2*beam.L**2)*(beam.L+beam.L-self.x)
            Mb = 0
        if beam.S == 2:
            Ma = -1*self.P*self.x*(beam.L-self.x)**2/beam.L**2
            Mb = -self.P*self.x**2*(beam.L-self.x)/beam.L**2
        if beam.S == 3:
            Ma = -1*self.P*self.x
            Mb = 0
        return Ma, Mb
class Shared_forse(object):
    'Распределенная нагрузка принимает величину, координату начала и длину приложения'
    def __init__(self, q, x, a):
        self.q = q
        self.x = x
        self.a = a
    def __str__(self):
        return self.q, self.x, self.a
    def support_moment(self, beam):
        # задание опорных моментов
        a = self.x + self.a/2
        b = beam.L - a
        c = self.a
        l = beam.L
        if beam.S == 0:
            Ma = 0
            Mb = 0
        if beam.S == 1:
            Ma = -1*self.q*a*b*c/(2*l**2)*(l+b-c**2/(4*a))
            Mb = 0
        if beam.S == 2:
            Ma = -1*self.q*c/l**2*(a*b**2-c**2/12*(2*b-a))
            Mb = -self.q*c/l**2*(a**2*b-c**2/12*(2*a-b))
        if beam.S == 3:
            Ma = -1*self.q*a*c
            Mb = 0
        return Ma, Mb
    def R1(self, beam):
        'опеределение опорной реакции 1'
        Ma, Mb = self.support_moment(beam)
        R1 = (self.q*self.a*(beam.L - (self.x + self.a/2)) - Ma + Mb)/beam.L 
        return R1
    def R2(self, beam):
        'опеределение опорной реакции 2'
        Ma, Mb = self.support_moment(beam)
        R2 = (self.q*self.a*(self.x + self.a / 2) - Ma + Mb )/ beam.L 
        return R2
class Graph(object):
    # 'Балка задается длина и схема (0 шарнирная, 1 с одной жесткой опорой, 2 с обоими жесткими
    # '3 консольная) и добавляются классы сил, и выдает списки значений'
    def __init__(self, L, S):
        # Задать длину балки и схему
        self.points = [] # поперечные силы
        self.sharedq = [] # распределенные силы
        self.L = L
        self.point_x = [i/20*L for i in range(20+1)]
        self.R1 = 0
        self.R2 = 0
        self.cross_power = []
        self.bending_moment = []
        self.deflections = []
        self.S = S
        self.Ma = 0
        self.Mb = 0
    def addP(self, P, x):
        'Добавить силу на балку, сначала величину силы(кгс), а потом координату х(м)'
        point = Power(P, x)
        self.points.append(point)
        if point.x-0.01 != self.point_x:
            self.point_x.append(point.x-0.01)
        if point.x+0.01 != self.point_x:
            self.point_x.append(point.x+0.01)
        self.point_x.sort()
    def addQ(self, q, x, a):
        'Добавить распределенную нагрузку (кгс) точка начала (м), длина нагрузки (м)'
        sharedq1 = Shared_forse(q, x, a)
        self.sharedq.append(sharedq1)
        if sharedq1.x != self.point_x:
            self.point_x.append(sharedq1.x)
        if sharedq1.x + sharedq1.a != self.point_x:
            self.point_x.append(sharedq1.x + sharedq1.a)
        self.point_x.sort()
    def ep(self):
        'Построение эпюр'
        self.Ma, self.Mb = 0, 0
        for i in self.points:
            Ma, Mb = i.support_moment(self)
            self.Ma += Ma
            self.Mb += Mb
        for i in self.sharedq:
            Ma, Mb = i.support_moment(self)
            self.Ma += Ma
            self.Mb += Mb
        self.R1 = 0
        for i in self.points:
            self.R1 += i.R1(self)
        for i in self.sharedq:
            self.R1 += i.R1(self)
        self.R2 = 0
        for i in self.points:
            self.R2 += i.R1(self)
        for i in self.sharedq:
            self.R2 += i.R2(self)
        # self.cross_power = []
        # создание списка значений поперечных сил
        for x in self.point_x:
            P = self.R1
            for point in self.points:
                if point.x < x:
                    P -= point.P
            for q in self.sharedq:
                if q.x + q.a <= x:
                    P -= q.q*q.a
                if q.x < x and q.x + q.a > x:
                    P -= q.q*(x - q.x)
            self.cross_power.append(P)
        # self.bending_moment = []
        # создание списка значений изгибающих моментов
        for x in self.point_x:
            M = self.R1*x + self.Ma
            for point in self.points:
                if point.x < x:
                    M -= point.P*(x-point.x)
            for q in self.sharedq:
               if q.x + q.a <= x:
                    M -= q.q*q.a*(x-(q.x + q.a/2))
               if q.x < x and q.x + q.a > x:
                    M -= q.q*(x - q.x)*(x-(q.x + x)/2)
            self.bending_moment.append(M)
        # создание списка значений прогибов
        for x in self.point_x:
            if self.S == 0:
                Ra=self.R1
                L=self.L
                fi=Ra*L**3/6/L
                for point in self.points:
                    P=point.P
                    Px=point.x
                    c=L-Px
                    fi -=(P*c**3/6)/L
                for q in self.sharedq:
                    q1 = q.q
                    a = q.x
                    b = q.a
                    c= L - a
                    fi -=(q1*c**4/24)/L
                    c= L - a - b
                    fi +=(q1*c**4/24)/L
                c=x
                f = -fi*x + Ra*c**3/6
            # для защемленных балок
            else:
                Ra=self.R1
                Ma=self.Ma
                c=x
                f = Ma*c**2/2 + Ra*c**3/6
                # для всех балок
            for point in self.points:
                P=point.P
                Px=point.x
                c=x-Px
                if Px < x :
                    f -=P*c**3/6
            for q in self.sharedq:
                q1 = q.q
                a = q.x
                b = q.a
                c= x - a
                c1 = x - a - b
                if a < x:
                    f -=q1*c**4/24
                if a + b < x:
                    f +=q1*c1**4/24
            self.deflections.append(f)        
    def epQ(self):
        'возврат списка значений поперечных сил'
        self.ep()
        return self.cross_power
    def epM(self):
        'возврат списка значений моментов'
        return self.bending_moment
    def all_ep(self):
        'возвращение всех списков одновременно'
        a = self.point_x
        b = self.epQ()
        c = self.epM()
        d = self.deflections
        return a, b, c, d

# координаты для построение эпюр
def epur(x,y):
    x1=[]
    y1=[]
    for i in range(len(x)):
        if i == 0:
            x1.append(x[i])
            x1.append(x[i])
            y1.append(0)
            y1.append(y[i])
        elif i == len(x):
            x1.append(x[i])
            x1.append(x[i])
            y1.append(y[i])
            y1.append(0)
        else:
            x1.append(x[i])
            x1.append(x[i])
            x1.append(x[i])
            y1.append(y[i])
            y1.append(0)
            y1.append(y[i])
    return x1,y1

# построение графика
def plot_G(save, tit, x, y):
    plt.figure(figsize=(9, 4)) # мастаб рисунка
    td = str(round(max([abs(min(y)),abs(max(y))]),2))
    min_rezult = str(round(abs(min(y)),2))
    max_rezult = str(round(abs(max(y)),2))
    tit = tit.replace('{0}', str(td))
    plt.title(tit) # заголовок
    plt.xlabel("L="+ str(round(max(x),1)) + 'м') # ось абсцисс
    plt.ylabel("Значение") # ось ординат
    plt.grid(True) # включение отображение сетки
    y2 = [0 for i in x]      
    x1,y1=epur(x,y)
    plt.plot(x1, y1, x, y2)  # построение графика  
    plt.savefig(str(save)) # сохранение графика
    return min_rezult, max_rezult

def share_paint(x1, x2, t):
    'построение распределенной нагрузки'
    def f_all(xx):
        '''построение одной стрелочки распределенной нагрузки '''
        plt.annotate( ' ', xy=(xx, 0), xytext=(xx, 1), 
        arrowprops=dict(facecolor='red', shrink=0.01, ec = 'r'), size = 10, ha = 'center')
    dx=(x2-x1)/11
    list_Q=list([round(x1+i*dx,2) for i in range(12)])
    plt.text((x2+x1)/2, 1, t, fontsize=15, ha='center')
    for i in list_Q:
        f_all(i)
    plt.plot([x1, x2], [0.95, 0.95], color = 'r')
def forse_paint(x, t):
    'постороение силы'
    plt.annotate(t, xy=(x, 0), xytext=(x, 2), 
            arrowprops=dict(facecolor='red', shrink=0.01, ec = 'r'), size = 15, ha = 'center')
def initial_graf(L, beam, save):
    'построение графика расположения нагрузок'
    plt.figure(figsize=(9, 4)) # мастаб рисунка
    plt.title("Схема приложения нагрузок для балки L="+ str(L) + 'м') # подпись
    plt.xlabel('Сосредоточенные нагрузки в кгс; распределенные нагрузки в кгс/м') # ось абсцисс
    plt.plot([0, 0], [0, 2.5], [0, L],[0,0], color = 'k')# построение рисунка
    for p in beam.points:
        P = p.P
        x = p.x
        forse_paint(x, round(P,2))
    for q in beam.sharedq:
        x1 = q.x
        x2 = q.x + q.a 
        q = q.q
        share_paint(x1, x2, round(q,2))
    plt.savefig(str(save)) # сохранение графика

def test_all(L, B1, name):
    '''для тестирования'''
    x, Q, M, f = B1.all_ep() # передача значений в графики
    def max_min(list_input):
        min_rezult = str(round(abs(min(list_input)),2))
        max_rezult = str(round(abs(max(list_input)),2))
        return min_rezult, max_rezult
    Qmin, Qmax = max_min(list_input = Q)
    t='Эпюра изгибающих моментов максмальное значение \n M ={0} кгс*м'
    
    M =[round(-i,2) for i in M]
    Mmin, Mmax = max_min(list_input= M)

    fmin, fmax = max_min(list_input= f)
    stress = [Qmin, Qmax, Mmin, Mmax, L, fmin]
    # stress = [Qmin, Qmax, Mmin, Mmax, L]
    return stress

def plot_all(L, B1, name):
    '''построение всех графиков одной функцией'''
    x, Q, M, f = B1.all_ep() # передача значений в графики
    t = 'Схема загружения балки'
    initial_graf(L = L, beam = B1, save = name +'1'  )
    t='Эпюра поперечных сил максмальное значение Q ={0} кгс'
    Qmin, Qmax = plot_G(save = name + '2' +  'Q', tit = t, x = x, y = Q)
    t='Эпюра изгибающих моментов максмальное значение \n M ={0} кгс*м'
    
    M =[round(-i,2) for i in M]
    Mmin, Mmax = plot_G(save = name + '3' +  'M', tit = t, x = x, y = M)

    t=r'Эпюра прогибов максмальное значение $f= {0} \times  \frac{10^9 \times кгс \times мм^3 }{EI}$'
    fmin, fmax = plot_G(save = name + '4' +  'f', tit = t, x = x, y = f)
    stress = [Qmin, Qmax, Mmin, Mmax, L, fmin]
    # матрица прогибов
    table_bending_f=[[x],[f]]
    return stress

def replase_point(k):
    k = str(k)
    if ',' in k:
        k=k.replace(',','.')
    k= float(k)
    return k


#Основная программа
def main():
    name ='1Балка'
    L = 6
    B1 = Graph(L = L ,S = 0) # задание балки
    # B1.addP(1200, 3) # добавление силы, величина, координатаQ, от левого конца балки
    B1.addQ(100,0,6) # добавление распределенной нагрузки, сила, координата, длина приложения
    plot_all(L, B1, name)
    name ='2Балка'
    B1 = Graph(L = L ,S = 1)
    B1.addP(1200, 4)
    B1.addQ(100,2,2)
    plot_all(L, B1, name)
    name ='3Балка'
    B1 = Graph(L = L ,S = 2)
    B1.addQ(100,2,2)
    B1.addP(1200, 4)
    plot_all(L, B1, name)
    name ='4Балка'
    B1 = Graph(L = L ,S = 3)
    B1.addQ(100,2,2)
    B1.addP(1200, 4)
    plot_all(L, B1, name)

def plot_csv_file(f, name, dict_load):
    # f-таблица расчета, name, dict_load
    # печать из csv файла замена букв на значения из таблицы
    L = replase_point(f[1][2])
    S = int(f[0][2])
    B1 = Graph(L = L ,S = S) # задание балки
    for i in f:
        if i[0] == 'Q':
            if i[1] in ['Q1', 'Q2', 'Q3', 'Q4']:
                a = dict_load[i[1]]
                if i[5] != '':
                    k= replase_point(i[5])
                    a = replase_point(a)*k
            else:
                a = replase_point(i[1])
            if 'L' in i[2]:
                b = i[2].replace('L',str(L))
                b = replase_point(b)*replase_point(i[4])
            else:
                b =replase_point(i[2])
            if 'L' in i[3]:
                c = i[3].replace('L',str(L))
                c = replase_point(c)*replase_point(i[4])
            else:
                c = replase_point(i[3])
            B1.addQ(a,b,c)
        if i[0] == 'P':
            if i[1] in ['Q1', 'Q2', 'Q3', 'Q4']:
                a = dict_load[i[1]]
                if i[4] != '':
                    k=replase_point(i[4])
                    a = replase_point(a)*k
            else:
                a = replase_point(i[1])
            if 'L' in i[2]:
                c = i[2].replace('L',str(L))
                c = replase_point(c)*replase_point(i[3])
            else:
                c =replase_point(i[2])
            B1.addP(a,c)
    stress = plot_all(L, B1, name)
    return stress
            
# Построение графиков
if __name__ == '__main__':
    main()
    # name ='2Балка'
    # f =[['Усилия', 'схема', '0', '', '', ''], 
    #     ['Длина балки м', 'L=', '6', '', '', ''], 
    #     ['Q', 'Q1', '0', 'L', '1', ''], 
    #     ['P', '500', '2', '', '', ''], 
    #     ['P', 'Q2', 'L', '0.5', '', '']]
    # dict_load = {'Q1': 500, 'Q2': 550, 'Q3': 700, 'Q4': 790}
    # stress = plot_csv_file(f, name, dict_load)
    # print(stress)
