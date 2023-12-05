import matplotlib.pyplot as plt
import astropy.io.fits as pyfits
from tkinter import *
from tkinter import ttk
import numpy as np


def changed():
    global px
    global py
    global p3
    px = 0
    py = 0
    p3 = 0
    if var.get() == 1:
        px = 10
    if var1.get() == 1:
        py = 10
    if var2.get() == 1:
        p3 = 10
def profil():
    global entf
    global entX
    global entY
    global entr
    global surf
    d = str(entf.get())
    hdulist = pyfits.open(d)
    scidata = hdulist[0].data

    X1 = []
    X2 = []
    Y1 = []  # изменяем х
    Y2 = []
    x = entX.get()
    x = int(x)
    y = int(entY.get())
    y = int(y)
    r = int(entr.get())
    r = int(r)
    for i in range(x - r, x + r):  # записываем х
        Y1.append(scidata[y][i])
        temp = i
        X1.append(temp)
    for i in range(y - r, y + r):
        Y2.append(scidata[i][x])
        temp = i
        X2.append(temp)
    if px == 10:
        plt.figure()  # создает полотно для нескольких графиков
        plt.title('                          Изменение светимости звезды от координаты')
        plt.plot(X1, Y1)
        plt.xlabel('Изменение координаты Х')
        plt.ylabel('Значение энергии')
        plt.show()
    if py == 10:
        plt.figure()
        plt.title('                          Изменение светимости звезды от координаты')
        plt.plot(X2, Y2)
        plt.xlabel('Изменение координаты Y')
        plt.ylabel('Значение энергии')
        plt.show()
    if p3 == 10:
        Z = np.empty((len(Y2), len(X2)), dtype=int)
        x1 = np.empty((len(X1), 1), dtype=int)
        y1 = np.empty((len(X2), 1), dtype=int)
        for i in range(len(X2)):
            y1[i] = int(X2[i])

        for i in range(len(Y1)):
            x1[i] = int(X1[i])

        X, Y = np.meshgrid(x1, y1)

        for i in range(x-r, x +r):
            for j in range(y-r, y+r):
                Z[j-y+r][i-x+r] = int(scidata[j][i])

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_surface(X, Y, Z) #color='grey'
        ax.set_xlabel('Номер пикселя')
        ax.set_ylabel('Номер пикселя')
        ax.set_zlabel('Изменение энергии по Y')
        plt.title('Профиль 3d')
        plt.show()
    hdulist.close()



def Energy():
    d = str(entf.get())
    hdulist = pyfits.open(d)
    scidata = hdulist[0].data
    global Eng
    global lblEn
    global entR
    global entRr
    x = int(entX.get())
    y = int(entY.get())
    r = int(entr.get())
    R1 = int(entRr.get())
    R2 = int(entR.get())
    R = abs(R2 - R1)

    count_ =0
    S = 0
    exp = float(hdulist[0].header['exptime'])

    for i in range(x - r, x + r):
        for j in range(y - r, y + r):
            if (i-x)**2 + (j-y)**2 <= r**2:
                S += scidata[j][i]
                count_ +=1
    S = float(S) / exp

    count = 0
    N = 0

    for i in range(x-R2, x+R2):
        for j in range(y-R2, y+R2):
            if (r ** 2 < (i - x) ** 2 + (j - y) ** 2) and ((i - x) ** 2 + (j - y) ** 2 <= R2 ** 2):
                count += 1
                N += scidata[j][i]

    print(f' s ={S}, N ={N}, count_ = {count_}, count ={count}, exp = {exp}')
    N = float(N) / (count * exp)
    Eng = 0
    Eng = S - N*count_
    lblEn["text"] = Eng






#Создаём интерфейс
root = Tk() #создаем окно "приложения"
root.title("Данные звезды")# даём ему название
root.geometry("900x300")# задаём его размер


#Лейблы, для подписи энтров и сами энтры
lblX = ttk.Label(text = "X", font=("Arial", 18), padding=5)#создаём лейбл для иксовой координаты
lblX.grid(row=0, column=0) #располагаем лейбл самым верхним и первым
entX = ttk.Entry() #создаём ввод для иксовой координаты
entX.grid(row=0, column=1)# располагаем энтер правее от его лейбла

lblY = ttk.Label(text = "Y", font=("Arial", 18), padding=5)#создаём лейбл для игрековой координаты
lblY.grid(row=1, column=0) #располагаем лейбл вторым сверху и первым
entY = ttk.Entry() #создаём ввод для иксовой координаты
entY.grid(row=1, column=1)# располагаем энтер правее от его лейбла

lblr = ttk.Label(text = "Радиус звезды", font=("Arial", 12), padding=5)#создаём лейбл для радиуса звезды
lblr.grid(row=2, column=0) #располагаем лейбл третим сверху и первым
entr = ttk.Entry() #создаём ввод для радиуса звезды
entr.grid(row=2, column=1)# располагаем энтер правее от его лейбла

lblR = ttk.Label(text = "Внешний радиус фонового кольцa", font=("Arial", 12), padding=5)#создаём лейбл для ширины фонового кольца
lblR.grid(row=3, column=0) #располагаем лейбл четвертым сверху и первым
entR = ttk.Entry() #создаём ввод для ширины
entR.grid(row=3, column=1)# располагаем энтер правее от его лейбла

lblRr = ttk.Label(text = "Внутренний радиус фонового кольцa", font=("Arial", 12), padding=5)#создаём лейбл для ширины фонового кольца
lblRr.grid(row=4, column=0) #располагаем лейбл четвертым сверху и первым
entRr = ttk.Entry() #создаём ввод для ширины
entRr.grid(row=4, column=1)# располагаем энтер правее от его лейбла

lblf = ttk.Label(text = "Путь к файлу", font=("Arial", 12), padding=5)#создаём лейбл для пути к файлу
lblf.grid(row=5, column=0) #располагаем лейбл четвертым сверху и первым
entf = ttk.Entry() #создаём ввод для пути к файлу
entf.grid(row=5, column=1)# располагаем энтер правее от его лейбла


#Делаем кнопки

btnEn = ttk.Button(text="Энергия звезды", command=Energy) #создаём кнопку с функцией подсчёта энергии btnEn = ttk.Button(text="Button", command=Energy)
btnEn.grid(row=0, column=2, ipadx=20, ipady=6, padx=50, pady=4)
lblEn = ttk.Label(font=("Arial", 12), padding=5)#создаём лейбл для пути к файлу
lblEn.grid(row=0, column=3)

btnGr = ttk.Button(text="Профиль", command=profil)# cоздаём кнопку для вывода профиля btnGr = ttk.Button(text="Профиль", command=Profil)
btnGr.grid(row=2, column=3, ipadx=6, ipady=6, padx=4, pady=4)

var = IntVar()
chbtn= ttk.Checkbutton(text ="Профиль по Х", variable=var, command=changed) #создаём кнопку выбора для вывода профиля по Х
chbtn.grid(row=1, column=2) #Размещаем кнопку третьей слева, второй сверху

var1 = IntVar()
chbtn= ttk.Checkbutton(text ="Профиль по У", variable=var1, command=changed) #создаём кнопку выбора для вывода профиля по У
chbtn.grid(row=2, column=2) #Размещаем кнопку третьей слева, третьей сверху

var2 = IntVar()
chbtn= ttk.Checkbutton(text ="Профиль 3d", variable=var2, command=changed) #создаём кнопку выбора для вывода профиля 3д
chbtn.grid(row=3, column=2, ipadx=7) #Размещаем кнопку третьей слева, четвёртой сверху

root.mainloop()#зацикливаем окно на открытие и не даём ему закрыться самостоятельно