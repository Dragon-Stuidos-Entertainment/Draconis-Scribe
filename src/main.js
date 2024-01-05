// Import the discord.js module
const { Client, GatewayIntentBits, Collection } = require('discord.js');
require('dotenv').config(); // Load environment variables from .env file
const fs = require('fs');

// Create a new Discord client with required intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
    ]
});

// Create a collection to store commands
client.commands = new Collection();

// Read all command files
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

// Load each command
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

// Set up an event listener for when the bot is ready
client.once('ready', () => {
    console.log('Bot is ready!');
});

// Set up an event listener for when a message is sent
client.on('messageCreate', (message) => {
    // Ignore messages from the bot itself
    if (message.author.bot) return;

    // Check if the message starts with the command prefix (e.g., !)
    if (!message.content.startsWith('!')) return;

    // Extract the command name and arguments
    const args = message.content.slice('!'.length).split(/ +/);
    const commandName = args.shift().toLowerCase();

    // Get the command from the collection
    const command = client.commands.get(commandName);

    // If the command doesn't exist, do nothing
    if (!command) return;

    // Execute the command
    try {
        command.execute(message, args);
    } catch (error) {
        console.error(error);
        message.reply('There was an error executing the command.');
    }
});

// Log in to Discord with your app's token from the environment variables
client.login(process.env.BOT_TOKEN);
