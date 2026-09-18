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
│   └── translations.py
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

## 🐛 Reportar bugs
Abre un **Issue** en GitHub con:
- Descripción del bug
- Pasos para reproducirlo
- Error que aparece en la terminal

---

## 👥 Contribuidores
- **Ayrton** — Desarrollo principal
- **Quetziko** — Colaborador