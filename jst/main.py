""""
Usage:
  jst [options] <command>

This tool manages jrs instances.

Options:
  -h --help           This help text
    
Commands:
  init                Initialize context and tomcat
  status              Tomcat status
  svn-status          Svn status
  ctx-status          Context info
  checkout            svn checkout
  update              svn update
  diff                svn diff
  revert              svn revert
"""

from docopt import docopt

from resources import context, ant
from resources import src
from resources import svn
from resources import tc


def init(ctx, options):
    tc.init(ctx)
    src.init(ctx)



if __name__ == "__main__":

    args = docopt(__doc__, version = "0.1")

    command = args["<command>"]
    options = []

    ctx = context.load(options)

    commands = {
              "init": init,
              # tomcat
              "deploy": tc.deploy,
              "status": tc.status,
              "start": tc.start,
              "stop": tc.stop,
              "restart": tc.restart,
              "go": tc.go,
              # svn
              "svn-status": svn.status,
              "checkout": svn.checkout,
              "update": svn.update,
              "diff": svn.diff,
              "revert": svn.revert,
              # ctx
              "ctx-status": context.show_context,
              # ant
              "build": ant.build,
              }

    commands[command](ctx, options)
