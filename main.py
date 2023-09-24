import discord
from config import TOKEN
from filter import filter_content

WARNINGS = {} # Decleare a dictionary to represent user -> warning_counts

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyClient(discord.Client):
    async def on_ready(self):
        print("Language Filter Bot is ready.")

    async def on_message(self, message):
        userID = str(message.author.id)
        content = message.content
        member = message.author
        send = message.channel.send

        if member == self.user:
            return

        if filter_content(content): # Filter the message content
            warning_embed = discord.Embed(title='⚠️ **Warning: Harmful Content Detected**', color=discord.Color.blue())
            warning_embed.description = """The message you posted has been removed by our
                                        moderation system due to the presence of harmful
                                        or inappropriate content. We take the safety and
                                        well-being of our community seriously. Please 
                                        remember to always communicate respectfully and 
                                        considerately. If you have any questions or concerns, 
                                        feel free to reach out to our moderation team. Thank 
                                        you for your understanding and cooperation in 
                                        maintaining a positive and inclusive environment for 
                                        everyone."""
            await send(embed = warning_embed) # Send a warning embed
            if userID not in WARNINGS:
                WARNINGS[userID] = 1
            else:
                WARNINGS[userID] += 1
            # Let users know their total warning counts
            if WARNINGS[userID] == 1:
                await message.reply(f"Hello <@{userID}>, You currently have 1 warning.")
            else:
                await message.reply(f"Hello <@{userID}>, You currently have {WARNINGS[userID]} warnings.")
            try:
                await message.delete() # Delete the inappropriate message
            except discord.Forbidden as e:
                # Handle missing permissions exception
                print(f"Permission error: {e}")
                await send("I don't have the necessary permissions to delete this message.")

client = MyClient(intents = intents)
client.run(TOKEN)