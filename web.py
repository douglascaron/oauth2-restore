import asyncio, role, config
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from requests.api import get
from module import exchange_code, opendb, get_user_profile

app = FastAPI()

@app.get("/callback")
async def callback(code : str):
    exchange_res = await exchange_code(code)
    if exchange_code == False:
        return "Permission not granted"
    profile = await get_user_profile(exchange_res["access_token"])
    if profile == False:
        return "Permission not granted"
    con,cur = opendb()
    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?);", (profile["id"], exchange_res["refresh_token"]))
    con.commit()
    con.close()
    role.add_role(config.guildid,profile["id"], config.roleid)
    return RedirectResponse("https://discord.com/oauth2/authorized")
