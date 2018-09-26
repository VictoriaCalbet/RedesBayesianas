"""
    El código de esta implementación del juego del buscaminas, está extraído de un usuario que lo compartió en:
    https://codereview.stackexchange.com/questions/191550/minesweeper-in-python-tkinter

    No obstante ha habido algunas pequeñas modificaciones, adaptado para que esté en castellano a la hora de poder
    rellenar los campos requeridos para jugar y una mejor optimización a la hora de guardar la configuración.

    Este código no es realizado por nosotras, las encargadas de resolver el problema del buscaminas con redes bayesianas,
    puesto que no era un requerimiento específico ni se indicaba como parte de la solución. Esta implementado, con el
    único objetivo de facilitar al usuario que pruebe nuestra solución, el manejo de las dos interfaces establecidas:

    - La del propio juego del buscaminas
    - La propia de la resolución del problema

    De esta forma podrá ejecutar ambas interfaces desde el mismo entorno de trabajo, sin necesidad de buscar otra
    aplicación para poder ir ejecutando el problema.

    Por lo tanto, como no somos autoras del código de este juego, no realizaremos comentarios sobre qué se realiza en
    cada uno de los métodos o líneas de código, puesto que será irrelevante para la elaboración y valoración del problema.

"""
import configparser
import random
import tkinter
import tkinter.messagebox
import tkinter.simpledialog

window = tkinter.Tk()

window.title("Buscaminas")
window.geometry("600x400")

# prepare default values

rows = 5
cols = 5
mines = 5

field = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

gameover = False
customsizes = []


def createMenu():
    menubar = tkinter.Menu(window)
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="Pequeño (5x5 con 5 minas)", command=lambda: setSize(5, 5, 5))
    menusize.add_command(label="Medio (8x8 con 13 minas)", command=lambda: setSize(8, 8, 13))
    menusize.add_command(label="Grande (10x10 con 35 minas)", command=lambda: setSize(10, 10, 35))
    menusize.add_command(label="Personalizar", command=setCustomSize)
    menusize.add_separator()
    for x in range(0, len(customsizes)):
        menusize.add_command(
            label=str(customsizes[x][0]) + "x" + str(customsizes[x][1]) + " con " + str(customsizes[x][2]) + " minas",
            command=lambda customsizes=customsizes: setSize(customsizes[x][0], customsizes[x][1], customsizes[x][2]))
    menusize.add_command(label="Salir", command=lambda: window.destroy())
    menubar.add_cascade(label="Tamaño", menu=menusize)

    # Menu de informacion
    menuinfo = tkinter.Menu(window, tearoff=0)
    menuinfo.add_command(label="Acerca de...", command=nosotras)
    menubar.add_cascade(label="Trabajo IA", menu=menuinfo)
    window.config(menu=menubar)


def nosotras():
    tkinter.messagebox.showinfo("Acerca de...",
                                "Este proyecto está realizado por: \nCalbet González, Mª Victoria\nRamos Castro, Eva\nPara la asignatura de Inteligencia Artificial - Problema del buscaminas")


def setCustomSize():
    global customsizes
    r = tkinter.simpledialog.askinteger("Número de filas", "Introduzca la cantidad de filas")
    c = tkinter.simpledialog.askinteger("Número de columnas", "Introduzca la cantidad de columnas")
    m = tkinter.simpledialog.askinteger("Número de minas", "Introduzca el número de minas")
    while m > r * c:
        m = tkinter.simpledialog.askinteger("Número de minas",
                                            "El número máximo de minas para esta dimensión es " + str(
                                                r * c) + "\nIntroduzca el número de minas")
    customsizes.insert(0, (r, c, m))
    customsizes = customsizes[0:5]
    setSize(r, c, m)
    createMenu()


def setSize(r, c, m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    saveConfig()
    restartGame()


def saveConfig():
    global rows, cols, mines
    # configuration
    config = configparser.SafeConfigParser()
    config.add_section("juego")
    config.set("juego", "filas", str(rows))
    config.set("juego", "columnas", str(cols))
    config.set("juego", "minas", str(mines))
    config.add_section("Tamaño")
    config.set("Tamaño", "cantidad", str(min(5, len(customsizes))))
    for x in range(0, min(5, len(customsizes))):
        config.set("Tamaño", "filas" + str(x), str(customsizes[x][0]))
        config.set("Tamaño", "columnas" + str(x), str(customsizes[x][1]))
        config.set("Tamaño", "minas" + str(x), str(customsizes[x][2]))

    with open("config.ini", "w") as file:
        config.write(file)


'''def loadConfig():
    global rows, cols, mines, customsizes
    config = configparser.SafeConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append((config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)), config.getint("sizes", "mines"+str(x))))
'''


def prepareGame():
    global rows, cols, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            # add button and init value for game
            field[x].append(0)
    # generate mines
    for _ in range(0, mines):
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        # prevent spawning mine on top of each other
        while field[x][y] == -1:
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)
        field[x][y] = -1
        if x != 0:
            if y != 0:
                if field[x - 1][y - 1] != -1:
                    field[x - 1][y - 1] = int(field[x - 1][y - 1]) + 1
            if field[x - 1][y] != -1:
                field[x - 1][y] = int(field[x - 1][y]) + 1
            if y != cols - 1:
                if field[x - 1][y + 1] != -1:
                    field[x - 1][y + 1] = int(field[x - 1][y + 1]) + 1
        if y != 0:
            if field[x][y - 1] != -1:
                field[x][y - 1] = int(field[x][y - 1]) + 1
        if y != cols - 1:
            if field[x][y + 1] != -1:
                field[x][y + 1] = int(field[x][y + 1]) + 1
        if x != rows - 1:
            if y != 0:
                if field[x + 1][y - 1] != -1:
                    field[x + 1][y - 1] = int(field[x + 1][y - 1]) + 1
            if field[x + 1][y] != -1:
                field[x + 1][y] = int(field[x + 1][y]) + 1
            if y != cols - 1:
                if field[x + 1][y + 1] != -1:
                    field[x + 1][y + 1] = int(field[x + 1][y + 1]) + 1


def prepareWindow():
    global rows, cols, buttons
    tkinter.Button(window, text="Restart", command=restartGame).grid(row=0, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(window, text=" ", width=2, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

def restartGame():
    global gameover
    gameover = False
    # destroy all - prevent memory leak
    for x in window.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    prepareWindow()
    prepareGame()


def clickOn(x, y):
    global field, buttons, colors, gameover, rows, cols
    if gameover:
        return
    buttons[x][y]["text"] = str(field[x][y])
    if field[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        tkinter.messagebox.showinfo("Fin del juego", "Has perdido.")
        # now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[_x][_y]["text"] = "*"
    else:
        buttons[x][y].config(disabledforeground=colors[field[x][y]])
    if field[x][y] == 0:
        buttons[x][y]["text"] = " "
        # now repeat for all buttons nearby which are 0... kek
        autoClickOn(x, y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()


def autoClickOn(x, y):
    global field, buttons, colors, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return
    if field[x][y] != 0:
        buttons[x][y]["text"] = str(field[x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground=colors[field[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if field[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x - 1, y - 1)
        if x != 0:
            autoClickOn(x - 1, y)
        if x != 0 and y != cols - 1:
            autoClickOn(x - 1, y + 1)
        if y != 0:
            autoClickOn(x, y - 1)
        if y != cols - 1:
            autoClickOn(x, y + 1)
        if x != rows - 1 and y != 0:
            autoClickOn(x + 1, y - 1)
        if x != rows - 1:
            autoClickOn(x + 1, y)
        if x != rows - 1 and y != cols - 1:
            autoClickOn(x + 1, y + 1)


def onRightClick(x, y):
    global buttons
    if gameover:
        return
    if buttons[x][y]["text"] == "?":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "?"
        buttons[x][y]["state"] = "disabled"


def checkWin():
    global buttons, field, rows, cols
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        tkinter.messagebox.showinfo("Fin del juego", "Has ganado.")


'''
if !os.path.exists("config.ini"):
    loadConfig()
else:
    saveConfig()'''

createMenu()

prepareWindow()
prepareGame()
window.mainloop()
