import probBuscaminas
import tkinter
import tkinter.messagebox
import tkinter.simpledialog

# Declaración de la ventana principal, en esta se irán añadiendo las distintas celdas necesarias para el problema
window = tkinter.Tk()

# Se indica el título que tendrá la ventana principal y el tamaño de la misma
window.title("Probabilidad buscaminas")
window.geometry("380x400")

# Barra de menu y los mensajes que contienen
def menu():
    menuB = tkinter.Menu(window)

    # Menu de instrucciones
    menuinstr = tkinter.Menu(window, tearoff=0)
    menuinstr.add_command(label="Cómo rellenar la tabla de evidencias", command=add)
    menuinstr.add_command(label="Cómo modificar la tabla de evidencias", command=update)
    menuinstr.add_command(label="Cómo eliminar la tabla de evidencias", command=delete)
    menuB.add_cascade(label="Instrucciones", menu=menuinstr)

    # Menu de informacion del trabajo
    menuinfo = tkinter.Menu(window, tearoff=0)
    menuinfo.add_command(label="Acerca de...", command=nosotras)
    menuB.add_cascade(label="Trabajo IA", menu=menuinfo)
    window.config(menu=menuB)


def nosotras():
    tkinter.messagebox.showinfo("Acerca de...",
                                "Este proyecto está realizado por: \n\nCalbet González, Mª Victoria\nRamos Castro, "
                                "Eva\n\nAsignatura: Inteligencia Artificial\n"
                                "Tutor del problema: Francisco J. Martín Mateos\nGrado en Ingeniería Informática de "
                                "Software (2017/18)\nUniversidad de Sevilla")


def add():
    tkinter.messagebox.showinfo("Añade una evidencia", "Para añadir una evidencia, habrá que hacerlo una a una, "
                                                       "introduciendo los siguientes datos: \n - Nodo: será aquella "
                                                       "casilla vacía, aún sin descubrir. \n - Número de casillas a su "
                                                       "alrededor: será la cantidad de casillas reveladas que sean "
                                                       "colindantes del nodo que se ha introducido. \n - Suma de "
                                                       "casillas vecinas: será el total de la suma de la información "
                                                       "que contengan las casillas colindantes.\n\nHay que tener en"
                                                       " cuenta, que si tenemos n filas y m columnas, los nodos irán"
                                                       "desde 0,0 hasta 0,m-1 [en horizontal]; desde 0,0 hasta n-1,0"
                                                       " [en vertical]; desde 0,0 hasta n-1,m-1 [en diagonal].\nPor lo "
                                                       "tanto, una matriz 5x5, tiene sin descubrir la casilla o nodo"
                                                       " 0,0 con 2 casillas descubiertas a su alrededor, que cada una"
                                                       " tiene un 1 y un 2 en su interior, se añadiría de la siguiente"
                                                       " forma:\n- Nodo: 0,0\n- Número de casillas: 2\n- Suma vecinos: "
                                                       "3.\nFinalmente se hace click en 'Añadir evidencia'.\n\nSe "
                                                       "entiende, que cada vez que se ofrece una sugerencia de casilla"
                                                       " y no se ha finalizado el juego, se debe borrar la casilla "
                                                       "sugerida de la lista de evidencias y realizar la modificación "
                                                       "de las casillas que se han visto afectadas por descubrir la "
                                                       "casilla sugerida.\n\nUna vez ganada o perdida una partida, se"
                                                       " hará click en 'He terminado el juego. Finalizar'")


def update():
    tkinter.messagebox.showinfo("Actualiza una evidencia", "Para actualizar una evidencia, habrá que volver a escribir"
                                                           " el nodo, número de casillas descubiertas y la suma de "
                                                           "vecinos del nodo que queremos cambiar.\nLuego se "
                                                           "seleccionará en la lista de las evidencias y se hará click"
                                                           " en 'Actualizar evidencia'.\nEs muy importante recordar que"
                                                           " para modificar la evidencia se ha de clickear sobre ella,"
                                                           " sino los cambios no se aplicarán.")


def delete():
    tkinter.messagebox.showinfo("Borra una evidencia", "Para borrar una evidencia, habrá que seleccionarla en la lista"
                                                       " de evidencias y hacer click en 'Borrar evidencia'.")


# Se declara el tamaño personalizado que demos para crear nuestro grafo, más adelante explicaremos su significado y uso
customsizes = []

# Declararemos a las siguientes variables el tipo que son. Si se indica IntVar() será de tipo int y si es StringVar(),
# de tipo String

filas = tkinter.IntVar()
columnas = tkinter.IntVar()
minas = tkinter.IntVar()
varNodo = tkinter.StringVar()
evidencia = tkinter.IntVar()
suma_vecinos = tkinter.IntVar()

# Si la lista anteriormente creada, su tamaño es igual a 0, mostraremos un pequeño formulario, dónde tenemos que
# ingresar las filas, columnas y minas que tendrá nuestro juego del buscaminas
if len(customsizes) == 0:
    '''
    El método "Label" nos permite añadir la etiqueta, el nombre que nos hace referencia y nos indicará qué representa cada
    una de las cajas a su lado.
    
    El método "Entry" nos permite introducir un elemento que se asociará a la variable anteriormente declarada, solamente
    del tipo que sea exactamente. Es un equivalente a "input()" para la ejecución en consola.
    '''
etiquetaF = tkinter.Label(window, text="Número de filas").place(x=50, y=50)
cajaF = tkinter.Entry(window, textvariable=filas).place(x=180, y=50)

etiquetaC = tkinter.Label(window, text="Número de columnas").place(x=50, y=80)
cajaC = tkinter.Entry(window, textvariable=columnas).place(x=180, y=80)

etiquetaM = tkinter.Label(window, text="Número de minas").place(x=50, y=110)
cajaM = tkinter.Entry(window, textvariable=minas).place(x=180, y=110)


'''
Este método se ejecutará una vez que se clickee sobre la casilla "siguiente" en la interfaz, en ella se introducirán los
datos correspondientes al nodo y al número de casillas descubiertas alrededor del nodo que queramos averiguar, para así 
poder obtener la probabilidad.
'''


def siguiente():
    # Se declara la nueva ventana donde se encontrará en nuevo formulario para la resolución del problema.
    # Con el método "Toplevel(window)", indicamos que la nueva ventana será hija de la principal.

    if not filas.get() or not columnas.get() or not minas.get():
        tkinter.messagebox.askretrycancel("Error", "No se puede ejecutar la acción.")
    else:

        ventana_evidencias = tkinter.Toplevel(window)
        ventana_evidencias.title("Introducir evidencias")  # Nombre de la nueva ventana
        ventana_evidencias.geometry("600x420")  # Tamaño de la nueva ventana
        '''
        Permite minimizar la ventana anterior, la principal, dónde hemos introducido el tamaño y el 
        número de minas de nuestro buscaminas 
        '''
        window.iconify()

        menuB = tkinter.Menu(window)

        # Menu de instrucciones
        menuinstr = tkinter.Menu(ventana_evidencias, tearoff=0)
        menuinstr.add_command(label="Cómo rellenar la tabla de evidencias", command=add)
        menuinstr.add_command(label="Cómo modificar la tabla de evidencias", command=update)
        menuinstr.add_command(label="Cómo eliminar la tabla de evidencias", command=delete)
        menuB.add_cascade(label="Instrucciones", menu=menuinstr)

        # Menu de informacion del trabajo
        menuinfo = tkinter.Menu(ventana_evidencias, tearoff=0)
        menuinfo.add_command(label="Acerca de...", command=nosotras)
        menuB.add_cascade(label="Trabajo IA", menu=menuinfo)
        ventana_evidencias.config(menu=menuB)



        global customsizes

        etiquetaN = tkinter.Label(ventana_evidencias, text="Nodo a consultar (Ej.: 1,2)").place(x=30, y=180)
        cajaN = tkinter.Entry(ventana_evidencias, textvariable=varNodo).place(x=180, y=180)

        etiquetaE = tkinter.Label(ventana_evidencias,
                                  text="Número de casillas a su alrededor con evidencia (Ej.: 1)").place(x=30, y=210)
        cajaE = tkinter.Entry(ventana_evidencias, textvariable=evidencia).place(x=330, y=210)

        etiquetaS = tkinter.Label(ventana_evidencias, text="Suma casillas de los vecinos (Ej.: 3)").place(x=30, y=240)
        cajaS = tkinter.Entry(ventana_evidencias, textvariable=suma_vecinos).place(x=220, y=240)

        # Se crea una lista, que será una caja dónde se irán almacenando las evidencias que vayamos creando.
        # tkinter.BROWSE, nos indica que sólo se podrán seleccionar las casillas de esta lista de una en una.

        # Crea una barra de desplazamiento de manera vertical en la lista en la que se añadirán las evidencias.

        yScroll = tkinter.Scrollbar(ventana_evidencias, orient=tkinter.VERTICAL)
        yScroll.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
        listaBox = tkinter.Listbox(ventana_evidencias, width=65, yscrollcommand=yScroll.set, selectmode=tkinter.BROWSE)

        listaBox.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)
        yScroll['command'] = listaBox.yview

        # Botón que llama al método añadir
        botonAñadir = tkinter.Button(ventana_evidencias, text="Añadir evidencia",
                                     command=lambda: añadir()).place(x=420, y=30)
        # Botón que llama al método borrar
        botonBorrar = tkinter.Button(ventana_evidencias, text="Borrar evidencia",
                                     command=lambda: borrar()).place(x=420, y=60)

        # Botón que llama al método actualizar
        botonActualizar = tkinter.Button(ventana_evidencias, text="Actualizar evidencia",
                                         command=lambda: actualizar()).place(x=420, y=90)

        # Botón que llama al método de mostrar datos
        botonGuardar = tkinter.Button(ventana_evidencias, text="Aceptar",
                                      command=lambda: mostrarDatos()).place(x=180, y=300)

        # Botón que llama al método de mostrar datos
        botonFinalizar = tkinter.Button(ventana_evidencias, text="He terminado el juego. Finalizar.",
                                      command=lambda: ventana_evidencias.quit()).place(x=280, y=300)

    # Método que añade a la caja de la lista de evidencias una nueva evidencia.
    def añadir():
        """
        Esta nueva evidencia se añadirá al final de la lista. Esta evidencia dependerá del valor del nodo introducido,
        el valor del número de evidencias y la suma de la información que contienen, quedando de la siguiente forma
        (por ejemplo): [(0,0), 2, 3] Puesto que ese será el formato que usaremos en nuestra resolución
        de la probabilidad
        """
        listaBox.insert(tkinter.END,
                        str([str("(") + varNodo.get() + str(")"), str(evidencia.get()), str(suma_vecinos.get())]))

    '''
     Método que borra una evidencia de la lista, para ello, se tendrá que seleccionar qué evidencia queremos borrar y
     luego borrarla
    '''

    def borrar():
        ind = listaBox.curselection()  # Devuelve una tupla con la posición del elemento seleccionado
        if listaBox.curselection() != ():  # Si está seleccionada una evidencia
            sel = ind  # Se asocia la anterior declaración a una nueva variable
            listaBox.delete(sel)  # Se borra de la lista la evidencia que tiene asociada esa posición

    '''
    Método que actualiza una evidencia de la lista. El proceso es parecido al de borrar una evidencia, se extrae
    la posición asociada de la evidencia seleccionada, se elimina de la lista y se añade con los nuevos datos que
    hemos seleccinado. Por lo que, si queremos actualizar, tendremos que añadir qué nuevos elementos queremos cambiar,
    seleccionar la evidencia que queremos modificar y clickear sobre el botón que llama a este método, "actualizar()"
    '''

    def actualizar():
        ind = listaBox.curselection()
        if listaBox.curselection() != ():
            sel = ind
            listaBox.delete(sel)
            listaBox.insert(sel,
                            str([str("(") + varNodo.get() + str(")"), str(evidencia.get()), str(suma_vecinos.get())]))

    # Método que nos mostrará los datos de la probabilidad por pantalla
    def mostrarDatos():
        # Declaramos 3 variables que se asociarán al valor introducido en la primera ventana
        f = filas
        c = columnas
        m = minas
        n = varNodo
        e = evidencia
        s = suma_vecinos
        '''
        Hacemos uso del método creado en el fichero "probBuscaminas.py" que nos crea el modelo de red bayesiana, 
        asociado al número de filas, columnas y minas que hayamos introducido en la interfaz.
        '''
        model = probBuscaminas.create_model(f.get(), c.get(), m.get())

        '''
        El resultado que devuelve la caja de la lista de evidencias, es una lista de items en formato String, por lo que
        para tratar los datos de cada uno de los items almacenados de manera más simple, crearemos una lista que vaya
        almacenando cada uno de los items, de manera que quedará [[(1, 2), 3, 4], [(2, 9), 0, 0], ...],
        en lugar de: [("['(1,2)', '3', '4']", "['(2,9)', '0', '0']"), ...]
        Luego declararemos una lista, dónde se almacenarán cada una de los items que tenga, generando una lista de 
        tuplas con todos los elementos, puesto que el método que usa las evidencias para generar la probabilidad, 
        necesita una lista con todos los nodos, casillas colindantes y total de casillas de vecinos, no una lista 
        de tuplas individuales, ni una lista de string. 
        Una vez explicado el planteamiento, iremos explicando poco a poco lo que realizaremos en el método
        '''
        listE = []  # Creo una lista dónde añadiré los items de la lista de evidencias
        evidencias = []  # Creo un diccionario que tendrá todas las claves y valores de las evidencias

        for i in range(listaBox.size()):  # Recorremos la caja de la lista de evidencias
            '''
            Asignamos a t, el item asociado a la posición de la lista, es decir, si mi lista tiene: 
            ("['(1,2)', '3', '4']", "['(2,9)', '0', '0']"), en t se almacenará el item ['(1,2)', '3', '4']
            y luego ['(2,9)', '0', '0']
            '''
            t = eval(listaBox.get(i))
            # Se añadirá a la lista creada anteriormente el valor almacenado en t, de esta forma
            # quedaría algo así: [['(1,2)', '3', '4'], ['(2,9)', '0', '0']]
            listE.append(t)

            '''
            Actualmente tenemos un resultado tal que así: ("['(1,2)', '3', '4']", "['(2,9)', '0', '0']") y queremos
            obtener el siguiente resultado: [[(1, 2), 3, 4], [(2, 9), 0, 0]]
            Por lo que para ello tendremos que construir en nuestro diccionario anteriormente declarado las claves y 
            valores asociados a los items de la lista que hemos obtenido.
            '''

        for al in range(len(listE)):  # Recorro la lista de items
            posicion = listE[al]  # Me devuelve la posición de cada uno de los items que contiene la lista
            p0 = eval(posicion[0])  # Me devuelve el item en la posición 0, casteado a una tupla
            p1 = int(posicion[1])  # Me devuelve el item en la posición 1, casteado a un int
            p2 = int(posicion[2])  # Me devuelve el item en la posición 2, casteado a un int
            evidencias.append([p0, p1, p2])  # Añado a mi lista una lista que contenga cada uno de los items
            # Formato de la evidencia que le paso al método getBox: [[(1, 2), 3, 4], [(2, 9), 0, 0]]

        # Llamo al método que nos da la probabilidad. Se le asocia el modelo creado anteriormente y la lista de
        # evidencias
        probBuscaminas.getBox(model, evidencias)

    customsizes.insert(0, (listaBox, etiquetaN, cajaN, etiquetaE, cajaE, etiquetaS, cajaS, botonAñadir
                           , botonActualizar, botonBorrar, botonGuardar, botonFinalizar))
    customsizes = customsizes[0:5]


# Botón que llama al método "siguiente()"
botonSiguiente = tkinter.Button(window, text="Siguiente",
                                command=lambda: siguiente()).place(x=180, y=260)

window.mainloop()  # Muestra la ventana principal
