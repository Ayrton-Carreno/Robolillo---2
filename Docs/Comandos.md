# 📖 Comandos — Robolillo 2.0

El prefijo del bot es `$`

> Los nombres anteriores en español (`$chiste`, `$dado`, `$cola`, `$ayuda`...) siguen funcionando como alias.

---

## 🎵 Música
> Únete a un canal de voz antes de usar estos comandos.

| Comando | Descripción |
|---------|-------------|
| `$join` | Unirse al canal de voz |
| `$leave` | Salir del canal de voz |
| `$play <canción>` | Reproduce o agrega a la cola |
| `$pause` | Pausar la música |
| `$resume` | Reanudar la música |
| `$stop` | Detener y limpiar la cola |
| `$skip` | Saltar canción |
| `$queue` | Ver la cola de reproducción |
| `$loop` | Activar/desactivar repetir |
| `$clear` | Vaciar la cola |

---

## 📥 Descargas
> Límite: 25 MB y 10 minutos de duración.

| Comando | Descripción |
|---------|-------------|
| `$download <url>` | Abre el panel interactivo de descarga |

**Plataformas soportadas:** YouTube, Instagram, TikTok y más.

**Opciones del panel:**
- 🎬 Video en 720p o 1080p
- 🎵 Solo audio en MP3

---

## 🎮 Diversión

| Comando | Descripción |
|---------|-------------|
| `$joke` | Chiste aleatorio (ES/EN/Chuck Norris) |
| `$joke es` | Chiste en español |
| `$joke en` | Chiste en inglés |
| `$joke chuck` | Chiste de Chuck Norris |
| `$dice <caras>` | Tirar un dado (default: 6 caras) |
| `$coin` | Lanzar una moneda |
| `$funny` | Menciona a un miembro aleatorio como chistoso |
| `$youre_funny @usuario` | Menciona a alguien específico como chistoso |
| `$who <pregunta>` | Elige un miembro aleatorio para responder |

---

## 🎲 Juegos

| Comando | Descripción |
|---------|-------------|
| `$rps` | Piedra Papel Tijeras vs bot |
| `$tor @usuario` | Verdad o Reto |
| `$insult @usuario` | Insulto gracioso aleatorio |
| `$ship @u1 @u2` | Calcula la compatibilidad entre dos personas |
| `$versus @u1 @u2` | Decide quién ganaría en distintos contextos |
| `$trivia` | Pregunta de trivia con categorías |
| `$connect4` | Jugar Conecta 4 vs bot |

**Categorías de trivia:**
- 🎮 Videojuegos
- 🎬 Películas
- 📺 Series
- 🎌 Anime
- 🎵 Música
- 🔬 Ciencia
- 🏆 Deportes
- 🌍 Geografía
- 🎭 General

---

## 🔨 Moderación
> Requiere permisos de administrador.

| Comando | Descripción |
|---------|-------------|
| `$kick @usuario <razón>` | Expulsar miembro del servidor |
| `$ban @usuario <razón>` | Banear miembro del servidor |
| `$purge <cantidad>` | Borrar mensajes del canal (default: 5) |

---

## 🌐 Idioma

| Comando | Descripción |
|---------|-------------|
| `$language` | Ver idioma actual |
| `$language es` | Cambiar tu idioma a español |
| `$language en` | Cambiar tu idioma a inglés |
| `$language es server` | Cambiar idioma del servidor a español (admin) |
| `$language en server` | Cambiar idioma del servidor a inglés (admin) |

---

## 🤖 IA
> Requiere API Key de Anthropic configurada en `.env`.

| Comando | Descripción |
|---------|-------------|
| `$ask <pregunta>` | Pregúntale a Claude |

---

## ❓ Ayuda

| Comando | Descripción |
|---------|-------------|
| `$help` | Abre el menú interactivo de ayuda |
| `$help <comando>` | Muestra qué hace un comando, cómo se usa y sus alias |