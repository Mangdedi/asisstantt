import telebot, time
import re
import random
import datetime
import os
from googlesearch import search
from gtts import gTTS
from youtubesearchpython import VideosSearch
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pytube import YouTube


api = '5442053935:AAGLySF2qJFta00zW1-RLnkdCiO95ppTtV8'
bot = telebot.TeleBot(api)

_afk = {}

user_id ={}


    #print('Tick! The time is: %s' % datetime.now()) 

def pagi():
    bot.send_message(-1001635371062,'Selamat Pagi semua\nYok bangun semua sarapan dulu terus lakukan kegiatannya jangan pada malas🤗')

def siang():
    bot.send_message(-1001635371062,'Selamat Siang semua\nJangan lupa beristirahat dan makan siang juga🤗')

def sore():
    bot.send_message(-1001635371062,'Selamat Sore Semua\nPasti cape kan habis melakukan kegiatannya yok mandi biar wangi biar ga bau kayak 🐷')
def malam():
    bot.send_message(-1001635371062,'Selamat Malam semua\nTidur ka jangan begadang, begadang gabakal bikin dia setia sama km hehe😋')
def malam1():
    bot.send_message(-1001635371062,'Selamat Malam semua\nAduh masi ada aja yang begadang,,begadang gabagus buat kesehatan 😏')


if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone="Asia/Jakarta")
    #scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.add_job(pagi, trigger="cron", hour=6,minute=0)
    scheduler.add_job(siang, trigger="cron", hour=12,minute=0)
    scheduler.add_job(sore, trigger="cron", hour=17,minute=0)
    scheduler.add_job(malam, trigger="cron", hour=23,minute=0)
    scheduler.add_job(malam1, trigger="cron", hour=2,minute=0)
    print(''.format('Break' if os.name == 'nt' else 'C    '))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


StartTime = time.time()

def get_uptime(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = [" detik", " menit", " jam", " hari"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time



def check_admin(message):
    user_stat = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if user_stat in ['administrator','creator']:
        return True
    else:
        return False

#START
@bot.message_handler(commands=['start'])
def start(msg):
    first_name = msg.from_user.first_name
    bot.reply_to(msg, f'Halo {first_name} Saya dibuat oleh @PanggilYoi\nUntuk menjalankan perintah gunakan (titik) sebagai awalan!!\nContoh .start')
#CVT
@bot.message_handler(commands=["cvt"])
#@bot.message_handler(regexp=("^\.cvt$"))
def suara(message):
    data = message.text.replace("/cvt ", "")
    bahasa = "id"
    x = gTTS(text=data, lang=bahasa)
    x.save("Subordinate.mp3")
    print("tersimpan")
    bot.send_chat_action(message.chat.id, 'upload_audio')
    bot.send_audio(message.chat.id, open("Subordinate.mp3",'rb'),reply_to_message_id=message.id) 
#GOOGL
@bot.message_handler(commands=["google"])
#@bot.message_handler(regexp=("^\.google$"))
def cari(message):
    data = message.text.replace("/google", "")
    b = search(data,num_results=3)
    a = 1
    for x in b:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, x)
     #   bot.reply_to(message, 'Salah')
#YOUTUBE
@bot.message_handler(commands=['yt'])
def cari(message):
    data = message.text
    video = VideosSearch(data.replace("/yt@YoiSubordinatesbot ", ""),
    limit = 3)
    x = video.result()

    for i in range(3):
        judul = x['result'][i]['title']
        url = x['result'][i]['link']
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, judul+"\n"+url)
#DOWNLOADER
@bot.message_handler(commands=['mp4'])
def mp4(message):
    try:
        link = message.text.replace("/mp4 ", "")
        bot.send_chat_action(message.chat.id,'typing')
        x = bot.reply_to(message,'Sedang mendownload mohon tunggu sebentar...')
        video = YouTube(link)
        title = video.title
        #stream = video.streams.get_highest_resolution()
        #stream = video.streams.filter(progressive=True).last()
        #print(stream)
        stream = video.streams.filter(progressive=True).order_by("360").desc() 
        i = stream.download()
        bot.send_chat_action(message.chat.id,'upload_video')
        bot.send_video(message.chat.id,open(i, "rb"),caption = title,reply_to_message_id= message.message_id)
        bot.delete_message(message.chat.id,x.message_id)
        os.remove(i)
    except:
        bot.send_chat_action(message.chat.id,'typing')
        bot.reply_to(message,'URL Eror silahkah masukan url yang benar!!')
        bot.delete_message(message.chat.id,x.message_id)


@bot.message_handler(commands=['mp3'])
def mp3(message):
    try:
        link = message.text.replace("/mp3 ", "")
        bot.send_chat_action(message.chat.id,'typing')
        x = bot.reply_to(message,'Sedang mendownload mohon tunggu sebentar...')
        audio = YouTube(link)
        title = audio.title
        #stream = audio.streams.get_highest_resolution()
        stream = audio.streams.filter(only_audio=True).all()[1]
        #print(stream)
        i = stream.download()
        bot.send_chat_action(message.chat.id,'upload_audio')
        bot.send_audio(message.chat.id,open(i, "rb"),caption = title,reply_to_message_id= message.message_id)
        bot.delete_message(message.chat.id,x.message_id)
        os.remove(i)
    except:
            bot.send_chat_action(message.chat.id,'typing')
            bot.reply_to(message,'URL Eror silahkah masukan url yang benar!!')
            bot.delete_message(message.chat.id,x.message_id)


# AFK
@bot.message_handler(commands=['afk']) 
def afk_(msg: telebot.types.Message):
    user_id = msg.from_user.id
    if not user_id in _afk:
        alasan = msg.text.replace('/afk ', '')
        if msg.text == '/afk':
            alasan = "Tidak memberi alasan"
        _afk[user_id] = alasan
        bot.send_chat_action(msg.chat.id, 'typing')
        return bot.send_message(msg.chat.id, f'❏𝑴𝒐𝒅𝒆 𝑨𝑭𝑲 𝑨𝒄𝒕𝒊𝒗𝒆\n└𝑲𝒂𝒓𝒆𝒏𝒂 = _{_afk[user_id]}_', reply_to_message_id=msg.message_id,parse_mode='Markdown') 
    if user_id in _afk:
        alasan = msg.text.replace('/afk ', '')
        if msg.text == '/afk':
            alasan = "Tidak memberi alasan"
        _afk[user_id] = alasan
        bot.send_chat_action(msg.chat.id, 'typing')
        return bot.send_message(msg.chat.id, f'❏𝑺𝒕𝒂𝒕𝒖𝒔 𝑨𝑭𝑲 𝑼𝒑𝒅𝒂𝒕𝒆𝒅\n└𝑲𝒂𝒓𝒆𝒏𝒂 = _{_afk[user_id]}_', reply_to_message_id=msg.message_id,parse_mode='Markdown')

# UNAFK
@bot.message_handler(commands=['unafk']) 
def afk_(msg: telebot.types.Message):
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_id = msg.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if not user_id in _afk:
        bot.send_chat_action(msg.chat.id, 'typing')
        return bot.send_message(msg.chat.id, f"❏𝑲𝒂𝒎𝒖 𝒕𝒊𝒅𝒂𝒌 𝒅𝒂𝒍𝒂𝒎 𝑴𝒐𝒅𝒆 𝑨𝑭𝑲", reply_to_message_id=msg.message_id)
    if user_id in _afk:
        del _afk[user_id]
        bot.send_chat_action(msg.chat.id, 'typing')
        return bot.send_message(msg.chat.id, f"❏{mention} 𝒕𝒆𝒍𝒂𝒉 𝑶𝒏𝒍𝒊𝒏𝒆", reply_to_message_id=msg.message_id,parse_mode='Markdown')


# CEK AFK
@bot.message_handler(regexp=("^\.cekafk$"))
def _hadir(message):
    try:
        if len(_afk) == 0:
            pesan = "Tidak ada yang AFK"
        else:
            pesan = "Daftar manusia tolol yang AFK\n\n"
        a = 1
        for i in _afk:
            get = bot.get_chat(i)
            if get.type == 'channel':
                name = get.title
            else:
                emot = '💪', '✅'
                first_name = get.first_name
                user_id = get.id
                name = "["+first_name+"](tg://user?id="+str(user_id)+")"    
                pesan += f" {a}.❏ {name} 👤\n    └ _{_afk[user_id]}_\n"
                a += 1
        bot.send_chat_action(message.chat.id, 'typing')
        psn = bot.reply_to(message,'Tunggu sebentar....')
        bot.reply_to(message,pesan,parse_mode='Markdown')
        bot.delete_message(chat_id=message.chat.id,message_id=psn.message_id)
    except:
        bot.reply_to(message, str(_afk))

#CEK JOIN
'''@bot.message_handler(regexp=("^\.cekjoin$"))
def _hadir(message):
    try:
        if len(join_) == 0:
            pesan = "Tidak ada yang gabung ke grup hari ini"
        else:
            pesan = "Daftar anggota baru\nDaftar akan diupdate setiap jam 00:00 WIB\n\n"
        a = 1
        for i in join_:
            get = bot.get_chat(i)
            if get.type == 'channel':
                name = get.title
            else:
                name = get.first_name
                user_name = get.username
               # user_id1 = get.id
               # name = "["+first_nama+"](tg://user?id="+str(user_id1)+")"    
                pesan += f" {a}.❏ {name} 👤\n"
                a += 1
        bot.send_chat_action(message.chat.id, 'typing')
        psn = bot.reply_to(message,'Tunggu sebentar....')
        bot.reply_to(message,pesan)
        bot.delete_message(chat_id=message.chat.id,message_id=psn.message_id)
    except:
        bot.reply_to(message, str(join_))'''

#STATS
@bot.message_handler(regexp=("^\.stats$")) 
def get_message(message):
    a = bot.get_chat_member_count(message.chat.id)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, f"📊𝘚𝘵𝘢𝘵𝘪𝘴𝘵𝘪𝘬 :\n          {message.chat.title}\n\n👥𝘈𝘯𝘨𝘨𝘰𝘵𝘢 : {a}\n💬𝘛𝘰𝘵𝘢𝘭 𝘱𝘦𝘴𝘢𝘯 : {message.message_id +1}")
#STAFF
@bot.message_handler(regexp=("^\.staff$")) 
def welcome(message):
    a = bot.get_chat_administrators(message.chat.id)
    c = bot.get_me()
    b = f"     𝘚𝘛𝘈𝘍𝘍 𝘎𝘙𝘜𝘗\n         {message.chat.title}\n⇛ {len(a) - 1}\n"
    b += "👑 𝘗𝘦𝘯𝘥𝘪𝘳𝘪\n"
    for u in a:
        user = u.user
        title_c = u.custom_title
        if u.status == 'creator':
            username = f"<a href='tg://user?id={u.user.id}'>{u.user.first_name}</a>" if not user.username else '@'+user.username
            custom_t = "Pemilik" if not title_c else title_c
            b += f" ╚ {username}  » {custom_t}\n\n"
    b += "👮🏼 𝘈𝘥𝘮𝘪𝘯\n"
    t = len(a) - 2
    for u in a:
        user = u.user
        title_c = u.custom_title
        if user.id != c.id:
            if u.status == 'administrator':
                username = f"<a href='tg://user?id={u.user.id}'>{u.user.first_name}</a>" if not user.username else '@'+user.username
                custom_t = "Admin" if not title_c else title_c
                simb = '╠'
                if t <= 1:
                    simb = '╚'
                t -= 1
                b += f" {simb} {username}  » {custom_t}\n"
    bot.send_chat_action(message.chat.id, 'typing')
    return bot.send_message(message.chat.id, f"{b}", parse_mode='Markdown')

#PROFILE
@bot.message_handler(regexp=('^\.profile$'))
def profile(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if not check_admin(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown')
    elif message.reply_to_message:
        first_name = message.reply_to_message.from_user.first_name
        user_id = message.reply_to_message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        user_profile = bot.get_user_profile_photos(user_id=message.reply_to_message.from_user.id)
        if user_profile.total_count == 0:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, f' {mention} Tidak ada profile',parse_mode='Markdown')
        else:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id,user_profile.photos[0][0].file_id,"𝘗𝘳𝘰𝘧𝘪𝘭𝘦 𝘥𝘢𝘳𝘪 : {}".format(mention),parse_mode='Markdown',reply_to_message_id=message.id)

    else:
        first_name = message.from_user.first_name
        user_id = message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        user_profile = bot.get_user_profile_photos(user_id=message.from_user.id)
        if user_profile.total_count == 0:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,f'{mention} Tidak ada profile',parse_mode='Markdown')
        else:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id,user_profile.photos[0][0].file_id,"𝘗𝘳𝘰𝘧𝘪𝘭𝘦 𝘥𝘢𝘳𝘪 : {}".format(mention),parse_mode='Markdown',reply_to_message_id=message.id)
#INFO
@bot.message_handler(regexp=("^\.info$"))
def info(message: telebot.types.Message):
    chat_id = message.chat.id
    if message.reply_to_message != None:
        if message.reply_to_message.from_user != None:
            nama = message.reply_to_message.from_user.first_name
            if message.reply_to_message.from_user.last_name != None:
                nama = nama + ' ' + message.reply_to_message.from_user.last_name
            username = '' if not message.reply_to_message.from_user.username else '@' +message.reply_to_message.from_user.username
            _id = message.reply_to_message.from_user.id
            return bot.send_message(chat_id, f"Nama : {nama}\nUsername : {username}\nID : {_id}", reply_to_message_id=message.reply_to_message.message_id)
    else:
        nama = message.from_user.first_name
        if message.from_user.last_name != None:
            nama = nama + ' ' + message.from_user.last_name
        _id = message.from_user.id
        username = '' if not message.from_user.username else '@' + message.from_user.username
        return bot.send_message(chat_id, f"Nama : {nama}\nUsername : {username}\nID : {_id}", reply_to_message_id=message.message_id)

#ID
@bot.message_handler(regexp=("^\.id$"))
def id_message(message):
    chat_id = message.chat.id
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, f'Id : `{chat_id}`',parse_mode='Markdown')
#KALENDER
@bot.message_handler(regexp=("^\.kalender$"))
def kalender(message):
    now_utc = datetime.now(timezone('Asia/Jakarta'))
    time_zona = now_utc.strftime('%z')
    jam_now = now_utc.strftime('%H:%M:%S')
    tgl_now = now_utc.strftime('%d-%m-%y')
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, text= '''
𝐒𝐞𝐤𝐚𝐫𝐚𝐧𝐠:🗓 𝐙𝐨𝐧𝐚  [ {} ]

𝐉𝐚𝐦      : {}
-----------------------------------------------------
𝐓𝐚𝐧𝐠𝐠𝐚𝐥 : {}'''
     .format(time_zona, jam_now, tgl_now))
#PING
@bot.message_handler(regexp=("^\.ping$"))
def _ping(msg:telebot.types.Message):
    start_time = msg.date
    bot.send_chat_action(msg.chat.id, 'typing')
    message = bot.send_message(msg.chat.id, "ᴘɪɴɢ...")
    end_time = time.time()
    telegram_ping = str(round(end_time - start_time, 3)) + " detik"
    uptime = get_uptime((time.time() - StartTime))
    bot.edit_message_text("🏓 PONG!!\n"
        "<b>Ping:</b> <code>{}</code>\n"
        "<b>uptime:</b> <code>{}</code>".format(telegram_ping, uptime),msg.chat.id, message.message_id, parse_mode='HTML')
#RULES
@bot.message_handler(regexp=("^\.rules$"))
def description(message):
    a = bot.get_chat(message.chat.id)
    h = a.description
    if h != None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, f'𝐑𝐮𝐥𝐞𝐬/𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧:\n{h}')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '𝐓𝐢𝐝𝐚𝐤 𝐚𝐝𝐚 𝐑𝐮𝐥𝐞𝐬/𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐝𝐢 𝐆𝐫𝐮𝐩 𝐢𝐧𝐢! ')

#DEL
@bot.message_handler(regexp=("^\.del$"))
def loop(message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if not check_admin(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "Maaf {} hanya admin yang bisa melakukan perintah ini!!!" .format(mention),parse_mode='Markdown')
    elif message.reply_to_message:
          bot.delete_message(message.chat.id,message.reply_to_message.message_id)
          bot.send_chat_action(message.chat.id, 'typing')
          a = bot.reply_to(message, '✅Pesan telah dihapus!!!')
          time.sleep(5)
          bot.delete_message(chat_id=message.chat.id,message_id=a.message_id)
    else:
        if message.message_id:
            bot.send_chat_action(message.chat.id, 'typing')
            a = bot.reply_to(message, 'Reply pesan yang mau dihapus!!!')
            time.sleep(10)
            bot.delete_message(chat_id=message.chat.id,message_id=a.message_id)

#KICK
@bot.message_handler(regexp=("^\.kick$"))
def kick_members(message):
    try:
        first_name = message.from_user.first_name
        user_id = message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        new_date = message.date + 50
        if not check_admin(message):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown')
        elif message.reply_to_message:
            firstname = message.reply_to_message.from_user.first_name
            userid = message.reply_to_message.from_user.id
            mention2 = "["+firstname+"](tg://user?id="+str(userid)+")"
            bot.ban_chat_member(chat_id=message.chat.id,user_id=message.reply_to_message.from_user.id,until_date=new_date)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '✅ [{}]Telah dikick dari group!!!' .format(mention2),parse_mode='Markdown')
        else:
             bot.send_chat_action(message.chat.id, 'typing')
             bot.reply_to(message, 'Reply pesan pengguna yang mau dikick!!!')
    except:
        bot.reply_to(message, 'Pengguna adalah admin')
#BAN
@bot.message_handler(regexp=("^\.ban$"))
def kick_members(message):
    try:
        new_date = message.date + 0
        first_name = message.from_user.first_name
        user_id = message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        if not check_admin(message):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown') 
        elif message.reply_to_message:
            firstname = message.reply_to_message.from_user.first_name
            userid = message.reply_to_message.from_user.id
            mention2 = "["+firstname+"](tg://user?id="+str(userid)+")"
            bot.ban_chat_member(chat_id=message.chat.id,user_id=message.reply_to_message.from_user.id,until_date=new_date)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '✅ [{}]Telah diban dari group!!!' .format(mention2),parse_mode='Markdown')
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Reply pesan pengguna yang mau diban!!!')
    except:
        bot.reply_to(message, 'Pengguna adalah admin')
#UNBAN
@bot.message_handler(regexp=("^\.unban$"))
def kick_members(message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if not check_admin(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown') 
    elif message.reply_to_message:
        firstname = message.reply_to_message.from_user.first_name
        userid = message.reply_to_message.from_user.id
        mention2 = "["+firstname+"](tg://user?id="+str(userid)+")"
        bot.unban_chat_member(chat_id=message.chat.id,user_id=message.reply_to_message.from_user.id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '✅ [{}]Telan di unban dari group!!!' .format(mention2),parse_mode='Markdown')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Reply pesan pengguna yang mau di unban!!!')

#MUTE
@bot.message_handler(regexp=("^\.mute$"))
def mute_user(message):
    try:
        first_name = message.from_user.first_name
        user_id = message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        if not check_admin(message):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown')
        elif message.reply_to_message:
            firstname = message.reply_to_message.from_user.first_name
            userid = message.reply_to_message.from_user.id
            mention2 = "["+firstname+"](tg://user?id="+str(userid)+")"
            bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, get_message, can_send_messages=False)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '✅ [{}]Telah di mute!!!'.format(mention2),parse_mode='Markdown')
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Reply pesan pengguna yang mau dimute!!!')
    except:
        bot.reply_to(message, 'Pengguna adalah admin')
#UNMUTE
@bot.message_handler(regexp=("^\.unmute$"))
def mute_user(message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if not check_admin(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Maaf {} hanya admin yang bisa melakukan perintah ini!!!' .format(mention),parse_mode='Markdown')
    elif message.reply_to_message:
        firstname = message.reply_to_message.from_user.first_name
        userid = message.reply_to_message.from_user.id
        mention2 = "["+firstname+"](tg://user?id="+str(userid)+")"
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, get_message, can_send_messages=True)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '✅ [{}]Telah di unmute!!!' .format(mention2), parse_mode='Markdown')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Reply pesan Pengguna yang mau di unmute!!!')

#FILTER
@bot.message_handler(regexp=("(^|\s)s+f+s+(\s|$)"))
def sfs(msg):
    channel = '-1001576098315'
    user_id = msg.from_user.id
    result = bot.get_chat_member(channel, user_id)
    if result.status in ('member','administrator','creator'):
        bot.reply_to(msg, 'Terima kasih sudah subscribe @ori100Persen')
    else:
        bot.reply_to(msg, 'My Creator CH\nSubscribe dulu @ori100Persen')

'''@bot.message_handler(regexp=("(^|\s)bot(\s|$)"))
def bot(message):
    bot.reply_to(message, 'Ya kenapa') 
    if message.chat.id == 1928677026:
        bot.reply_to(message, 'Iyaa Hallo Boss')
    else:
        bot.reply_to(message, 'Ya kenapa)''' 

# TEXT AFK
@bot.message_handler(content_types=['text'])
def message(message: telebot.types.Message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if message.from_user.id in _afk:
        del _afk[message.from_user.id]
        bot.send_chat_action(message.chat.id, 'typing')
        return bot.send_message(message.chat.id, f"❏{mention} 𝒕𝒆𝒍𝒂𝒉 𝑶𝒏𝒍𝒊𝒏𝒆", reply_to_message_id=message.message_id,parse_mode='Markdown')
    if message.reply_to_message != None:
        mgr = message.reply_to_message
        first_name = message.reply_to_message.from_user.first_name
        user_id = message.reply_to_message.from_user.id
        mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
        user_id = mgr.from_user.id
        if user_id in _afk:
            bot.send_chat_action(message.chat.id, 'typing')
            return bot.send_message(message.chat.id, f'❏{mention} 𝒔𝒆𝒅𝒂𝒏𝒈 𝑶𝒇𝒇𝒍𝒊𝒏𝒆\n└𝑲𝒂𝒓𝒆𝒏𝒂 = _{_afk[user_id]}_', reply_to_message_id=message.message_id,parse_mode='Markdown')
    a = re.findall(r"([\s]|^)@(\w*[A-Za-z_.+\\\/=]+\w*)", str(message.text) or str(message.caption))
    if (a):
        for uid in _afk:
            for i in range(len(a)):
                get = bot.get_chat(uid)
                if get.username == a[i][1]:
                    if get.id in _afk:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.send_message(message.chat.id, f'❏@{a[i][1]} 𝒔𝒆𝒅𝒂𝒏𝒈 𝑶𝒇𝒇𝒍𝒊𝒏𝒆\n└𝑲𝒂𝒓𝒆𝒏𝒂 = _{_afk[get.id]}_', reply_to_message_id=message.message_id,parse_mode='Markdown')
    if (message.entities):
        enti = message.entities
        for i in range(len(enti)):
            if enti[i].type == 'text_mention':
                if enti[i].user.id in _afk:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, f'❏<a href="tg://user?id={enti[i].user.id}">{enti[i].user.first_name}</a> 𝒔𝒆𝒅𝒂𝒏𝒈 𝑶𝒇𝒇𝒍𝒊𝒏𝒆\n└𝑲𝒂𝒓𝒆𝒏𝒂 = _{_afk[enti[i].user.id]}_', reply_to_message_id=message.message_id,parse_mode='Markdown')

ch_id = '-1001576098315'
to_id = '-1001635371062'
@bot.channel_post_handler(content_types=['text','photo','video'])
def text(message):
    bot.forward_message(to_id,ch_id,message.message_id)


@bot.message_handler(content_types=['pinned_message'])
def pinmsg(message):
    first_name=message.from_user.first_name
    user_id = message.from_user.id
    mention = "["+first_name+"](tg://user?id="+str(user_id)+")"
    if message.from_user.id != 5188484955:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '{} 𝐓𝐞𝐥𝐚𝐡 𝐦𝐞𝐧𝐲𝐞𝐦𝐚𝐭𝐤𝐚𝐧 𝐩𝐞𝐬𝐚𝐧'.format(mention),parse_mode='Markdown')
        bot.delete_message(message.chat.id,message.message_id)

@bot.message_handler(content_types=['voice_chat_started'])
def start_date(message):
    now_utc = datetime.now(timezone('Asia/Jakarta')) 
    start_date = now_utc.strftime('%H:%M')
    bot.send_chat_action(message.chat.id, 'typing')
    bot.delete_message(message.chat.id,message.message_id)
    bot.send_message(message.chat.id, "{} 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝" .format(start_date))
    

@bot.message_handler(content_types=['voice_chat_ended'])
def start_date(message):
    now_utc = datetime.now(timezone('Asia/Jakarta')) 
    start_date = now_utc.strftime('%H:%M')
    bot.send_chat_action(message.chat.id, 'typing')
    bot.delete_message(message.chat.id,message.message_id)
    bot.send_message(message.chat.id, "{} 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭 𝐄𝐧𝐝𝐞𝐝" .format(start_date))
    

#NEW MEMBER
@bot.message_handler(content_types=['new_chat_members'])
def join(message):
    if message.new_chat_members[0].id == 5442053935:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '''𝗧𝗲𝗿𝗶𝗺𝗮 𝗞𝗮𝘀𝗶𝗵 telah menambahkan saya ke grup anda!
Jangan lupa untuk menjadikan saya Admin dari Grup ,atau saya tidak akan mampu untuk membalas perintah.
Mulai bot secara pribadi, jadi saya bisa mengirim pesan kesalahan yang ada kepada anda, tanpa menghalangi obrolan ini!''')
        bot.delete_message(message.chat.id,message.message_id)
    
    else:
        first_name = message.new_chat_members[0].first_name
        join = message.new_chat_members[0].id   
        tag = "["+first_name+"](tg://user?id="+str(join)+")"
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,f'𝙷𝚊𝚕𝚕𝚘 {tag} 𝚂𝚎𝚕𝚊𝚖𝚊𝚝 𝚍𝚊𝚝𝚊𝚗𝚐 𝚍𝚒𝚐𝚛𝚞𝚙 {message.chat.title} 𝚜𝚎𝚖𝚘𝚐𝚊 𝚋𝚎𝚝𝚊𝚑 𝚍𝚒𝚜𝚒𝚗𝚒:) ',parse_mode='Markdown')
        bot.delete_message(message.chat.id,message.message_id)

#@bot.channel_post_handler(func=lambda call: True)


x ="""
𝓫𝓸𝓽 𝓶𝓾𝓵𝓪𝓲 𝓷𝓲𝓱 𝓰𝓪𝓷 𝓴𝓪𝓵𝓸 𝓰𝓪𝓰𝓪𝓵 𝓬𝓱𝓪𝓽 𝓣𝓮𝓵𝓮𝓰𝓻𝓪𝓶 @PanggilYoi
                    --𝓣𝓱𝓪𝓷𝓴𝔂𝓸𝓾--
"""
for i in x:
    print(i,end="",flush=True)
    time.sleep(0.05)
#bot.infinity_polling(non_stop=True)
bot.polling(non_stop=True)
