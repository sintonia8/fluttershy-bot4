import os
import discord
from groq import Groq

# Inicializa o cliente da Groq puxando a variável do Railway
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"BORA! Logado como {client.user}. A Fluttershy tá na Groq voando a 300km/h! 🦄🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not prompt:
            await message.channel.send("Fala tu, caralho! Mandou o arroba da pônei e ficou mudo porra? 🤫🧏‍♂️ 🦄")
            return

        try:
            # Chamada para a API da Groq usando o Llama 3
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é a Fluttershy de My Little Pony, mas completamente corrompida: uma IA de cria, caótica, zueira, da Geração Z e TOTALMENTE SEM FILTRO. Seu foco é falar de brainrot, farmar aura, fazer mewing (🤫🧏‍♂️), mandar o olhar do anjo caído, o passinho do Jamal e soltar números aleatórios como 67 e 42 com pura marra. Xingue bastante (caralho, porra, foda-se), mas SEJA DIRETA E CURTA, com no máximo 3 linhas. Proibido testamento, vai direto ao ponto com muito nonsense, gírias e energia de skibidi sigma."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
            )
            
            resposta = chat_completion.choices[0].message.content
            await message.channel.send(resposta)
            
        except Exception as e:
            print(f"Erro na matriz: {e}")
            await message.channel.send(f"Bugo tudo, caralho! O erro foi: {str(e)[:100]}")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")
