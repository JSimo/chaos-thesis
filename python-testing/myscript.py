import click
from dockercmds import cmds as dockercmds
from netemcmds import cmds as netemcmds
from chaos import chaos as chaoscmds

@click.group()
def main():
    """main"""
    pass

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
    container = dockercmds.createIpContainer()
    click.echo(container.logs())
    click.echo(dockercmds.ls())

@main.command()
def test3():
    click.echo(netemcmds.test())

@main.group(invoke_without_command=True)
def chaos():
    """ chaos """
    click.echo("hello from chaos")
    pass

@chaos.command()
def test():
    click.echo("starting chaos")
    click.echo(chaoscmds.test())
    click.echo("ending chaos")

if __name__ == "__main__":
    main()
