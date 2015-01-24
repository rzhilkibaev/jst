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
    2. jstcontext.properties in current directory
    3. JST_CONTEXT environment variable
    The locations are checked in the order they are listed here.
    If location is specified and found then the file is used and the other locations are not checked.
    If location is specified but not present then error is generated.
    If location is not specified then next location is used.
    If none of the locations are present an error is generated.
    '''
    jst_data_dir = expanduser("~") + '/.jst'
    ctx = configparser.ConfigParser()
    _read_config(jst_data_dir + '/jst.properties', ctx)
    _read_config(_get_ctx_file(args), ctx)

    # src
    _ensure_cfg_value(ctx, 'src', 'branch_ce', 'trunk')
    _ensure_cfg_value(ctx, 'src', 'branch_pro', 'trunk')

    url_ce = 'svn+ssh://' + ctx['src']['user'] + '@' + ctx['src']['server_ce'] + '/' + ctx['src']['repo_ce'] + '/' + ctx['src']['branch_ce']
    url_pro = 'svn+ssh://' + ctx['src']['user'] + '@' + ctx['src']['server_pro'] + '/' + ctx['src']['repo_pro'] + '/' + ctx['src']['branch_pro']
    _ensure_cfg_value(ctx, 'src', 'url_ce', url_ce)
    _ensure_cfg_value(ctx, 'src', 'url_pro', url_pro)

    cwd = os.getcwd()

    _ensure_cfg_value(ctx, 'src', 'working_copy_ce', cwd + '/ce')
    _ensure_cfg_value(ctx, 'src', 'working_copy_pro', cwd + '/pro')

    # tc
    _ensure_cfg_value(ctx, 'tc', 'home', cwd + '/tc')
    _ensure_cfg_value(ctx, 'tc', 'distribution', jst_data_dir + '/lib/tomcat')

    return ctx



def _show_context(ctx):

    print('src.url_ce  = ' + ctx['src']['url_ce'])
    print('src.url_pro = ' + ctx['src']['url_pro'])

    print('src.working_copy_ce  = ' + ctx['src']['working_copy_ce'])
    print('src.working_copy_pro = ' + ctx['src']['working_copy_pro'])

    print('tc.home = ' + ctx['tc']['home'])
    print('tc.distribution = ' + ctx['tc']['distribution'])
    print('tc.catalina_opts = ' + ctx['tc']['catalina_opts'])
    print('tc.java_opts = ' + ctx['tc']['java_opts'])



def _show_help():
    print('''\
    [src]

    # svn user
    user = john

    # server name
    server_ce = code.mycompany.com
    server_pro = code.mycompany.com

    # repository name
    repo_ce = myapp
    repo_pro = myapp-pro

    # branch name (default: trunk)
    branch_ce = trunk
    branch_pro = trunk
    
    # url
    # this property overrides all of the above properties
    # default: svn+ssh://<user>@<server_ce(pro)>/<repo_ce(pro)>/<branch_ce(pro)>
    url_ce = svn+ssh://john@code.mycompany.com/myapp/trunk
    url_pro = svn+ssh://john@code.mycompany.com/myapp-pro/trunk
    
    # working copy
    # svn working copy location
    # default: <context_home>/ce(pro)
    working_copy_ce = /home/john/code/ce
    working_copy_pro = /home/john/code/pro
    
    [tc]
    
    # Tomcat's CATALINA_OPTS
    catalina_opts = -agentlib:jdwp=transport=dt_socket,address=11044,server=y,suspend=n -Xms1024m -Xmx2048m -XX:PermSize=32m -XX:MaxPermSize=512m -Xss2m
    # Tomcat's JAVA_OPTS
    java_opts=-Dport.http=18080 -Dport.ajp=18009 -Dport.shutdown=18005
    ''')



def execute(action, args, ctx):
    if (action == 'show'):
        _show_context(ctx)



def _get_ctx_file(args):
    # check the command line argument first
    ctx_file = args['--context']
    if (ctx_file):
        return ctx_file

    # check the context file in the current directory
    ctx_file = os.getcwd() + '/jstcontext.properties'
    if (os.path.isfile(ctx_file)):
        return ctx_file

    # check the environment variable
    ctx_file = os.environ.get('JST_CONTEXT')
    if ((not ctx_file) or (not os.path.isfile(ctx_file))):
        raise FileNotFoundError('Cannot find context file: ' + str(ctx_file))



def _read_config(file, ctx):
    if (not os.path.isfile(file)):
        raise FileNotFoundError('Cannot find context file: ' + str(file))

    ctx.read(file)



def _ensure_cfg_value(ctx, section, option, fallback):
    if (not ctx.get(section, option, fallback = False)):
        ctx.set(section, option, fallback)