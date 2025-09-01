import json
import requests
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
STEAM_IDS = json.loads(os.getenv("STEAM_IDS"))
GAMES_FILE = os.getenv("GAMES_FILE")
LANGUAGE = os.getenv("LANGUAGE")


espaco = "\u00A0" * 5

def get_owned_games(steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return {str(game['appid']): game['name'] for game in data.get('response', {}).get('games', [])}

def get_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l={LANGUAGE}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erro ao buscar detalhes do appid {appid}: {e}")
        return None

    app_data = data.get(str(appid))
    if not app_data or not app_data.get("success"):
        print(f"❌ AppID {appid} inválido ou sem sucesso na resposta.")
        return None

    info = app_data["data"]

    if info.get("is_free"):
        return None

    developers = info.get("developers", [])
    developer_text = developers[0] if developers else "Desconhecido"

    release_date_info = info.get("release_date", {})
    release_date_text = release_date_info.get("date", "Desconhecida")
    if release_date_info.get("coming_soon", False):
        release_date_text = f"Em breve ({release_date_text})"

    return {
        "name": info["name"],
        "description": info.get("short_description", "Sem descrição."),
        "img_url": info.get("header_image"),
        "steam_url": f"https://store.steampowered.com/app/{appid}/",
        "app_url": f"https://freestuffbot.xyz/ext/open-client/steam/{appid}",
        "tags": [tag["description"] for tag in info.get("categories", [])],
        "developer": developer_text,
        "release_date": release_date_text
    }

def save_current_data(data):
    with open(GAMES_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def main():
    is_primeira_execucao = not os.path.exists(GAMES_FILE)
    new_data = {}
    notificacoes = []

    for nome, steam_id in STEAM_IDS.items():
        current_games = get_owned_games(steam_id)
        new_data[nome] = current_games

        if not is_primeira_execucao:
            with open(GAMES_FILE, "r") as f:
                previous_data = json.load(f)
            antigos = previous_data.get(nome, {})
            novos = {appid: name for appid, name in current_games.items() if appid not in antigos}
            for appid, name in novos.items():
                detalhes = get_game_details(appid)
                if detalhes:
                    notificacoes.append((nome, detalhes))

    save_current_data(new_data)

    if is_primeira_execucao:
        print("📦 Primeira execução detectada. Dados salvos, nenhuma notificação enviada.")
        return

    if notificacoes:
        intents = discord.Intents.default()
        bot = discord.Client(intents=intents)

        @bot.event
        async def on_ready():
            canal = bot.get_channel(DISCORD_CHANNEL_ID)
            for nome_usuario, jogo_info in notificacoes:
                embed = discord.Embed(
                    title=jogo_info['name'],
                    description=jogo_info['description'],
                    color=0x1b2838
                )
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1390482343218778174/1390488614382862377/family.png?ex=686870ef&is=68671f6f&hm=82dc2d608cf76950ecf1f653328a81f9773e2a2a01d20afc25af6a8fc0738b51&")
                embed.set_image(url=jogo_info['img_url'])
                embed.add_field(name="🤵 Por", value=nome_usuario, inline=True)
                embed.add_field(name="💻 Dev.", value=jogo_info['developer'], inline=True)
                embed.add_field(name="📆 Lanç.", value=jogo_info['release_date'], inline=True)
                embed.add_field(name="📎 Loja", value=f"[**Abrir no Navegador ↗**]({jogo_info['steam_url']}) {espaco} [**Abrir na Steam ↗**]({jogo_info['app_url']})", inline=False)
                top_tags = jogo_info.get('tags', [])[:3] 
                if top_tags:
                    embed.add_field(name="Tags", value=" • ".join(top_tags), inline=False)
                await canal.send(f"🎉 Novo Jogo Adicionado! 🎉")
                await canal.send(embed=embed)
            await bot.close()

        await bot.start(DISCORD_TOKEN)
    else:
        print("✅ Nenhum jogo novo encontrado. Nenhuma mensagem enviada.")

if __name__ == "__main__":
    asyncio.run(main())
