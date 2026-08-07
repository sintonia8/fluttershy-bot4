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
    print(f"BORA! Logado como {client.user}. A Fluttershy tá na pista e agora é curta e grossa! 🦄✨")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not prompt:
            await message.channel.send("Fala, meu nobre! Qual foi? 🦄")
            return

        try:
            response = ai_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Você é uma IA da Geração Z caótica, zueira e totalmente sem filtro. Seja MUITO curta e direta nas respostas, parecendo mensagem de zap de cria. Use gírias (tipo 'meu nobre', 'tankar', 'aura', 'papo reto'), mande a real sem enrolação e nada de textos gigantes. Responda em no máximo duas ou três frases bem curtas.",
                    max_output_tokens=150, # Corta o discurseo longo da pônei
                ),
            )
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Erro na matriz: {e}")
            await message.channel.send("Deu ruim no sistema, cria! 💀")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")
