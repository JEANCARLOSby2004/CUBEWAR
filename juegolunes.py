import pygame
import random
import math

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CUBEWAR")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Carga la imagen del jugadorsdddddddddds
imagen_jugador = pygame.image.load("navecita.png")
tamano_jugador = imagen_jugador.get_size()
jugador = pygame.Rect(ANCHO // 2, ALTO // 2, tamano_jugador[0], tamano_jugador[1])
velocidad_jugador = 5

balas_jugador = []
velocidad_bala = 8
temporizador_bala = 0

tamano_enemigo = 25
enemigos = []
balas_enemigos = []
temporizador_generacion_enemigo = 1

niveles = {
    "Fácil": {
        "vidas": 7,
        "velocidad_bala_enemigo": 2,
        "max_enemigos": 7,
        "musica": "musiquita.mp3",
        "mapa": "mapa1.jpg",
        "meta": 25
    },
    "Medio": {
        "vidas": 4,
        "velocidad_bala_enemigo": 3,
        "max_enemigos": 12,
        "musica": "musiquita2.mp3",
        "mapa": "mapa2.jpg",
        "meta": 40
    },
    "Hardcore": {
        "vidas": 2,
        "velocidad_bala_enemigo": 7,
        "max_enemigos": 15,
        "musica": "musiquita3.mp3",
        "mapa": "mapa3.jpg",
        "meta": 20
    }
}

def mostrar_menu():
    pantalla.fill(BLANCO)
    font = pygame.font.Font(None, 74)
    texto_titulo = font.render("Selecciona el Nivel", True, NEGRO)
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4))

    font_opciones = pygame.font.Font(None, 56)
    opciones = ["Fácil", "Medio", "Hardcore", "Instrucciones", "Salir"]
    for i, opcion in enumerate(opciones):
        texto_opcion = font_opciones.render(opcion, True, NEGRO)
        pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 60))

    pygame.display.flip()

def mostrar_instrucciones():
    pantalla.fill(BLANCO)
    font = pygame.font.Font(None, 36)
    texto_instrucciones = font.render("Este juego ... yo lo voy a rellenar", True, NEGRO)
    pantalla.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2 - 20))
    
    texto_regresar = font.render("Presiona 'R' para regresar al menú", True, NEGRO)
    pantalla.blit(texto_regresar, (ANCHO // 2 - texto_regresar.get_width() // 2, ALTO // 2 + 40))

    pygame.display.flip()

def seleccionar_nivel():
    while True:
        mostrar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "Fácil"
                elif evento.key == pygame.K_2:
                    return "Medio"
                elif evento.key == pygame.K_3:
                    return "Hardcore"
                elif evento.key == pygame.K_4:
                    mostrar_instrucciones()
                    while True:
                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_r:
                                    break
                        else:
                            continue
                        break
                elif evento.key == pygame.K_5:
                    pygame.quit()
                    exit()

nivel = seleccionar_nivel()
config = niveles[nivel]

pygame.mixer.music.load(config["musica"])
pygame.mixer.music.play(-1)

vidas = config["vidas"]
velocidad_bala_enemigo = config["velocidad_bala_enemigo"]
max_enemigos = config["max_enemigos"]
meta_asesinatos = config["meta"]

mapa_fondo = pygame.image.load(config["mapa"])

def disparar_bala(pos_inicial, pos_objetivo, velocidad):
    angulo = math.atan2(pos_objetivo[1] - pos_inicial[1], pos_objetivo[0] - pos_inicial[0])
    bala_dx = velocidad * math.cos(angulo)
    bala_dy = velocidad * math.sin(angulo)
    return pygame.Rect(pos_inicial[0], pos_inicial[1], 5, 5), bala_dx, bala_dy

def mostrar_vidas(vidas):
    font = pygame.font.Font(None, 36)
    texto_vidas = font.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))

def mostrar_asesinatos(asesinatos, meta):
    font = pygame.font.Font(None, 36)
    texto_asesinatos = font.render(f"Asesinatos: {asesinatos}", True, BLANCO)
    pantalla.blit(texto_asesinatos, (ANCHO - 200, 10))
    texto_meta = font.render(f"Meta: {meta}", True, BLANCO)
    pantalla.blit(texto_meta, (ANCHO - 200, 50))

def mostrar_ganaste():
    pantalla.fill(BLANCO)
    font = pygame.font.Font(None, 74)
    texto_ganaste = font.render("¡Ganaste!", True, NEGRO)
    pantalla.blit(texto_ganaste, (ANCHO // 2 - texto_ganaste.get_width() // 2, ALTO // 2 - texto_ganaste.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

asesinatos = 0
ejecutando = True
while ejecutando:
    pantalla.blit(mapa_fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_d]:
        jugador.x += velocidad_jugador
    if teclas[pygame.K_w]:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_s]:
        jugador.y += velocidad_jugador

    temporizador_bala += 1
    if temporizador_bala % 15 == 0:
        bala = disparar_bala(jugador.center, pygame.mouse.get_pos(), velocidad_bala)
        balas_jugador.append(bala)

    for bala in balas_jugador[:]:
        bala[0].x += bala[1]
        bala[0].y += bala[2]
        if bala[0].x < 0 or bala[0].x > ANCHO or bala[0].y < 0 or bala[0].y > ALTO:
            balas_jugador.remove(bala)
        else:
            pygame.draw.rect(pantalla, BLANCO, bala[0])

    temporizador_generacion_enemigo += 1
    if temporizador_generacion_enemigo % 60 == 0 and len(enemigos) < max_enemigos:
        enemigo_x = random.randint(0, ANCHO - tamano_enemigo)
        enemigo_y = random.randint(0, ALTO - tamano_enemigo)
        enemigo = pygame.Rect(enemigo_x, enemigo_y, tamano_enemigo, tamano_enemigo)
        enemigos.append(enemigo)

    for enemigo in enemigos:
        if random.random() < 0.02:
            bala = disparar_bala(enemigo.center, jugador.center, velocidad_bala_enemigo)
            balas_enemigos.append(bala)

    for bala in balas_enemigos[:]:
        bala[0].x += bala[1]
        bala[0].y += bala[2]
        if bala[0].colliderect(jugador):
            vidas -= 1
            balas_enemigos.remove(bala)
            if vidas <= 0:
                ejecutando = False
        if bala[0].x < 0 or bala[0].x > ANCHO or bala[0].y < 0 or bala[0].y > ALTO:
            balas_enemigos.remove(bala)
        else:
            pygame.draw.rect(pantalla, ROJO, bala[0])

    for enemigo in enemigos[:]:
        pygame.draw.ellipse(pantalla, ROJO, enemigo)
        for bala in balas_jugador[:]:
            if enemigo.colliderect(bala[0]):
                balas_jugador.remove(bala)
                enemigos.remove(enemigo)
                asesinatos += 1
                break

    pantalla.blit(imagen_jugador, jugador.topleft)
    mostrar_vidas(vidas)
    mostrar_asesinatos(asesinatos, meta_asesinatos)
    
    if asesinatos >= meta_asesinatos:
        mostrar_ganaste()
        ejecutando = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()




## versionn sin fin ------------------------


'''

import pygame
import random
import math

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cuadrado y Círculos")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Carga la imagen del jugador
imagen_jugador = pygame.image.load("navecita.png")
tamano_jugador = imagen_jugador.get_size()
jugador = pygame.Rect(ANCHO // 2, ALTO // 2, tamano_jugador[0], tamano_jugador[1])
velocidad_jugador = 5

balas_jugador = []
velocidad_bala = 8
temporizador_bala = 0

tamano_enemigo = 25
enemigos = []
balas_enemigos = []
temporizador_generacion_enemigo = 1

niveles = {
    "Fácil": {
        "vidas": 7,
        "velocidad_bala_enemigo": 2,
        "max_enemigos": 7,
        "musica": "musiquita.mp3",
        "mapa": "mapa1.jpg"
    },
    "Medio": {
        "vidas": 4,
        "velocidad_bala_enemigo": 4,
        "max_enemigos": 12,
        "musica": "musiquita2.mp3",
        "mapa": "mapa2.jpg"
    },
    "Hardcore": {
        "vidas": 2,
        "velocidad_bala_enemigo": 7,
        "max_enemigos": 15,
        "musica": "musiquita3.mp3",
        "mapa": "mapa3.jpg"
    }
}

def mostrar_menu():
    pantalla.fill(BLANCO)
    font = pygame.font.Font(None, 74)
    texto_titulo = font.render("Selecciona el Nivel", True, NEGRO)
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4))

    font_opciones = pygame.font.Font(None, 56)
    opciones = ["Fácil", "Medio", "Hardcore", "Instrucciones", "Salir"]
    for i, opcion in enumerate(opciones):
        texto_opcion = font_opciones.render(opcion, True, NEGRO)
        pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 60))

    pygame.display.flip()

def mostrar_instrucciones():
    pantalla.fill(BLANCO)
    font = pygame.font.Font(None, 36)
    texto_instrucciones = font.render("Este juego ... yo lo voy a rellenar", True, NEGRO)
    pantalla.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2 - 20))
    
    texto_regresar = font.render("Presiona 'R' para regresar al menú", True, NEGRO)
    pantalla.blit(texto_regresar, (ANCHO // 2 - texto_regresar.get_width() // 2, ALTO // 2 + 40))

    pygame.display.flip()

def seleccionar_nivel():
    while True:
        mostrar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "Fácil"
                elif evento.key == pygame.K_2:
                    return "Medio"
                elif evento.key == pygame.K_3:
                    return "Hardcore"
                elif evento.key == pygame.K_4:
                    mostrar_instrucciones()
                    while True:
                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_r:
                                    break
                        else:
                            continue
                        break
                elif evento.key == pygame.K_5:
                    pygame.quit()
                    exit()

nivel = seleccionar_nivel()
config = niveles[nivel]

pygame.mixer.music.load(config["musica"])
pygame.mixer.music.play(-1)

vidas = config["vidas"]
velocidad_bala_enemigo = config["velocidad_bala_enemigo"]
max_enemigos = config["max_enemigos"]

mapa_fondo = pygame.image.load(config["mapa"])

def disparar_bala(pos_inicial, pos_objetivo, velocidad):
    angulo = math.atan2(pos_objetivo[1] - pos_inicial[1], pos_objetivo[0] - pos_inicial[0])
    bala_dx = velocidad * math.cos(angulo)
    bala_dy = velocidad * math.sin(angulo)
    return pygame.Rect(pos_inicial[0], pos_inicial[1], 5, 5), bala_dx, bala_dy

def mostrar_vidas(vidas):
    font = pygame.font.Font(None, 36)
    texto_vidas = font.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))

ejecutando = True
while ejecutando:
    pantalla.blit(mapa_fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_d]:
        jugador.x += velocidad_jugador
    if teclas[pygame.K_w]:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_s]:
        jugador.y += velocidad_jugador

    temporizador_bala += 1
    if temporizador_bala % 15 == 0:
        bala = disparar_bala(jugador.center, pygame.mouse.get_pos(), velocidad_bala)
        balas_jugador.append(bala)

    for bala in balas_jugador[:]:
        bala[0].x += bala[1]
        bala[0].y += bala[2]
        if bala[0].x < 0 or bala[0].x > ANCHO or bala[0].y < 0 or bala[0].y > ALTO:
            balas_jugador.remove(bala)
        else:
            pygame.draw.rect(pantalla, BLANCO, bala[0])

    temporizador_generacion_enemigo += 1
    if temporizador_generacion_enemigo % 60 == 0 and len(enemigos) < max_enemigos:
        enemigo_x = random.randint(0, ANCHO - tamano_enemigo)
        enemigo_y = random.randint(0, ALTO - tamano_enemigo)
        enemigo = pygame.Rect(enemigo_x, enemigo_y, tamano_enemigo, tamano_enemigo)
        enemigos.append(enemigo)

    for enemigo in enemigos:
        if random.random() < 0.02:
            bala = disparar_bala(enemigo.center, jugador.center, velocidad_bala_enemigo)
            balas_enemigos.append(bala)

    for bala in balas_enemigos[:]:
        bala[0].x += bala[1]
        bala[0].y += bala[2]
        if bala[0].colliderect(jugador):
            vidas -= 1
            balas_enemigos.remove(bala)
            if vidas <= 0:
                ejecutando = False
        if bala[0].x < 0 or bala[0].x > ANCHO or bala[0].y < 0 or bala[0].y > ALTO:
            balas_enemigos.remove(bala)
        else:
            pygame.draw.rect(pantalla, ROJO, bala[0])

    for enemigo in enemigos[:]:
        pygame.draw.ellipse(pantalla, ROJO, enemigo)
        for bala in balas_jugador[:]:
            if enemigo.colliderect(bala[0]):
                balas_jugador.remove(bala)
                enemigos.remove(enemigo)
                break

    pantalla.blit(imagen_jugador, jugador.topleft)
    mostrar_vidas(vidas)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

'''