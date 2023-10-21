import nextcord
from nextcord.ext import commands
import mysql.connector
import config
from nextcord.ext import commands
from nextcord.ext import application_checks

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

def slut():
    async def predicate(ctx):
        return any(role.id == config.slut for role in ctx.author.roles)
    return commands.check(predicate)

def master():
    async def predicate2(ctx):
        return any(role.id == config.owner for role in ctx.author.roles)
    return commands.check(predicate2)

## error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the required role to use this command.")

# Command to get the "code" value from the "code" table
@bot.slash_command(
    name='unlock',
    description='Provides your chastity keysafe code for emergencies only and pings Owner Echo.'
)
@slut()
async def get_code(ctx):
    try:
        member = ctx.user  # Access the user who triggered the interaction

        has_slut_role = any(role.id == config.slut for role in member.roles)

        if has_slut_role:
            # Create a MySQL connection
            connection = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                password=config.db_pass,
                database=config.db_name
            )

            cursor = connection.cursor()

            # Execute the SQL query to fetch the "code" value
            cursor.execute("SELECT code FROM main WHERE ID = 1")
            code_value = cursor.fetchone()[0]

            # Close the cursor and the connection
            cursor.close()
            connection.close()
            await ctx.send(f"<@181322150131531777> **EMERGENCY UNLOCK INITIALISED**\nYour code is: {code_value}\nIf this is not an emergency, you will be punished.")
        else:
            await ctx.send("If there is no need to unlock for an emergency, it can wait until you are available to call.", ephemeral=True)


    except mysql.connector.Error as e:
        await ctx.send(f"An error occurred while fetching data from the database: {e}")

@bot.slash_command(
    name='lock',
    description='Changes the code for the chastity keysafe.'
)
@master()
async def upload_code(ctx, code: int):
    try:
        member = ctx.user  # Access the user who triggered the interaction

        has_master_role = any(role.id == config.owner for role in member.roles)

        if has_master_role:

            connection = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                password=config.db_pass,
                database=config.db_name
            )

            cursor = connection.cursor()

            # Use parameterized query to update the "code" value
            update_query = "UPDATE main SET code = %s WHERE ID = 1"
            cursor.execute(update_query, (code,))

            # Commit the changes to the database
            connection.commit()

            # Close the cursor and the connection
            cursor.close()
            connection.close()
            await ctx.send(f"Successfully updated keysafe code to {code}", ephemeral=True)
        else:
            await ctx.send("<@181322150131531777> **MISBEHAVIOR ALERT**\nNice try whore, you will be punished for this.")
        # Send the retrieved code value as a response


    except mysql.connector.Error as e:
        await ctx.send(f"An error occurred while fetching data from the database: {e}")

bot.run(config.token)
