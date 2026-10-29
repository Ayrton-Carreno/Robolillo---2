# 🤝 Contribuir — Robolillo 2.0

¡Gracias por querer contribuir a Robolillo! Aquí están las reglas y flujo de trabajo.

---

## 📋 Reglas generales
- Código en **inglés** (variables, funciones, archivos)
- Comentarios en **español o inglés**
- Sin código espaguetti — si un archivo supera 300 líneas, considera dividirlo
- Nunca subas el `.env` al repositorio
- Siempre trabaja en tu rama, nunca directo en `main`

---

## 🌿 Estructura de ramas
main                    ← Producción estable
├── pre-main            ← Testing antes de subir a main
├── fun                 ← Comandos de diversión
├── games               ← Juegos
├── menus               ← UI y ayuda
├── profiles_preference ← Perfiles y actividad
└── tuNombre_avances    ← Tus experimentos personales

---

## 🚀 Flujo de trabajo

### 1. Trabaja en tu rama
```bash
git checkout tu_rama
# haz tus cambios
git add .
git commit -m "Descripción del cambio"
git push origin tu_rama
```

### 2. Mergea a pre-main para probar
```bash
git checkout pre-main
git merge tu_rama --no-edit
git push origin pre-main
```

### 3. Cuando esté listo, mergea a main
```bash
git checkout main
git merge pre-main --no-edit
git push origin main
```

---

## 📁 Estructura del proyecto
Robolillo - 2/
├── main.py             ← Núcleo del bot
├── .env                ← Variables de entorno (no subir)
├── .gitignore
├── README.md
├── requirements.txt
├── ejemplo.env         ← Plantilla del .env
├── cogs/               ← Módulos del bot
│   ├── music.py
│   ├── fun.py
│   ├── games.py
│   ├── downloads.py
│   ├── moderation.py
│   ├── help.py
│   └── ai.py
├── utils/              ← Funciones compartidas
│   ├── translation.py  ← Carga los idiomas y la función t()
│   └── lang/           ← Un JSON por idioma
│       ├── es.json
│       └── en.json
├── docs/               ← Documentación
│   ├── INSTALLATION.md
│   ├── COMMANDS.md
│   └── CONTRIBUTING.md
├── data/               ← Base de datos SQLite
├── logs/               ← Logs del bot
└── assets/             ← Imágenes y recursos

---

## ✅ Buenas prácticas

### Nombrar commits
"Agrego comando $trivia"
"Corrijo bug en cola de música"
"Actualizo sistema de idiomas"
"Refactorizo downloads.py"

### Nombrar funciones y variables
```python
# ✅ Bien
async def get_song_info(query: str) -> dict:
    song_queue = []

# ❌ Mal
async def obtenerCancion(q):
    cola = []
```

### Estructura de un cog
```python
import discord
from discord.ext import commands

class NombreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Cog NombreCog inicializado")

    @commands.command()
    async def comando(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(NombreCog(bot))
```

---

## 🌐 Agregar un idioma
Los textos del bot viven en `Utils/lang/`, un archivo JSON por idioma. El bot carga todos los `.json` de esa carpeta al iniciar.

1. Copia `Utils/lang/es.json` y renómbralo con el código del idioma (ej. `pt.json`, `fr.json`).
2. Cambia `"nombre_idioma"` (ej. `"Português 🇧🇷"`) y traduce los textos.
   - **No cambies las claves** (lo de la izquierda), solo los valores.
   - Deja intactos los `{placeholders}` como `{usuario}` o `{titulo}`.
3. Reinicia el bot. El idioma aparece en `$language` y se activa con `$language pt`.

Si a tu archivo le falta alguna clave, el bot usa el texto en español para esa clave, así que puedes traducir poco a poco.

Para agregar un **texto nuevo**, ponlo en `es.json` (obligatorio) y en los demás idiomas, y úsalo con `t(idioma, "mi_clave")`.

---

## 🐛 Reportar bugs
Abre un **Issue** en GitHub con:
- Descripción del bug
- Pasos para reproducirlo
- Error que aparece en la terminal

---

## 👥 Contribuidores
- **Ayrton** — Desarrollo principal
- **Quetziko** — Colaborador