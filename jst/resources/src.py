"""
Created on Jan 7, 2015

@author: rz
"""
import os
import shutil
import subprocess


def execute(action, args, ctx):
    """ executes an action against ce and pro source trees """

    buildomatic_dir = ctx["src"]["working_copy_ce"] + "/buildomatic"

    if action == "init":
        _init(buildomatic_dir, ctx)
    elif action in ["build", "rebuild"]:
        _build(ctx, buildomatic_dir, args)
    else:
        _execute_svn_action(action, ctx["src"]["url_ce"], ctx["src"]["working_copy_ce"])
        _execute_svn_action(action, ctx["src"]["url_pro"], ctx["src"]["working_copy_pro"])



def _init(buildomatic_dir, ctx):
    """ configures build system and application (set database properties, etc...) """

    _clean_checkout(ctx["src"]["url_ce"], ctx["src"]["working_copy_ce"])
    _clean_checkout(ctx["src"]["url_pro"], ctx["src"]["working_copy_pro"])

    _write_default_master_properties(buildomatic_dir, ctx)

    _build(ctx, buildomatic_dir)

    _write_maven_settings_xml(buildomatic_dir, ctx)



def _clean_checkout(url, working_copy):
    if (os.path.exists(working_copy)):
        subprocess.call(["rm", "-R", working_copy])

    _execute_svn_action("checkout", url, working_copy)



def _write_default_master_properties(buildomatic_dir, ctx):
    """ writes default_master.properties file """
    properties_template_file = ctx["core"]["data_dir"] + "/templates/default_master.properties"
    with open(buildomatic_dir + "/default_master.properties", "wt") as fout:
        with open(properties_template_file, "rt") as fin:
            for line in fin:
                result_line = line.replace("%tc.home%", ctx["tc"]["home"])
                result_line = result_line.replace("%src.working_copy_ce%", ctx["src"]["working_copy_ce"])
                result_line = result_line.replace("%src.working_copy_pro%", ctx["src"]["working_copy_pro"])
                fout.write(result_line)
                print(result_line, end = "")

def _build(ctx, buildomatic_dir, args = []):
    """
    builds both source trees
        args - if empty then both ce and pro source trees are built, otherwise
            first argument is either "ce" or "pro" and the second a directory to build
    """
    skip_tests_arg = ""

    if (ctx["src"]["skip_tests"] == "true"):
        skip_tests_arg = "-DSKIP_TEST_ARG=skipTests"

    if len(args) == 0:
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", "build-src-all"])
    else:
        ant_target = "build-dir-" + args[0] # ce/pro
        dir_name = args[1]
        subprocess.call(["ant", skip_tests_arg, "-buildfile", buildomatic_dir + "/build.xml", ant_target, "-DdirName=" + dir_name])



def _write_maven_settings_xml(buildomatic_dir, ctx):
    jst_xml = buildomatic_dir + "/jst.xml"
    if (not os.path.isfile(jst_xml)):
        shutil.copy(ctx["core"]["templates"] + "/jst.xml", jst_xml)

    lines = subprocess.check_output(["ant", "-buildfile", jst_xml, "maven-effective-settings"], universal_newlines = True).split("\n")

    first_line = '[java] <?xml version="1.0" encoding="UTF-8"?>'
    last_line = '[java] </settings>'

    xml_started = False

    result = ""

    for line in lines:

        if (first_line in line):
            xml_started = True

        if (xml_started):
            # strip '     [java] '
            result += line[12:] + "\n"

        if (last_line in line):
            break

    with open(ctx["ctx"]["home"] + "/maven-settings.xml", "w") as text_file:
        print(result, file = text_file)


def _execute_svn_action(action, url, working_copy):
    """ executes shell one-liner """
    action_to_cmd = {"checkout": ["svn", "checkout", url, working_copy],
                     "update": ["svn", "update", working_copy],
                     "status": ["svn", "status", "--quiet", working_copy],
                     "diff": ["svn", "diff", working_copy],
                     "revert": ["svn", "revert", "-R", working_copy]}
    try:
        cmd = action_to_cmd[action]
    except KeyError:
        raise ValueError("Unknown action: " + action)

    subprocess.call(cmd)

