""""
Usage: jst [-h|--help] <resource> <action> [<args>...]

This tool manages jrs instances.

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
"""
from docopt import docopt

from resources import context


if __name__ == '__main__':

    args = docopt(__doc__, version = '0.1', options_first = True)

    resource = args['<resource>']
    action = args['<action>']
    action_args = args['<args>']

    ctx = context.load(args)

    if (resource == 'tc'):

        from resources import tc

        tc.execute(action, action_args, ctx)

    elif (resource == 'src'):

        from resources import src

        src.execute(action, action_args, ctx)

    elif (resource == 'ctx'):

        context.execute(action, action_args, ctx)

    else:
        print('Unknown resource: ' + resource)

