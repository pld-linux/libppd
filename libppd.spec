#
# Conditional build:
%bcond_with	static_libs	# static libraries
#
Summary:	Library for retro-fitting legacy printer drivers
Summary(pl.UTF-8):	Biblioteka do modernizacji starszych sterowników
Name:		libppd
Version:	2.1.1
Release:	1
License:	Apache v2.0 with GPL v2 LGPL v2 Exception
Group:		Libraries
Source0:	https://github.com/OpenPrinting/libppd/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	65accc86f9956a1160937b14e0f516a6
URL:		https://github.com/OpenPrinting/libppd
BuildRequires:	cups-devel >= 1:2
BuildRequires:	gettext-tools >= 0.18.3
BuildRequires:	libcupsfilters-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Suggests:	ghostscript
Suggests:	mupdf
Suggests:	poppler-progs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libppd provides all PPD related function/API which is going to be
removed from CUPS 3.X, but are still required for retro-fitting
support of legacy printers. The library is meant only for
retro-fitting printer applications, any new printer drivers have to be
written as native printer application without libppd.

%description -l pl.UTF-8
Libppd dostarcza wszystkie funkcje/API związane z PPD, które zostaną
usunięte z CUPS-a 3.x, ale są nadal wymagane do modernizacji obsługi
starszych drukarek. Biblioteka jest przeznaczona tylko dla starszych
aplikacji drukarek, każdy nowy sterownik drukarki powinien być pisany
jako natywna aplikacja drukarki bez libppd.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cups-devel >= 1:2

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package tools
Summary:	PPD compiler tools and definition files
Summary(pl.UTF-8):	Narzędzia do kompilacji PPD i pliki definicji
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}

%description tools
The package contains PPD compiler and definition files needed for
generating PPD files from *.drv files.

%description tools -l pl.UTF-8
Ten pakiet zawiera kompilator PPD oraz pliki definicji, wymagane do
generowania plików PPD z plików *.drv.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-ppdc-utils \
	--enable-testppdfile \
	--with-gs-path=/usr/bin/gs \
	--with-mutool-path=/usr/bin/mutool \
	--with-pdftocairo-path=/usr/bin/pdftocairo \
	--with-pdftops=hybrid \
	--with-pdftops-path=/usr/bin/pdftops

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove .la pollution
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libppd

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.md COPYING README.md
%attr(755,root,root) %{_libdir}/libppd.so.*.*.*
%ghost %{_libdir}/libppd.so.2
%{_datadir}/ppdc

%files devel
%defattr(644,root,root,755)
%{_libdir}/libppd.so
%{_includedir}/ppd
%{_pkgconfigdir}/libppd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libppd.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ppdhtml
%attr(755,root,root) %{_bindir}/ppdc
%attr(755,root,root) %{_bindir}/ppdi
%attr(755,root,root) %{_bindir}/ppdmerge
%attr(755,root,root) %{_bindir}/ppdpo
%attr(755,root,root) %{_bindir}/testppdfile
