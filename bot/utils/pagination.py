import discord
from discord.ext.commands import Context
from reactionmenu import ViewButton, ViewMenu


async def paginate_embed(ctx: Context, pages: list):
    if len(pages) == 0:
        await ctx.send(
            embed=discord.Embed(
                description="¡Oops! Parece que no hay elementos para mostrar.",
                color=discord.Color.brand_red(),
            )
        )
        return
    elif len(pages) == 1:
        await ctx.send(embed=pages[0])
        return

    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style="Página $/&")

    menu.add_pages(pages)

    first_button = ViewButton(emoji="⏪", custom_id=ViewButton.ID_GO_TO_FIRST_PAGE)
    back_button = ViewButton(emoji="◀️", custom_id=ViewButton.ID_PREVIOUS_PAGE)
    next_button = ViewButton(emoji="▶️", custom_id=ViewButton.ID_NEXT_PAGE)
    last_button = ViewButton(emoji="⏩", custom_id=ViewButton.ID_GO_TO_LAST_PAGE)

    menu.add_buttons([first_button, back_button, next_button, last_button])

    menu.timeout = 300

    await menu.start()
