import click, AliasedGroup
from powercfg_commands import *

@click.group(cls=AliasedGroup.AliasedGroup)
def cli():
    pass

@cli.command('list', help="lists all the available plans", epilog="can be used with /l")
def show_plans():
    for plan in get_plans():
        click.echo(("*" if plan["is_running"] else "") + plan["name"])

@cli.command('running', help="shows the currently running plan", epilog="can be used with /r")
def show_current_plan():
    click.echo(get_current_plan()['name'])

@cli.command('show', help="shows all details about a given plan")
@click.argument('plan_name')
def show_plan(plan_name):
    if (details := get_plan_details(plan_name)) != -1:
        query_plan(details["GUID"])
        return
    click.echo(f"Plan {plan_name} not found")

@cli.command('set', help="activates the given plan", epilog="can be used with /s")
@click.argument('plan_name')
def set_plan(plan_name):
    if (plan_details := get_plan_details(plan_name)) != -1:
        set_power_plan(plan_details["GUID"])
        click.echo(f"{plan_name} was activated successfully")
        return

    click.echo(f"Plan {plan_name} not found")

#
# cli.add_command(show_plans, name='l')
# cli.add_command(show_current_plan, name='r')
# cli.add_command(set_plan, name='s')

