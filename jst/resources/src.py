'''
Created on Jan 7, 2015

@author: rz
'''
from os.path import expanduser
import subprocess


def execute(action, args, ctx):
    """ executes an action against ce and pro source trees """

    buildomatic_dir = ctx['src']['working_copy_ce'] + '/buildomatic'

    if action == 'init':
        _init(buildomatic_dir, ctx)
    elif action == 'build':
        _build(args, buildomatic_dir)
    else:
        _execute_shell_action_on_working_copy(action, ctx['src']['url_ce'], ctx['src']['working_copy_ce'])
        _execute_shell_action_on_working_copy(action, ctx['src']['url_pro'], ctx['src']['working_copy_pro'])



def _init(buildomatic_dir, ctx):
    """ configures build system and application (set database properties, etc...) """
    _execute_shell_action_on_working_copy('checkout', ctx['src']['url_ce'], ctx['src']['working_copy_ce'])
    _execute_shell_action_on_working_copy('checkout', ctx['src']['url_pro'], ctx['src']['working_copy_pro'])
    _write_default_master_properties(buildomatic_dir, ctx)
    _build(buildomatic_dir)
    _configure_eclipse(buildomatic_dir, ctx)



def _configure_eclipse(buildomatic_dir, ctx):
    cmd = ['mvn', 'eclipse:eclipse', '-DdownloadSources=true', '-DdownloadJavadocs=true']
    subprocess.call(cmd, cwd = ctx['src']['working_copy_ce'])
    subprocess.call(cmd, cwd = ctx['src']['working_copy_pro'])



def _write_default_master_properties(buildomatic_dir, ctx):
    """ writes default_master.properties file """
    properties_template_file = expanduser("~") + '/.jst/templates/default_master.properties'
    with open(buildomatic_dir + '/default_master.properties', 'wt') as fout:
        with open(properties_template_file, 'rt') as fin:
            for line in fin:
                result_line = line.replace('%tc.home%', ctx['tc']['home'])
                result_line = result_line.replace('%src.working_copy_ce%', ctx['src']['working_copy_ce'])
                result_line = result_line.replace('%src.working_copy_pro%', ctx['src']['working_copy_pro'])
                fout.write(result_line)
                print(result_line, end = '')

def _build(buildomatic_dir, args = []):
    """
    builds both source trees
        args - if empty then both ce and pro source trees are built, otherwise
            first argument is either 'ce' or 'pro' and the second a directory to build
    """
    if len(args) == 0:
        subprocess.call(['ant', '-DSKIP_TEST_ARG=skipTests', '-buildfile', buildomatic_dir + '/build.xml', 'build-src-all'])
    else:
        ant_target = 'build-dir-' + args[0]
        dir_name = args[1]
        subprocess.call(['ant', '-DSKIP_TEST_ARG=skipTests', '-buildfile', buildomatic_dir + '/build.xml', ant_target, '-DdirName=' + dir_name])

def _execute_shell_action_on_working_copy(action, url, working_copy):
    """ executes shell one-liner """
    action_to_cmd = {'checkout': ['svn', 'checkout', url, working_copy],
                     'update': ['svn', 'update', working_copy],
                     'status': ['svn', 'status', '--quiet', working_copy],
                     'diff': ['svn', 'diff', working_copy],
                     'revert': ['svn', 'revert', '-R', working_copy],
                     'wipe': ['rm', '-R', working_copy]}
    try:
        cmd = action_to_cmd[action]
    except KeyError:
        raise ValueError("Unknown action: " + action)

    subprocess.call(cmd)

