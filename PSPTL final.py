#! encoding: utf-8

# ============================================================================
# =========================== MODULOS ========================================
# ============================================================================
import pygame
import random
import sys
# ============================================================================

# ============================================================================
# =========================== CONSTANTES =====================================
# ============================================================================
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
FPS = 30
VERDE = (0,200,0)
# ============================================================================
# =========================== FUNCIONES ======================================
# ============================================================================
def texto(texto, tam=20, color=(0, 0, 0)):#Esta funcion nos facilita el dibujado de caracteres en la ventana
    fuente = pygame.font.Font(None, tam)
    return fuente.render(texto, True, color)
# ============================================================================

# ============================================================================
# =========================== CLASES =========================================
# ============================================================================
class Manos(pygame.sprite.Sprite):#metodo inicializador de nuestra clase
    def __init__(self, texto, x, y):#llama al método inicializador de pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)       
        self.image = pygame.image.load("imagenes/"+ texto + ".png")
        self.rect = self.image.get_rect() #obtenemos los valores de posición y dimensiones de la imágen que 
                                          #cargamos y los almacenamos en la variable self.rect.        
        self.rect.topleft = x, y#asigna la posición que va a tener en la pantalla la imagen con los valores x e y.
        self.copia_imagen = self.image#guardo una copia de la imagen
        self.copia2_imagen = self.image
        self.tipo = texto#guardo el nombre de la imagen
        self.x = x#almaceno las coordenadas
        self.y = y
        self.factor_reduccion = 15        
    
    def obtener_imagen(self):#me regresa una copia de la imagen
        return self.copia_imagen

    def obtener_rect(self):#me regresa una copia de la variable self.rect
        return self.rect

    def tipo_mano(self):#me regresa el nombre (en formato string) de la mano
        return self.tipo 

    def presionar(self, estado):#lo que hace es que al presionar la imagen esta reduce su dimensión para dar esa 
                                #sensación de que la estamos presionando y al soltar el click o quitar el cursor 
                                #de la imagen esta vuelva a su tamaño normal. El módulo   
        if estado:            
            dim_imagen = self.rect.size[0] - self.factor_reduccion#en la variblae dim_imagen guardamos la resta entre
                                                                  #self.rect.size que obtiene el tamaño de la imagen y
                                                                  #self.factor_reduccion que este caso es 15


            if self.tipo == "tijera":
                self.copia_imagen = pygame.image.load("imagenes/tijera2.png")
            elif self.tipo == "lagarto":
                self.copia_imagen = pygame.image.load("imagenes/lagarto2.png")
            elif self.tipo == "piedra":
                self.copia_imagen = pygame.image.load("imagenes/piedra2.png")
            elif self.tipo == "papel":
                self.copia_imagen = pygame.image.load("imagenes/papel2.png")
            else:
                self.copia_imagen = pygame.image.load("imagenes/spock2.png")
           


            self.image = pygame.transform.scale(self.image, (dim_imagen, dim_imagen))#reducimos la imagen con tamaño
                                                                                     #de la resta


            #self.rect.topleft = self.x + self.factor_reduccion / 2, self.y + self.factor_reduccion / 2
        else:
            self.image = self.copia2_imagen
            self.rect.topleft = self.x, self.y


class Juego():
    def __init__(self):
        self.manos = []

        posicion_vertical = 320
        self.manos.append(Manos("piedra", 10, posicion_vertical))#agregamos la piedra en el vector self.manos
        self.manos.append(Manos("papel", 100, posicion_vertical))#agregamos el papel en el vector self.manos
        self.manos.append(Manos("tijera", 190, posicion_vertical))#agregamos la tijera en el vector self.manos 
        self.manos.append(Manos("lagarto", 370, posicion_vertical))#agregamos el lagarto en el vector self.manos 
        self.manos.append(Manos("spock", 280, posicion_vertical))#agregamos el spock en el vector self.manos    

        self.todos_los_sprites = pygame.sprite.Group(self.manos)#característica de pygame que nos permite controlar
                                                                #más fácilmente listas de objetos creados con el
                                                                #módulo pygame.sprite.Sprite

        self.jugador_escoge = ""
        self.comp_escoge = ""
        self.resultado = ""       
        self.texto_jugador = texto("Jugador", 40, BLANCO)        
        self.texto_computadora = texto("Computadora", 40, BLANCO)
        self.texto_resultado = texto("Resultado: ", 40, BLANCO)

        self.vs_imagen = pygame.image.load("imagenes/vs.png")
        self.mano_seleccionada = None
        self.jugador_imagen = None
        self.comp_imagen = None
        
        self.jugador_pos = 170
        self.comp_pos = 770

        self.puntuacion = [0, 0]  


    def copiar_imagen(self, mano_seleccionada):
        for mano in self.manos:
            if mano.tipo_mano() == mano_seleccionada:
                return pygame.transform.scale(mano.obtener_imagen(), (150, 150))  


    def obtener_manos(self):#simplemente me regresa la lista self.manos
        return self.manos

    def seleccionar(self, mano):#guarda en la variable self.mano_seleccionada la mano
                                #u objeto en la que hayamos dado un click.
        self.mano_seleccionada = mano

    def obtener_mano_seleccionada(self):#nos regresara que mano tenemos seleccionada en ese momento.
        return self.mano_seleccionada   

    def dibujar(self, pantalla):
        #dibujamos y colocamos todos los textos e imágenes que mostrará nuestro juego.
        pantalla.blit(self.texto_jugador, (185, 30))
        pantalla.blit(self.texto_resultado, (420, 470))
        pantalla.blit(self.texto_computadora, (780, 30))

        pantalla.blit(texto(str(self.puntuacion[0]), 80, BLANCO), (220, 60))
        pantalla.blit(texto(str(self.puntuacion[1]), 80, BLANCO), (850, 60))        

        if self.jugador_imagen:#esta variable la iniciamos como None por lo que la condición if la considera 
                              #como Falso y no dibujara lo que esta contenga hasta que tengamos una imagen 
                              #en la variable.                
            pantalla.blit(texto(self.resultado, 30, VERDE ), (580, 475))
            pantalla.blit(texto(self.jugador_escoge, 40, (0,0,250)), (205, 120))
            pantalla.blit(texto(self.comp_escoge, 40, (0,0,250)), (830, 120))
            pantalla.blit(self.vs_imagen, (450,130))

            pantalla.blit(self.jugador_imagen, (self.jugador_pos,150))            
            pantalla.blit(self.comp_imagen, (self.comp_pos,150))

        self.todos_los_sprites.draw(pantalla)

    def nombre_a_numero(self, nombre):    
        if   nombre == 'piedra':  return 0
        elif nombre == 'spock':   return 1
        elif nombre == 'papel':   return 2
        elif nombre == 'lagarto': return 3
        elif nombre == 'tijera': return 4
        else:
            print ('Introduce un nombre valido')    

    def numero_a_nombre(self, numero):    
        if   numero == 0: return 'piedra'
        elif numero == 1: return 'spock'
        elif numero == 2: return 'papel'
        elif numero == 3: return 'lagarto'
        elif numero == 4: return 'tijera'
        else:
            print ('Numero fuera de rango')

    def jugar(self, jugador):
        self.jugador_escoge = jugador
        self.jugador_imagen = self.copiar_imagen(jugador)
        numero_jugador = self.nombre_a_numero(jugador)

        numero_comp = random.randrange(5)         
        self.comp_escoge = self.numero_a_nombre(numero_comp)
        self.comp_imagen = self.copiar_imagen(self.comp_escoge)        

        res = (numero_jugador - numero_comp) % 5        

        if    res == 0:
            self.resultado = 'EMPATE!'
        elif  res < 3:
            self.resultado = 'GANASTE'
            self.puntuacion[0] += 1            
        elif  res > 2:
            self.resultado = 'PIERDES'
            self.puntuacion[1] += 1     

    def actualizar(self):
        if pygame.mouse.get_pressed()[0]:#detecta cuando tenemos presionado el click izquierdo
            mouse = pygame.mouse.get_pos()#guardamos en la variable mouse la posición que tiene es ese momento el mouse
            self.seleccionar(None)#llamamos al método de la clase en la que nos encontramos (Juego()) para resetear 
                                  #la variable self.mano_seleccionada (en caso de que tengamos otra mano almacenada).
            for mano in self.obtener_manos():#recorremos nuestras 5 manos
                if mano.obtener_rect().collidepoint(mouse):#lo que hace es detectar si el mouse se encuentra encima 
                                                           #de la imagen de la mano
                    mano.presionar(True)#decirle a esa mano que está siendo presionada 
                    self.seleccionar(mano)
                else:
                    mano.presionar(False)
         
# ============================================================================

# ============================================================================
# =========================== FUNCION PRINCIPAL ==============================
# ============================================================================
def main():
    pygame.init()

    posX,posY = 50,20#posicion donde ira la imagen
    posXbarco,posYbarco = 10,400
    posXmono, posYmono = 0,445

    fondo = pygame.image.load("imagenes/fondo.gif")

    ancho = 1052
    alto = 522
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Piedra-Spock-Papel-Lagarto-Tijera")
    
    juego = Juego() 

    reloj = pygame.time.Clock()

    marcha = True  

    # ============================================================================

    # ============================================================================
    # =========================== ANIMALES ==============================

    Aves = pygame.image.load("imagenes/paloma.png")
    chupahuevo1 = pygame.image.load("imagenes/chupahuevo.png")
    chupahuevo2 = pygame.image.load("imagenes/chupahuevo2.png")
    flamingo = pygame.image.load("imagenes/flamingo.png")
    flamingo2 = pygame.image.load("imagenes/flamingo2.png")
    barco = pygame.image.load("imagenes/barco.png")
    mono =  pygame.image.load("imagenes/mono.png")

    velocidad = 3
    velocidadBarco = 1
    velocidadMono = 3

    derecha = True
    bulBarco = True
    monkey = True

    # ============================================================================


    Fuente = pygame.font.Font(None,50)
    aux = 1
    j = 0
    minuto = 3
    contador = ""
    while marcha:
        # establece los frames por segundo
        reloj.tick(FPS) 

        Tiempo = pygame.time.get_ticks()/1000

        if aux == Tiempo:
            aux+=1
        # ============ INICIO MANEJADORES DE EVENTOS ====================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                marcha = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:                
                marcha = False 

            elif event.type is pygame.MOUSEBUTTONUP:
                if juego.obtener_mano_seleccionada():
                    juego.jugar(juego.obtener_mano_seleccionada().tipo_mano())

                for mano in juego.obtener_manos():
                    mano.presionar(False)

        if derecha ==True:#todo este codigo es para el movimiento
            if posX<1000:
                posX+=velocidad
                Aves = pygame.image.load("imagenes/paloma.png")
            else:
                derecha = False
        else:
            posX-=velocidad
            Aves = pygame.image.load("imagenes/paloma2.png")
            if posX<100:
                derecha = True


        if bulBarco ==True:#todo este codigo es para el movimiento
            if posXbarco<1000:
                posXbarco+=velocidadBarco
                barco = pygame.image.load("imagenes/barco.png")
            else:
                bulBarco = False
        else:
            posXbarco-=velocidadBarco
            barco = pygame.image.load("imagenes/barco2.png")
            if posXbarco<100:
                bulBarco = True

        if monkey ==True:#todo este codigo es para el movimiento
            if posXmono<1000:
                posXmono+=velocidadMono
                mono = pygame.image.load("imagenes/mono.png")
            else:
                monkey = False
        else:
            posXmono-=velocidadMono
            mono = pygame.image.load("imagenes/mono2.png")
            if posXmono<100:
                monkey = True

        contador = Fuente.render("Tiempo: "+str(Tiempo),50,(250,250,250))#cronometro

                       
        # =============== FIN MANEJADORES DE EVENTOS==========================

        # ============= AQUI VA LOGICA DEL JUEGO =============================        
        juego.actualizar()
        # ====================================================================

        # ============= AQUI VA LO QUE SE VA A DIBUJAR EN LA PANTALLA ========

        pantalla.blit(fondo,(0,0))
        pantalla.blit(mono,(posXmono,posYmono))
        pantalla.blit(contador,(420,20))
        pantalla.blit(Aves,(posX,posY))
        pantalla.blit(Aves,(posX-10,posY+20))
        pantalla.blit(Aves,(posX+30,posY+40))
        pantalla.blit(Aves,(posX-20,posY+60))
        pantalla.blit(flamingo,(700,450))
        pantalla.blit(flamingo,(600,450))
        pantalla.blit(flamingo2,(500,450))
        pantalla.blit(flamingo2,(250,450))
        pantalla.blit(barco,(posXbarco,posYbarco))
        juego.dibujar(pantalla)  
        # ====================================================================      
        # Avanza y actualiza la pantalla con lo que hemos dibujado
        pygame.display.flip()
# ============================================================================

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
