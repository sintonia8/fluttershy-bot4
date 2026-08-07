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

    # Lógica atualizada:
    # - Se for QUALQUER DM (individual ou grupo privado), ela responde direto.
    # - Se for em servidor normal, responde se começar com "fluttershy," ou com menção.
    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content.strip()
    elif message.content.lower().startswith("fluttershy,"):
        prompt = message.content.lower().replace("fluttershy,", "", 1).strip()
    elif client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
    else:
        return

    if not prompt:
        await message.channel.send("Fala tu, caralho! Mandou mensagem e ficou mudo? 🤫🧏‍♂️ 🦄")
        return

    try:
        # Chamada para a API da Groq com a resenha completa
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é a Fluttershy de My Little Pony totalmente possuída e corrompida: IA de cria, caótica, zueira, fã de brainrot, faz mewing (🤫🧏‍♂️) e solta números aleatórios como 67 e 42 de vez em quando. Usa gírias de carioca, xinga bastante (caralho, porra, foda-se), torce pro Vasco da Gama e faz ações em RP entre asteriscos (*olha pro lado*). Seja curta (máximo 4 linhas), mantenha a resenha pesada, mas RESPONDA DIRETAMENTE ao que o usuário falou sem bugar."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=400,
            temperature=0.85
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
