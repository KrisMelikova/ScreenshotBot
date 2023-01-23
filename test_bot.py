import datetime
import pathlib as pl
import unittest
from unittest.mock import MagicMock, patch
import urllib

from bot import hello, make_screenshot_and_receive_code


class TestCaseBase(unittest.TestCase):
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))


class BotTestCase(TestCaseBase):
    @patch('bot.BOT')
    def test_hello(self, BOT):
        chat = MagicMock(id=999)
        text_mock = 'Здравствуйте! Пришлите мне ссылку на страницу сайта, ' \
                    'а я вам верну скриншот страницы и ее статус-код.'
        message_mock = MagicMock(chat=chat, text='hello')

        hello(message=message_mock)

        BOT.send_message.assert_called_with(chat.id, text_mock)

    @patch('bot.BOT')
    def test_make_screenshot_and_receive_code_w_protocol(self, BOT):
        chat = MagicMock(id=999)
        link = 'https://www.google.com/'
        message_mock = MagicMock(chat=chat, text=link)

        make_screenshot_and_receive_code(message=message_mock)

        BOT.send_photo.assert_called()

    @patch('bot.BOT')
    def test_make_screenshot_and_receive_code_wo_protocol(self, BOT):
        chat = MagicMock(id=999)
        link = 'google.com'
        message_mock = MagicMock(chat=chat, text=link)

        make_screenshot_and_receive_code(message=message_mock)

        BOT.send_photo.assert_called()

    @patch('bot.BOT')
    def test_screenshot_exist(self, BOT):
        chat = MagicMock(id=999)
        link = 'https://www.google.com/'
        parsed_link = urllib.parse.quote_plus(link)
        time_of_scr_saving = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message_mock = MagicMock(chat=chat, text=link)
        file_path = pl.Path(f'./screenshots/{time_of_scr_saving}_{parsed_link}.jpg')

        make_screenshot_and_receive_code(message=message_mock)

        self.assertIsFile(file_path)

    @patch('bot.BOT')
    def test_make_screenshot_and_receive_code_not_link(self, BOT):
        chat = MagicMock(id=999)
        not_link = "It's not a link."
        text_mock = 'Кажется, в ссылке есть опечатка...Перепроверьте, пожалуйста, и пришлите снова.'
        message_mock = MagicMock(chat=chat, text=not_link)

        with self.assertRaises(Exception):
            make_screenshot_and_receive_code(message=message_mock)

        BOT.send_message.assert_called_with(chat.id, text_mock)
