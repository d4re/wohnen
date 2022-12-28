import logging
import urllib.parse

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config
from scanner import find_flats

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
ids = set()

group_size = 5
center = "berlin"
key = "google maps key here"
str_len_limit = 60


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ids
    ids.add(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Your id is {update.effective_chat.id}"
    )


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = " ".join(context.args).upper()
    context.job_queue.run_repeating
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def update(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send periodic message"""
    maps_api = "https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom=11&size=500x500&scale=2{marker_query}&key={key}"
    sites = await find_flats()
    flats = []
    for name, site in sites.items():
        for flat in site:
            flat["site"] = name
            flats.append(flat)
    grouped = (flats[i : i + group_size] for i in range(0, len(flats), group_size))
    for group in grouped:
        markers = []
        messages = []
        for idx, flat in enumerate(group):
            markers.append(get_marker(idx, flat))
            messages.append(format_message(idx, flat))
        marker_query = "".join(markers)
        if marker_query:
            map_url = maps_api.format(center=center, marker_query=marker_query, key=key)
        else:
            map_url = ""

        for id in ids:
            if map_url:
                await context.bot.send_photo(id, map_url)
            for message in messages:
                await context.bot.send_message(id, message, parse_mode=ParseMode.HTML)


def get_marker(idx: int, flat: dict) -> str:
    marker_tpl = "&markers=color:{color}%7Clabel:{idx}%7C{pos_str}"
    if pos := flat.get("pos"):
        pos_str = f"{pos['lat']},{pos['long']}"
        return marker_tpl.format(color="0x00FF00", idx=idx, pos_str=pos_str)
    elif addr := flat.get("addr"):
        pos_str = urllib.parse.quote_plus(addr)
        return marker_tpl.format(color="0xFFFF00", idx=idx, pos_str=pos_str)
    else:
        return ""


def format_message(idx: int, flat: dict) -> str:
    message = f"<b>{idx}: {flat['title'][:str_len_limit]}</b>"
    message += f"\n<b>Address</b>: {flat['addr']}"
    for name, value in flat["properties"].items():
        message += f"\n<b>{name}:</b> {str(value)[:str_len_limit]}"
    message += f"\n{flat['link']}"
    return message


if __name__ == "__main__":
    telegram_account = config.get_telegram_account()
    application = ApplicationBuilder().token(telegram_account.api_key).build()

    register_handler = CommandHandler("register", register)
    application.add_handler(register_handler)

    caps_handler = CommandHandler("caps", caps)
    application.add_handler(caps_handler)
    application.job_queue.run_repeating(update, interval=600, first=30)

    application.run_polling()
