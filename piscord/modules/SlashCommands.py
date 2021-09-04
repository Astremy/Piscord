slash_command = SlashCommand(
    name="permissions",
    description="Get or edit permissions for a user or a role"
)
# user_sub_commands = SubCommandGroup()
# user_sub_commands.add_subcommand(name="get", description="Get permissions for a user")
# user_sub_commands.add_subcommand(name="edit", description="Edit permissions for a user")
user_get = SubCommand(name="get", description="Get permissions for a user")
user_edit = SubCommand(name="edit", description="Edit permissions for a user")
slash_command.add_option(name="user", description="Get or edit permissions for a user",
                         sub_commands_group=[user_get, user_edit])

@bot.command(slash_command=slash_command)
def command():
    ...