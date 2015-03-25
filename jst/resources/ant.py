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

    dir_name = options.get("--dir")
    flavor = options.get("--flavor")
    if (dir_name):
        ant_target = "build-dir-" + flavor # ce/pro
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", ant_target, "-DdirName=" + dir_name])
    else:
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", "build-src-all"])
