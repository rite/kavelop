#! /usr/bin/env python

VERSION='0.0.1'
APPNAME='kafelop'

top = '.'
out = 'build'

def configure(conf):

	conf.setenv('debug')
        conf.load('compiler_cxx')
	conf.write_config_header('debug/config.h', remove=False)

	conf.setenv('release', env=conf.env.derive()) # start with a copy instead of a new env
	conf.env.CFLAGS = ['-O2']
        conf.load('compiler_cxx')
	conf.write_config_header('release/config.h')

def build(bld):

	if not bld.variant:
		bld.fatal('Call "waf build_debug" or "waf build_release", and read the comments in the wscript file!')

        bld.recurse('src')

def options(opt):
        opt.load('compiler_cxx')

def init(ctx):
	from waflib.Build import BuildContext, CleanContext, InstallContext, UninstallContext

	for x in 'debug release'.split():
		for y in (BuildContext, CleanContext, InstallContext, UninstallContext):
			name = y.__name__.replace('Context','').lower()
			class tmp(y):
				cmd = name + '_' + x
				variant = x

	def buildall(ctx):
		import waflib.Options
		for x in ('build_debug', 'build_release'):
			waflib.Options.commands.insert(0, x)
