import pygame 
import sys #salirnos cuando agamos clic en salir 
import math #acceso a funciones matematicas 
import time #permite cronometrar un intervalo de tiempo
import random #mesclar las tarjetas 
#iniciamos todo lo de Pygame para poder usar sonido, pantalla, etc.

pygame.init() # sirve para garantizar que todos los módulos que importemos de Pygame se inicialicen de manera correcta
pygame.font.init() #se utiliza para comprobar si el módulo de fuentes de Pygame ha sido incializado. 
pygame.mixer.init() #poder reproducir sonidos 

#Variables y configuracion que vamos a usar a lo largo del programa

altura_boton= 40 #el boton d abajo, para iniciar el juego
medida_cuadro= 180 #medida de la imagen en pixeles
 
nombre_imagen_oculta="imagenes/pregunta(1)(1).png"
imagen_oculta=pygame.image.load(nombre_imagen_oculta)#se utiliza para subir nuevas imágenes de un documento externo al programa
segundo_mostrar_pieza= 2 #segundos para ocultar la pieza si no es correcta

"""
Una clase que representa el cuadro. El mismo tiene una imagen y puede estar
descubierto (cuando ya lo han descubierto anteriormente y no es la tarjeta buscada actualmente)
o puede estar mostrado (cuando se voltea la imagen)
También tiene una fuente o nombre de imagen que servirá para compararlo más tarde
"""


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        """
        Una cosa es la fuente de la imagen (es decir, el nombre del archivo) y otra
        la imagen lista para ser pintada por PyGame
        La fuente la necesitamos para más tarde, comparar las tarjetas
        """
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)

"""todo el juego; que al final es un arreglo de objetos"""

#Esto es un arreglo es un tipo de variable especial que puede alojar dentro de sí varios valores al mismo tiempo.
cuadros = [
    [Cuadro("imagenes/coco(1)(1).png"), Cuadro("imagenes/coco(1)(1).png"),
     Cuadro("imagenes/manzana(1)(1).png"), Cuadro("imagenes/manzana(1)(1).png")],
    [Cuadro("imagenes/limon(1)(1).png"),Cuadro("imagenes/limon(1)(1).png"),
     Cuadro("imagenes/naranja(1)(1).png"), Cuadro("imagenes/naranja(1)(1).png")],
    [Cuadro("imagenes/pera(1)(1).png"), Cuadro("imagenes/pera(1)(1).png"),
     Cuadro("imagenes/pina(1)(1).png"), Cuadro("imagenes/pina(1)(1).png")],
    [Cuadro("imagenes/platano(1)(1).png"), Cuadro("imagenes/platano(1)(1).png"),
     Cuadro("imagenes/sandia(1)(1).png"), Cuadro("imagenes/sandia(1)(1).png")],
]        


#colores 
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)

# Los sonidos
sonido_fondo = pygame.mixer.Sound("sonidos/fondo.wav")
sonido_clic = pygame.mixer.Sound("sonidos/clic.wav")
sonido_exito = pygame.mixer.Sound("sonidos/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("sonidos/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("sonidos/voltear.wav")

# Calculamos el tamaño de la pantalla en base al tamaño de los cuadrados
anchura_pantalla =700   #(len(cuadros[0]) * medida_cuadro)
altura_pantalla =700   #(len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla

# La fuente que estará sobre el botón
tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

# El botón, que al final es un rectángulo
boton = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)

# Banderas
# Bandera para saber si se debe ocultar la tarjeta dentro de N segundos
ultimos_segundos = None
puede_jugar = True  # Bandera para saber si reaccionar a los eventos del usuario
# Saber si el juego está iniciado; así sabemos si ocultar o mostrar piezas, además del botón
juego_iniciado = False
# Banderas de las tarjetas cuando se busca una pareja. Las necesitamos como índices para el arreglo de cuadros
# x1 con y1 sirven para la primer tarjeta
x1 = None
y1 = None
# Y las siguientes para la segunda tarjeta
x2 = None
y2 = None

"""
Funciones útiles
"""


# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros(): #calcula la cantidad de filas y de columnas
    # Elegir X e Y aleatorios, intercambiar
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):#recorre desde cero las filas
        for x in range(cantidad_columnas):#recorre desde cero las columnas
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()


# Regresa False si al menos un cuadro NO está descubierto. True en caso de que absolutamente todos estén descubiertos
def gana():#recorre cada cuadro de cada fila y cada fila de cada cuadro
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True


"""
Iniciamos la pantalla con las medidas previamente calculadas, colocamos título y
reproducimos el sonido de fondo
"""
pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memorama en Python - By Parzibyte')
pygame.mixer.Sound.play(sonido_fondo, -1)  # El -1 indica un loop infinito
# Ciclo infinito...
while True:
    # Escuchar eventos, pues estamos en un ciclo infinito que se repite varias veces por segundo
    for event in pygame.event.get():# utilizamos los eventos de pygame
        # Si quitan el juego, salimos
        if event.type == pygame.QUIT:
            sys.exit()
        # Si hicieron clic y el usuario puede jugar...
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            """
            xAbsoluto e yAbsoluto son las coordenadas de la pantalla en donde se hizo
            clic. PyGame no ofrece detección de clic en imagen, por ejemplo. Así que
            se deben hacer ciertos trucos
            """
            # Si el click fue sobre el botón y el juego no se ha iniciado, entonces iniciamos el juego
            xAbsoluto, yAbsoluto = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                """
                Ahora necesitamos a X e Y como índices del arreglo. Los índices no
                son lo mismo que los pixeles, pero sabemos que las imágenes están en un arreglo
                y por lo tanto podemos dividir las coordenadas entre la medida de cada cuadro, redondeando
                hacia abajo, para obtener el índice.
                Por ejemplo, si la medida del cuadro es 100, y el clic es en 140 entonces sabemos que le dieron
                a la segunda imagen porque 140 / 100 es 1.4 y redondeado hacia abajo es 1 (la segunda posición del
                arreglo) lo cual es correcto. Por poner otro ejemplo, si el clic fue en la X 50, al dividir da 0.5 y
                resulta en el índice 0
                """
                x = math.floor(xAbsoluto / medida_cuadro)
                y = math.floor(yAbsoluto / medida_cuadro)
                # Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    # continue ignora lo de abajo y deja que el ciclo siga
                    continue
                # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas
                # están descubriendo la primera)
                if x1 is None and y1 is None:
                    # Entonces la actual es en la que acaban de dar clic, la mostramos
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(sonido_voltear)
                else:
                    # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    # Si coinciden, entonces a ambas las ponemos en descubiertas:
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sonido_clic)
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        # Si no coinciden, tenemos que ocultarlas en el plazo de [segundos_mostrar_pieza] segundo(s). Así que establecemos
                        # la bandera. Como esto es un ciclo infinito y asíncrono, podemos usar el tiempo para saber
                        # cuándo fue el tiempo en el que se empezó a ocultar
                        ultimos_segundos = int(time.time())
                        # Hasta que el tiempo se cumpla, el usuario no puede jugar
                        puede_jugar = False
                comprobar_si_gana()

    ahora = int(time.time())
    # Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
    # en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
    # se ocultan las dos tarjetas y se reinician las banderas
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundo_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
        puede_jugar = True

    # Hacer toda la pantalla blanca
    pantalla_juego.fill(color_blanco)
    # Banderas para saber en dónde dibujar las imágenes, pues al final
    # la pantalla de PyGame son solo un montón de pixeles
    x = 0
    y = 0
    # Recorrer los cuadros
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            """
            Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
            dibujamos la imagen oculta
            """
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    # También dibujamos el botón
    if juego_iniciado:
        # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_blanco), (xFuente, yFuente))

    # Actualizamos la pantalla
    pygame.display.update()


