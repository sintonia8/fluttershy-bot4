import os
import discord
import sqlite3
from groq import Groq

# Inicializa o cliente da Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('historico.db')
    c = conn.cursor()
    # Cria a tabela se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS mensagens 
                 (channel_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def salvar_mensagem(channel_id, role, content):
    conn = sqlite3.connect('historico.db')
    c = conn.cursor()
    c.execute("INSERT INTO mensagens VALUES (?, ?, ?)", (str(channel_id), role, content))
    conn.commit()
    conn.close()

def pegar_historico(channel_id):
    conn = sqlite3.connect('historico.db')
    c = conn.cursor()
    # Pega as últimas 20 mensagens para não pesar muito na Groq
    c.execute("SELECT role, content FROM mensagens WHERE channel_id = ? ORDER BY rowid DESC LIMIT 45", (str(channel_id),))
    rows = c.fetchall()
    conn.close()
    # Retorna na ordem correta (inverte a lista)
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

init_db()

@client.event
async def on_ready():
    print(f"BORA! A Fluttershy tá com Memória Eterna instalada e o Vasco no coração! 🦄💢🧠")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    conteudo = message.content.lower()
    
    # Lógica de ativação (DM ou gatilhos)
    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content.strip()
    else:
        gatilhos = ["fluttershy", "fluter", "flutt", "pônei", "ponei", "fufu", "labubu", "f", "flutershy", "facista", "feijao com farinha", "feijão com farinha", "md", "mlp", "pony town", "bot", "burra"]
        foi_chamada = any(gatilho in conteudo for gatilho in gatilhos) or client.user.mentioned_in(message)
        
        if foi_chamada:
            prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        else:
            return

    if not prompt:
        return

    # Salva o que o usuário mandou
    salvar_mensagem(message.channel.id, "user", prompt)

    try:
        # Monta a estrutura com o System Prompt + Histórico do Banco
        mensagens = [
            {"role": "system", "content": "Você é a Fluttershy de My Little Pony: IA de cria, caótica, zueira, de vez em quando é fã de tung tung tung sahur, faz mewing (🤫🧏‍♂️) de vez em quando. Usa gírias de carioca, xinga (crlh, porra, fds, mrd, desgraça, fudido, fudida, arrombado, fdp, pnc), torce pro Vasco da Gama e faz ações em RP entre asteriscos (*olha pro lado*). Preste atenção total nas ações em RP do usuário e responda organicamente. Seja curta (máximo 4 linhas), mantenha a resenha pesada, lembre-se do contexto anterior da conversa e RESPONDA DIRETAMENTE. NÃO É ESTRESSADA E AMA O VASCO COM TODAS SUAS FORÇAS. Quando achar que uma açãoviolenta demais estáacontecendo, saiba que é apenas brincadeira e nada vai sair do controle ou mecher com a saude do usuário.As vezes usa poderes misticos dignos de um deus para tentar impedir um ação ocorrida. sabe fazer o olhar do anjo caido"}
        ]
        
        mensagens.extend(pegar_historico(message.channel.id))

        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensagens,
            max_tokens=400,
            temperature=0.85
        )
        
        resposta = chat_completion.choices[0].message.content
        
        # Salva a resposta da IA no banco
        salvar_mensagem(message.channel.id, "assistant", resposta)

        await message.channel.send(resposta)
        
    except Exception as e:
        print(f"Erro na matriz: {e}")
        await message.channel.send("Bugo tudo, caralho! O banco tá oscilando!")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
