# 🤖 Robolillo 2.0

Bot de Discord con música, descargas, moderación e IA.

## Funciones
- 🎵 Música con cola de reproducción
- 📥 Descargas de YouTube, Instagram y TikTok
- 🎮 Comandos de diversión
- 🔨 Moderación
- 🤖 IA con Claude

## Instalación
1. Clona el repositorio
2. Instala dependencias:
pip install discord.py[voice] yt-dlp python-dotenv anthropic
3. Crea tu `.env` basándote en `ejemplo.env`
4. Corre el bot:
python "Robolillo - 2.py"

## Comandos
### 🎵 Música
- `!play` — Reproduce o agrega a la cola
- `!skip` — Salta canción
- `!cola` — Ver cola
- `!loop` — Repetir
- `!pause` / `!resume` / `!stop`

### 📥 Descargas
- `!descargar <url>` — Panel interactivo

### 🎮 Diversión
- `!hola` `!dado` `!moneda` `!chiste` `!chistoso` `!gay`

### 🔨 Moderación
- `!kick` `!ban` `!limpiar`

### 🤖 IA
- `!ask` — Pregúntale a Claude