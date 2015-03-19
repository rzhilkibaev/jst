"""
Created on Jan 7, 2015

@author: rz
"""
import subprocess


def build(ctx, options):
    """
    builds both source trees
        args - if empty then both ce and pro source trees are built, otherwise
            first argument is either "ce" or "pro" and the second a directory to build
    """
    buildomatic_dir = ctx["src"]["working_copy_ce"] + "/buildomatic"
    skip_tests_arg = ""

    if (ctx["src"]["skip_tests"] == "true"):
        skip_tests_arg = "-DSKIP_TEST_ARG=skipTests"

    if len(options) == 0:
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", "build-src-all"])
    else:
        ant_target = "build-dir-" + options[0] # ce/pro
        dir_name = options[1]
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", ant_target, "-DdirName=" + dir_name])
