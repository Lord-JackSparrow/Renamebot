from helper.progress import progress_for_pyrogram, TimeFormatter

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import os
import random
from PIL import Image
import time
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb
from helper.progress import humanbytes
from helper.set import escape_invalid_curly_brackets
import os

log_channel = int(os.environ.get("LOG_CHANNEL", "-1001753267608"))

API_ID = int(os.environ.get("API_ID", "24397477"))

API_HASH = os.environ.get("API_HASH", "d9b7b677552e995ed2945fe1bdea13d2")

STRING = os.environ.get("STRING", "")

ADMIN = os.environ.get("ADMIN", "1720319665")

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🧑‍💻 Oᴡɴᴇʀ Iɴғᴏ', callback_data='owner_info'),
            InlineKeyboardButton('📑 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ', callback_data='source')
        ],[
            InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/1c15be412eb886ba1c8e3.jpg")
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        await query.message.edit_text(
            text="╭───────────⍟\n├🤖 ᴍy ɴᴀᴍᴇ : File Renamer Bot\n├🤍 Dᴇᴠᴇʟᴏᴩᴇʀꜱ : IT'S LUFFY\n├👨‍💻 Pʀᴏɢʀᴀᴍᴇʀ : IT'S LUFFY\n├📕 Lɪʙʀᴀʀy : Pyʀᴏɢʀᴀᴍ\n├✏️ Lᴀɴɢᴜᴀɢᴇ: Pyᴛʜᴏɴ 3\n├💾 Dᴀᴛᴀ Bᴀꜱᴇ: Mᴏɴɢᴏ DB\n├📊 Bᴜɪʟᴅ Vᴇʀꜱɪᴏɴ: Rᴇɴᴀᴍᴇʀ V3.0.0\n╰───────────────⍟",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    chat_id = update.message.chat.id
    id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(f"»»——— 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙣𝙚𝙬 𝙛𝙞𝙡𝙚 𝙣𝙖𝙢𝙚...", reply_to_message_id=id,
                                    reply_markup=ForceReply(True))
    dateupdate(chat_id, date)


@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("`Trying To Download...`")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`༻☬ད𝘽𝙪𝙡𝙞𝙙𝙞𝙣𝙜 𝙈𝙚𝙩𝙖𝙙𝙖𝙩𝙖...`",  ms, c_time))

    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    try:
        c_caption = data[1]
    except:
        pass
    thumb = data[0]
    if c_caption:
        doc_list = ["filename", "filesize"]
        new_tex = escape_invalid_curly_brackets(c_caption, doc_list)
        caption = new_tex.format(
            filename=new_filename, filesize=humanbytes(file.file_size))
    else:
        caption = f"**{new_filename}**"
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()

    else:
        ph_path = None

    value = 2090000000
    if value < file.file_size:
        await ms.edit("`Trying To Upload`")
        try:
            filw = await app.send_document(log_channel, document=file_path, thumb=ph_path, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                pass
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                return
    else:
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_document(update.from_user.id, document=file_path, thumb=ph_path, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            return


@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("`Trying To Download...`")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`༻☬ད𝘽𝙪𝙡𝙞𝙙𝙞𝙣𝙜 𝙈𝙚𝙩𝙖𝙙𝙖𝙩𝙖...`",  ms, c_time))

    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    try:
        c_caption = data[1]
    except:
        pass
    thumb = data[0]

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(
            file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()

    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    value = 2090000000
    if value < file.file_size:
        await ms.edit("`Trying To Upload`")
        try:
            filw = await app.send_video(log_channel, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                pass
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                return
    else:
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_video(update.from_user.id, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            return


@Client.on_callback_query(filters.regex("aud"))
async def aud(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    ms = await update.message.edit("`Trying To Download...`")
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`༻☬ད𝘽𝙪𝙡𝙞𝙙𝙞𝙣𝙜 𝙈𝙚𝙩𝙖𝙙𝙖𝙩𝙖...`",  ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1]
    thumb = data[0]
    if c_caption:
        aud_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, aud_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(
            file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, thumb=ph_path, duration=duration, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
            os.remove(ph_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            os.remove(ph_path)
    else:
        await ms.edit("`Trying To Upload`")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, duration=duration, progress=progress_for_pyrogram, progress_args=("`Trying To Uploading`",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            await ms.edit(e)
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            os.remove(file_path)


# 
#  LazyDeveloperr
# 
