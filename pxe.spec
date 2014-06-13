%define tftpbase /var/lib/tftpboot

Summary:	A Linux PXE (Preboot eXecution Environment) package
Name:		pxe
Group:		System/Servers
Version:	1.4.2
Release:	27
License:	GPLv2
Url:		http://www.kano.org.uk/projects/pxe
Source0:	http://www.kano.org.uk/projects/pxe/%{name}-%{version}.tar.gz
Source1:	pxe
Source2:	pxe.conf
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
Requires:	chkconfig
Requires:	coreutils
Requires:	dhcp-server
Requires:	grep
Requires:	tftp-server
Requires:	pxelinux
Requires(post,preun):	rpm-helper
Provides:	pxeserver

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
Patch2:		pxe-linux-config.patch

%description bootstraps
This package contains a compiltation of PXE bootstraps.

%description 
The pxe package contains the PXE (Preboot eXecution Environment)
server and code needed for Linux to boot from a boot disk image on a
Linux PXE server.

%prep 
%setup -q
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
%configure2_5x
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

%post 
%_post_service pxe
mkdir -p %{tftpbase}/X86PC/linux

%preun
%_preun_service pxe

%files bootstraps
%doc grubNBI/*

%files
%doc README LICENCE INSTALL Changes pxedoc/*
%attr(755,root,root) %{_sbindir}/pxe
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/pxe.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.pxe
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux//pxelinux.cfg/default
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux//messages
#%attr(644,root,root) %config(noreplace) %{tftpbase}/X86PC/linux/help.txt
%attr(755,root,root) %{_initrddir}/pxe
%{tftpbase}/IA64PC/linux

