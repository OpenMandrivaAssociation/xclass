%define major	0
%define libname	%mklibname %{name} %{major}

Summary: Xclass is a Win95-looking GUI toolkit
Name: xclass
Version: 0.6.3
Release: 15mdk
Source0: http://download.hexonet.com/software/xclass/%{name}-%{version}.tar.bz2
Patch0: xclass-0.6.3-c++fixes.patch.bz2
Patch1: xclass-0.6.3-link-with-g++.patch.bz2
Patch2: xclass-0.6.3-mime-types.patch.bz2
Patch3:	xclass-0.6.3-no-min-max-defines.patch.bz2
Patch4:	xclass-0.6.3-stl-warnings.patch.bz2
Url:	http://sourceforge.net/projects/xclass
License: LGPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: XFree86-devel xpm-devel
Requires: %{libname}

%description
Xclass is a Win95-looking GUI toolkit, it is Xlib-based and is written in C++.

%package icons
Summary: Xclass icons
Group: System/Libraries

%description icons
Xclass is a Win95-looking GUI toolkit, it is Xlib-based and is written
in C++. This package contains necessary icons for certain dialog
boxes.

%package -n %{libname}
Summary: Xclass is a Win95-looking GUI toolkit
Group: System/Libraries
Obsoletes: %{name} , %{name} = %{version}
Provides: %{name} = %{version}
Requires: %{name}-icons

%description -n %{libname}
Xclass is a Win95-looking GUI toolkit, it is Xlib-based and is written in C++.

%package -n %{libname}-devel
Summary: Xclass is a Win95-looking GUI toolkit
Group: System/Libraries
Provides: %{name}-devel = %{version}
Provides: lib%{name}-devel = %{version}
Requires: %{libname} = %{version}

%description -n %{libname}-devel
Xclass is a Win95-looking GUI toolkit, it is Xlib-based and is written in C++.

This package contains headers and static libraries to develop program using
Xclass


%prep
%setup -q
%patch0 -p1 -b .c++fixes
%patch1 -p1 
%patch2 -p1 -b .mime-types
%patch3 -p1 -b .no-min-max-defines
%patch4 -p1 -b .stl-warnings

# make it lib64 aware, avoid patch
perl -pi -e "s,(/usr/X11R6|@exec_prefix@)/lib\b,\1/%{_lib},g" \
  lib/libxclass/Makefile.in config/xc-config.in

%build

export CFLAGS="$RPM_OPT_FLAGS -DPIC -fPIC"
export CXXFLAGS="$CFLAGS"
%configure --enable-debug=no

make DEFINES='-DOX_DEFAULT_POOL=\"%{_datadir}/xclass/xclass-icons\" -DOX_DEFAULT_ROOT=\"/\"'

(cd lib/libxclass
make DEFINES='-DOX_DEFAULT_POOL=\"%{_datadir}/xclass/xclass-icons\" -DOX_DEFAULT_ROOT=\"/\"' shared
)

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir} 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir} $RPM_BUILD_ROOT%{_datadir}/xclass/icons
make etc_dir=$RPM_BUILD_ROOT%{_sysconfdir} config_dir=$RPM_BUILD_ROOT%{_bindir} \
  doc_dir=$RPM_BUILD_ROOT%{_docdir} header_dir=$RPM_BUILD_ROOT%{_includedir}/xclass lib_dir=$RPM_BUILD_ROOT%{_libdir} \
  icon_dir=$RPM_BUILD_ROOT%{_datadir}/xclass/icons install 

(cd lib/libxclass
make lib_dir=$RPM_BUILD_ROOT%{_libdir} install_shared
)
ln -sf libxclass.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libxclass.so.%{major}.6
ln -sf libxclass.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libxclass.so.%{major}
ln -sf libxclass.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libxclass.so

# fix reference to icons dir
perl -pi -e "s,(^icon dir).+,\1 = %{_datadir}/xclass/icons," \
  $RPM_BUILD_ROOT%{_sysconfdir}/xclassrc

# fix reference to mime.types file
mv $RPM_BUILD_ROOT%{_sysconfdir}/{,xclass-}mime.types
perl -pi -e "s,(^mime type file).+,\1 = xclass-mime.types," \
  $RPM_BUILD_ROOT%{_sysconfdir}/xclassrc

# remove unpackaged files
rm -f  $RPM_BUILD_ROOT%{_datadir}/xclass/icons/Makefile{,.in}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

# multiarch support
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/xc-config

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig


%files icons
%defattr(-,root,root)
%dir %{_datadir}/xclass
%dir %{_datadir}/xclass/icons
%{_datadir}/xclass/icons/*.xpm
%{_datadir}/xclass/icons/*.xbm
%{_datadir}/xclass/icons/*.icon

%files -n %{libname}
%defattr(-,root,root)
%doc doc/Programming.notes doc/INSTALL doc/Layout.notes
%config(noreplace) %{_sysconfdir}/xclassrc
%config(noreplace) %{_sysconfdir}/xclass-mime.types
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%_bindir/xc-config
%multiarch %multiarch_bindir/xc-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%doc doc/Programming.notes doc/INSTALL doc/Layout.notes
