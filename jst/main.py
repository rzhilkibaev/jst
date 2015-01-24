""""
Usage: jst [--context=FILE] <resource> <action> [<args>...]


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

