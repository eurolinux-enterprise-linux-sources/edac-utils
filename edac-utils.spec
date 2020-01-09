Name:		edac-utils
Version:	0.9
Release:	14%{?dist}
Summary:	Userspace helper for kernel EDAC drivers

Group:		System Environment/Base
License:	GPLv2+
URL:		http://sourceforge.net/projects/edac-utils/
Source0:	http://dl.sourceforge.net/sourceforge/edac-utils/%{name}-%{version}.tar.bz2
Patch0:		edac_ctl-remove_driver_loading.patch
Patch1:		edac_init-fix_messages.patch
Patch2:		edac_ctl-fix_model_parsing.patch
Patch3:		edac_init-sysv-compliance.patch
Patch4:		edac_init-only_return_defined_error_codes.patch
Patch5:		labels.db-Add-new-labels-from-edac-utils-0.16.patch
Patch6:		libedac-allow-handling-up-to-6-channels-instead-of-2.patch
Patch7:		libedac-Returns-an-error-if-get_sysfs_uint_attr-fail.patch
Patch8:		edac-util.1-Fix-a-few-mistakes-at-the-spec.patch
Patch9:		edac-ctl-add-delay-status-and-improve-motherboard-id.patch
Patch10:	add-more-labels-to-sync-with-rhel5.patch
Patch11:	edac_ctl_improve_parser.patch
Patch12:	no_strict_aliasing.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
Requires:	hwdata, dmidecode, sysfsutils
Requires(post):	chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

BuildRequires:	libsysfs-devel
ExclusiveArch:	%{ix86} x86_64

%description 
EDAC is the current set of drivers in the Linux kernel that handle
detection of ECC errors from memory controllers for most chipsets
on i386 and x86_64 architectures. This userspace component consists
of an init script which makes sure EDAC drivers and DIMM labels
are loaded at system startup, as well as a library and utility
for reporting current error counts from the EDAC sysfs files.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development headers and libraries
for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
%configure --disable-static
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
make install-exec install-data DESTDIR="$RPM_BUILD_ROOT"
# Remove libtool archive
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ $1 = 1 ]; then
	/sbin/chkconfig --add edac
fi

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del edac
fi

%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
	/sbin/service edac condrestart >/dev/null 2>&1 || :
fi

%files 
%defattr(-,root,root,-)
%doc COPYING README NEWS ChangeLog DISCLAIMER
%{_sbindir}/edac-ctl
%{_bindir}/edac-util
%{_libdir}/*.so.*
%{_mandir}/*/*
%dir %attr(0755,root,root) %{_sysconfdir}/edac
%config(noreplace) %{_sysconfdir}/edac/*
%{_initddir}/edac

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/edac.h

%changelog
* Wed Apr 27 2011 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.9-14
- Fix a gcc new warning: warning: dereferencing pointer 'pfree' does break strict-aliasing rules

* Fri Apr 22 2011 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.9-13
- Enhance motherboard dmi decoding to use DMI type 1, if type 2 
  is not available

* Thu Oct  4 2010 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.9-12
- Add improvements from upstream version 0.16, in order to support newer
  edac drivers. Also, sync edac labels with RHEL5 package

* Thu Sep  9 2010 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.9-11.3
- return 4 for lack of permissions, 1 for any other error at the edac-ctl

* Mon Jun 12 2010 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.9-11.2
- Make init script compliant with https://fedoraproject.org/wiki/Packaging/SysVInitScript

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.9-11.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9-9
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-8
- Autorebuild for GCC 4.3

* Wed Jul 18 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-7
- including missing .patch file

* Tue Jul 17 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-6
- building FC7 package

* Thu Jul 09 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-5
- Fixed start/stop message, missing echo
- Fixed status command to use edac-util

* Thu Jun 15 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-4
- Removed debug code left by mistake on initrd file
- Fixed model comparing in edac-ctl script

* Wed Jun 13 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-3
- Adding COPYING to documents
- Fixing Requires to use a single equal sign, instead of two

* Wed Jun 13 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-2
- Multiple updates in spec file to conform to the standards pointed by
  Jarod Wilson

* Wed Jun 06 2007 Aristeu Rozanski <arozansk@redhat.com> 0.9-1
- Updated version to 0.9, separate project now
- Updated spec file based on upstream edac-utils spec file
- Removed driver loading portion in a separate patch, it'll be removed from
  upstream too
- Fixed init script to use functions and daemon function

* Thu Apr 19 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-3
- Updated initrd script to start after syslogd, otherwise if the board isn't
  supported, the user will never know.

* Thu Apr 19 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-2
- Changing this package to noarch and preventing the build on ia64, ppc64,
  s390 and s390x

* Thu Mar 12 2007 Aristeu Rozanski <arozansk@redhat.com> 20061222-1
- Package created

