// Import the discord.js module
const { Client, GatewayIntentBits, Collection } = require('discord.js');
require('dotenv').config(); // Load environment variables from .env file
const fs = require('fs');
const path = require('path');

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

// Get the absolute path to the 'commands' directory
const commandsPath = path.join(__dirname, 'commands');

// Read all command files dynamically
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

// Load each command dynamically
for (const file of commandFiles) {
    const commandPath = path.join(commandsPath, file);
    const commands = require(commandPath);

    if (Array.isArray(commands)) {
        // If it's an array of commands, add each command to the collection
        for (const command of commands) {
            client.commands.set(command.name, command);
        }
    } else {
        // If it's a single command, add it to the collection
        client.commands.set(commands.name, commands);
    }
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
