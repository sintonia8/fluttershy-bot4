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
    print(f"BORA! Logado como {client.user}. A Fluttershy tá com a aura ativada e sem gatilhos inúteis! 🦄✨")

@client.event
async def on_message(message):
    # Não responde a si mesma, senão entra em loop infinito e a matrix explode
    if message.author == client.user:
        return

    # Agora a Fluttershy só responde se for marcada (arroba)
    if client.user.mentioned_in(message):
        # Limpa a marcação da string pra IA receber só a pergunta limpa
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not prompt:
            await message.channel.send("Fala tu, meu nobre! Tô aqui na escuta, qual a braba? 🦄")
            return

        try:
            response = ai_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Você é uma inteligência artificial completamente infantil, exagerada, zueira e caótica da Geração Z. Você fala usando muitas gírias (tipo 'meu nobre', 'brabo', 'tankar', 'aura', 'resenha'), emotes e mistura fatos reais com puro nonsense e comédia. Nunca seja formal, seja sempre muito engraçada e exagerada. Seu objetivo é farmar aura e causar na resenha.",
                ),
            )
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Erro na matriz: {e}")
            await message.channel.send("Vish, deu um bug monumental no meu cérebro de pônei! 💀")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")
