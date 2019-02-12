import click
from dockercmds import cmds as dockercmds

@click.group()
def main():
    """main"""

@main.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name",
              help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo("Hello, %s!" % name)

@main.command()
def docker():
	"""Docker stuff"""
	click.echo(dockercmds.ls())

@main.command()
def test():
	click.echo(dockercmds.buildIpImage())


@main.command()
def test2():
	click.echo(dockercmds.createIpContainer())

if __name__ == "__main__":
    main()
