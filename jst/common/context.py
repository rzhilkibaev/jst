'''
Created on Jan 18, 2015

@author: rz
'''
import configparser
import os
from os.path import expanduser


def load():
    global_cfg_file = expanduser("~") + '/.jst/jst.properties'
    if (not os.path.isfile(global_cfg_file)):
       raise FileNotFoundError(global_cfg_file)

    cwd = os.getcwd()
    ctx_file = cwd + '/jstcontext.properties'
    if (not os.path.isfile(ctx_file)):
       raise FileNotFoundError(ctx_file)

    global_cfg = configparser.ConfigParser()
    global_cfg.read(global_cfg_file)

    
    ctx = configparser.ConfigParser()
    ctx.read(ctx_file)
    ctx['src']['url_ce'] = 'svn+ssh://' + global_cfg['src']['user'] + '@' + global_cfg['src']['url_ce'] + '/' + ctx['src']['branch_ce']
    ctx['src']['url_pro'] = 'svn+ssh://' + global_cfg['src']['user'] + '@' + global_cfg['src']['url_pro'] + '/' + ctx['src']['branch_pro']

    ctx['src']['working_copy_ce'] = cwd + '/ce'
    ctx['src']['working_copy_pro'] = cwd + '/pro'

    ctx['tc']['distribution'] = global_cfg['tc']['distribution']
    ctx['tc']['home'] = cwd + '/tc'
    
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