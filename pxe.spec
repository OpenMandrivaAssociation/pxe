%define name    pxe 
%define version 1.4.2

%define tftpbase /var/lib/tftpboot

Name:           %{name}
Summary:        A Linux PXE (Preboot eXecution Environment) package
Group:          System/Servers
Version:        %{version}
Release:        23
License:        GPL
URL: 		http://www.kano.org.uk/projects/pxe
Requires:       chkconfig, dhcp-server, coreutils, grep, tftp-server, pxelinux
Provides:	pxeserver
BuildRoot:      %{_tmppath}/%{name}-%{version}
Requires(post): rpm-helper
Requires(preun): rpm-helper

Source:		http://www.kano.org.uk/projects/pxe/%{name}-%{version}.tar.gz
Source1: 	pxe
Source2: 	pxe.conf
Source3:	dhcpd.conf.pxe
#Source8:	default
#Source9:	messages
Source10:	elilo.efi
Source11:	elilo.txt
Source12:	elilovars.txt
Source13:	elilo.conf
#Source14:	help.txt
Patch0:		pxe-1.4.patch
Patch3:		pxe-autoconf.patch
Patch4:		pxe-mtftp.patch
Patch5:		pxe-1.4.2-arch_id.patch
Patch7:		pxe-segfault_on_exit.patch

%package	bootstraps
Summary:	A compilation of Linux PXE (Preboot eXecution Environment) Bootstraps
Group:		System/Servers
%ifarch %{ix86}
BuildRequires:	dev86-devel
%endif
Requires:	syslinux >= 1.67
Source5:	pxe-linux.tar.bz2
Source6:	grubNBI.tar.bz2
Source7:	pxedoc.tar.bz2
Patch1:		pxe-1.0-cmdlinearg.patch
Patch2:	 	pxe-linux-config.patch


%description bootstraps
This package contains a compiltation of PXE bootstraps.

%description 
The pxe package contains the PXE (Preboot eXecution Environment)
server and code needed for Linux to boot from a boot disk image on a
Linux PXE server.


%prep 
rm -rf ${RPM_BUILD_ROOT}
%setup -q -n %{name}-%{version}
%setup -q -T -D -a 5
%setup -q -T -D -a 6
%setup -q -T -D -a 7
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1 -b .arch_id
%patch7 -p0

%build
%configure
%make

%install
myname=`id -un`
mygroup=`id -gn`
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sbindir}
#mkdir -p %{buildroot}%{tftpbase}/X86PC/linux/pxelinux.cfg
mkdir -p %{buildroot}%{tftpbase}/IA64PC/linux/

install -m755 %{_builddir}/%{name}-%{version}/pxe %{buildroot}%{_sbindir}
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/pxe
install -m755 %{SOURCE2} %{buildroot}%{_sysconfdir}/pxe.conf
install -m755 %{SOURCE3} %{buildroot}%{_sysconfdir}/dhcpd.conf.pxe
#install -m644 %{SOURCE8} %{buildroot}%{tftpbase}/X86PC/linux/pxelinux.cfg/default
#install -m644 %{SOURCE9} %{buildroot}%{tftpbase}/X86PC/linux/messages
install -m644 %{SOURCE10} %{buildroot}%{tftpbase}/IA64PC/linux/linux.0
install -m644 %{SOURCE11} %{buildroot}%{tftpbase}/IA64PC/linux/
install -m644 %{SOURCE12} %{buildroot}%{tftpbase}/IA64PC/linux/
install -m644 %{SOURCE13} %{buildroot}%{tftpbase}/IA64PC/linux/linux.1
#install -m644 %{SOURCE14} %{buildroot}%{tftpbase}/X86PC/linux/help.txt

%clean
rm -rf ${RPM_BUILD_ROOT}

%post 
%_post_service pxe
mkdir -p %{tftpbase}/X86PC/linux

%preun
%_preun_service pxe

%files bootstraps
%defattr(-,root,root)
%doc grubNBI/*

%files
%defattr(-,root,root)
%doc README LICENCE INSTALL Changes pxedoc/*
%attr(755,root,root) %{_sbindir}/pxe
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/pxe.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.pxe
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux//pxelinux.cfg/default
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux//messages
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux/help.txt
%attr(755,root,root) %{_initrddir}/pxe
%{tftpbase}/IA64PC/linux




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-21mdv2011.0
+ Revision: 667901
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-20mdv2011.0
+ Revision: 607254
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-19mdv2010.1
+ Revision: 523747
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.4.2-18mdv2010.0
+ Revision: 426790
- rebuild

  + Erwan Velu <erwan@mandriva.org>
    - Mandrake is dead :p

* Wed Aug 13 2008 Erwan Velu <erwan@mandriva.org> 1.4.2-17mdv2009.0
+ Revision: 271588
- Adding more sample configuration for pxelinux
- Adding more config sample

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.4.2-16mdv2009.0
+ Revision: 225121
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-15mdv2008.1
+ Revision: 179372
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot
    - really use architecture-specific file (do not always use X86PC, fix IA64PC)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.4.2-13mdv2008.0
+ Revision: 69956
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago


* Fri Feb 09 2007 Erwan Velu <erwan@mandriva.org> 1.4.2-12mdv2007.0
+ Revision: 118455
- Rebuild
- Import pxe

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.4.2-11mdk
- drop some useless rpm tags
- fix typo in initscript

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.4.2-10mdk
- convert parallel init to LSB
- mkrel
- fix incorrect Requires(X)
- remove useless ldconfig postun

* Mon Jan 02 2006 Olivier Blin <oblin@mandriva.com> 1.4.2-9mdk
- parallel init support

* Sat Jul 23 2005 Erwan Velu <velu@seanodes.com>  1.4.2-8mdk
- Removing pxelinux stuff

* Tue Jun 14 2005 Erwan Velu <erwan@seanodes.com> 1.4.2-7mdk
- Fixing x86_64 build

* Tue Jun 14 2005 Erwan Velu <erwan@seanodes.com> 1.4.2-6mdk
- Fixing rights & stupid things

* Tue Feb 08 2005 Erwan Velu <erwan@seanodes.com> 1.4.2-5mdk
- Fixing requires

* Mon Jan 31 2005 Pascal Terjan <pterjan@mandrake.org> 1.4.2-4mdk
- Drop nbp

* Wed Sep 15 2004 Pascal Terjan <pterjan@mandrake.org> 1.4.2-3mdk
- Fix a segfault when run without -d

* Wed Aug 04 2004 Erwan Velu <erwan@mandrakesoft.com> 1.4.2-2mdk
- Fixing pxelinux sample configuration (thx aginies)

* Thu Jul 22 2004 Erwan Velu <erwan@mandrakesoft.com> 1.4.2-1mdk
- 1.4.2
- Adding prereq
- Rpmbuildupdate aware

* Sat Jun 05 2004 <lmontel@n2.mandrakesoft.com> 1.4.1-2mdk
- Rebuild

* Tue Apr 06 2004 Erwan Velu <erwan@mandrakesoft.com> 1.4.1-1mdk
- New release
- Remove patch6 (merged upstream)

