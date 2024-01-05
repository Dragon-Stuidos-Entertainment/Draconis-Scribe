// commands/ping.js
module.exports = {
    name: 'ping',
    description: 'Check the bot\'s response time',
    execute(message, args) {
        // Calculate the latency between sending a message and editing it
        const latency = Date.now() - message.createdTimestamp;
        
        // Send a message with the calculated latency
        message.reply(`Pong! Latency is ${latency}ms.`);
    },
};
