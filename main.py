# -*- coding: utf-8 -*-
import pygame
import json
from sys import exit
from random import randint
import math

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
        
        asset_map = {
            "Mercurio": "mercurio.png",
            "Venus": "venus.png",
            "Tierra": "tierra.png",
            "Luna": "tierra.png",
            "Marte": "marte.png",
            "Júpiter": "jupiter.png",
            "Saturno": "saturno.png",
            "Urano": "urano.png",
            "Neptuno": "neptuno.png",
            "Estrella": "tierra.png"
        }
        
        asset_file = asset_map.get(self.nombre, "estrella.png")
        self.image = pygame.image.load(f"assets/Graphics/{asset_file}").convert_alpha()
        
        escala_map = {
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
        
        escala = escala_map.get(self.nombre, 0.5)
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * escala), int(original_size[1] * escala))
        self.image = pygame.transform.scale(self.image, new_size)
        self.seleccionado = False
        rect = '' 
        encontrado = False
        position = (0,0)
        while not encontrado:
            random_y = randint(0, alto)
            random_x = randint(0, ancho)
            position = (random_x, random_y)
            rect = self.image.get_rect(center = position)
            colision = False
            for astro in astros_grupo:
                if rect.colliderect(astro.rect) or rect.colliderect(camara.sprite.rect):
                    colision = True
                    break
            if not colision:
                encontrado = True
        self.rect = rect
        self.image_original = self.image.copy()
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

def mostrar_menu():
    pantalla.fill((0,0,0))
    
    scores_actualizados = []
    with open('data/scores.json', 'r') as f:
        datos = json.load(f)
        for item in datos["top_scores"]:
            scores_actualizados.append(item)
    
    nombre = fuente_titulo.render("ArcSpace", False, (255,255,255))
    nombre_rect = nombre.get_rect(center = (ancho / 2, alto / 8))
    scores_title = fuente_normal.render("Puntajes", False, (255,0,0))
    scores_title_rect = scores_title.get_rect(midleft = (ancho / 1.31 , alto / 7))

    ancla = (ancho / 1.38, alto / 14)
    offset = (0, 50)
    posicion_final = tuple(a + b for a, b in zip(ancla, offset))

    for score in scores_actualizados:
        posicion_final = tuple(a + b for a, b in zip(posicion_final, offset))
        score_surf = fuente_normal.render(f'{score["nombre"]}: {score["puntos"]}', False, (255, 0, 0))
        score_rect = score_surf.get_rect(topleft = posicion_final)
        pantalla.blit(score_surf, score_rect)

    pantalla.blit(nombre, nombre_rect)
    pantalla.blit(scores_title, scores_title_rect)
    dibujar_controles()

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
    from datetime import date
    scores = []
    with open('data/scores.json', 'r') as f:
        datos = json.load(f)
        for item in datos["top_scores"]:
            scores.append(item)
    
    nuevo_score = {
        "nombre": nombre, 
        "puntos": puntos, 
        "fecha": str(date.today()),
        "album": astros_encontrados.copy()
    }
    scores.append(nuevo_score)
    scores.sort(key=lambda x: x["puntos"], reverse=True)
    scores = scores[:5]
    
    with open('data/scores.json', 'w') as f:
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
    
    album_imagenes = {}
    asset_names = {
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
    
    texto_info = {}
    for item in astros:
        texto_info[item["nombre"]] = item.get("texto", "")
    texto_info["Estrella"] = "Brilla en el cielo"
    
    for nombre, archivo in asset_names.items():
        try:
            img = pygame.image.load(f"assets/Graphics/{archivo}").convert_alpha()
            album_imagenes[nombre] = img
        except:
            pass
    
    cols = 5
    cell_width = 200
    cell_height = 130
    start_x = (ancho - cols * cell_width) // 2 + 30
    start_y = 180
    
    for i, nombre in enumerate(astros_encontrados):
        col = i % cols
        row = i // cols
        x = start_x + col * cell_width
        y = start_y + row * cell_height
        
        pygame.draw.rect(pantalla, (40, 40, 80), (x, y, cell_width - 10, cell_height - 10), border_radius=10)
        
        if nombre in album_imagenes:
            img = pygame.transform.scale(album_imagenes[nombre], (70, 70))
            img_x = x + (cell_width - 10 - 70) // 2
            img_y = y + 10
            pantalla.blit(img, (img_x, img_y))
        
        nombre_label = fuente_normal.render(nombre, False, (255, 255, 200))
        nombre_rect = nombre_label.get_rect(center=(x + cell_width/2 - 5, y + 85))
        pantalla.blit(nombre_label, nombre_rect)
        
        info = texto_info.get(nombre, "")[:20]
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
centro = (ancho //2, alto // 2)
pantalla = pygame.display.set_mode((ancho, alto))
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

# Estado inicial
estado_actual = ESTADO_MENU
nombre_jugador = ""
input_activo = False

#Menu
img_up = pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_up.png").convert_alpha()
img_down = pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_down.png").convert_alpha()
img_left = pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_left.png").convert_alpha()
img_right = pygame.image.load("assets/Graphics/Keyboard & Mouse/Default/keyboard_arrow_right.png").convert_alpha()
img_space = pygame.image.load("assets/Graphics/Keyboard & Mouse/Double/keyboard_space.png").convert_alpha()
datos_teclas = [
    {"img": img_up, "offset": (0, -50)},   
    {"img": img_down, "offset": (0, 0)},  
    {"img": img_left, "offset": (-50, 0)},  
    {"img": img_right, "offset": (50, 0)},
    {"img": img_space, "offset": (250, -5)}   
    ]

#Mostrar scores
scores = []
with open('data/scores.json', 'r') as f:
    datos = json.load(f)
    for item in datos["top_scores"]:
        scores.append(item)

#Juego
fotos = 5
tiempo_juego = 15000
tiempo_restante = tiempo_juego
puntos = 0
astros_encontrados = []
MAX_ASTROS = 12
camara = pygame.sprite.GroupSingle()
camara.add(Camara(ancho, alto))

EVENTO_NUEVO_ASTRO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_NUEVO_ASTRO, 5000)

#Astros
astros = []
with open("data/astros.json", "r") as f:
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_actual = ESTADO_JUGANDO
                tiempo_restante = tiempo_juego
                puntos = 0
                nombre_jugador = ""
                astros_encontrados.clear()
                astros_grupo = pygame.sprite.Group()
                for astro in astros:
                    astros_grupo.add(Astro(astro))
                for _ in range(9):
                    astros_grupo.add(Astro({"nombre": "Estrella", "puntos": 50, "texto": "Brilla"}))
        
        elif estado_actual == 'jugando':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                astro_encontrado = tomar_foto()
                if astro_encontrado:
                    if astro_encontrado.nombre == "Estrella":
                        tiempo_restante += 3000
                    agregar_puntos(100 if astro_encontrado.nombre != "Estrella" else 50)
            
            if tiempo_restante <= 0:
                estado_actual = ESTADO_GAMEOVER
            
            if event.type == EVENTO_NUEVO_ASTRO:
                astros_grupo.add(Astro({"nombre": "Estrella", "puntos": 50, "texto": "Brilla en el cielo"}))
        
        elif estado_actual == ESTADO_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif event.key == pygame.K_RETURN and len(nombre_jugador) > 0:
                    guardar_score(nombre_jugador, puntos)
                    nombre_jugador = ""
                    estado_actual = ESTADO_MENU
                elif len(nombre_jugador) < 10:
                    char = pygame.key.name(event.key)
                    if char.isalnum():
                        nombre_jugador += char.upper()
    
    if estado_actual == 'menu':
        mostrar_menu()
    
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
        
        timer_texto = fuente_normal.render(f"Tiempo: {tiempo_restante // 1000}s", False, (255, 255, 255))
        puntos_texto = fuente_normal.render(f"Puntos: {puntos}", False, (255, 255, 255))
        pantalla.blit(timer_texto, (20, 20))
        pantalla.blit(puntos_texto, (20, 60))
        
        camara.draw(pantalla)
        camara.update()

        pos_v = camara.sprite.rect.center
        for astro in astros_grupo:
            astro.update_visual(pos_v)
        
        astros_grupo.draw(pantalla)
        astro_actual = colision()
        
    pygame.display.update()
    clock.tick(60)