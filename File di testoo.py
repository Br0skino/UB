 
"""
Edit This
"""
apiId = 993290
apiHash = "xtpcehdqg9fxnutlkmjut1abewezf5yc"

# These are NOT valid apiId and apiHash but they are in the correct format.
# Take your apiId and apiHash from my.telegram.org/

"""
Afk message. {original_msg} is the text
of message sent by the user
"""
afkMessage = "Sorry, I'm currently unavaible.\n" \
             "Your message got saved here:\n" \
             "\n" \
             "{original_msg}\n" \
             "\n" \
             "Only one message in every 30 seconds will be saved.\n" \
             ""

"""
Boring stuff
"""

import sys

if sys.version_info.major != 3:
    raise Exception("You need python 3")
elif sys.version_info.minor < 7:
    print("You should use python 3.7 or higher.\n")
import os
import time
from datetime import datetime
from pathlib import Path
import requests
from pyrogram import Client, Filters, Emoji
from pyrogram.errors import *

users = {}
afk = False
accepted_users = []
banned_users = []
bot = Client(
    "Session_MultiUserbot",
    api_id=apiId,
    api_hash=apiHash)


@bot.on_message(Filters.private)
def check_saved(Client, msg):
    global users
    if not msg.from_user.id in users:
        users[msg.from_user.id] = 0
    msg.continue_propagation()


@bot.on_message(Filters.private & ~Filters.user("self"))
def logger(Client, msg):
    print("[PM] Got a new message from: {}. Text: {}".format(
        "@" + msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
        str(msg.text)[0:50]))
    msg.continue_propagation()


@bot.on_message(Filters.user("self") & Filters.command("afk", prefixes=[".", "/", "!", "#"]))
def afk_command(Client, msg):
    global afk
    if len(msg.command) == 1:
        msg.edit_text("You are afk" if afk else "You are not afk")
    else:
        if msg.command[1] == "on":
            afk = True
            msg.edit_text("Afk enabled.")
        elif msg.command[1] == "off":
            afk = False
            msg.edit_text("Afk disabled.")
        else:
            msg.edit_text("You are afk" if afk else "You are not afk")


@bot.on_message(Filters.user("self") & (
        Filters.command("accept", prefixes=[".", "/", "!", "#"]) | Filters.command("allow",
                                                                                   prefixes=[".", "/", "!", "#"])))
def accept_command(Client, msg):
    global accepted_users
    global banned_users
    accepted_users.append(msg.chat.id)
    if msg.chat.id in banned_users: banned_users.remove(msg.chat.id)
    msg.edit_text("Accepted {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & (
        Filters.command("ban", prefixes=[".", "/", "!", "#"]) | Filters.command("deny", prefixes=[".", "/", "!", "#"])))
def accept_command(Client, msg):
    global banned_users
    global accepted_users
    banned_users.append(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Banned {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & (
        Filters.command("unaccept", prefixes=[".", "/", "!", "#"]) | Filters.command("unallow",
                                                                                     prefixes=[".", "/", "!", "#"])))
def accept_command(Client, msg):
    global accepted_users
    accepted_users.remove(msg.chat.id)
    msg.edit_text("Removed {} from accepted list.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & (
        Filters.command("unban", prefixes=[".", "/", "!", "#"]) | Filters.command("undeny",
                                                                                  prefixes=[".", "/", "!", "#"])))
def accept_command(Client, msg):
    global banned_users
    banned_users.remove(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Unbanned {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("commands", prefixes=[".", "/", "!", "#"]))
def commands_command(Client, msg):
    msg.edit_text("Avaiable Commands:\n"
                  "/afk - see if you are afk\n"
                  "/afk on - turn on afk\n"
                  "/afk off - turn off afk\n"
                  "/accept - in private, this person can now talk as much as he wants\n"
                  "/ban - in private, every message will be deleted and he'll not get any answer\n"
                  "/info - in reply, shows user info\n"
                  "/leave - in a group or channel, leaves the chat\n"
                  "/chatinfo - shows infos about the chat\n"
                  "/paste - in reply, posts the message text on del.dog\n"
                  "/short - in reply, looks for links and make them shorter\n"
                  "/download - in reply, downloads medias from a message (photos, documents...)\n"
                  "/save - in reply, saves the replied message in saved messages.\n"
                  "/google keywords - it'll make a google search with keywords.\n"
                  "/flood amount text - send amount times text.\n"
                  "/setfloodtimeout time - sets the timeout of /flood at time seconds. (default to 1)\n"
                  ""
                  "\n"
                  "Prefixes: . / ! #")


@bot.on_message(Filters.user("self") & Filters.command("info", prefixes=[".", "/", "!", "#"]) & Filters.reply)
def info_command(Client, msg):
    if len(msg.command) == 1:
        user_chat = bot.get_chat(msg.reply_to_message.from_user.id)
        msg.edit_text(f"{Emoji.INFORMATION} Info {Emoji.INFORMATION}\n\n"
                      f"{Emoji.ID_BUTTON} ID: `{msg.reply_to_message.from_user.id}`\n"
                      f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} Name: `{msg.reply_to_message.from_user.first_name}`\n"
                      f"{Emoji.BUST_IN_SILHOUETTE} Last Name: `{msg.reply_to_message.from_user.last_name}`\n"
                      f"{Emoji.LINK} Username: `{msg.reply_to_message.from_user.username}`\n" +
                      (f"{Emoji.TRIDENT_EMBLEM} Bio: {user_chat.description}\n" if user_chat.description else "") +
                      (
                          f"{Emoji.DESKTOP_COMPUTER} Dc: `{msg.reply_to_message.from_user.dc_id}`\n" if msg.reply_to_message.from_user.dc_id else f"{Emoji.DESKTOP_COMPUTER} Dc: `Unknown`\n") +
                      (f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n" +
                       f"{Emoji.TWELVE_O_CLOCK} Last Online Status: `{datetime.fromtimestamp(msg.reply_to_message.from_user.last_online_date).strftime('%H:%M %d/%m/%Y')}`\n" if msg.reply_to_message.from_user.last_online_date else f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n") +
                      f"{Emoji.ROBOT_FACE} Is Bot: `{msg.reply_to_message.from_user.is_bot}`\n"
                      f"{Emoji.TELEPHONE} Is Contact: `{msg.reply_to_message.from_user.is_contact}`\n"
                      f"{Emoji.MOBILE_PHONE} Is Mutual Contact: `{msg.reply_to_message.from_user.is_mutual_contact}`\n"
                      f"❌ Is Scam: `{msg.reply_to_message.from_user.is_scam}`\n"
                      f"\n<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">Profile link</a>\n")
    else:
        user_chat = bot.get_chat(msg.reply_to_message.from_user.id)
        if user_chat.photo:
            uphoto = bot.get_profile_photos(msg.reply_to_message.from_user.id, limit=1)[0]
            uphotoid = uphoto.file_id
            uphotoref = uphoto.file_ref
            bot.send_photo(msg.chat.id,
                           uphotoid,
                           file_ref=uphotoref, caption=
                           f"{Emoji.INFORMATION} Info {Emoji.INFORMATION}\n\n"
                           f"{Emoji.ID_BUTTON} ID: `{msg.reply_to_message.from_user.id}`\n"
                           f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} Name: `{msg.reply_to_message.from_user.first_name}`\n"
                           f"{Emoji.BUST_IN_SILHOUETTE} Last Name: `{msg.reply_to_message.from_user.last_name}`\n"
                           f"{Emoji.LINK} Username: `{msg.reply_to_message.from_user.username}`\n" +
                           (f"{Emoji.TRIDENT_EMBLEM} Bio: {user_chat.description}\n" if user_chat.description else "") +
                           (
                               f"{Emoji.DESKTOP_COMPUTER} Dc: `{msg.reply_to_message.from_user.dc_id}`\n" if msg.reply_to_message.from_user.dc_id else f"{Emoji.DESKTOP_COMPUTER} Dc: `Unknown`\n") +
                           (f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n" +
                            f"{Emoji.TWELVE_O_CLOCK} Last Online Status: `{datetime.fromtimestamp(msg.reply_to_message.from_user.last_online_date).strftime('%H:%M %d/%m/%Y')}`\n" if msg.reply_to_message.from_user.last_online_date else f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n") +
                           f"{Emoji.ROBOT_FACE} Is Bot: `{msg.reply_to_message.from_user.is_bot}`\n"
                           f"{Emoji.TELEPHONE} Is Contact: `{msg.reply_to_message.from_user.is_contact}`\n"
                           f"{Emoji.MOBILE_PHONE} Is Mutual Contact: `{msg.reply_to_message.from_user.is_mutual_contact}`\n"
                           f"❌ Is Scam: `{msg.reply_to_message.from_user.is_scam}`\n"
                           f"\n<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">Profile link</a>\n")
            msg.delete()
        else:
            msg.edit_text(f"{Emoji.INFORMATION} Info {Emoji.INFORMATION}\n\n"
                          f"{Emoji.ID_BUTTON} ID: `{msg.reply_to_message.from_user.id}`\n"
                          f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} Name: `{msg.reply_to_message.from_user.first_name}`\n"
                          f"{Emoji.BUST_IN_SILHOUETTE} Last Name: `{msg.reply_to_message.from_user.last_name}`\n"
                          f"{Emoji.LINK} Username: `{msg.reply_to_message.from_user.username}`\n" +
                          (f"{Emoji.TRIDENT_EMBLEM} Bio: {user_chat.description}\n" if user_chat.description else "") +
                          (
                              f"{Emoji.DESKTOP_COMPUTER} Dc: `{msg.reply_to_message.from_user.dc_id}`\n" if msg.reply_to_message.from_user.dc_id else f"{Emoji.DESKTOP_COMPUTER} Dc: `Unknown`\n") +
                          (f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n" +
                           f"{Emoji.TWELVE_O_CLOCK} Last Online Status: `{datetime.fromtimestamp(msg.reply_to_message.from_user.last_online_date).strftime('%H:%M %d/%m/%Y')}`\n" if msg.reply_to_message.from_user.last_online_date else f"{Emoji.TRIDENT_EMBLEM} Status: `{msg.reply_to_message.from_user.status}`\n") +
                          f"{Emoji.ROBOT_FACE} Is Bot: `{msg.reply_to_message.from_user.is_bot}`\n"
                          f"{Emoji.TELEPHONE} Is Contact: `{msg.reply_to_message.from_user.is_contact}`\n"
                          f"{Emoji.MOBILE_PHONE} Is Mutual Contact: `{msg.reply_to_message.from_user.is_mutual_contact}`\n"
                          f"❌ Is Scam: `{msg.reply_to_message.from_user.is_scam}`\n"
                          f"\n<a href=\"tg://user?id={msg.reply_to_message.from_user.id}\">Profile link</a>\n")


@bot.on_message(Filters.user("self") & ~Filters.private & Filters.command("leave", prefixes=[".", "/", "!", "#"]))
def leave_command(Client, msg): msg.chat.leave()


@bot.on_message(Filters.user("self") & Filters.command("chatinfo", prefixes=[".", "/", "!", "#"]))
def chat_info_command(Client, msg):
    tchat = bot.get_chat(msg.chat.id)
    if bot.get_profile_photos_count(msg.chat.id) > 0:
        uphoto = bot.get_profile_photos(msg.chat.id, limit=1)[0]
        uphotoid = uphoto.file_id
        uphotoref = uphoto.file_ref
        msg.delete()
        bot.send_photo(msg.chat.id, uphotoid, file_ref=uphotoref, caption=
        f"{Emoji.INFORMATION} Chat Info {Emoji.INFORMATION}\n\n" +
        f"".join([f"{Emoji.BUST_IN_SILHOUETTE} Title: <code>{tchat.title}</code>\n" if tchat.title else (
            f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} First Name: <code>{tchat.first_name}</code> \n{Emoji.BUST_IN_SILHOUETTE} Last Name: <code>{tchat.last_name}</code>\n" if tchat.last_name else f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} First Name: <code>{tchat.first_name}</code>\n")]) +
        f"".join([
            f"{Emoji.INPUT_NUMBERS} Members count: <code>{tchat.members_count}</code>\n" if tchat.members_count else ""]) +
        f"{Emoji.ID_BUTTON} Id: <code>{tchat.id}</code>\n"
        f"{Emoji.JAPANESE_SYMBOL_FOR_BEGINNER} Type: <code>{tchat.type}</code>\n"
        f"{Emoji.LINK} Username: <code>{tchat.username}</code>\n" +
        f"".join([f"{Emoji.TRIDENT_EMBLEM} Bio: <code>{tchat.description}</code>\n" if tchat.description else ""]) +
        f"")
    else:
        msg.edit(
            f"{Emoji.INFORMATION} Chat Info {Emoji.INFORMATION}\n\n" +
            f"".join([f"{Emoji.BUST_IN_SILHOUETTE} Title: <code>{tchat.title}</code>\n" if tchat.title else (
                f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} First Name: <code>{tchat.first_name}</code> \n{Emoji.BUST_IN_SILHOUETTE} Last Name: <code>{tchat.last_name}</code>\n" if tchat.last_name else f"{Emoji.BLOND_HAIRED_MAN_LIGHT_SKIN_TONE} First Name: <code>{tchat.first_name}</code>\n")]) +
            f"".join([
                f"{Emoji.INPUT_NUMBERS} Members count: <code>{tchat.members_count}</code>\n" if tchat.members_count else ""]) +
            f"{Emoji.ID_BUTTON} Id: <code>{tchat.id}</code>\n"
            f"{Emoji.JAPANESE_SYMBOL_FOR_BEGINNER} Type: <code>{tchat.type}</code>\n"
            f"{Emoji.LINK} Username: <code>{tchat.username}</code>\n" +
            f"".join([f"{Emoji.TRIDENT_EMBLEM} Bio: <code>{tchat.description}</code>\n" if tchat.description else ""]) +
            f"")


@bot.on_message(Filters.reply & Filters.user("self") & Filters.command("paste", prefixes=[".", "/", "!", "#"]))
def paste_command(Client, msg):
    stime = time.time()
    msg.edit_text(f"{Emoji.GLOBE_WITH_MERIDIANS} PASTE {Emoji.GLOBE_WITH_MERIDIANS}\n"
                  f"\n"
                  f"{Emoji.LINK} Url: Generating...\n"
                  f"{Emoji.INPUT_LATIN_UPPERCASE} Text: Generating...\n"
                  f"\n"
                  f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
    if not msg.reply_to_message.text: msg.edit_text(f"{Emoji.GLOBE_WITH_MERIDIANS} PASTE {Emoji.GLOBE_WITH_MERIDIANS}\n"
                                                    f"\n"
                                                    f"{Emoji.LINK} Url: Failed\n"
                                                    f"{Emoji.INPUT_LATIN_UPPERCASE} Text: No text to paste\n"
                                                    f"\n"
                                                    f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}"); return 1
    msg.edit_text(f"{Emoji.GLOBE_WITH_MERIDIANS} PASTE {Emoji.GLOBE_WITH_MERIDIANS}\n"
                  f"\n"
                  f"{Emoji.LINK} Url: https://del.dog/{requests.post('https://del.dog/documents?frontend=true', data=msg.reply_to_message.text.encode('UTF-8'), headers={'Content-Type': 'application/json, charset=utf-8'}).json()['key']}\n"
                  f"{Emoji.INPUT_LATIN_UPPERCASE} Text: {msg.reply_to_message.text[0:100]}...\n"
                  f"\n"
                  f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")


@bot.on_message(Filters.reply & Filters.user("self") & Filters.command("short", prefixes=[".", "/", "!", "#"]))
def short_command(Client, msg):
    stime = time.time()
    msg.edit_text(f"{Emoji.LINK} Shortener {Emoji.LINK}\n"
                  f"\n"
                  f"{Emoji.GLOBE_WITH_MERIDIANS} Results:\n"
                  f"{Emoji.HEAVY_MINUS_SIGN} Generating...\n\n"
                  f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
    result = ""
    urls = []
    if not msg.reply_to_message.entities and not msg.reply_to_message.caption_entities:
        msg.edit_text(
            f"{Emoji.LINK} Shortener {Emoji.LINK}\n"
            f"\n"
            f"{Emoji.CROSS_MARK} Error: No links found.\n"
            f"\n"
            f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
    if msg.reply_to_message.entities:
        for entity in msg.reply_to_message.entities:
            if entity.type == "url" or entity.type == "text_link": urls.append(entity)

    if msg.reply_to_message.caption_entities:
        for entity in msg.reply_to_message.caption_entities:
            if entity.type == "url" or entity.type == "text_link": urls.append(entity)

    if len(urls) <= 0:
        msg.edit_text(f"{Emoji.LINK} Shortener {Emoji.LINK}\n"
                      f"\n"
                      f"{Emoji.CROSS_MARK} Error: No links found.\n"
                      f"\n"
                      f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
        return 1

    if msg.reply_to_message.text:
        for url in urls:
            result += f"{Emoji.HEAVY_MINUS_SIGN} {msg.reply_to_message.text[url.offset:url.offset + url.length] if len(msg.reply_to_message.text[url.offset:url.offset + url.length]) <= 40 else msg.reply_to_message.text[url.offset:url.offset + url.length][0:40] + '...'}\n" \
                      f"{Emoji.HEAVY_CHECK_MARK} {requests.post('https://cutt.ly/scripts/shortenUrl.php', data={'url': msg.reply_to_message.text[url.offset:url.offset + url.length], 'domain': '0'}).text}\n" \
                      f"\n"

    if msg.reply_to_message.caption:
        for url in urls:
            result += f"{Emoji.HEAVY_MINUS_SIGN} {msg.reply_to_message.caption[url.offset:url.offset + url.length] if len(msg.reply_to_message.caption[url.offset:url.offset + url.length]) <= 40 else msg.reply_to_message.caption[url.offset:url.offset + url.length][0:40] + '...'}\n" \
                      f"{Emoji.HEAVY_CHECK_MARK} {requests.post('https://cutt.ly/scripts/shortenUrl.php', data={'url': msg.reply_to_message.caption[url.offset:url.offset + url.length], 'domain': '0'}).text}\n" \
                      f"\n"

    msg.edit_text(f"{Emoji.LINK} Shortener {Emoji.LINK}\n"
                  f"\n"
                  f"{Emoji.GLOBE_WITH_MERIDIANS} Results:\n"
                  f"{result}"
                  f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")


@bot.on_message(Filters.user("self") & Filters.reply & Filters.command("download", prefixes=[".", "/", "!", "#"]))
def download_command(Client, msg):
    stime = time.time()
    msg.edit_text(f"{Emoji.DOWN_ARROW} Download {Emoji.DOWN_ARROW}\n"
                  f"\n"
                  f"{Emoji.COUNTERCLOCKWISE_ARROWS_BUTTON} Status: Downloading...\n"
                  f"{Emoji.INBOX_TRAY} File Name: Not avaiable.\n"
                  f"\n"
                  f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}"
                  )
    try:
        tmp_fpath = msg.reply_to_message.download()
    except ValueError:
        msg.edit_text(
            f"{Emoji.DOWN_ARROW} Download {Emoji.DOWN_ARROW}\n"
            f"\n"
            f"{Emoji.CROSS_MARK} Status: Failed.\n"
            f"{Emoji.INBOX_TRAY} File Name: Not avaiable.\n"
            f"\n"
            f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
        return 1
    if not tmp_fpath:
        msg.edit_text(
            f"{Emoji.DOWN_ARROW} Download {Emoji.DOWN_ARROW}\n"
            f"\n"
            f"{Emoji.CROSS_MARK} Status: Failed.\n"
            f"{Emoji.INBOX_TRAY} File Name: Not avaiable.\n"
            f"\n"
            f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")
        return 1
    tmp_fname = Path(tmp_fpath).relative_to(Path(os.curdir).absolute())
    msg.edit_text(
        f"{Emoji.DOWN_ARROW} Download {Emoji.DOWN_ARROW}\n"
        f"\n"
        f"{Emoji.WHITE_HEAVY_CHECK_MARK} Status: Downloaded.\n"
        f"{Emoji.INBOX_TRAY} File Name: {tmp_fname}.\n"
        f"\n"
        f"{Emoji.TIMER_CLOCK} Time Needed: {round(float(time.time()) - float(stime), 6)}")


@bot.on_message(Filters.user("self") & Filters.reply & Filters.command("save", prefixes=[".", "/", "!", "#"]))
def save_command(Client, msg):
    try:
        msg.reply_to_message.forward("me")
    except Exception as e:
        msg.edit_text(f"{Emoji.CROSS_MARK} Error:\n"
                      f"\n"
                      f"{e}")
    else:
        msg.edit_text(f"{Emoji.WHITE_HEAVY_CHECK_MARK} Done!")
        time.sleep(1)
        msg.delete()


flood_timeout = 1


@bot.on_message(Filters.user("self") & Filters.command("flood", prefixes=[".", "/", "!", "#"]))
def flood_command(Client, msg):
    if len(msg.command) < 3:
        msg.edit_text(f"{Emoji.CROSS_MARK} Please use: \n<code>/flood amount text</code>")
        return 1
    amount = msg.command[1]
    text = " ".join(msg.command[2:])
    try:
        amount = int(amount)
    except ValueError:
        msg.edit_text(f"{Emoji.CROSS_MARK} Value Error: {amount} is not a valid number.")
        return
    msg.edit_text(f"{Emoji.HEAVY_MINUS_SIGN} Started...")
    c = 0
    for i in range(amount):
        try:
            bot.send_message(msg.chat.id, text)
        except FloodWait as e:
            print(f"Sleeping {e.x} seconds.")
            time.sleep(e.x)
        c += 1
        time.sleep(0.1)
        msg.edit_text(
            f"{Emoji.HEAVY_MINUS_SIGN} Started...\n{Emoji.HOURGLASS_NOT_DONE} Timeout: {flood_timeout} \n{Emoji.MOBILE_PHONE_WITH_ARROW} Messages Sent: {c}")
        time.sleep(flood_timeout)
    msg.edit_text(
        f"{Emoji.HEAVY_CHECK_MARK} Done!\n{Emoji.HOURGLASS_DONE} Timeout: {flood_timeout} \n{Emoji.MOBILE_PHONE_WITH_ARROW} Messages Sent: {c}")


@bot.on_message(Filters.user("self") & Filters.command("setfloodtimeout", prefixes=[".", "/", "!", "#"]))
def setfloodtimeout_command(Client, msg):
    global flood_timeout
    if len(msg.command) < 2:
        msg.edit_text(
            f"{Emoji.CROSS_MARK} Please Use:\n<code>/setfloodtimeout timeout</code>\nNote: timout needs to be in seconds.")
        return 1
    timeout = msg.command[1]
    try:
        flood_timeout = float(timeout)
    except ValueError:
        msg.edit_text(f"{Emoji.CROSS_MARK} Value Error: {timeout} is not a valid number.")
    else:
        msg.edit_text(f"{Emoji.HEAVY_CHECK_MARK} Timeout set to: {timeout} seconds.")


@bot.on_message(Filters.user("self") & Filters.command("google", prefixes=[".", "/", "!", "#"]))
def google_command(Client, msg):
    if len(msg.command) < 2:
        msg.edit_text(f"{Emoji.CROSS_MARK} Please use:\n<code>/google search</code>")
        return 1
    stime = time.time()
    query = "+".join(msg.command[1:])
    msg.edit_text(f"{Emoji.GLOBE_WITH_MERIDIANS} Google {Emoji.GLOBE_WITH_MERIDIANS}\n"
                  f"\n"
                  f"{Emoji.HEAVY_MINUS_SIGN} Search: http://www.google.com/search?q={query}\n")


@bot.on_message(Filters.private & ~Filters.user("self"))
def on_private_afk_message(Client, msg):
    if not msg.from_user.id in accepted_users:
        if afk:
            msg.delete()
            if users[msg.from_user.id] + 30 < int(time.time()) and not msg.from_user.id in banned_users:
                bot.send_message(msg.chat.id,
                                 afkMessage.replace("{original_msg}", str(msg.text)),
                                 disable_web_page_preview=True)
                users[msg.from_user.id] = int(time.time())


bot.run()
