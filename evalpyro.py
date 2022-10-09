import io
import sys
import os
import traceback
import asyncio
import time
from pyrogram import Client, filters
from subprocess import run as srun

own = [1928677026,2003696861]

app = Client(
    'my_account',
    api_id=18079109,
    api_hash="61150fac03232e1410262f87ee786c57",
    session_string=
    "BQAhIHQAHyslaSlvjBSYv8oDUWko3qHbd4BNtIMG89tdmsLfKl03yM9mPv6LU8zVTgB_UKz-mnafEamalxK-RfFK-y93UgOHxLGe2TK1ffkW6zEHH4LgeC6yBSDxx_H3LTIDb4kp6iLovt5dTiVS55gaMfsC-zwGff4nVaZzEukx_nx-CMq50T8HWzZ8C9ZdytyTRj2yAFpX0PBMwmENmK6-bAB42SB5k8eJGwfhoD9I-3BOoz4prK2r8NOGwMQJ8MUk3sCU1DFCzErQaf62H8EWULzu02KnDVNJs1hO3sV0qiEXh_dWwXWe8iQ3jCQFrFNSJ7Yf081pN2UhlqP4AISYlRV9ggAAAAFMnTVyAA"
)
#bot_token = "5629734337:AAHDeT11D-QI4SQROP7hGKIo9f3jNWkH-4Y")

@app.on_message(filters.regex("^\.q$"))
async def q(client, message):
  try:
    if message.reply_to_message:
        text = message.reply_to_message.text
        quot = await app.forward_messages("@QuotLyBot", message.chat.id, message.reply_to_message.id)
        a = await message.reply("`Sedang generate sticker text...`",quote=True)
        time.sleep(4)
        await a.delete()
        await app.copy_message(message.chat.id, "@QuotLyBot", quot.id + 1,reply_to_message_id=message.id)
    else:
      await message.reply("`Silahkan reply pesan!!` ")
  except Exception as e:
    await message.reply(e)


@app.on_message(filters.command("balas") & filters.user(own) & filters.reply)
async def balas(client, m):
    pesan = m.text.split(' ', 1)
    await m.delete()
    await m.reply(pesan[1], reply_to_message_id=m.reply_to_message.id)


@app.on_message(filters.command("neofetch") & filters.user(own))
async def neofetch(client, m):
    neofetch = (await shell_exec("neofetch --stdout"))[0]
    await m.reply(f"<code>{neofetch}</code>")


@app.on_message(filters.command("remove"))
async def clearlocal(client, m):
    cmd = m.text.split(' ', 1)
    if len(cmd) == 1:
        return await m.reply('Give path file to delete.')
    remove = (await shell_exec(f"rm -rf {cmd[1]}"))[0]
    await m.reply("Done")


@app.on_message(
    filters.command("shell")
    & filters.user(own))
@app.on_edited_message(
    filters.command("shell")
    & filters.user(own))
async def shell(client, message):
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        return await message.reply('No command to execute was given.')
    shell = (await shell_exec(cmd[1]))[0]
    if len(shell) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(shell)
        with open('shell_output.txt', 'rb') as doc:
            await message.reply_document(document=doc, file_name=doc.name)
            try:
                os.remove('shell_output.txt')
            except:
                pass
    elif len(shell) != 0:
        await message.reply(shell)
    else:
        await message.reply('No Reply')


@app.on_message(filters.command("pyro") & filters.user(own))
@app.on_edited_message(
    filters.command("pyro")
    & filters.user(own))
async def eval(client, message):
    if len(message.command) < 2:
        return await message.reply("Masukkan kode yang ingin dijalankan..")
    status_message = await message.reply_text("Sedang Memproses Eval...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Berhasil"

    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "MissKaty_Eval.txt"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[:4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
            try:
                os.remove("MissKaty_Eval.txt")
            except:
                pass
    else:
        await reply_to_.reply_text(final_output, quote=True)
    await status_message.delete()


async def aexec(code, client, message):
    exec("async def __aexec(client, message): " +
         "".join(f"\n {l_}" for l_ in code.split("\n")))
    return await locals()["__aexec"](client, message)


async def shell_exec(code, treat=True):
    process = await asyncio.create_subprocess_shell(
        code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    stdout = (await process.communicate())[0]
    if treat:
        stdout = stdout.decode().strip()
    return stdout, process


print('Running')
app.run()
