""""
Usage: jst [-h|--help] <resource> [<action>] [<args>...]

This tool manages jrs instances.

For a quick start run:
mkdir jrs-trunk
cd jrs-trunk
jst ctx init
jst tc init
jst src init --skip-tests
jst tc deploy
jst tc start
jst tc go

jst ctx init              Initialize context (create configuration files with default values)
                          There are two configuration files: ~/.jst/jst.properties (user config)
                          and jst.properties (context config) in the current directory
jst tc init               Initialize tomcat (download, unpack and configure tomcat)
jst src init              Initialize sources (checkout sources,
                          write default_master.properties in buildomatic directory,
                          build sources, write maven settings.xml)
jst ctx show              Show context (print configuration)
                         
jst tc status             Show tomcat status (pid, ports)
jst tc go                 Open the application in a default browser
jst tc deploy|redeploy    Deploy the application to tomcat
jst tc start              Start tomcat
jst tc stop               Stop tomcat
jst tc restart            Restart tomcat

jst src checkout          Checkout both ce and pro sorces (svn co)
jst src status            Status of both ce and pro sorces (svn status -q)
jst src diff              Diff of both ce and pro sorces (svn diff)
jst src revert            Revert both ce and pro sorces (svn revert -R .)

jst src build|rebuild     Build both ce and pro sources (ant build-src-all)
                          optional argument: --skip-tests=[true|false] to skip tests

jst src build|rebuild pro|ce <directory>
                          Build a single ce/pro directory
                          optional argument: --skip-tests=[true|false] to skip tests
                          
                          
init
status                   tomcat, --verbose gives context info

#todo: svn <any_svn_command>
# svn shortcuts
checkout
status
diff
revert

start
stop
restart

build --skip-tests
deploy
go
"""
from docopt import docopt

from resources import context
from resources import src
from resources import tc


if __name__ == "__main__":

    args = docopt(__doc__, version = "0.1", options_first = True)

    resource = args["<resource>"]
    action = args["<action>"]
    action_args = args["<args>"]

    ctx = context.load(args)

    if (resource == "tc"):

        tc.execute(action, action_args, ctx)

    elif (resource == "src"):

        src.execute(action, action_args, ctx)

    elif (resource == "ctx"):

        context.execute(action, action_args, ctx)

    elif (resource == "init"):

        tc.execute("init", action_args, ctx)
        src.execute("init", action_args, ctx)

    elif (resource == "status"):

        tc.execute("status", action_args, ctx)
        context.execute("show", action_args, ctx)
        src.execute("status", action_args, ctx)

    elif (resource == "checkout"):

        src.execute("checkout", action_args, ctx)

    elif (resource == "diff"):

        src.execute("diff", action_args, ctx)

    elif (resource == "revert"):

        src.execute("revert", action_args, ctx)

    elif (resource == "start"):

        tc.execute("start", action_args, ctx)

    elif (resource == "stop"):

        tc.execute("stop", action_args, ctx)

    elif (resource == "restart"):

        tc.execute("restart", action_args, ctx)

    elif (resource == "build"):

        src.execute("build", action_args, ctx)

    elif (resource == "deploy"):

        tc.execute("deploy", action_args, ctx)

    elif (resource == "go"):

        tc.execute("go", action_args, ctx)

    else:
        print("Unknown resource: " + resource)

