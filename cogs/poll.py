@commands.command(name="create_poll")
async def create_poll(self, ctx: Context, question, duration: int, *options):
    # Create a new poll
    if ctx.author.id in self.active_polls:
        await ctx.send("You already have an active poll. Finish or cancel it before creating a new one.")
        return

    if len(options) < 2:
        await ctx.send("You need to provide at least two options for the poll.")
        return

    poll = {"question": question, "options": list(options), "votes": {}}
    self.active_polls[ctx.author.id] = poll

    # Set the poll duration in seconds
    poll_duration = duration

    # Send the poll to the channel
    poll_message = f"**{question}**\n"
    for index, option in enumerate(options):
        poll_message += f"{index + 1}. {option}\n"

    poll_message += f"\nVote using the command: !vote <option_number> (Poll will end in {poll_duration} seconds)"
    await ctx.send(poll_message)

    # Schedule the poll to end after the specified duration
    await asyncio.sleep(poll_duration)
    await self.finish_poll(ctx)
