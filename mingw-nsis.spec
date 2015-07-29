%global sconsopts VERSION=%{version} PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} SKIPUTILS='NSIS Menu' STRIP_CP=false NSIS_MAX_STRLEN=8192
%global _default_patch_fuzz 2

Name:           mingw-nsis
Version:        2.46
Release:        15%{?dist}
Summary:        Nullsoft Scriptable Install System

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://downloads.sourceforge.net/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This patch fixes NSIS to actually build 64-bit versions.
# Originally from Debian, updated by Kevin Kofler.
Patch0:         nsis-2.43-64bit-fixes.patch
# Use RPM_OPT_FLAGS for the natively-built parts
Patch1:         nsis-2.43-rpm-opt.patch
# Make plugins not depend on libgcc_s_sjlj-1.dll (#553971)
Patch2:         nsis-2.45-static-libgcc.patch
# Make plugins not depend on libstdc++-6.dll (#734905)
Patch3:         nsis-2.46-static-libstdc++.patch
# Missing #include <unistd.h> to get close(2) function.
Patch4:         nsis-2.46-missing-unistd-include.patch
# Add support to build against the mingw-w64 toolchain
Patch5:         nsis-add-mingw-w64-support.patch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  python
BuildRequires:  scons

# Don't build NSIS Menu as it doesn't actually work on POSIX systems: 1. it
# doesn't find its index.html file without patching, 2. it has various links to
# .exe files such as the makensisw.exe W32 GUI which are not available in the
# POSIX version at all and 3. the documentation links have backslashes in the
# URLs and the relative paths are wrong. Almost none of the links worked when I
# tested it (after patching problem 1.).
# Also removes unnecessary wxGTK dependency for this otherwise GUI-less package.
# (Does it really make sense to drag in wxGTK just to display a HTML file?)
# If you really want to reenable this, it needs a lot of fixing. Oh, and it'd
# need a .desktop file too.
# -- Kevin Kofler
# BuildRequires:  wxGTK-devel


%description
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.) and
all plugins.


%package -n mingw32-nsis
Summary:        Nullsoft Scriptable Install System
# upgrade path for CalcForge users
Obsoletes:      nsis < %{version}-%{release}
Provides:       nsis = %{version}-%{release}
Obsoletes:      nsis-data < %{version}-%{release}
Provides:       nsis-data = %{version}-%{release}

%description -n mingw32-nsis
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.) and
all plugins.


%prep
%setup -q -n nsis-%{version}-src

%patch0 -p1 -b .64bit
%patch1 -p1 -b .rpmopt
%patch2 -p1 -b .static-libgcc
%patch3 -p1 -b .static-libstdc++
%patch4 -p1 -b .missing-unistd-include
%patch5 -p0 -b .mingw-w64


%build
scons %{sconsopts}


%install
rm -rf $RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT
scons %{sconsopts} PREFIX_DEST=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT%{_docdir}/nsis $RPM_BUILD_ROOT%{_docdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -n mingw32-nsis
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%{_bindir}/*
#{_includedir}/nsis
%{_datadir}/nsis


%changelog
* Fri May 29 2015 Richard W.M. Jones <rjones@redhat.com> - 2.46-15
- Add NSIS_MAX_STRLEN=8192 to sconsopts (RHBZ#1090075).

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.46-14
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug  6 2013 Richard W.M. Jones <rjones@redhat.com> - 2.46-11
- Unversioned docdir on Fedora 20 (RHBZ#993867).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.46-7
- Renamed the source package to mingw-nsis (#800987)

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.46-6
- Rebuild against the mingw-w64 toolchain
- Added a patch to fix compatibility with mingw-w64

* Mon Jan 16 2012 Richard W.M. Jones <rjones@redhat.com> - 2.46-5
- Missing #include <unistd.h> to get close(2) function.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.46-3
- Make plugins not depend on libstdc++-6.dll (#734905)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.46-1
- Update to 2.46 (#544675)

* Mon Jan 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.45-3
- Make plugins not depend on libgcc_s_sjlj-1.dll (#553971)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.45-1
- Update to 2.45 (#512429)

* Tue Jun 30 2009 Stu Tomlinson <stu@nosnilmot.com> - 2.44-2
- Re-enable System.dll plugin, inline Microsoft assembler code was
  replaced in 2.42 (#509234)

* Sat Mar 14 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.44-1
- Update to 2.44 (#488522)

* Tue Mar  3 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.43-6
- Don't build the MinGW parts with debugging information, NSIS corrupts the
  debugging information in the stubs when building installers from them
- Drop debian-debug-opt patch, all its changes are either taken care of by our
  rpm-opt patch, unwanted (see above) or unneeded

* Wed Feb 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.43-5
- Use RPM_OPT_FLAGS for the natively-built parts

* Wed Feb 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.43-4
- Updated 64bit-fixes patch (remove some more -m32 use)
- Drop ExclusiveArch, not needed with the above
- Obsoletes/Provides nsis and nsis-data for migration path from CalcForge
- Disable NSIS Menu (does not work on *nix, see specfile comment for details)
- Drop BR wxGTK-devel

* Sat Feb 21 2009 Richard W.M. Jones <rjones@redhat.com> - 2.43-3
- Restore ExclusiveArch line (Levente Farkas).

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.43-2
- Rebuild for mingw32-gcc 4.4

* Fri Feb 13 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.43-1
- update to the latest upstream

* Wed Jan 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.42-1
- update to the latest upstream
- a few small changes

* Fri Oct 17 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-5
- Fix the Summary line.

* Wed Oct  8 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-4
- Initial RPM release.
