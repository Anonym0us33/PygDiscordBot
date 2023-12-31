import discord
from discord import app_commands
from discord.ext import commands

def embedder(msg):
    embed = discord.Embed(
        description=f"{msg}",
        color=0x9C84EF
    )
    return embed


class DevCommands(commands.Cog, name="dev_commands"):
    def __init__(self, bot):
        self.bot = bot

    
    async def embedder(self, msg):
        embed = discord.Embed(
                description=f"{msg}",
                color=0x9C84EF
            )
        return embed

    async def gorilla_embedder(self, interaction, prompt, message):
        embed = discord.Embed(
                title="GorillaLLM 🦍",
                description=f"Author: {interaction.user.name}\nPrompt: {prompt}\n\Response:\n{message}",
                color=0x9C84EF
            )
        return embed
        
    async def name_cleaner(self, name):
        clean_name = name.split("#")[0]
        return clean_name

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dev Commands cog loaded.")

    @commands.command(name='sync', description='sync up')
    async def sync(self, interaction: discord.Interaction) -> None:
        await self.bot.tree.sync()
        print("synced")

    @app_commands.command(name="test", description="Test command")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test passed and tree synced.", delete_after=3)

    @app_commands.command(name="reload", description="reload cog")
    async def reload(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await interaction.response.send_message(embed=await self.embedder(f"Reloaded `{cog}`"), delete_after=3)
        except Exception:
            await interaction.response.send_message(embed=await self.embedder(f"Reloaded `{cog}`"), delete_after=3)


    @app_commands.command(name="gorillallm", description="Query Gorilla")
    async def gorilla_call(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(embed=await self.embedder(f"{interaction.user} used 🦍\nPlease Wait.."), delete_after=3)
        message = await self.bot.get_cog("gorilla_llm").gorilla_query(prompt)
        await interaction.channel.send(embed=await self.gorilla_embedder(interaction, prompt, message))
        # await interaction.channel.reply(message)

    

async def setup(bot):
    await bot.add_cog(DevCommands(bot))
