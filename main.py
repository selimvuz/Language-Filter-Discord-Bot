import discord
import json
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
        await self.on_load()

    async def on_load(self):
        global WARNINGS
        # Load data from a JSON file into a Python dictionary
        try:
            with open('data.json', 'r') as file:
                WARNINGS = json.load(file)
        except:
            print("Error. Data file is not found.")

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
            warning_text = f"Hello <@{userID}>, You currently have "
            if WARNINGS[userID] == 1:
                await message.reply(warning_text + "1 warning.")
            else:
                await message.reply(warning_text + f"{WARNINGS[userID]} warnings.")
            try:
                await message.delete() # Delete the inappropriate message
            except discord.Forbidden as e:
                # Handle missing permissions exception
                print(f"Permission error: {e}")
                await send("I don't have the necessary permissions to delete this message.")

            json_string = json.dumps(WARNINGS) # Serialize the dictionary to a JSON string

            # Save the JSON to file
            with open('data.json', 'w') as file:
                file.write(json_string)

client = MyClient(intents = intents)
client.run(TOKEN)