import datetime
import logging
import urllib

import playwright
from playwright.sync_api import sync_playwright
import telebot

from constants import MAX_FILENAME_LEN
from settings import BOT_TOKEN
from utils import match_url

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT = telebot.TeleBot(BOT_TOKEN)


def hello(message):
    BOT.send_message(
        message.chat.id,
        'Здравствуйте! Пришлите мне ссылку на страницу сайта, а я вам верну скриншот страницы и ее статус-код.',
    )


def make_screenshot_and_receive_code(message):
    url = match_url(message.text)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        time_of_scr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # URL may have symbols unsupported by filesystem, so urlencode it.
        parsed_url = urllib.parse.quote_plus(url)
        # Usually filesystem has limits on max file name length.
        url_for_file = (parsed_url[:MAX_FILENAME_LEN] + '..') if len(parsed_url) > MAX_FILENAME_LEN else parsed_url

        try:
            response = page.goto(url)
        except playwright._impl._api_types.Error:
            BOT.send_message(
                message.chat.id,
                'Кажется, в ссылке есть опечатка...Перепроверьте, пожалуйста, и пришлите снова.',
            )
            raise
        except Exception:  # Just to inform our user
            BOT.send_message(
                message.chat.id,
                'При попытке загрузки страницы что-то пошло не так, попробуйте еще раз.',
            )
            raise

        status_code = response.status

        try:
            screenshot = page.screenshot(type="jpeg", path=f'./screenshots/{time_of_scr}_{url_for_file}.jpg')
        except Exception:  # Just to inform our user
            BOT.send_message(
                message.chat.id,
                'При создании скриншота что-то пошло не так, попробуйте еще раз.',
            )
            raise

        BOT.send_photo(message.chat.id, photo=screenshot, caption=f'Status code of {url} is: {status_code}')

        browser.close()


if __name__ == "__main__":
    # For convenient unit testing added handlers here instead of via decorators

    BOT.message_handler(commands=['start'])(hello)
    BOT.message_handler(content_types=['text'])(make_screenshot_and_receive_code)

    BOT.infinity_polling()
