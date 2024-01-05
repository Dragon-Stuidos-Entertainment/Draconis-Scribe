// commands/moderation.js
const checkPermissions = (message, requiredPermission) => {
    // Check if the user has the required permission
    if (!message.member.permissions.has(requiredPermission)) {
        return message.reply(`You do not have the required \`${requiredPermission}\` permission to use this command.`);
    }
    return true;
};

module.exports = [
    {
        name: 'kick',
        description: 'Kick a user from the server',
        execute(message, args) {
            // Check if the user has the 'KICK_MEMBERS' permission
            if (!checkPermissions(message, 'KICK_MEMBERS')) return;

            // Mention the user to be kicked
            const targetUser = message.mentions.users.first();
            
            // Check if a user was mentioned
            if (!targetUser) {
                return message.reply('Please mention a user to kick.');
            }

            // Get the member object of the mentioned user
            const targetMember = message.guild.members.cache.get(targetUser.id);

            // Kick the user
            targetMember.kick()
                .then(() => {
                    message.reply(`Successfully kicked ${targetUser.tag}.`);
                })
                .catch(error => {
                    console.error(error);
                    message.reply('There was an error kicking the user.');
                });
        },
    },
    {
        name: 'ban',
        description: 'Ban a user from the server',
        execute(message, args) {
            // Check if the user has the 'BAN_MEMBERS' permission
            if (!checkPermissions(message, 'BAN_MEMBERS')) return;

            // Mention the user to be banned
            const targetUser = message.mentions.users.first();
            
            // Check if a user was mentioned
            if (!targetUser) {
                return message.reply('Please mention a user to ban.');
            }

            // Get the member object of the mentioned user
            const targetMember = message.guild.members.cache.get(targetUser.id);

            // Ban the user
            targetMember.ban()
                .then(() => {
                    message.reply(`Successfully banned ${targetUser.tag}.`);
                })
                .catch(error => {
                    console.error(error);
                    message.reply('There was an error banning the user.');
                });
        },
    },
    {
        name: 'ping',
        description: 'Check the bot\'s response time',
        execute(message, args) {
            // Calculate the latency between sending a message and editing it
            const latency = Date.now() - message.createdTimestamp;
            
            // Send a message with the calculated latency
            message.reply(`Pong! Latency is ${latency}ms.`);
        },
    },
    // Add more moderation commands as needed
];
