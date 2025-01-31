# Tanjun Examples - A collection of examples for a Hikari guide.
# Written in 2023 by Faster Speeding Lucina@lmbyrne.dev
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

import hikari
import tanjun


def hikari_listener() -> None:
    bot = hikari.GatewayBot("TOKEN")

    @bot.listen()
    async def on_event(event: hikari.MessageCreateEvent) -> None:
        if not event.is_human:
            return  # Ignore message creates from non-humans (so bots and webhooks).

        if event.message.content == "Hello Botto":
            await event.message.respond("Good morning human-kyun")


class DatabaseProto:
    async def start(self) -> None: ...

    async def stop(self) -> None: ...


def lifetime_management() -> None:
    bot = hikari.GatewayBot("TOKEN")
    db: DatabaseProto = DatabaseProto()

    @bot.listen(hikari.StartingEvent)
    async def on_starting_event(event: hikari.StartingEvent) -> None:
        await db.start()  # Start our database client while Hikari is starting.

    async def on_stopping_event(event: hikari.StoppedEvent) -> None:
        await db.stop()  # Stop our database client when Hikari is stopping..

    bot.subscribe(hikari.StoppedEvent, on_stopping_event)


def wait_for() -> None:
    async def handle_edit(bot: hikari.GatewayBot, message: hikari.Message) -> None:
        try:
            edit_event = await bot.wait_for(
                hikari.MessageUpdateEvent,
                timeout=60,
                predicate=lambda event: event.message_id == message.id,
            )

        except TimeoutError:
            # In this example we try to delete the message if it's not edited by
            # author within 60 seconds.
            try:
                await message.delete()

            # ForbiddenError will be raised if the bot can no-longer access the channel.
            # and NotFoundError will be raised if the message doesn't exist anymore.
            # We ignore these expected cases and return early to guard against the
            # edit handling logic being called.
            except (hikari.ForbiddenError, hikari.NotFoundError):
                return

        # ... Handle edit.


def stream() -> None:
    async def stream_follow_ups(
        bot: hikari.GatewayBot, channel: hikari.PartialChannel
    ) -> None:
        iterator = bot.stream(hikari.MessageCreateEvent, timeout=5).filter(
            ("event.channel_id", channel.id)
        )

        with iterator:
            async for _event in iterator:
                ...  # ... process message create


def tanjun_listener() -> None:
    component = tanjun.Component()

    @component.with_listener()
    async def on_member_event(
        event: hikari.MemberCreateEvent | hikari.MemberUpdateEvent,
    ) -> None: ...

    @component.with_listener(hikari.StartedEvent, hikari.StartingEvent)
    async def on_event(event: hikari.Event) -> None: ...
