# TODO: qt5 version as libaccounts-qt5-*?
Summary:	Accounts management library for Qt 4 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 4
Name:		libaccounts-qt
Version:	1.11
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: http://code.google.com/p/accounts-sso/downloads/list
Source0:	http://accounts-sso.googlecode.com/files/accounts-qt-%{version}.tar.bz2
# Source0-md5:	a76f26849603f229399dc46eb83ed5a8
URL:		http://code.google.com/p/accounts-sso/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtTest-devel >= 4
BuildRequires:	QtXml-devel >= 4
BuildRequires:	doxygen
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaccounts-glib-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is a library for managing accounts which can be used from
Qt 4 applications. It is part of the accounts-sso project.

%description -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece Qt 4. Jest to część
projektu accounts-sso.

%package devel
Summary:	Development files for libaccounts-qt library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libaccounts-qt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4

%description devel
Development files for libaccounts-qt library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-qt.

%package static
Summary:	Static libaccounts-qt library
Summary(pl.UTF-8):	Statyczna biblioteka libaccounts-qt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libaccounts-qt library.

%description static -l pl.UTF-8
Statyczna biblioteka libaccounts-qt.

%package apidocs
Summary:	API documentation for libaccounts-qt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libaccounts-qt
Group:		Documentation

%description apidocs
API documentation for libaccounts-qt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libaccounts-qt.

%prep
%setup -q -n accounts-qt-%{version}

# clean
%{__rm} Accounts/libaccounts-qt5.so*

%build
qmake-qt4 accounts-qt.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt.so.1.?
# test suite
%{__rm} $RPM_BUILD_ROOT%{_bindir}/accountstest
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libaccounts-qt-tests
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/accounts-qt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccounts-qt.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt.so
%{_includedir}/accounts-qt
%{_pkgconfigdir}/accounts-qt.pc
%{_libdir}/cmake/AccountsQt

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
