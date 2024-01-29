#!/usr/bin/env python3
import os,sys
from invoke import task

@task
def execute(c):
	os.system(str(sys.executable) + " setup.py run 8899")

@task
def gitr(c):
	for x in [
		'git config --global user.email "EMAIL"',
		'git config --global user.name "UserName (pythondev@lite)"'
	]:
		print(x);os.system(x)

@task
def cleanenv(c):
	for x in [
		'CachedExtensions/',
		'CachedExtensionVSIXs/',
		'User/',
		'Machine/',
		'extensions/',
		'logs/',
		'coder.json',
		'machineid',
	]:
		x = "yes|rm -r " + str(x)
		print(x);os.system(x)

@task
def extensions(c):
	cmd = f"{sys.executable} .devcontainer/devcontainer.py"
	print(cmd);os.system(cmd)
