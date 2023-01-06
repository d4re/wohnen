import argparse
import logging
from pathlib import Path
import urllib.parse

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import config
from site_handler import apply_to_flats, find_flats

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE, ids: list[int]):
    id = update.effective_chat.id
    ids.append(id)
    # TODO: update yaml
    logging.info(f"New registration: {id}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You were registered for updates on flats in Berlin. To unregister, send /unregister.",
    )


async def unregister(
    update: Update, context: ContextTypes.DEFAULT_TYPE, ids: list[int]
):
    id = update.effective_chat.id
    ids.remove(id)
    # TODO: update yaml
    logging.info(f"Unregistering id {id}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You were unregistered for updates on flats in Berlin.",
    )


async def update(
    context: ContextTypes.DEFAULT_TYPE,
    conf: config.Config,
    cache_folder: Path,
) -> None:
    """Send periodic message"""
    maps_api = "https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom={zoom}&size=500x500&scale=2{marker_query}&key={key}"
    sites = await find_flats(conf.search, cache_folder)
    if conf.general.auto_apply:
        await apply_to_flats(sites)
    flats = []
    for name, site in sites.items():
        for flat in site:
            flat["site"] = name
            flats.append(flat)
    grouped = (
        flats[i : i + conf.maps.group_size]
        for i in range(0, len(flats), conf.maps.group_size)
    )
    for group in grouped:
        markers = []
        messages = []
        for idx, flat in enumerate(group, start=1):
            markers.append(get_marker(idx, flat))
            messages.append(format_message(idx, flat, conf.telegram.max_field_len))
        marker_query = "".join(markers)
        if marker_query:
            map_url = maps_api.format(
                center=conf.maps.center,
                marker_query=marker_query,
                key=conf.maps.key,
                zoom=conf.maps.zoom,
            )
        else:
            map_url = ""

        for id in conf.telegram.ids:
            if map_url:
                await context.bot.send_photo(id, map_url, disable_notification=(not conf.telegram.notify))
            for message in messages:
                await context.bot.send_message(id, message, parse_mode=ParseMode.HTML, disable_notification=(not conf.telegram.notify))


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


def format_message(idx: int, flat: dict, str_len_limit: int) -> str:
    message = f"<b>{idx}: {flat['title'][:str_len_limit]}</b>"
    message += f"\n<b>Address</b>: {flat['addr']}"
    for name, value in flat["properties"].items():
        message += f"\n<b>{name}:</b> {str(value)[:str_len_limit]}"
    message += f"\n{flat['link']}"
    return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Flat finder",
        description="Get flats sent to you via telgram",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("--config", type=str, default="local/config.yaml")
    parser.add_argument("--cache-folder", type=str, default="local/cache/")
    args = parser.parse_args()
    conf = config.load_config(args.config)

    application = (
        ApplicationBuilder()
        .token(conf.telegram.api_key)
        .rate_limiter(AIORateLimiter())
        .connect_timeout(10)
        .build()
    )

    register_handler = CommandHandler(
        "register", lambda update, context: register(update, context, conf.telegram.ids)
    )
    application.add_handler(register_handler)

    unregister_handler = CommandHandler(
        "unregister",
        lambda update, context: unregister(update, context, conf.telegram.ids),
    )
    application.add_handler(unregister_handler)

    application.job_queue.run_repeating(
        lambda x: update(x, conf, Path(args.cache_folder)),
        interval=conf.general.period,
        first=10,
    )

    application.run_polling()
