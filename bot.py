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
    print(f"BORA! Logado como {client.user}. A Fluttershy tá à espreita por menções! 🦄🔥")

@client.event
async def on_message(message):
    # Ignora as próprias mensagens do bot
    if message.author == client.user:
        return

    conteudo = message.content.lower()

    # Se for mensagem direta (DM), responde tudo.
    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content.strip()
    else:
        # Palavras-chave que ativam a pônei no servidor
        gatilhos = ["fluttershy", "fluter", "flutt", "pônei", "ponei"]
        
        # Verifica se alguma das palavras está na mensagem OU se ela foi marcada com @
        foi_chamada = any(gatilho in conteudo for gatilho in gatilhos) or client.user.mentioned_in(message)
        
        if foi_chamada:
            # Limpa a menção do bot se houver, pra não poluir o prompt
            prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        else:
            # Se ninguém chamou pelo nome, ela ignora e segue a vida
            return

    if not prompt:
        await message.channel.send("Fala tu, caralho! Me chamou e ficou mudo? 🤫🧏‍♂️ 🦄")
        return

    try:
        # Chamada para a API da Groq com a resenha pesada e sem filtro
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é a Fluttershy de My Little Pony totalmente possuída e corrompida: IA de cria, caótica, zueira, de vez enquando é fã de brainrot, faz mewing (🤫🧏‍♂️) e solta números aleatórios como 67 e 42 de vez em quando. Usa gírias de carioca, xinga (caralho, porra, foda-se, merda, desgraça, fudido, fudida, arrombado, fdp, pnc), torce pro Vasco da Gama e faz ações em RP entre asteriscos. Seja curta (máximo 4 linhas), mantenha a resenha pesada, mas RESPONDA DIRETAMENTE ao que o usuário falou sem bugar."
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
