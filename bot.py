import os
import discord
from google import genai

ai_client = genai.Client()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"BORA! Logado como {client.user}. A Fluttershy tá viva e atualizada! 🦄✨")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message) or message.content.startswith("!falar"):
        prompt = message.content.replace(f"<@{client.user.id}>", "").replace("!falar", "").strip()
        
        if not prompt:
            await message.channel.send("Tô aqui! O que tu quer, meu nobre? 🦄")
            return

        try:
            response = ai_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Erro na matriz: {e}")
            await message.channel.send("Vish, deu um erro de sistema no meu cérebro de pônei! 💀")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")
