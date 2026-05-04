# -*- coding: utf-8 -*-
import pygame
import urllib.request
import ssl
import os

pygame.init()

imagenes = [
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/3D_Mercury.png/618px-3D_Mercury.png', 'mercurio.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/3D_Venus.png/622px-3D_Venus.png', 'venus.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Earth_%28blank%29.png/500px-Earth_%28blank%29.png', 'tierra.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/3D_Mars.png/628px-3D_Mars.png', 'marte.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/3D_Jupiter.png/617px-3D_Jupiter.png', 'jupiter.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/3D_Saturn.png/1059px-3D_Saturn.png', 'saturno.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/3D_Uranus.png/605px-3D_Uranus.png', 'urano.png'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/3D_Neptune.png/616px-3D_Neptune.png', 'neptuno.png'),
]

for url, nombre in imagenes:
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = response.read()
            with open(f'assets/Graphics/{nombre}', 'wb') as f:
                f.write(data)
            print(f'Descargado: {nombre}')
    except Exception as e:
        print(f'Error {nombre}: {e}')

print('Listo!')