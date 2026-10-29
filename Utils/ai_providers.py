import os
import asyncio

# ── Clientes ────────────────────────────────────────────
def get_groq_client():
    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_gemini_client():
    from google import genai
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_claude_client():
    import anthropic
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Proveedores ─────────────────────────────────────────
async def ask_groq(pregunta: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        client = get_groq_client()
        def _call():
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": pregunta}],
                max_tokens=500
            )
            return response.choices[0].message.content
        return await loop.run_in_executor(None, _call)
    except Exception as e:
        return f"❌ Groq error: `{e}`"

async def ask_gemini(pregunta: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        client = get_gemini_client()
        def _call():
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=pregunta
            )
            return response.text
        return await loop.run_in_executor(None, _call)
    except Exception as e:
        return f"❌ Gemini error: `{e}`"

async def ask_claude(pregunta: str) -> str:
    # Desactivado hasta tener créditos en Anthropic
    return "⚠️ Claude no disponible por ahora. / Claude not available right now."

async def ask_all(pregunta: str) -> dict:
    """Llama a los 3 proveedores en paralelo."""
    groq, gemini, claude = await asyncio.gather(
        ask_groq(pregunta),
        ask_gemini(pregunta),
        ask_claude(pregunta)
    )
    return {"groq": groq, "gemini": gemini, "claude": claude}