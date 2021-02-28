#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	SMACK userspace package
Summary(pl.UTF-8):	Pakiet SMACK dla przestrzeni użytkownika
Name:		smack
Version:	1.3.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/smack-team/smack/releases
Source0:	https://github.com/smack-team/smack/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f80d163127c0db8441faf3bbb7d887da
URL:		https://github.com/smack-team/smack
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	doxygen
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel >= 1:198
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Simplified Mandatory Access Control Kernel (SMACK) provides a
complete Linux kernel based mechanism for protecting processes and
data from inappropriate manipulation. Smack uses process, file, and
network labels combined with an easy to understand and manipulate way
to identify the kind of accesses that should be allowed.

%description -l pl.UTF-8
SMACK (Simplified Mandatory Access Control Kernel - uproszczone jądro
obowiązkowej kontroli dostępu) to oparty na jądrze Linuksa kompletny
mechanizm ochrony procesów i danych od niewłaściwych operacji. Smack
wykorzystuje etykiety procesów, plików oraz sieci w połączeniu z
łatwymi do zrozumienia i operowania rodzajami dostępu, który powinien
być dozwolony.

%package libs
Summary:	Shared library for interaction with SMACK
Summary(pl.UTF-8):	Biblioteka współdzielona do współpracy z systemem SMACK
Group:		Libraries

%description libs
Shared library for interaction with SMACK.

%description libs -l pl.UTF-8
Biblioteka współdzielona do współpracy z systemem SMACK.

%package devel
Summary:	Header file for SMACK library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki SMACK
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for SMACK library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki SMACK.

%package static
Summary:	Static SMACK library
Summary(pl.UTF-8):	Statyczna biblioteka SMACK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SMACK library.

%description static -l pl.UTF-8
Statyczna biblioteka SMACK.

%package apidocs
Summary:	SMACK API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SMACK
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SMACK library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SMACK.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsmack.la
# packaged unarchived in -apidocs
%{__rm} $RPM_BUILD_ROOT%{_docdir}/libsmack/libsmack-%{version}-doc.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chsmack
%attr(755,root,root) %{_bindir}/smackaccess
%attr(755,root,root) %{_bindir}/smackcipso
%attr(755,root,root) %{_bindir}/smackctl
%attr(755,root,root) %{_bindir}/smackload
%{_mandir}/man1/smackaccess.1*
%{_mandir}/man8/chsmack.8*
%{_mandir}/man8/smackcipso.8*
%{_mandir}/man8/smackctl.8*
%{_mandir}/man8/smackload.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmack.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmack.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmack.so
%{_includedir}/sys/smack.h
%{_pkgconfigdir}/libsmack.pc
%{_mandir}/man3/SMACK_LABEL_LEN.3*
%{_mandir}/man3/smack.h.3*
%{_mandir}/man3/smack_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsmack.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
