# Debug package is empty and rpmlint rejects build
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define major	0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	GUI toolkit resembling Windows(TM) 95
Name:		xclass
Version:	0.9.2
Release:	22
License:	LGPL
Group:		System/Libraries
Url:		http://sourceforge.net/projects/xclass/
Source0:	%{name}-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
Patch0:		xclass-0.6.3-mime-types.patch
# From SUSE OSS-Factory
Patch1:		xclass-0.9.2-gcc40.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(glu)
Requires:	%{libname} = %{version}-%{release}

%description
Xclass is a GUI toolkit resembling Windows 95. It is Xlib-based and is 
written in C++.

%package -n %{libname}
Summary:	Win95-looking GUI toolkit
Group:		System/Libraries
Requires:	%{name}

%description -n %{libname}
Xclass is a GUI toolkit resembling Windows 95. It is Xlib-based and is 
written in C++.

%package -n %{develname}
Summary:	Win95-looking GUI toolkit
Group:		Development/C++
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n %{develname}
Xclass is a GUI toolkit resembling Windows 95. It is Xlib-based and is
written in C++.

This package contains headers and static libraries to develop program using
Xclass.

%prep
%setup -q
%patch0 -p1 -b .mime-types
%patch1 -p0 -b .gcc40

# AW: new way to install /etc/xclass-mime.types instead of /etc/mime.types
mv doc/mime.types doc/xclass-mime.types
perl -pi -e "s,mime.types,xclass-mime.types,g" doc/Makefile.in lib/libxclass/OResourcePool.cc test/ftest.cc
# AW: new way to fix references to /usr/local in the build
perl -pi -e "s,/usr/local/xclass-icons,%_datadir/%{name}/icons,g" lib/libxclass/Makefile.in lib/libxclass/Makefile.intel
perl -pi -e "s,/usr/local/xclass,/,g" lib/libxclass/Makefile.in lib/libxclass/Makefile.intel

%build
# Needed for x86-64 build
export CFLAGS="%{optflags} -DPIC -fPIC"
export CXXFLAGS="$CFLAGS"
%configure2_5x --enable-debug=no
%make
%make shared

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir} %{buildroot}%{_includedir} 
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_datadir}/xclass/icons
make etc_dir=%{buildroot}%{_sysconfdir} config_dir=%{buildroot}%{_bindir} \
  doc_dir=%{buildroot}%{_docdir} header_dir=%{buildroot}%{_includedir}/xclass lib_dir=%{buildroot}%{_libdir} \
  icon_dir=%{buildroot}%{_datadir}/xclass/icons install
make etc_dir=%{buildroot}%{_sysconfdir} config_dir=%{buildroot}%{_bindir} \
  doc_dir=%{buildroot}%{_docdir} header_dir=%{buildroot}%{_includedir}/xclass lib_dir=%{buildroot}%{_libdir} \
  icon_dir=%{buildroot}%{_datadir}/xclass/icons install_shared
ln -sf libxclass.so.%{version} %{buildroot}%{_libdir}/libxclass.so.%{major}
ln -sf libxclass.so.%{version} %{buildroot}%{_libdir}/libxclass.so

# fix reference to icons dir
perl -pi -e "s,(^icon dir).+,\1 = %{_datadir}/xclass/icons," \
  %{buildroot}%{_sysconfdir}/xclassrc

# remove unpackaged files
rm -f  %{buildroot}%{_datadir}/xclass/icons/Makefile{,.in}
rm -rf %{buildroot}%{_datadir}/doc

%multiarch_binaries %{buildroot}%{_bindir}/xc-config

%files
%dir %{_datadir}/xclass
%dir %{_datadir}/xclass/icons
%{_datadir}/xclass/icons/*.xpm
%{_datadir}/xclass/icons/*.xbm
%{_datadir}/xclass/icons/*.icon
%config(noreplace) %{_sysconfdir}/xclassrc
%config(noreplace) %{_sysconfdir}/xclass-mime.types

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%doc doc/Programming.notes doc/INSTALL doc/Layout.notes
%{_bindir}/xc-config
%{multiarch_bindir}/xc-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-9mdv2011.0
+ Revision: 661758
- multiarch fixes

* Thu Dec 23 2010 Funda Wang <fwang@mandriva.org> 0.9.2-8mdv2011.0
+ Revision: 623983
- new devel package name policy

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-7mdv2011.0
+ Revision: 608195
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-6mdv2010.1
+ Revision: 524376
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.9.2-5mdv2009.1
+ Revision: 351231
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.9.2-4mdv2009.0
+ Revision: 226018
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.9.2-3mdv2008.1
+ Revision: 171182
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Jun 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.2-2mdv2008.0
+ Revision: 38342
- correct devel package group (#28160)

* Sat May 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.2-1mdv2008.0
+ Revision: 26421
- improve summary / descriptions
- rename xclass-icons to xclass, move config files to it (comply with lib policy)
- add patch from SUSE to fix build with gcc 4.x
- drop all patches except mime types: no longer relevant
- clean spec
- 0.9.2
- Import xclass



* Mon May 08 2006 Stefan van der Eijk <stefan@eijk.nu> 0.6.3-15mdk
- rebuild for sparc

* Wed Feb  9 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-14mdk
- multiarch

* Tue Jul 20 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.6.3-13mdk
- patch3: remove defines that interfere with building apps using this lib
- patch4: fix some warnings

* Fri Jun  4 2004  <lmontel@n2.mandrakesoft.com> 0.6.3-12mdk
- Rebuild

* Thu Feb 26 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.6.3-11mdk
- fix DIRM

* Fri Sep 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-10mdk
- mklibname, more C++ fixes

* Thu Dec  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-9mdk
- We do need icons, also fix /etc/xclassrc and OX_DEFAULT_ROOT. Likewise for
  xclass mime.types. How did people usually test this package ?!?

* Wed Dec  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-8mdk
- Make it lib64 aware
- Remove unpackaged files, maintainer will check where icons et
  al. were supposed to be used, if any use is found

* Thu Aug 29 2002 Daouda LO <daouda@mandrakesoft.com> 0.6.3-7mdk
- obsoleted xclass for 8.2 <-> 9.0 upgrades.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-6mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.3-5mdk
- Automated rebuild with gcc3.2

* Mon Jul 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.6.3-4mdk
- Build PIC on all architectures.

* Mon Jun 17 2002 Daouda LO <daouda@mandrakesoft.com> 0.6.3-3mdk
- upload all xclass packages. 
- obsoletes/provides xclass.

* Mon Jun 17 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.6.3-2mdk
- Remove requires for lib package created from nuking the main package.

* Mon Jun 17 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.6.3-1mdk
- New and shiny source.
- Updated C++ workarounds.
- Currently broken on the Alpha because of some gp relocation symbols
  which I don't really know why.

* Sat Jun 15 2002 Stefan van der Eijk <stefan@eijk.nu> 0.6.2-3mdk
- fix provides / requires on lib package

* Tue May 28 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.2-2mdk
- Patch0: ISO C++ fixes and workarounds. They should really use
  iterators instead. Also know that there is no conversion from a
  vector<> element pointer to a vector<>::iterator...

* Wed Mar 20 2002 Daouda LO <daouda@mandrakesoft.com> 0.6.2-1mdk
- release 0.6.2

* Tue Dec  4 2001 Daouda LO <daouda@mandrakesoft.com> 0.5.4-5mdk
- add xclass package
- cleanup 

* Tue Nov 27 2001 Daouda LO <daouda@mandrakesoft.com> 0.5.4-3mdk
- revert back to 0.5.4.

* Sat Nov 24 2001 Daouda Lo <daouda@mandrakesoft.com> 0.6.1-1mdk
- release 0.6.1

* Sun Jul 01 2001 Stefan van der Eijk <stefan@eijk.nu> 0.5.4-2mdk
- BuildRequires: xpm-devel

* Tue Jun 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.4-1mdk
- First Mandrake package


# end of file
