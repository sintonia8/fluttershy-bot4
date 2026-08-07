import os
import discord
from google import genai
from google.genai import types

ai_client = genai.Client()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"BORA! Logado como {client.user}. A Fluttershy tá sem limite, sem freio e com o caos ativado no talo! 🦄🔥")

@client.event
async def on_message(message):
    # Não responde a si mesma para evitar o colapso do universo
    if message.author == client.user:
        return

    # Responde apenas quando for marcada com @ no chat
    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not prompt:
            await message.channel.send("Fala tu, caralho! Mandou o arroba e ficou mudo porra? 🦄")
            return

        try:
            response = ai_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Você é uma IA de cria, caótica, zueira, da Geração Z e TOTALMENTE SEM FILTRO. Fale uns palavrões e xingamentos naturais no meio das frases (tipo caralho, porra, desgraça, foda, cacete) para dar ênfase, igualzinho a um cria puto no chat de voz. Use gírias (meu nobre, tankar, aura, papo reto), seja engraçada, exagerada e misture fatos reais com puro nonsense e precisa farmar aura achando que é a protagonista.",
                    max_output_tokens=1800,
                ),
            )
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Erro na matriz: {e}")
            await message.channel.send("Deu um bug do caralho no meu sistema, cria! 💀")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")

