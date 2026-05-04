# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import pygame
import json
from sys import exit
from random import randint
import math

IMAGENES_ASTROS = {}
IMAGENES_TECLAS = {}

ASSET_MAP = {
    "Mercurio": "mercurio.png",
    "Venus": "venus.png",
    "Tierra": "tierra.png",
    "Luna": "luna.png",
    "Marte": "marte.png",
    "Júpiter": "jupiter.png",
    "Saturno": "saturno.png",
    "Urano": "urano.png",
    "Neptuno": "neptuno.png",
    "Estrella": "estrella.png"
}

ESCALA_MAP = {
    "Mercurio": 0.5,
    "Venus": 0.55,
    "Tierra": 0.55,
    "Luna": 0.5,
    "Marte": 0.5,
    "Júpiter": 0.35,
    "Saturno": 0.35,
    "Urano": 0.4,
    "Neptuno": 0.4
}

RADIANES_36 = math.pi / 180

def cargar_imagenes():
    global IMAGENES_ASTROS, IMAGENES_TECLAS
    
    for nombre, archivo in ASSET_MAP.items():
        try:
            IMAGENES_ASTROS[nombre] = pygame.image.load(f"assets/Graphics/{archivo}").convert_alpha()
        except:
            pass
    
    IMAGENES_TECLAS = {
        "up": pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_up.png").convert_alpha(),
        "down": pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_down.png").convert_alpha(),
        "left": pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_left.png").convert_alpha(),
        "right": pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_right.png").convert_alpha(),
        "space": pygame.image.load("assets/Graphics/Keyboard & Mouse/Double/keyboard_space.png").convert_alpha()
    }

_ESTRELLA_CACHE = None

def dibujar_estrella(radio, color):
    global _ESTRELLA_CACHE
    if _ESTRELLA_CACHE is None:
        superficie = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        puntos = []
        for i in range(10):
            ang = (i * 36 - 90) * RADIANES_36
            r = radio if i % 2 == 0 else radio * 0.4
            puntos.append((radio + r * math.cos(ang), radio + r * math.sin(ang)))
        pygame.draw.polygon(superficie, color, puntos)
        pygame.draw.circle(superficie, (255, 255, 255), (radio, radio), radio // 3)
        _ESTRELLA_CACHE = superficie
    return _ESTRELLA_CACHE.copy()

class Camara(pygame.sprite.Sprite):
    def __init__(self, limite_ancho, limite_alto):
        super().__init__()
        radio = 80
        color_metal = (60, 60, 70)
        color_bronce = (180, 140, 80)
        self.image = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (ancho/2, alto/2))
        self.velocidad = 4
        self.limite_ancho = limite_ancho
        self.limite_alto = limite_alto
        
        pygame.draw.circle(self.image, color_metal, (radio, radio), radio, 8)
        pygame.draw.circle(self.image, color_metal, (radio, radio), radio - 5, 6)
        pygame.draw.circle(self.image, color_bronce, (radio, radio), radio - 10, 4)
        pygame.draw.circle(self.image, (0, 50, 0), (radio, radio), radio - 15, 2)
        
        for i in range(4):
            ang = i * 1.57
            x = int(radio + 30 * math.cos(ang))
            y = int(radio + 30 * math.sin(ang))
            pygame.draw.circle(self.image, color_bronce, (x, y), 3)
        
        pygame.draw.line(self.image, color_metal, (radio - 20, radio), (radio - 35, radio), 4)
        pygame.draw.line(self.image, color_metal, (radio + 20, radio), (radio + 35, radio), 4)
        pygame.draw.line(self.image, color_metal, (radio, radio - 20), (radio, radio - 35), 4)
        pygame.draw.line(self.image, color_metal, (radio, radio + 20), (radio, radio + 35), 4)

    def controlar_bordes(self):
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > self.limite_ancho: 
            self.rect.right = self.limite_ancho
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > self.limite_alto: 
            self.rect.bottom = self.limite_alto      

    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.velocidad
        
        self.controlar_bordes()
          
    def update(self):
        self.movimiento()

class Astro(pygame.sprite.Sprite):
    def __init__(self, astro):
        super().__init__()
        self.nombre = astro["nombre"]
        
        if self.nombre == "Estrella":
            self.image = dibujar_estrella(40, (255, 255, 200))
        else:
            img_cargada = IMAGENES_ASTROS.get(self.nombre)
            if img_cargada:
                self.image = img_cargada.copy()
            else:
                self.image = pygame.Surface((50, 50))
                self.image.fill((255, 255, 255))
        
        escala = ESCALA_MAP.get(self.nombre, 0.5)
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * escala), int(original_size[1] * escala))
        self.image = pygame.transform.scale(self.image, new_size)
        self.seleccionado = False
        
        intentos = 0
        max_intentos = 100
        while intentos < max_intentos:
            random_y = randint(0, alto)
            random_x = randint(0, ancho)
            self.rect = self.image.get_rect(center = (random_x, random_y))
            colision = False
            for astro in astros_grupo:
                if self.rect.colliderect(astro.rect) or self.rect.colliderect(camara.sprite.rect):
                    colision = True
                    break
            if not colision:
                break
            intentos += 1
        
        self.image.set_alpha(0)
        self.radio_deteccion = 150
    
    def update_visual(self, pos_visor):
        distancia = math.dist(self.rect.center, pos_visor)

        if distancia < self.radio_deteccion:
            proporcion = 1 - (distancia / self.radio_deteccion)            
            nuevo_alpha = int(proporcion * 255)
            self.image.set_alpha(nuevo_alpha)
            
            if proporcion > 0.8:
                self.seleccionado = True 
            else:
                False
        else:
            self.image.set_alpha(0)
            self.seleccionado = False
    

    def update(self):
        pass
        

def dibujar_controles():
    ancla = (ancho / 2.5, alto / 1.2)
    texto_mov = fuente_normal.render("Movimiento", False, (255,255,255))
    texto_mov_rect = texto_mov.get_rect(midbottom = tuple(a + b for a, b in zip(ancla, (0, -80))))
    texto_inicio = fuente_normal.render("Presione", False, (255,255,255))
    texto_inicio_rect = texto_inicio.get_rect(midbottom = tuple(a + b for a, b in zip(ancla, (250, -80))))
    texto_foto = fuente_normal.render("Para Jugar", False, (255,255,255))
    texto_foto_rect = texto_foto.get_rect(midbottom = tuple(a + b for a, b in zip(ancla, (250, -50)))) 
    
    for t in datos_teclas:
        ancla_flecha = tuple(a + b for a, b in zip(ancla, t["offset"]))
        rectangulo = t["img"].get_rect(center = ancla_flecha)
        pantalla.blit(t["img"], rectangulo)
    
    pantalla.blit(texto_mov, texto_mov_rect)
    pantalla.blit(texto_inicio, texto_inicio_rect)
    pantalla.blit(texto_foto, texto_foto_rect)

BOTON_SCORES = None
BOTON_SALIR = None

def crear_boton_scores():
    global BOTON_SCORES, BOTON_SALIR
    texto = fuente_normal.render("PUNTOS", False, (255, 255, 255))
    BOTON_SCORES = {
        "imagen": texto,
        "x": ancho - 180,
        "y": 20,
        "ancho": 160,
        "alto": 50
    }
    texto_salir = fuente_normal.render("SALIR", False, (255, 255, 255))
    BOTON_SALIR = {
        "imagen": texto_salir,
        "x": ancho - 180,
        "y": 80,
        "ancho": 160,
        "alto": 50
    }

def mostrar_menu():
    global scores_actualizados
    global album_imagenes
    global texto_info
    global ultimo_score_posicion
    pantalla.fill((0,0,0))
    
    crear_boton_scores()
    
    scores_actualizados = []
    with open('data/scores.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
        for item in datos["top_scores"]:
            scores_actualizados.append(item)
    
    album_imagenes = {}
    for nombre in IMAGENES_ASTROS:
        album_imagenes[nombre] = IMAGENES_ASTROS[nombre]
    
    texto_info = {}
    for item in astros:
        texto_info[item["nombre"]] = item.get("texto", "")
    texto_info["Estrella"] = "Brilla en el cielo"
    
    nombre = fuente_titulo.render("ArcSpace", False, (255,255,255))
    nombre_rect = nombre.get_rect(center = (ancho / 2, alto / 8))
    pantalla.blit(nombre, nombre_rect)
    
    if BOTON_SCORES is None:
        crear_boton_scores()
    pygame.draw.rect(pantalla, (100, 100, 200), (BOTON_SCORES["x"], BOTON_SCORES["y"], BOTON_SCORES["ancho"], BOTON_SCORES["alto"]), border_radius=10)
    pygame.draw.rect(pantalla, (255, 255, 255), (BOTON_SCORES["x"], BOTON_SCORES["y"], BOTON_SCORES["ancho"], BOTON_SCORES["alto"]), 3, border_radius=10)
    pantalla.blit(BOTON_SCORES["imagen"], (BOTON_SCORES["x"] + 30, BOTON_SCORES["y"] + 10))
    
    pygame.draw.rect(pantalla, (200, 100, 100), (BOTON_SALIR["x"], BOTON_SALIR["y"], BOTON_SALIR["ancho"], BOTON_SALIR["alto"]), border_radius=10)
    pygame.draw.rect(pantalla, (255, 255, 255), (BOTON_SALIR["x"], BOTON_SALIR["y"], BOTON_SALIR["ancho"], BOTON_SALIR["alto"]), 3, border_radius=10)
    pantalla.blit(BOTON_SALIR["imagen"], (BOTON_SALIR["x"] + 45, BOTON_SALIR["y"] + 10))
    
    dibujar_controles()

def mostrar_scores():
    global scores_actualizados, scroll_offset
    pantalla.fill((10, 10, 30))
    
    scores_actualizados = []
    with open('data/scores.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
        for item in datos["top_scores"]:
            scores_actualizados.append(item)
    
    titulo = fuente_titulo.render("TOP PUNTOS", False, (255, 215, 0))
    titulo_rect = titulo.get_rect(center = (ancho / 2, 40))
    pantalla.blit(titulo, titulo_rect)
    
    colores_top = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
    tamano_top = [50, 40, 35]
    
    for i in range(3):
        if i >= len(scores_actualizados):
            break
        score = scores_actualizados[i]
        veces = score.get("veces", 1)
        fuente = pygame.font.Font("assets/Fonts/Silkscreen/Silkscreen-Regular.ttf", tamano_top[i])
        texto = fuente.render(f"{i+1}. {score['nombre']}: {score['puntos']} ({veces})", False, colores_top[i])
        texto_rect = texto.get_rect(center = (ancho / 2, 120 + i * 60))
        pantalla.blit(texto, texto_rect)
    
    y_restantes = 280
    max_mostrar = min(len(scores_actualizados), ultimo_score_posicion + 1) if ultimo_score_posicion is not None else len(scores_actualizados)
    
    pygame.draw.line(pantalla, (80, 80, 120), (50, 260), (ancho - 50, 260), 2)
    
    for i in range(3, max_mostrar):
        score = scores_actualizados[i]
        veces = score.get("veces", 1)
        if i == ultimo_score_posicion:
            color = (255, 100, 100)
            fuente = fuente_normal
        else:
            color = (150, 150, 150)
            fuente = fuente_chica
        texto = fuente.render(f"{i+1}. {score['nombre']}: {score['puntos']} ({veces})", False, color)
        pantalla.blit(texto, (ancho / 2 - 150, y_restantes))
        y_restantes += 25
    
    instruccion = fuente_normal.render("Presiona ESC para volver", False, (150, 150, 150))
    instruccion_rect = instruccion.get_rect(center = (ancho / 2, alto - 40))
    pantalla.blit(instruccion, instruccion_rect)

def mostrar_ingreso():
    pantalla.fill((10, 10, 30))
    
    pygame.draw.rect(pantalla, (50, 50, 100), (ancho//2 - 250, alto//3, 500, 150), border_radius=20)
    pygame.draw.rect(pantalla, (255, 215, 0), (ancho//2 - 250, alto//3, 500, 150), 4, border_radius=20)
    
    titulo = fuente_titulo.render("INGRESA TU NOMBRE", False, (255, 215, 0))
    titulo_rect = titulo.get_rect(center = (ancho / 2, alto // 3 + 40))
    pantalla.blit(titulo, titulo_rect)
    
    pygame.draw.rect(pantalla, (30, 30, 60), (ancho//2 - 150, alto//2 + 20, 300, 50), border_radius=10)
    pygame.draw.rect(pantalla, (255, 255, 255), (ancho//2 - 150, alto//2 + 20, 300, 50), 3, border_radius=10)
    
    nombre_mostrar = nombre_jugador if len(nombre_jugador) > 0 else "_"
    nombre_texto = fuente_titulo.render(nombre_mostrar, False, (255, 255, 100))
    nombre_rect = nombre_texto.get_rect(center = (ancho / 2, alto // 2 + 45))
    pantalla.blit(nombre_texto, nombre_rect)
    
    instruccion = fuente_chica.render("Presiona ENTER para comenzar", False, (150, 150, 150))
    instruccion_rect = instruccion.get_rect(center = (ancho / 2, alto - 60))
    pantalla.blit(instruccion, instruccion_rect)

def tomar_foto():    
    colisiones = pygame.sprite.spritecollide(camara.sprite, astros_grupo, False)
    if colisiones:
        astro = colisiones[0]
        astros_grupo.remove(astro)
        if astro.nombre not in astros_encontrados:
            astros_encontrados.append(astro.nombre)
        return astro
    return None

def agregar_puntos(cantidad):
    global puntos
    puntos += cantidad

def colision():
        colisiones = pygame.sprite.spritecollide(camara.sprite, astros_grupo, False)
        if colisiones:
            return colisiones[0]
        else:
            return None

def guardar_score(nombre, puntos):
    global ultimo_score_posicion
    from datetime import date
    scores = []
    with open('data/scores.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
        for item in datos["top_scores"]:
            scores.append(item)
    
    existente = None
    for s in scores:
        if s["nombre"] == nombre:
            existente = s
            break
    
    if existente:
        if puntos > existente["puntos"]:
            existente["puntos"] = puntos
            existente["album"] = astros_encontrados.copy()
            existente["fecha"] = str(date.today())
        existente["veces"] = existente.get("veces", 1) + 1
    else:
        nuevo_score = {
            "nombre": nombre, 
            "puntos": puntos, 
            "fecha": str(date.today()),
            "album": astros_encontrados.copy(),
            "veces": 1
        }
        scores.append(nuevo_score)
    
    scores.sort(key=lambda x: x["puntos"], reverse=True)
    
    for i, s in enumerate(scores):
        if s["nombre"] == nombre:
            ultimo_score_posicion = i
            break
    
    with open('data/scores.json', 'w', encoding='utf-8') as f:
        json.dump({"top_scores": scores}, f, indent=4)

def mostrar_gameover():
    pantalla.fill((10, 10, 30))
    
    titulo = fuente_titulo.render("ALBUM DE FOTOS", False, (255, 215, 0))
    titulo_rect = titulo.get_rect(center = (ancho / 2, 50))
    pantalla.blit(titulo, titulo_rect)
    
    puntos_texto = fuente_titulo.render(f"Puntos: {puntos}", False, (255, 255, 255))
    puntos_rect = puntos_texto.get_rect(center = (ancho / 2, 120))
    pantalla.blit(puntos_texto, puntos_rect)
    
    pygame.draw.line(pantalla, (100, 100, 150), (50, 160), (ancho - 50, 160), 2)
    
    texto_info = {}
    for item in astros:
        texto_info[item["nombre"]] = item.get("texto", "")
    texto_info["Estrella"] = "Brilla en el cielo"
    
    album_imagenes = {}
    for nombre in IMAGENES_ASTROS:
        album_imagenes[nombre] = IMAGENES_ASTROS[nombre]
    
    mostrar_album(astros_encontrados, album_imagenes, texto_info)
    
    pygame.draw.rect(pantalla, (50, 50, 100), (ancho//2 - 200, alto - 80, 400, 50), border_radius=10)
    pygame.draw.rect(pantalla, (255, 255, 255), (ancho//2 - 200, alto - 80, 400, 50), 3, border_radius=10)
    instruccion = fuente_normal.render("ENTER: Menu  |  R: Jugar de nuevo", False, (255, 255, 255))
    instruccion_rect = instruccion.get_rect(center = (ancho / 2, alto - 55))
    pantalla.blit(instruccion, instruccion_rect)

def mostrar_album(lista_astros, album_img, info_texto, offset_y=180):
    cols = 5
    cell_width = 200
    cell_height = 130
    start_x = (ancho - cols * cell_width) // 2 + 30
    start_y = offset_y
    
    for i, nombre in enumerate(lista_astros):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_width
        y = start_y + row * cell_height
        
        pygame.draw.rect(pantalla, (40, 40, 80), (x, y, cell_width - 10, cell_height - 10), border_radius=10)
        
        if nombre in album_img:
            img = pygame.transform.scale(album_img[nombre], (70, 70))
            img_x = x + (cell_width - 10 - 70) // 2
            img_y = y + 10
            pantalla.blit(img, (img_x, img_y))
        
        nombre_label = fuente_normal.render(nombre, False, (255, 255, 200))
        nombre_rect = nombre_label.get_rect(center=(x + cell_width/2 - 5, y + 85))
        pantalla.blit(nombre_label, nombre_rect)
        
        info = info_texto.get(nombre, "")[:20]
        info_label = fuente_chica.render(info, False, (150, 180, 220))
        info_rect = info_label.get_rect(center=(x + cell_width/2 - 5, y + 108))
        pantalla.blit(info_label, info_rect)
    
    pygame.draw.line(pantalla, (100, 100, 150), (50, alto - 120), (ancho - 50, alto - 120), 2)
    
    instruccion = fuente_normal.render("Ingrese su nombre:", False, (255, 255, 255))
    instruccion_rect = instruccion.get_rect(center = (ancho / 2, alto - 90))
    pantalla.blit(instruccion, instruccion_rect)
    
    nombre_texto = fuente_titulo.render(nombre_jugador + "_", False, (0, 255, 100))
    nombre_rect = nombre_texto.get_rect(center = (ancho / 2, alto - 50))
    pantalla.blit(nombre_texto, nombre_rect)

pygame.init()
ancho = 1280
alto = 720
info = pygame.display.Info()
ancho = info.current_w
alto = info.current_h
centro = (ancho //2, alto // 2)
pantalla = pygame.display.set_mode((ancho, alto), pygame.FULLSCREEN)
cargar_imagenes()
pygame.display.set_caption("ArcSpace")
clock = pygame.time.Clock()
fuente_titulo = pygame.font.Font("assets/Fonts/Silkscreen/Silkscreen-Regular.ttf", 80)
fuente_normal = pygame.font.Font("assets/Fonts/Silkscreen/Silkscreen-Regular.ttf", 30)
fuente_chica = pygame.font.Font("assets/Fonts/Silkscreen/Silkscreen-Regular.ttf", 18)
# Estados posibles
ESTADO_MENU = "menu"
ESTADO_JUGANDO = "jugando"
ESTADO_REPORTE = "reporte"
ESTADO_GAMEOVER = "gameover"
ESTADO_SCORES = "scores"
ESTADO_INGRESO = "ingreso"

# Estado inicial
estado_actual = ESTADO_MENU
nombre_jugador = ""
input_activo = False
ultimo_score_posicion = None
scroll_offset = 0

#Menu
datos_teclas = [
    {"img": IMAGENES_TECLAS["up"], "offset": (0, -50)},   
    {"img": IMAGENES_TECLAS["down"], "offset": (0, 0)},  
    {"img": IMAGENES_TECLAS["left"], "offset": (-50, 0)},  
    {"img": IMAGENES_TECLAS["right"], "offset": (50, 0)},
    {"img": IMAGENES_TECLAS["space"], "offset": (250, -5)}   
    ]

#Mostrar scores
scores = []
with open('data/scores.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    for item in datos["top_scores"]:
        scores.append(item)

#Juego
fotos = 5
tiempo_juego = 10000
tiempo_restante = tiempo_juego
puntos = 0
astros_encontrados = []
score_seleccionado = 0
album_mostrado = False
MAX_ASTROS = 12
camara = pygame.sprite.GroupSingle()
camara.add(Camara(ancho, alto))

EVENTO_NUEVO_ASTRO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_NUEVO_ASTRO, 5000)

#Astros
astros = []
with open("data/astros.json", "r", encoding="utf-8") as f:
    datos = json.load(f)
    for item in datos["astros"]:
        astros.append(item)

astro_en_foco = None
astro_actual = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if estado_actual == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if BOTON_SCORES and BOTON_SCORES["x"] <= mouse_pos[0] <= BOTON_SCORES["x"] + BOTON_SCORES["ancho"] and BOTON_SCORES["y"] <= mouse_pos[1] <= BOTON_SCORES["y"] + BOTON_SCORES["alto"]:
                        estado_actual = ESTADO_SCORES
                    elif BOTON_SALIR and BOTON_SALIR["x"] <= mouse_pos[0] <= BOTON_SALIR["x"] + BOTON_SALIR["ancho"] and BOTON_SALIR["y"] <= mouse_pos[1] <= BOTON_SALIR["y"] + BOTON_SALIR["alto"]:
                        pygame.quit()
                        exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nombre_jugador = ""
                    estado_actual = ESTADO_INGRESO
        
        elif estado_actual == 'jugando':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                astro_encontrado = tomar_foto()
                if astro_encontrado:
                    if astro_encontrado.nombre == "Estrella":
                        tiempo_restante = min(tiempo_restante + 3000, 10000)
                    agregar_puntos(100 if astro_encontrado.nombre != "Estrella" else 50)
                else:
                    tiempo_restante = max(tiempo_restante - 1000, 0)
            
            if tiempo_restante <= 0:
                estado_actual = ESTADO_GAMEOVER
            
            if event.type == EVENTO_NUEVO_ASTRO:
                astros_grupo.add(Astro({"nombre": "Estrella", "puntos": 50, "texto": "Brilla en el cielo"}))
        
        elif estado_actual == ESTADO_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tiempo_restante = tiempo_juego
                    puntos = 0
                    astros_encontrados.clear()
                    album_mostrado = False
                    astros_grupo = pygame.sprite.Group()
                    for astro in astros:
                        astros_grupo.add(Astro(astro))
                    for _ in range(9):
                        astros_grupo.add(Astro({"nombre": "Estrella", "puntos": 50, "texto": "Brilla"}))
                    estado_actual = ESTADO_JUGANDO
                elif event.key == pygame.K_RETURN:
                    guardar_score(nombre_jugador, puntos)
                    nombre_jugador = ""
                    estado_actual = ESTADO_MENU
        
        elif estado_actual == ESTADO_INGRESO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif event.key == pygame.K_RETURN and len(nombre_jugador) > 0:
                    estado_actual = ESTADO_JUGANDO
                    tiempo_restante = tiempo_juego
                    puntos = 0
                    astros_encontrados.clear()
                    album_mostrado = False
                    astros_grupo = pygame.sprite.Group()
                    for astro in astros:
                        astros_grupo.add(Astro(astro))
                    for _ in range(9):
                        astros_grupo.add(Astro({"nombre": "Estrella", "puntos": 50, "texto": "Brilla"}))
                elif event.key == pygame.K_ESCAPE:
                    estado_actual = ESTADO_MENU
                elif len(nombre_jugador) < 10:
                    char = pygame.key.name(event.key)
                    if char.isalpha():
                        nombre_jugador += char.upper()
        
        elif estado_actual == ESTADO_SCORES:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                estado_actual = ESTADO_MENU
    
    if estado_actual == 'menu':
        mostrar_menu()
    
    if estado_actual == ESTADO_SCORES:
        mostrar_scores()
    
    if estado_actual == ESTADO_INGRESO:
        mostrar_ingreso()
    
    if estado_actual == 'gameover':
        mostrar_gameover()
    
    if estado_actual == 'jugando':
        pantalla.fill((5, 5, 15))
        
        pygame.draw.circle(pantalla, (20, 20, 30), camara.sprite.rect.center, 250, 200)
        
        pygame.draw.circle(pantalla, (40, 40, 50), camara.sprite.rect.center, 260, 10)
        
        tiempo_restante -= clock.get_time()
        if tiempo_restante <= 0:
            tiempo_restante = 0
            estado_actual = ESTADO_GAMEOVER
        
        proporcion = tiempo_restante / tiempo_juego
        barra_alto = 30
        barra_y = alto - barra_alto - 10
        barra_x = 10
        barra_ancho = ancho - 20
        
        pygame.draw.rect(pantalla, (50, 50, 50), (barra_x, barra_y, barra_ancho, barra_alto), border_radius=8)
        pygame.draw.rect(pantalla, (100, 100, 100), (barra_x, barra_y, barra_ancho, barra_alto), 3, border_radius=8)
        
        if proporcion > 0.5:
            color_barra = (100, 255, 100)
        elif proporcion > 0.25:
            color_barra = (255, 200, 50)
        else:
            color_barra = (255, 100, 100)
        
        pygame.draw.rect(pantalla, color_barra, (barra_x + 5, barra_y + 5, int((barra_ancho - 10) * proporcion), barra_alto - 10), border_radius=5)
        
        puntos_texto = fuente_normal.render(f"Puntos: {puntos}", False, (255, 255, 255))
        pantalla.blit(puntos_texto, (20, 20))
        
        scores_juego = []
        with open('data/scores.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
            for item in datos["top_scores"]:
                scores_juego.append(item)
        
        colores_top = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
        
        pygame.draw.rect(pantalla, (0, 0, 0, 150), (ancho - 250, 10, 240, min(len(scores_juego), 10) * 18 + 20), border_radius=10)
        
        y_scores = 20
        for i, score in enumerate(scores_juego[:10]):
            if i < 3:
                color = colores_top[i]
                fuente = fuente_normal
            else:
                color = (180, 180, 180)
                fuente = fuente_chica
            score_texto = fuente.render(f"{i+1}. {score['nombre']}: {score['puntos']}", False, color)
            pantalla.blit(score_texto, (ancho - 230, y_scores))
            y_scores += 18
        
        camara.draw(pantalla)
        camara.update()

        pos_v = camara.sprite.rect.center
        for astro in astros_grupo:
            astro.update_visual(pos_v)
        
        astros_grupo.draw(pantalla)
        astro_actual = colision()
        
    pygame.display.update()
    clock.tick(60)