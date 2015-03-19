"""
Created on Jan 7, 2015

@author: rz
"""
import subprocess


def checkout(ctx, options):
    subprocess.call(["svn", "checkout", ctx["src"]["url_ce"], ctx["src"]["working_copy_ce"]])
    subprocess.call(["svn", "checkout", ctx["src"]["url_pro"], ctx["src"]["working_copy_pro"]])

def update(ctx, options):
    subprocess.call(["svn", "update", ctx["src"]["working_copy_ce"]])
    subprocess.call(["svn", "update", ctx["src"]["working_copy_pro"]])

def status(ctx, options):
    subprocess.call(["svn", "status", ctx["src"]["working_copy_ce"]])
    subprocess.call(["svn", "status", ctx["src"]["working_copy_pro"]])

def diff(ctx, options):
    subprocess.call(["svn", "diff", ctx["src"]["working_copy_ce"]])
    subprocess.call(["svn", "diff", ctx["src"]["working_copy_pro"]])

def revert(ctx, options):
    subprocess.call(["svn", "revert", ctx["src"]["working_copy_ce"], "-R"])
    subprocess.call(["svn", "revert", ctx["src"]["working_copy_pro"], "-R"])

