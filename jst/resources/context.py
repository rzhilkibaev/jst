"""
Created on Jan 18, 2015

@author: rz
"""
import configparser
import os
from os.path import expanduser
import shutil


_app_name = "jst"
_app_home = os.path.dirname(__file__).replace("/jst/resources", "")

def _ensure_core_properties(ctx):
    data_dir = expanduser("~") + "/." + _app_name
    _ensure_property(ctx, "core", "data_dir", data_dir)

    _ensure_property(ctx, "core", "download_cache", data_dir + "/download_cache")
    if (not os.path.exists(ctx["core"]["download_cache"])):
        os.makedirs(ctx["core"]["download_cache"])

    _ensure_property(ctx, "core", "templates", data_dir + "/templates")
    try:
        shutil.copytree(_app_home + "/templates", ctx["core"]["templates"])
    except FileExistsError:
        pass



def load(args):
    ctx = configparser.ConfigParser()

    _ensure_core_properties(ctx)

    _load_user_properties(ctx)
    _load_workspace_properties(ctx)

    _ensure_all_properties(ctx, args)

    return ctx



def _load_user_properties(ctx):
    user_properties_file = ctx["core"]["data_dir"] + "/" + _app_name + ".properties"
    default_user_properties_file = os.path.dirname(__file__) + "/" + "default.user.properties"

    _ensure_file_present(user_properties_file, default_user_properties_file)
    _load_properties(user_properties_file, ctx)



def _load_workspace_properties(ctx):
    workspace_properties_file = os.getcwd() + "/" + _app_name + ".properties"
    default_workspace_properties_file = os.path.dirname(__file__) + "/" + "default.workspace.properties"

    _ensure_file_present(workspace_properties_file, default_workspace_properties_file)
    _load_properties(workspace_properties_file, ctx)



def _ensure_file_present(file, default):
    if (not os.path.isfile(file)):
        shutil.copy(default, file)



def _load_properties(file, ctx):
    if (not os.path.isfile(file)):
        raise FileNotFoundError("Cannot find properties file: " + str(file))

    ctx.read(file)



def _ensure_all_properties(ctx, args):

    # src
    _ensure_property(ctx, "src", "user", "anonymous")

    _ensure_property(ctx, "src", "server", "svnserver.jaspersoft.com")

    _ensure_property(ctx, "src", "repo_ce", "jasperserver")
    _ensure_property(ctx, "src", "repo_pro", "jasperserver-pro")

    _ensure_property(ctx, "src", "branch_ce", "trunk")
    _ensure_property(ctx, "src", "branch_pro", "trunk")

    url_ce = "https://" + ctx["src"]["user"] + "@" + ctx["src"]["server"] + "/" + ctx["src"]["repo_ce"] + "/" + ctx["src"]["branch_ce"]
    url_pro = "https://" + ctx["src"]["user"] + "@" + ctx["src"]["server"] + "/" + ctx["src"]["repo_pro"] + "/" + ctx["src"]["branch_pro"]
    _ensure_property(ctx, "src", "url_ce", url_ce)
    _ensure_property(ctx, "src", "url_pro", url_pro)

    cwd = os.getcwd()

    _ensure_property(ctx, "src", "working_copy_ce", cwd + "/ce")
    _ensure_property(ctx, "src", "working_copy_pro", cwd + "/pro")

    _ensure_property(ctx, "src", "skip_tests", "false")

    action_args = args['<args>']
    if (("--skip-tests=true" in action_args) or ("--skip-tests" in action_args)):
        ctx["src"]["skip_tests"] = "true"
    elif ("--skip-tests=false" in action_args):
        ctx["src"]["skip_tests"] = "false"

    # tc
    _ensure_property(ctx, "tc", "distribution_url", "http://www.gtlib.gatech.edu/pub/apache/tomcat/tomcat-7/v7.0.59/bin/apache-tomcat-7.0.59.tar.gz")
    _ensure_property(ctx, "tc", "home", cwd + "/tomcat")
    _ensure_property(ctx, "tc", "java_opts", "-Dport.http=8080 -Dport.ajp=8009 -Dport.shutdown=8005")
    _ensure_property(ctx, "tc", "catalina_opts", "-agentlib:jdwp=transport=dt_socket,address=1044,server=y,suspend=n -Djavax.xml.soap.SOAPFactory=org.apache.axis.soap.SOAPFactoryImpl -Djavax.xml.transform.TransformerFactory=org.apache.xalan.processor.TransformerFactoryImpl -Djavax.xml.soap.SOAPConnectionFactory=org.apache.axis.soap.SOAPConnectionFactoryImpl -Djavax.xml.soap.MessageFactory=org.apache.axis.soap.MessageFactoryImpl -Djava.net.preferIPv4Stack=true -Xms1024m -Xmx2048m -XX:PermSize=32m -XX:MaxPermSize=512m -Xss2m -XX:+UseConcMarkSweepGC -XX:+CMSClassUnloadingEnabled")

    # ctx
    _ensure_property(ctx, "ctx", "home", cwd)




def _ensure_property(ctx, section, prop, default = None):
    """
    Ensures that the property is present in the context.
    If default is None and the property is not present then ValueError is thrown.
    If default is set and the property is not present the default is used.
    """
    if (not ctx.get(section, prop, fallback = False)):
        if (default):
            if (not ctx.has_section(section)):
                ctx.add_section(section)
            ctx.set(section, prop, default)
        else:
            raise ValueError("Property " + section + "." + prop + " is mandatory")



def _show_context(ctx):

    print("src.url_ce  = " + ctx["src"]["url_ce"])
    print("src.url_pro = " + ctx["src"]["url_pro"])

    print("src.working_copy_ce  = " + ctx["src"]["working_copy_ce"])
    print("src.working_copy_pro = " + ctx["src"]["working_copy_pro"])
    print("src.skip_tests = " + ctx["src"]["skip_tests"])

    print("tc.home = " + ctx["tc"]["home"])
    print("tc.catalina_opts = " + ctx["tc"]["catalina_opts"])
    print("tc.java_opts = " + ctx["tc"]["java_opts"])



def execute(action, args, ctx):
    if (action == "show"):
        _show_context(ctx)



