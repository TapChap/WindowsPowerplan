import click

class AliasedGroup(click.Group):
    _aliases = {
        '/s': 'set',
        '/r': 'running',
        '/l': 'list',
    }

    def get_command(self, ctx, cmd_name):
        # Use alias if it exists
        cmd_name = self._aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)

    def list_commands(self, ctx):
        # Only list primary command names, not aliases
        return [cmd for cmd in super().list_commands(ctx) if cmd not in self._aliases]