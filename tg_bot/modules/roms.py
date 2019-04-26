import html
import json
import time
from datetime import datetime
from typing import Optional, List
from hurry.filesize import size as sizee

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, LOGGER
from tg_bot.__main__ import GDPR
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from requests import get

# DO NOT DELETE THIS, PLEASE.
# Made by @peaktogoo on GitHub and Telegram.
# This module was inspired by Android Helper Bot by Vachounet.
# None of the code is taken from the bot itself, to avoid any more confusion.

LOGGER.info("Original Android Modules by @peaktogoo on Telegram")

@run_async
def dot(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/dot '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/dot whyred`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/DotOS/ota_config/dot-p/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']
        changelog = response['changelog_device']

        reply_text = (f" * Download dot OS for {device} *\n"

                      f"• *Download:* [{filename}]({url})\n"
                      f"• *Build size:* {buildsize_b}\n"
                      f"• *Version:* {version}\n"
                      f"• *Device Changelog:* {changelog}")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def miui(bot: Bot, update: Update):
    giturl = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/"
    message = update.effective_message
    device = message.text[len('/miui '):]
    result = "*Recovery ROM*\n\n"
    result += "*Stable*\n"
    stable_all = json.loads(get(giturl + "stable_recovery/stable_recovery.json").content)
    data = [i for i in stable_all if device == i['codename']]
    if len(data) != 0:
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")\n\n"

        result += "*Weekly*\n"
        weekly_all = json.loads(get(giturl + "weekly_recovery/weekly_recovery.json").content)
        data = [i for i in weekly_all if device == i['codename']]
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")"
    else:
        result = "Couldn't find any device matching your query."

    message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


__help__ = """
 - /dot <device>: Get the DotOS Rom
 - /miui <stable/weekly>: Get the weekly or Stable Firmwares
"""

__mod_name__ = "Roms"


MIUI_HANDLER = DisableAbleCommandHandler("miui", miui, admin_ok=True)
SUPERIOR_HANDLER = DisableAbleCommandHandler("superior", superior, admin_ok=True)

dispatcher.add_handler(MIUI_HANDLER)
dispatcher.add_handler(DOT_HANDLER)
