"""Commands for administrating the bot."""

import subprocess
import typing
from sys import exit
import os.path

from discord.ext import commands

from exceptions import *

from utils import config


class Config(commands.Cog, name="Administration", description="Administrer le bot"):
    @commands.command(brief="Met à jour le bot")
    async def update(self, ctx):
        """Updates the bot."""

        if os.path.exists("update.sh"):
            await ctx.send_embed({"description": "Mise à jour du bot"})
            subprocess.run(["./update.sh"])
            exit(0)
        else:
            raise MissingUpdateScriptError("Script de mise à jour manquant")

    @commands.command(
        brief="Définir ou afficher des paramètres de configuration",
        extras={
            "args": {
                "key": "propriété (utiliser des points pour les props imbriquées)",
                "value": "valeur sur laquelle la configurer",
            }
        },
    )
    async def config(
        self, ctx, key: typing.Optional[str], *, value: typing.Optional[str]
    ):
        """Defines or shows configuration parameters."""

        if key is None:
            configuration = config.get_config()

            def walk_conf(dict_=configuration, i=0, opts=[]):
                for key in dict_:
                    if isinstance(dict_[key], dict):
                        opts.append(f"{'⠀'*(2*i+1)}`{key}`:")
                        walk_conf(dict_[key], i + 1, opts)
                    else:
                        opts.append(f"{'⠀'*(2*i+1)}`{key}`: {dict_[key]}")
                return "\n".join(opts)

            string = walk_conf()

            message = f"{string}"

        elif value is None:
            value = config.get(key)
            message = f"{key.capitalize()} est {value}"

        else:
            config.set(key, value)
            message = f"{key.capitalize()} a été défini sur {value}"

        await ctx.send_embed({"description": message})

    @commands.command(brief="Relancer le scheduler après un changement d'intervalle")
    async def reschedule(self, ctx):
        """Manually reschedules the job after an interval change."""

        ctx.bot.reschedule_job()
        await ctx.send(f"Envoi reprogrammé à {config.get('interval')}")

    @commands.command(brief="Lancer manuellement la génération d'un sujet")
    async def trigger(self, ctx):
        """Manually starts sending a subject."""

        await ctx.bot.send_subject()


def setup(bot):
    bot.add_cog(Config(bot))