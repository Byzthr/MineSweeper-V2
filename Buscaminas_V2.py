import tkinter as tk
import tkinter.messagebox as mbox
import numpy as np
from PIL import ImageTk, Image



class Procesador():

    """
    Motor algebraico del buscaminas.

    """

    def __init__(self, dificultad):

        """
        Se define la dificultad del juego, las dimensions de las matrices y el número inicial de bombas a partir del argumento.
        Se definen las matrices de minas, mostradas y marcas, en blanco.
        Se definen aleatoriamente las coordenadas de las bombas y se colocan en la matriz de minas.
        Se obtiene el número de bombas y sus coordenadas. Se definen el número de movimientos, el de marcas correctas y el de marcas como 0.
        Se define la ventana de la interfaz gráfica y se inicia el loop.

        """

        self.dificultad = dificultad
        self.fin_bueno = False
        self.fin_malo = False

        self.sizex = dificultad*8
        self.sizey = dificultad*6
        self.nbombas_inicial = dificultad**2*10

        self.Mbombas = np.zeros((self.sizey,self.sizex), dtype=bool)
        self.Munlock = np.zeros((self.sizey,self.sizex), dtype=bool)
        self.Mmarcas = np.zeros((self.sizey,self.sizex), dtype=bool)

        self.coords_bombas_inicial_x = np.random.randint(0, self.sizex, self.nbombas_inicial)
        self.coords_bombas_inicial_y = np.random.randint(0, self.sizey, self.nbombas_inicial)

        for i, j in zip(self.coords_bombas_inicial_y, self.coords_bombas_inicial_x):
            self.Mbombas[i,j] = True

        self.movimientos = 0
        self.banderas = 0
        self.banderas_colocadas = 0

        self.ventana = VentanaBuscaminas(40, self.sizex, self.sizey, self)

        self.ventana.mainloop()

    def primer_movimiento(self, x, y):

        """
        Fuerza al juego para que no haya bombas en el entorno del movimiento.
        A continuación define la matriz de entornos llamando a la función matriz_numero().
        Finalmente llama a la función movimiento().

        """

        if x==0 and y==0:
            self.Mbombas[y:y+2,x:x+2] = False
        elif x==0:
            self.Mbombas[y-1:y+2,x:x+2] = False
        elif y==0:
            self.Mbombas[y:y+2,x-1:x+2] = 0
        else:
            self.Mbombas[y-1:y+2,x-1:x+2] = 0

        self.coords_bombas = np.where(self.Mbombas)
        self.nbombas = len(self.coords_bombas[0])

        self.Mnumero = self.matriz_numero()

        # self.runing = True

        self.movimiento(x,y)

    def matriz_numero(self):

        """
        Genera la matriz de entornos contando las casillas mina del entorno de cada casilla.
        Posteriormente, a las casillas mina se les asigna el número 10.

        """

        Mnumero = np.zeros((self.sizey,self.sizex), dtype=int)

        for i in range(self.sizey):
            for j in range(self.sizex):
                if i==0 and j==0:
                    n = len(np.where(self.Mbombas[i:i+2,j:j+2])[0])
                elif i==0:
                    n = len(np.where(self.Mbombas[i:i+2,j-1:j+2])[0])
                elif j==0:
                    n = len(np.where(self.Mbombas[i-1:i+2,j:j+2])[0])
                else:
                    n = len(np.where(self.Mbombas[i-1:i+2,j-1:j+2])[0])
                Mnumero[i,j] = n
                if self.Mbombas[i,j]:
                    Mnumero[i,j]=10

        return Mnumero

    def movimiento(self, x, y):

        """
        Recibe las coordenadas de la casilla inicada y lo manifiesta en la
        matriz de casillas desbloqueadas.
        En caso de ser una casilla libre llama a la función blanqueo().
        En caso de ser una casilla mina llama a la función fallo().
        Añade uno a la cuenta de movimientos.
        [En caso de que las casillas desbloqueadas sean iguales al número de
        casillas menos el número de bombas o las marcas reales ean iguales al
        número de bombas (pass)]

        """

        self.Munlock[y,x] = True

        if self.Mnumero[y,x]==0:
            self.blanqueo()

        elif self.Mbombas[y,x]:
            self.fallo()

        self.movimientos += 1

        if self.sizey*self.sizex-self.nbombas == len(np.where(self.Munlock)[0]):

            # self.runing = False
            self.fin_bueno = True

        if (self.banderas==self.nbombas and self.banderas==self.banderas_colocadas):

            # self.runing = False
            self.fin_bueno = True

    def blanqueo(self):

        """
        Recorre la matriz número buscando casillas blancas y desbloqueando su
        alrededor.

        """

        for it in range(10):
            for i in range(self.sizey):
                for j in range(self.sizex):
                    if self.Mnumero[i,j] == 0:
                        if i==0 and j==0:
                            n = len(np.where((self.Munlock[i:i+2,j:j+2] == True) & (self.Mnumero[i:i+2,j:j+2] == 0))[0])
                            # print("i,j={},{} \t n= {}, ".format(i,j, n))
                        elif i==0:
                            n = len(np.where((self.Munlock[i:i+2,j-1:j+2] == True) & (self.Mnumero[i:i+2,j-1:j+2] == 0))[0])
                            # print("i,j={},{} \t n= {}, ".format(i,j, n))
                        elif j==0:
                            n = len(np.where((self.Munlock[i-1:i+2,j:j+2] == True) & (self.Mnumero[i-1:i+2,j:j+2] == 0))[0])
                            # print("i,j={},{} \t n= {}, ".format(i,j, n))
                        else:
                            n = len(np.where((self.Munlock[i-1:i+2,j-1:j+2] == True) & (self.Mnumero[i-1:i+2,j-1:j+2] == 0))[0])
                            # print("i,j={},{} \t n= {}, ".format(i,j, n))
                        
                        if n!=0:
                            self.Munlock[i,j] = True
                            if i==0 and j==0:
                                self.Munlock[i:i+2,j:j+1] = True
                            elif j==0:
                                self.Munlock[i-1:i+2,j:j+2] = True
                            elif i==0:
                                self.Munlock[i:i+2,j-1:j+2] = True
                            elif i>0 and j>0:
                                self.Munlock[i-1:i+2,j-1:j+2] = True
                            else:
                                print("Algo raro en blanqueo()")

    def marca(self, x, y):

        """
        Conmuta el elemento de la matriz marcas con las coordenadas recibidas,
        en caso de ser la coordenada de una casilla bomba lo a ñade a la cuenta
        de banteras.

        """

        self.Mmarcas[y, x] = not self.Mmarcas[y, x]

        if self.Mmarcas[y, x]:
            self.banderas_colocadas += 1
        else:
            self.banderas_colocadas -= 1

        if self.Mbombas[y, x]:
            if self.Mmarcas[y, x]:
                self.banderas += 1
            else:
                self.banderas -= 1

    def fallo(self):

        # self.runing = False

        for i, j in zip(self.coords_bombas[0], self.coords_bombas[1]):
            self.Munlock[i,j] = True

        self.fin_malo = True


class VentanaDificultad(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Buscaminas - Dificultad")
        self.iconbitmap("mine_icon.ico")

        texto_dificultad = tk.Label(self, text="Seleccione nivel de dificultad:", padx=10, pady=10)
        texto_dificultad.pack()

        frame_dificultad = tk.Frame(master=self)
        frame_dificultad.pack(padx=40, pady=20)

        self.init_botones(frame_dificultad)

    def init_botones(self, frame_dificultad):

        boton_facil = tk.Button(
            master = frame_dificultad,
            text = "Fácil",
            width = 30,
            command = lambda: self.selector(1)
        )
        boton_intermedio = tk.Button(
            master=frame_dificultad,
            text="Intermedio",
            width=30,
            command=lambda: self.selector(2)
        )
        boton_dificil = tk.Button(
            master=frame_dificultad,
            text="Difícil",
            width=30,
            command=lambda: self.selector(3)
        )
        boton_extremo = tk.Button(
            master=frame_dificultad,
            text="Extremo",
            width=30,
            command=lambda: self.selector(4)
        )
        boton_facil.pack()
        boton_intermedio.pack()
        boton_dificil.pack()
        boton_extremo.pack()

        self.mainloop()

    def selector(self, dif):
        self.dificultad = dif
        self.destroy()


class VentanaBuscaminas(tk.Tk):
    
    def __init__(self, size_ventana, sizex, sizey, partida):
        
        super().__init__()

        # Prearación de las imagenes utlizadas en el juego --------------------------------------------------------------

        self.icono_image = Image.open('mine_icon.ico')
        self.icono_image = self.icono_image.resize((20,20), Image.ANTIALIAS)
        self.icono = ImageTk.PhotoImage(self.icono_image)

        self.flag_image = Image.open('Flag.png')
        self.flag_image = self.flag_image.resize((20, 20), Image.ANTIALIAS)
        self.flag = ImageTk.PhotoImage(self.flag_image)

        # Definición de mecanismo de parada, los parámetros de entrada y el diccionariode colores -----------------------

        self.stop = False

        self.partida = partida
        self.sizex = sizex
        self.sizey = sizey

        self.color_dict = {
            1: 'deep sky blue',
            2: 'green2',
            3: 'yellow3',
            4: 'tan1',
            5: 'red2',
            6: 'red4',
            7: 'maroon4',
            8: 'black'
        }

        # Configuración de la ventana ---------------------------------------------------------------------------------

        self.title("Busca Minas")
        self.iconbitmap("mine_icon.ico")
        # self.resizable(False, False)
        self.config(bg='grey82')

        # Creación de la barra menú --------------------------------------------------------------------------------------

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.menu_opciones = tk.Menu(self.menu, tearoff=0)
        self.menu_juego = tk.Menu(self.menu, tearoff=0)
        self.menu_ayuda = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label='Opciones', menu=self.menu_opciones)
        self.menu.add_cascade(label='Juego', menu=self.menu_juego)
        self.menu.add_cascade(label='Ayuda', menu=self.menu_ayuda)

        # self.menu_juego.add_command(label='Eliminar todas las marcas', command=self.limpiar_marcas)
        self.menu_juego.add_command(label='Reiniciar', command=lambda: self.reiniciar(self.partida.dificultad))
        self.cascada_dificultad = tk.Menu(self.menu_juego, tearoff=0)
        self.menu_juego.add_cascade(label='Dificultad', menu=self.cascada_dificultad)
        self.cascada_dificultad.add_command(label='Fácil', command= lambda: self.reiniciar(1))
        self.cascada_dificultad.add_command(label='Intermedio', command= lambda: self.reiniciar(2))
        self.cascada_dificultad.add_command(label='Difícil', command= lambda: self.reiniciar(3))
        self.cascada_dificultad.add_command(label='Extremo', command= lambda: self.reiniciar(4))

        self.menu_opciones.add_command(label='Talón de campeones', command=self.marcadores)
        self.menu_opciones.add_command(label='Idioma', command=self.idioma)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label='Cerrar', command=self.cerrar)

        self.menu_ayuda.add_command(label='Acerca de', command=self.info)
        self.menu_ayuda.add_command(label='Instrucciones', command=self.instrucciones)


        # Título del frame principal ----------------------------------------------------------------------------------

        self.frame_titulo = tk.Frame(self, bg = 'grey82')
        self.frame_titulo.pack(
            padx = 30,
            pady = 10,
            side = 'top'
        )

        self.bombas_restantes = tk.Label(
			master = self.frame_titulo,
            text = str('GO'),
			bg = "grey82",
			font = (30*np.sqrt(self.partida.dificultad))
		)
        self.bombas_restantes_icono = tk.Label(
            master = self.frame_titulo,
            image=self.icono,
            bg="grey82"
        )
        self.bombas_restantes.grid(row=0, column=0)
        self.bombas_restantes_icono.grid(row=0, column=1)

        # Grid ---------------------------------------------------------------------------------------------------------

        self.grid = tk.Frame(
			master = self,
			width = sizex*size_ventana,
			height = sizey*size_ventana
		)
        self.grid.grid_propagate(False)
        self.grid.columnconfigure(tuple(range(sizex)), weight=1, uniform='column')
        self.grid.rowconfigure(tuple(range(sizey)), weight=1, uniform='row')
        self.grid.pack(padx=50, pady=50, side='bottom')

        self.Mbotones = []
        self.Mbanderas = []
        for i in range(sizey):
            self.Mbotones.append([])
            self.Mbanderas.append([])
            for j in range(sizex):
                but = tk.Button(self.grid, bd=5)
                but.bind('<Button-1>', lambda event, row=i, column=j: self.left_click(event, row, column))
                but.bind('<Button-3>', lambda event, row=i, column=j: self.right_click(event, row, column))
                self.Mbotones[i].append(but)
                band = tk.Label(self.grid, image=self.flag, relief='raised', bd=5)
                band.bind('<Button-3>', lambda event, row=i, column=j: self.right_click(event, row, column))
                self.Mbanderas[i].append(band)

                self.Mbotones[i][j].grid(row=i, column=j, stick='news')


    def matriz_inferior(self):

        self.Mmostrado = []
        for i in range(self.sizey):
            self.Mmostrado.append([])
            for j in range(self.sizex):
                if self.partida.Mnumero[i,j] == 0:
                    self.Mmostrado[i].append(
                        tk.Label(
                            master = self.grid,
                            relief = 'ridge',
                        )
                    )

                elif self.partida.Mbombas[i,j]:
                    self.Mmostrado[i].append(
                        tk.Label(
                            master = self.grid,
                            image = self.icono,
                            relief = 'ridge'
                        )
                    )

                else:
                    self.Mmostrado[i].append(
                        tk.Label(
                            master = self.grid,
                            text = self.partida.Mnumero[i,j],
                            fg = self.color_dict[self.partida.Mnumero[i,j]],
                            font =  ('bold'),
                            relief = 'ridge'
                        )
                    )


    def left_click(self, event, y, x):

        # if self.partida.Mmarcas[y, x]:
        #     pass

        if not self.stop and self.partida.movimientos == 0:
            self.partida.primer_movimiento(x,y)
            self.matriz_inferior()
            self.bombas_restantes.config(text = str(self.partida.nbombas))

        elif not self.stop:
            self.partida.movimiento(x,y)
        
        self.coords_unlock = np.where(self.partida.Munlock)
        for i, j in zip(self.coords_unlock[0], self.coords_unlock[1]):
            if not self.partida.Mmarcas[i, j]:
                self.Mbotones[i][j].grid_forget()
                self.Mmostrado[i][j].grid(row=i, column=j, stick='news')

        if self.partida.fin_malo and not self.stop:

            self.stop = True
            self.game_over()

        elif self.partida.fin_bueno and not self.stop:

            self.stop = True
            self.victoria()


    def right_click(self, event, y, x):

        """
        Llama a la función Procesador.marca() y coloca una banderilla en las coordenadas que recibe.

        """

        self.partida.marca(x, y)

        if self.partida.Mmarcas[y, x]:
            self.Mbotones[y][x].grid_forget()
            self.Mbanderas[y][x].grid(row=y, column=x, stick='news')

        else:
            self.Mbanderas[y][x].grid_forget()
            self.Mbotones[y][x].grid(row=y, column=x, stick='news')

        if self.partida.nbombas >= self.partida.banderas_colocadas:
            self.bombas_restantes.config(text=self.partida.nbombas-self.partida.banderas_colocadas)


    def limpiar_marcas(self):

        self.partida.Mmarcas[:,:] = False

        self.partida.banderas = 0


    def game_over(self):

        box = mbox.askyesnocancel("Peldite", 'PELDITE REY \n \n¿Jugar de nuevo? \n \n"Yes" para reiniciar, "No" para cerrar')
        print(box)
        if box:
            self.reiniciar(self.partida.dificultad)

        elif box==None:
            pass

        else:
            self.cerrar()


    def victoria(self):
        ventana_victoria = VentanaVictoria(self.partida.dificultad)
        ventana_victoria.mainloop()


    def reiniciar(self, dificultad):

        self.destroy()
        self.partida = Procesador(dificultad)


    def info(self):
        mbox.showinfo(
            'Acerca de Buscaminas-V2',
            'Juego creado por Byzthr para el disfrute de sus panitas y el propio crecimiento personal. \n'
            'Creado con python y con mucho amor.')


    def instrucciones(self):
        mbox.showinfo(
            'Instrucciones',
            # 'Me cuesta creer que hagan falta pero aquí tan: \n'
            '- Pulsa en una casilla para cavar. \n'
            '- El número de la casilla indica el número de minas que hay en las 8 casillas de su alrededor. \n'
            '- Si pulsas en una casilla con una mina habrás perdido. \n'
            '- Utiliza el botón derecho para colocar banderillas donde pcreas que hay una bomba. \n'
            '- El número de arriba indica las bombas que supuestamente te quedan por marcar con una banderilla. \n'
            '- Si consigues poner una banderilla encima de todas las bombas correctamente o pulsas todas las casillas sin mina habrás ganado.'

        )


    def marcadores(self):

        file = open('Jugadores-'+str(self.partida.dificultad)+'.txt', 'r')
        jogos=''
        cont = 0
        try:
            for line in file.readlines(100):
                jogos = jogos+line

            mbox.showinfo('Marcadores', jogos)

        except:
            mbox.showinfo('Marcadores', 'No hay registros')

        finally:
            file.close()


    def idioma(self):

        mbox.showinfo('Idioma', 'Tas loco si crees que voy a traducir todo')


    def cerrar(self):

        if mbox.askyesno('Cerrar', '¿Desea cerrar la aplicación?'):
            self.destroy()


class VentanaVictoria(tk.Tk):

    def __init__(self, dif):

        super().__init__()

        self.iconbitmap("mine_icon.ico")

        self.dificultad = dif

        self.congratulacion = tk.Label(
            master = self,
            text = "FELICIDADES, introduce tu nombre para los anales:",
            # bg = "grey",
            padx = 30,
            pady = 30
        )
        self.congratulacion.pack()

        self.nombre = tk.StringVar()

        self.cuadro_texto = tk.Entry(self, textvariable=self.nombre)
        self.cuadro_texto.pack()

        self.boton = tk.Button(self, text="Submit", command=self.guardar_nombre)
        self.boton.pack()


    def guardar_nombre(self):
        nombre_str = self.nombre.get()
        Nombres = open("Jugadores-"+str(self.dificultad)+'.txt',"a")
        print(nombre_str)
        Nombres.write(nombre_str + "\n")
        Nombres.close()
        self.nombre.set("")
        self.destroy()
        return
