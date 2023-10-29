import json
import os
from typing import Callable, TypeVar

from discord.ext import commands

from exceptions import *
from helpers import db_manager

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    """
    This is a custom check to see if the user executing the command is an owner of the bot.
    """

    async def predicate(context: commands.Context) -> bool:
        config_path = f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"
        with open(config_path) as file:
            config = json.load(file)
        if context.author.id not in config["ownerid"]:
            raise UserNotOwner
        return True

    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    """
    This is a custom check to see if the user executing the command is blacklisted.
    """

    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_blacklisted(context.author.id):
            raise UserBlacklisted
        return True

    return commands.check(predicate)


# Checks if the user is the owner or a mod
def is_mod() -> Callable[[T], T]:
    """
    This is a custom check to see if the user executing the command is a moderator.
    """

    async def predicate(context: commands.Context) -> bool:
        config_path = f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"
        with open(config_path) as file:
            config = json.load(file)
        if (
            context.author.id not in config["modroleid"]
            or context.author.id not in config["ownerid"]
        ):
            if not any(role.id in config["modroleid"] for role in context.author.roles):
                raise UserNotModerator
        return True

    return commands.check(predicate)
