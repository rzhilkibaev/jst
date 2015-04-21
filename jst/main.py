""""
Usage:
  jst [options] <command>

This tool manages jrs instances.

Options:
  -h --help           This help text
  --skip-tests=<val>        Skip test while running maven build [default: true]
  --dir=<directory>   Directory where the project is located
  --edition=<edition> ce or pro
    
Commands:
  init                Initialize context and tomcat
  deploy              Deploy to tomcat
  status              Tomcat status
  start               Start tomcat
  stop                Stop tomcat
  restart             Restart tomcat
  go                  Open jrs in browser
  svn-status          Svn status
  checkout            svn checkout
  update              svn update
  diff                svn diff
  revert              svn revert
  ctx-status          Context info
  build               Build
"""

from docopt import docopt
import time

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

    ctx = context.load(args)

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

    start_time = time.strftime("%I:%M:%S %p")

    commands[command](ctx, args)

    print("Start/end time: " + start_time + " - " + time.strftime("%I:%M:%S %p"))
