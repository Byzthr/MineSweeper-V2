from Buscaminas_V2 import Procesador, VentanaBuscaminas, VentanaDificultad

def main():

    ventana_dificultad = VentanaDificultad()
    ventana_juego = Procesador(ventana_dificultad.dificultad)


    return 0;

if __name__=='__main__':

    main()