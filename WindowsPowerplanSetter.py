import click, subprocess, re

def get_plans(raw=False):
    plans = subprocess.run(['powercfg', '/l'], capture_output=True, text=True).stdout.splitlines()
    plans = plans[3:]

    if not raw:
        return [(unpack_plan(plan)) for plan in plans]
    return plans

def get_current_plan():
    plan = subprocess.run(['powercfg', '/GETACTIVESCHEME'], capture_output=True, text=True).stdout
    return unpack_plan(plan)

def get_plan_details(plan_name):
    raw_plans = get_plans(raw=True)
    for plan in raw_plans:
        if plan.find(plan_name) != -1:
            return unpack_plan(plan)
    return -1 # plan not found

def set_power_plan(GUID):
    subprocess.run(['powercfg', '/SETACTIVE', str(GUID)])

def unpack_plan(plan_string):
    regEx = re.search(r"Power Scheme GUID:\s+([a-f0-9\-]+)\s+\((.*?)\)\s*(\*)?", plan_string, re.IGNORECASE)

    plan_GUID = regEx.group(1)
    plan_name = regEx.group(2)
    is_running = regEx.group(3) == "*"

    return {"GUID": plan_GUID, "name": plan_name, "is_running": is_running}

@click.group()
def cli():
    pass

@cli.command('plans', help="lists all the available plans")
def show_plans():
    for plan in get_plans():
        click.echo(("*" if plan["is_running"] else "") + plan["name"])

@cli.command('running', help="shows the currently running plan")
def show_current_plan():
    click.echo(get_current_plan()['name'])

@cli.command('show', help="shows all details about a given plan")
@click.argument('plan_name')
def show_plan(plan_name):
    if (details := get_plan_details(plan_name)) != -1:
        click.echo(details)
    click.echo(f"Plan {plan_name} not found")

@cli.command('set', help="activates the given plan")
@click.argument('plan_name')
def set_plan(plan_name):
    if (plan_details := get_plan_details(plan_name)) != -1:
        set_power_plan(plan_details["GUID"])
        click.echo(f"{plan_name} was activated successfully")
        return

    click.echo(f"Plan {plan_name} not found")

