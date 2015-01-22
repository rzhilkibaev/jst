'''
Created on Jan 18, 2015

@author: rz
'''
import configparser
import os
from os.path import expanduser


def load(args):
    '''
    Loads a context from a context file.
    A context file is a file in INI format which specifies properties associated with a particular context.
    There are several ways to specify context file location.
    1. --context command line argument
    2. JST_CONTEXT environment variable
    3. jstcontext.properties in current directory
    The locations are checked in the order they are listed here.
    If location is specified and found then the file is used and the other locations are not checked.
    If location is specified but not present then error is generated.
    If location is not specified then next location is used.
    If none of the locations are present an error is generated.
    '''
    ctx = configparser.ConfigParser()
    _read_config(expanduser("~") + '/.jst/jst.properties', ctx)
    _read_config(_get_ctx_file(args), ctx)

    ctx['src']['url_ce'] = 'svn+ssh://' + ctx['src']['user'] + '@' + ctx['src']['url_ce'] + '/' + ctx['src']['branch_ce']
    ctx['src']['url_pro'] = 'svn+ssh://' + ctx['src']['user'] + '@' + ctx['src']['url_pro'] + '/' + ctx['src']['branch_pro']

    cwd = os.getcwd()

    ctx['src']['working_copy_ce'] = cwd + '/ce'
    ctx['src']['working_copy_pro'] = cwd + '/pro'

    ctx['tc']['home'] = cwd + '/tc'
    ctx['tc']['distribution'] = ctx['tc']['distribution']

    return ctx



def show(ctx):

    print('src.url_ce  = ' + ctx['src']['url_ce'])
    print('src.url_pro = ' + ctx['src']['url_pro'])

    print('src.working_copy_ce  = ' + ctx['src']['working_copy_ce'])
    print('src.working_copy_pro = ' + ctx['src']['working_copy_pro'])

    print('tc.home = ' + ctx['tc']['home'])
    print('tc.distribution = ' + ctx['tc']['distribution'])
    print('tc.catalina_opts = ' + ctx['tc']['catalina_opts'])
    print('tc.java_opts = ' + ctx['tc']['java_opts'])



def _get_ctx_file(args):
    ctx_file = args['--context']
    if (not ctx_file):
        ctx_file = os.environ.get('JST_CONTEXT')
    if (not ctx_file):
        ctx_file = os.getcwd() + '/jstcontext.properties'

    return ctx_file



def _read_config(file, ctx):
    if (not os.path.isfile(file)):
        raise FileNotFoundError(file)

    ctx.read(file)
