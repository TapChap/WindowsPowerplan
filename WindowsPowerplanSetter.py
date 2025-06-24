import click, AliasedGroup
from powercfg_commands import *


@click.group(cls=AliasedGroup.AliasedGroup)
def cli():
    pass


@cli.command('list', help="lists all the available plans", epilog="can be used with /l")
def show_plans():
    index = 1
    click.echo("Available Powerplans:")
    for plan in get_plans():
        if not plan["is_running"]:
            click.echo(f"[{index}] " + plan["name"])
            index += 1
    click.echo("")
    click.echo("Current Powerplan:")
    click.echo(get_current_plan()['name'])


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


@cli.command('set', help="activates the given plan, accepts plan name & index", epilog="can be used with /s")
@click.argument('plan_id')
def set_plan(plan_id):
    if plan_id.isalpha():  #plan_id is the plan's name
        if (plan_details := get_plan_details(plan_id)) != -1:
            set_power_plan(plan_details["GUID"])
            click.echo(f"{plan_id} was activated successfully")
            return
    else:  #plan_id is an index
        plan_id = int(plan_id)
        plans = get_plans()
        if 0 < plan_id < len(plans):
            available_plans = [plan for plan in plans if not plan['is_running']]
            selected_plan = available_plans[plan_id - 1]
            set_power_plan(selected_plan["GUID"])
            click.echo(f"Plan {selected_plan["name"]} activated successfully")
            return

    click.echo(f"Plan {plan_id} not found")

#
# cli.add_command(show_plans, name='l')
# cli.add_command(show_current_plan, name='r')
# cli.add_command(set_plan, name='s')
