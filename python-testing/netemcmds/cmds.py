from dockercmds import cmds as dockercmds

# http://man7.org/linux/man-pages/man8/tc-netem.8.html
# See above link for information about netem.

def tcBaseCmd(iface="eth0", option="add"):
    """ Returns the base tc command """
    return "tc qdisc {} dev {} root".format(option, iface)

def tcClearCmd(iface="eth0"):
    """ Returns the netem reset command"""
    return tcBaseCmd(iface, "del")

def netemDelay(iface="eth0", time="1000ms"):
    """ Returns the command for adding a delay with netem """
    return "delay {}".format(time)

def netemLoss(percent="50%"):
    """ Returns the command for adding a loss with netem """
    return "loss {}".format(percent)

def netemDrop():
    """ Returns the command for dropping traffic with netem """
    return lossCmd(percent="100%")

def tcGetCmd(iface="eth0"):
    """ Returns the command for showing applied cmds """
    return "tc qdisc show dev {}".format(iface)

def parseOpts(opts):
    """ Parse a list of opts """
    opts = opts.rstrip()
    options = ["delay", "loss"]
    parsedopts = []
    curropt = ""
    currind = 0
    for string in opts.split(" "):
        if string in options:
            parsedopts.append(curropt)
            curropt = string
        else: 
            curropt += " " + string
    parsedopts.append(curropt) # grab the last finished string
    return parsedopts[1:]

def hasAppliedOptions(containerId): 
    """ Return true when options are applied otherwise false. """
    return len(getAppliedOptions(containerId)) > 0

def getAppliedOptions(containerId):
    options = dockercmds.execTcCmd(containerId, tcGetCmd()).logs()
    parsedOptions = parseOpts(options)
    return parsedOptions