// Import the discord.js module
const { Client, GatewayIntentBits } = require('discord.js');
require('dotenv').config(); // Load environment variables from .env file

// Create a new Discord client with required intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
    ]
});

// Set up an event listener for when the bot is ready
client.once('ready', () => {
    console.log('Bot is ready!');
});

// Set up an event listener for when a message is sent
client.on('messageCreate', (message) => {
    // Ignore messages from the bot itself
    if (message.author.bot) return;

    // Check if the message starts with the command prefix (e.g., !)
    if (message.content.startsWith('!hello')) {
        // Reply with a greeting
        message.reply('Hello, ' + message.author.username + '!');
    }
});

// Log in to Discord with your app's token from the environment variables
client.login(process.env.BOT_TOKEN);
