# ⚙️ Instalación — Robolillo 2.0

## 📋 Requisitos
- Python 3.10+
- FFmpeg instalado en el sistema
- Token de Discord
- API Key de Anthropic (opcional, para IA)

## 🚀 Pasos

### 1. Clona el repositorio
```bash
git clone https://github.com/Ayrton-Carreno/Robolillo---2.git
cd Robolillo---2
```

### 2. Instala dependencias
```bash
pip install -r requirements.txt
```

### 3. Instala FFmpeg
**Windows:**
```bash
winget install ffmpeg
```
Luego agrega FFmpeg al PATH del sistema.

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 4. Configura el archivo `.env`
Crea un archivo `.env` en la raíz del proyecto basándote en `ejemplo.env`:
```env
# Discord
DISCORD_TOKEN=tu_token

# IA
ANTHROPIC_API_KEY=tu_key

# APIs Fun
JOKEAPI_URL=https://v2.jokeapi.dev/joke
CHUCKNORRIS_URL=https://api.chucknorris.io/jokes/random

# APIs Juegos
OPENTDB_URL=https://opentdb.com/api.php

# APIs Recomendaciones (próximamente)
LASTFM_API_KEY=
RAWG_API_KEY=
TMDB_API_KEY=
UNSPLASH_API_KEY=
```

### 5. Configura el bot en Discord Developer Portal
1. Ve a [discord.com/developers](https://discord.com/developers)
2. Crea una aplicación o usa la existente
3. En **Bot** activa estos intents:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
4. En **OAuth2** genera una URL con estos permisos:
   - Scopes: `bot`, `applications.commands`
   - Permisos: Ver canales, Enviar mensajes, Gestionar mensajes, Adjuntar archivos, Conectarse, Hablar, Expulsar miembros, Banear miembros

### 6. Corre el bot
```bash
python main.py
```

## 📁 Estructura del proyecto