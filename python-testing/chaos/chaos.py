from dockercmds import cmds as dockercmds
from netemcmds import cmds as netemcmds

import time
import click

def test():
    containerId = dockercmds.filterContainers()[0].id
    # If we have rules, we need to issue a change instead of a add.
    tcBase = netemcmds.tcBaseCmd()
    if netemcmds.hasAppliedOptions(containerId):
        tcBase = netemcmds.tcBaseCmd(option="change")

    # Build the command string.
    command = " ".join([
        tcBase, 
        "netem",
        netemcmds.netemDelay(time="2000ms"),
        netemcmds.netemLoss()
    ])
    click.echo(command)

    # Execute the command.
    click.echo(dockercmds.execTcCmd(containerId, command).logs())

    # Echo currently applied options
    click.echo(netemcmds.getAppliedOptions(containerId))

    time.sleep(2) # TODO: move sleep logic to another package. Only contain docker logic in this class.

    #Clean out any applied commands.
    dockercmds.execTcCmd(containerId, netemcmds.tcClearCmd())