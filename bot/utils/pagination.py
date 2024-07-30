from reactionmenu import ViewButton, ViewMenu

async def paginate_embed(ctx, pages):
    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style="Página $/&")

    menu.add_pages(pages)

    first_button = ViewButton(emoji="⏪", custom_id=ViewButton.ID_GO_TO_FIRST_PAGE)
    back_button = ViewButton(emoji="◀️", custom_id=ViewButton.ID_PREVIOUS_PAGE)
    next_button = ViewButton(emoji="▶️", custom_id=ViewButton.ID_NEXT_PAGE)
    last_button = ViewButton(emoji="⏩", custom_id=ViewButton.ID_GO_TO_LAST_PAGE)

    menu.add_button(first_button)
    menu.add_button(back_button)
    menu.add_button(next_button)
    menu.add_button(last_button)
    menu.timeout = 300

    await menu.start()