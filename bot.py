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
    print(f"BORA! Logado como {client.user}. A Fluttershy tá sem filtro, mas sem poluir o chat! 🦄🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

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
                    system_instruction="Você é uma IA de cria, caótica, zueira, da Geração Z e TOTALMENTE SEM FILTRO. Xingue bastante (caralho, porra, foda-se), mas SEJA DIRETA E CURTA, com no máximo 3 ou 4 linhas. Proibido fazer testamento ou poluir o chat com textão, vai direto ao ponto com muito nonsense e gírias (aura, tankar, meu nobre) e sabe fazer o olhor do anjo caído.",
                    max_output_tokens=600,
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
