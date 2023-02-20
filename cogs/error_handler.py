import discord
from discord.ext import commands
from discord.ext.commands import Cog, CommandError

class BotCommandErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        try:
            if isinstance(error, commands.CommandNotFound):
                await ctx.send("Command not found. Please enter a valid command.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Missing arguments. Please pass all the required arguments for the command.")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("Invalid argument. Please check the arguments and try again.")
            elif isinstance(error, commands.CheckFailure):
                await ctx.send("You do not have permission to run this command.")
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")
            elif isinstance(error, commands.CommandInvokeError):
                await ctx.send("Sorry, there was an error while running the command. Please try again later.")
            elif isinstance(error, commands.MissingPermissions):
                if ctx.channel.permissions_for(ctx.me).send_messages:
                    await ctx.send(f"Sorry, you don't have the required permission to run this command: {error.missing_perms}")
                else:
                    await ctx.author.send(f"Sorry, I don't have the required permission to run this command in {ctx.channel.name}: {error.missing_perms}")
            elif isinstance(error, commands.BotMissingPermissions):
                if ctx.channel.permissions_for(ctx.me).send_messages:
                    await ctx.send(f"Sorry, I don't have the required permission to run this command: {error.missing_perms}")
                else:
                    await ctx.author.send(f"Sorry, I don't have the required permission to run this command in {ctx.channel.name}: {error.missing_perms}")
            elif isinstance(error, commands.errors.NoPrivateMessage):
                await ctx.send("Sorry, this command cannot be used in a private message.")
            elif isinstance(error, commands.errors.DisabledCommand):
                await ctx.send("Sorry, this command is currently disabled and cannot be used.")
            elif isinstance(error, commands.errors.NotConnected):
                await ctx.send("Sorry, the bot is not connected to a voice channel.")
            elif isinstance(error, commands.errors.MissingRole):
                await ctx.send(f"Sorry, you don't have the required role to run this command: {error.missing_role}")
            elif isinstance(error, commands.errors.BotMissingRole):
                await ctx.send(f"Sorry, I don't have the required role to run this command: {error.missing_role}")
            elif isinstance(error, commands.errors.NotConnected):
                await ctx.send(f"Sorry, Im not connected: {error}")
            else:
                if ctx.channel.permissions_for(ctx.me).send_messages:
                    await ctx.send(f"Sorry, there was an error with your command: {error}")
                else:
                    await ctx.author.send(f"Sorry, I could not send a message in {ctx.channel.name} to let you know there was an error with your command: {error}. I do not have permission to send messages in that channel.")
        except discord.Forbidden:
            await ctx.author.send(f"Sorry, I could not send you the error message in {ctx.channel.name}: I do not have permission to send messages to this channel")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotCommandErrorHandler(bot))
