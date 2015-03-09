"""
Created on Jan 7, 2015

@author: rz
"""
from distutils import dir_util
import glob
import os
from os.path import basename
import psutil
import re
import shutil
import subprocess
from time import sleep
import urllib.request


def execute(action, args, ctx):
    """ executes an action against a tomcat instance """

    if action == "init":
        _init(ctx)
    elif action == "status":
        _show_status(ctx)
    elif action == "go":
        _go(ctx)
    elif action == "deploy":
        _deploy(args, ctx)
    elif action == "restart":
        _execute_catalina_action("stop", ctx)
        sleep(6)
        _execute_catalina_action("start", ctx)
        _show_status(ctx)
    elif action == "start":
        _execute_catalina_action(action, ctx)
        _show_status(ctx)
    else:
        _execute_catalina_action(action, ctx)



def _init(ctx):
    tomcat_distribution_file = ctx["core"]["download_cache"] + "/" + basename(ctx["tc"]["distribution_url"])

    if (not os.path.isfile(tomcat_distribution_file)):
        tomcat_distribution_file = urllib.request.urlretrieve(ctx["tc"]["distribution_url"], tomcat_distribution_file)[0]

    if (not os.path.exists(ctx["tc"]["home"])):
        os.makedirs(ctx["tc"]["home"])

    subprocess.call(["tar", "-xf", tomcat_distribution_file, "-C", ctx["tc"]["home"], "--strip-components=1"])

    dir_util.copy_tree(ctx["core"]["templates"] + "/tomcat", ctx["tc"]["home"])



def _show_status(ctx):
    catalina_main_class_arg = "org.apache.catalina.startup.Bootstrap"
    catalina_home_arg = "-Dcatalina.home=" + ctx["tc"]["home"]

    for proc in psutil.process_iter():
        if proc.name == "java" \
                and catalina_main_class_arg in proc.cmdline \
                and catalina_home_arg in proc.cmdline:
            http_port = _get_http_port(proc.cmdline)
            debug_port = _get_debug_port(proc.cmdline)
            print("pid=" + str(proc.pid) + ", port.http=" + str(http_port) + ", port.jdwp=" + str(debug_port))



def _get_http_port(catalina_args):
    for catalina_arg in catalina_args:
        match = re.search("-Dport\.http=(\d*)", catalina_arg)
        if match:
            return match.group(1)



def _get_debug_port(catalina_args):
    for catalina_arg in catalina_args:
        match = re.search("-agentlib:.*,address=(\d*)", catalina_arg)
        if match:
            return match.group(1)



def _go(ctx):
    match = re.search("-Dport\.http=(\d*)", ctx["tc"]["java_opts"])
    if match:
        http_port = match.group(1)
        subprocess.call(["xdg-open", "http://localhost:" + http_port + "/jasperserver-pro"],
                        stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)



def _deploy(args, ctx):

    if len(args) == 0:
        build_xml = ctx["src"]["working_copy_ce"] + "/buildomatic/build.xml"
        subprocess.call(["ant", "-buildfile", build_xml, "deploy-webapp-pro"])
    else:
        edition = args[0]
        source = ctx["src"]["working_copy_" + edition] + "/" + args[1] + "/target/*.jar"
        files = glob.glob(source)
        destination = ctx["tc"]["home"] + "/webapps/jasperserver-pro/WEB-INF/lib/"
        if (len(files)):
            shutil.copy(files[0], destination)
            print(files[0])
        else:
            print("nothing to copy at: " + source)



def _execute_catalina_action(action, ctx):
    """ executes catalina.sh script passing action as an argument """

    os.environ["CATALINA_HOME"] = ctx["tc"]["home"]
    os.environ["CATALINA_OPTS"] = ctx["tc"]["catalina_opts"]
    os.environ["JAVA_OPTS"] = ctx["tc"]["java_opts"]
    catalina = ctx["tc"]["home"] + "/bin/catalina.sh"
    subprocess.call([catalina, action])

