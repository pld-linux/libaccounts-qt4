#
# Conditional build:
%bcond_without	qt4	# Qt 4 version
%bcond_without	qt5	# Qt 5 version
#
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
%{?with_qt4:BuildRequires:	QtCore-devel >= 4}
%{?with_qt4:BuildRequires:	QtTest-devel >= 4}
%{?with_qt4:BuildRequires:	QtXml-devel >= 4}
%{?with_qt5:BuildRequires:	Qt5Core-devel >= 5}
%{?with_qt5:BuildRequires:	Qt5Test-devel >= 5}
%{?with_qt5:BuildRequires:	Qt5Xml-devel >= 5}
BuildRequires:	doxygen
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaccounts-glib-devel
BuildRequires:	pkgconfig
%{?with_qt4:BuildRequires:	qt4-build >= 4}
%{?with_qt4:BuildRequires:	qt4-qmake >= 4}
%{?with_qt5:BuildRequires:	qt5-build >= 5}
%{?with_qt5:BuildRequires:	qt5-qmake >= 5}
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

%package -n libaccounts-qt5
Summary:	Accounts management library for Qt 5 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 5
Group:		Libraries

%description -n libaccounts-qt5
This project is a library for managing accounts which can be used from
Qt 5 applications. It is part of the accounts-sso project.

%description -n libaccounts-qt5 -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece Qt 5. Jest to część
projektu accounts-sso.

%package -n libaccounts-qt5-devel
Summary:	Development files for libaccounts-qt5 library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libaccounts-qt5
Group:		Development/Libraries
Requires:	libaccounts-qt5 = %{version}-%{release}
Requires:	Qt5Core-devel >= 5

%description -n libaccounts-qt5-devel
Development files for libaccounts-qt5 library.

%description -n libaccounts-qt5-devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-qt5.

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
%{__rm} Accounts/{libaccounts-qt5.so*,*.cmake}

%build

%if %{with qt4}
install -d build-qt4
cd build-qt4
qmake-qt4 ../accounts-qt.pro \
	BUILD_DIR=build-qt4 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
qmake-qt5 ../accounts-qt.pro \
	BUILD_DIR=build-qt5 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%{__make} -C build-qt5 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt5.so.1.?

# separate from qt4 version
%{__mv} $RPM_BUILD_ROOT%{_libdir}/cmake/{AccountsQt,AccountsQt5}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/cmake/AccountsQt5/{AccountsQt,AccountsQt5}Config.cmake
%{__mv} $RPM_BUILD_ROOT%{_libdir}/cmake/AccountsQt5/{AccountsQt,AccountsQt5}ConfigVersion.cmake
%endif

%if %{with qt4}
%{__make} -C build-qt4 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt.so.1.?
%endif

# test suite
%{__rm} $RPM_BUILD_ROOT%{_bindir}/accountstest
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libaccounts-qt-tests
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/accounts-qt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libaccounts-qt5 -p /sbin/ldconfig
%postun	-n libaccounts-qt5 -p /sbin/ldconfig

%if %{with qt4}
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
%endif

%if %{with qt5}
%files -n libaccounts-qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccounts-qt5.so.1

%files -n libaccounts-qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt5.so
%{_includedir}/accounts-qt5
%{_pkgconfigdir}/accounts-qt5.pc
%{_libdir}/cmake/AccountsQt5
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
