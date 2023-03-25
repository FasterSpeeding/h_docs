# -*- coding: utf-8 -*-
# Tanjun Examples - A collection of examples for a Hikari guide.
# Written in 2023 by Lucina Lucina@lmbyrne.dev
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

import alluka
import hikari
import tanjun
from yuyo import components


class LinkColumn(components.ActionColumnExecutor):
    @components.as_button(hikari.ButtonStyle.DANGER)
    async def on_button(self, ctx: components.Context) -> None:
        await ctx.respond("Button pressed")

    link_button = components.link_button("htts://example.com/yee")


class SelectColumn(components.ActionColumnExecutor):
    @components.as_channel_select
    async def on_channel_select(self, ctx: components.Context) -> None:
        await ctx.respond(f"Selected {len(ctx.select_channels)} channels")

    @components.with_option("borf", "dog")
    @components.with_option("meow", "cat")
    @components.with_option("label", "value")
    @components.as_text_select(min_values=0, max_values=3)
    async def on_text_select(self, ctx: components.Context) -> None:
        await ctx.respond("Animals: " + ", ".join(ctx.select_texts))

    @components.as_select_menu(hikari.ComponentType.ROLE_SELECT_MENU)
    async def on_role_select(self, ctx: components.Context) -> None:
        roles = ", ".join(role.name for role in ctx.select_roles.values())
        await ctx.respond(f"Selected roles: {roles}")

    @components.as_select_menu(hikari.ComponentType.USER_SELECT_MENU)
    async def on_user_select(self, ctx: components.Context) -> None:
        users = ", ".join(map(str, ctx.select_users.values()))
        await ctx.respond(f"Selected users: {users}")

    @components.as_select_menu(hikari.ComponentType.MENTIONABLE_SELECT_MENU)
    async def on_mentionable_select(self, ctx: components.Context) -> None:
        role_count = len(ctx.select_roles)
        user_count = len(ctx.select_users)
        await ctx.respond(f"Selected {user_count} users and {role_count} roles")


@tanjun.as_slash_command("name", "description")
async def command(
    ctx: tanjun.abc.Context, client: alluka.Injected[components.ComponentClient]
) -> None:
    component = SelectColumn()
    message = await ctx.respond(
        "hello!", components=component.rows, ensure_result=True
    )
    client.set_executor(message, component)
