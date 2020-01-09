##*****************************************************************************
## $Id: Makefile.am 4266 2007-05-08 22:58:01Z grondo $
##*****************************************************************************
## Process this file with automake to produce Makefile.in.
##***************************************************************************** 

AM_CPPFLAGS = \
	-I$(top_srcdir)/src/lib/

bin_PROGRAMS = \
	edac-util 

man_MANS = \
	edac-util.1 \
	edac-ctl.8

dist_sbin_SCRIPTS = \
	edac-ctl

edac_util_LDADD = \
	$(top_builddir)/src/lib/libedac.la

edac_util_SOURCES = \
	edac-util.c \
	list.h      \
	list.c      \
	split.h     \
	split.c
