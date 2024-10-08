import nextcord
from nextcord.ext import commands
from random import choice
from .util import Config

conf = Config("./bot-config/bot_settings.json")

class OOCQC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    def setup(self):
        pass

    @nextcord.slash_command()
    async def oocqc(self, interaction: nextcord.Interaction):
        pass

    @oocqc.subcommand(description="gets a specific string from oocqc")
    async def string(self, interaction: nextcord.Interaction, string: str):
        """
        searches for a specific string in oocqc
        """
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            results = [s for s in oocqc_strings if string.lower() in s.lower()]
            results_formatted = nextcord.Embed(
                title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"",
                description="\n".join(results),
            )
            char_limit = conf["oocqc"]["embeds"]["char_limit"]
            if len(results_formatted) > char_limit:
                results_formatted = nextcord.Embed(
                    title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"",
                    description="\n".join(results)[:char_limit],
                )
                await interaction.response.send_message(
                    embed=results_formatted,
                    content=f"only showing first {char_limit} characters",
                )
            else:
                await interaction.response.send_message(embed=results_formatted)

    @oocqc.subcommand(description="gets a random string from oocqc")
    async def random(self, interaction: nextcord.Interaction):
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            await interaction.response.send_message(choice(oocqc_strings))

    @oocqc.subcommand(description="get the quote in the oocqc file at a specified line")
    async def line(self, interaction: nextcord.Interaction, line: int):
        """
        specific line from oocqc file
        """
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            try:
                assert line < len(oocqc_strings)
            except:
                await interaction.response.send_message("wow that line is out of this world!1!! L bozo", ephemeral=True)
            await interaction.response.send_message(content=oocqc_strings[line - 1])