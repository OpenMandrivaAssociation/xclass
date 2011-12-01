%define major	0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %name

Summary: GUI toolkit resembling Windows(TM) 95
Name: xclass
Version: 0.9.2
Release: %mkrel 9
Source0: %{name}-%{version}.tar.bz2
Patch0: xclass-0.6.3-mime-types.patch
# From SUSE OSS-Factory
Patch1:	xclass-0.9.2-gcc40.patch
Url:	http://sourceforge.net/projects/xclass/
License: LGPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: libx11-devel
BuildRequires: libxpm-devel
BuildRequires: libxext-devel
BuildRequires: mesaglu-devel
Requires: %{libname}
Provides: %{name}-icons
Obsoletes: %{name}-icons

%description
Xclass is a GUI toolkit resembling Windows 95. It is Xlib-based and is 
written in C++.

%package -n %{libname}
Summary: Win95-looking GUI toolkit
Group: System/Libraries
Requires: %{name}

%description -n %{libname}
Xclass is a GUI toolkit resembling Windows 95. It is Xlib-based and is 
written in C++.

%package -n %{develname}
Summary: Win95-looking GUI toolkit
Group: Development/C++
Obsoletes: %{_lib}xclass0-devel < 0.9.2-9
Provides: %{name}-devel = %{version}
Provides: lib%{name}-devel = %{version}
Requires: %{libname} = %{version}

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
export CFLAGS="$RPM_OPT_FLAGS -DPIC -fPIC"
export CXXFLAGS="$CFLAGS"
%configure2_5x --enable-debug=no
%make
%make shared

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root)
%dir %{_datadir}/xclass
%dir %{_datadir}/xclass/icons
%{_datadir}/xclass/icons/*.xpm
%{_datadir}/xclass/icons/*.xbm
%{_datadir}/xclass/icons/*.icon
%config(noreplace) %{_sysconfdir}/xclassrc
%config(noreplace) %{_sysconfdir}/xclass-mime.types

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/Programming.notes doc/INSTALL doc/Layout.notes
%_bindir/xc-config
%multiarch_bindir/xc-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
