# -*- coding: utf-8 -*-
# Tanjun Examples - A collection of examples for Tanjun.
# Written in 2023 by Lucina Lucina@lmbyrne.dev
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.
import os

import agraffe
import tanjun
import yuyo


def make_asgi_bot() -> yuyo.AsgiBot:
    bot = yuyo.AsgiBot(token=os.environ["TOKEN"].strip())
    yuyo.modals.ModalClient.from_gateway_bot(bot)
    yuyo.ComponentClient.from_gateway_bot(bot)
    tanjun.Client.from_gateway_bot(bot)
    return bot


def serverless():
    bot = yuyo.AsgiBot(token=os.environ["TOKEN"].strip())

    # ... Setup bot

    entry_point = agraffe.Agraffe(bot)
