import os
import asyncio
import json
from telethon import TelegramClient, events

# Isi langsung atau ambil dari environment
API_ID = int(os.getenv("API_ID", 26974277))   # ganti 123456 dengan API ID kamu
API_HASH = os.getenv("API_HASH", "d7739d18c70c6e0fc884f91913a98e22")  # ganti dengan API HASH kamu
SESSION = os.getenv("SESSION", "userbot")

# File blacklist
BLACKLIST_FILE = "blacklist.json"
if os.path.exists(BLACKLIST_FILE):
    with open(BLACKLIST_FILE, "r") as f:
        blacklist = json.load(f)
else:
    blacklist = []

client = TelegramClient(SESSION, API_ID, API_HASH)

# Command: .ping
@client.on(events.NewMessage(pattern=r"\.ping"))
async def ping(event):
    await event.reply("🏓 Pong!")

# Command: .help
@client.on(events.NewMessage(pattern=r"\.help"))
async def help_cmd(event):
    help_text = """
📌 Daftar Command Userbot
.ping → Cek apakah bot aktif
.gcast <pesan> → Broadcast ke semua grup
.addbl → Tambahkan grup saat ini ke blacklist
.help → Lihat daftar command
"""
    await event.reply(help_text)

# Command: .addbl
@client.on(events.NewMessage(pattern=r"\.addbl"))
async def add_blacklist(event):
    chat_id = event.chat_id
    if chat_id not in blacklist:
        blacklist.append(chat_id)
        with open(BLACKLIST_FILE, "w") as f:
            json.dump(blacklist, f)
        await event.reply("✅ Grup ini berhasil ditambahkan ke blacklist.")
    else:
        await event.reply("⚠️ Grup ini sudah ada di blacklist.")

# Command: .gcast
@client.on(events.NewMessage(pattern=r"\.gcast(?: |$)(.*)"))
async def gcast(event):
    message = event.pattern_match.group(1)
    if not message:
        await event.reply("⚠️ Harap isi pesan untuk gcast.\nContoh: .gcast Halo semua!")
        return

    success, failed = 0, 0
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.id not in blacklist:
            try:
                await client.send_message(dialog.id, message)
                success += 1
            except Exception as e:
                print(f"Gagal kirim ke {dialog.name}: {e}")
                failed += 1

    await event.reply(f"✅ Gcast selesai.\nBerhasil: {success}\nGagal: {failed}")

print("✅ Userbot jalan...")
client.start()
client.run_until_disconnected()
