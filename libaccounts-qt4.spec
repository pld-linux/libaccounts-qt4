Summary:	Accounts management library for Qt 4 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 4
Name:		libaccounts-qt4
Version:	1.14
Release:	3
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libaccounts-qt/tags?sort=updated_desc
Source0:	https://gitlab.com/accounts-sso/libaccounts-qt/repository/archive.tar.bz2?ref=VERSION_%{version}&fake_out=/libaccounts-qt-%{version}.tar.bz2
# Source0-md5:	c6c16ea482613c11ab076b84ebae5633
Patch0:		x32.patch
Patch1:		libaccounts-qt-qt4.patch
URL:		https://gitlab.com/accounts-sso/libaccounts-qt
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtTest-devel >= 4
BuildRequires:	QtXml-devel >= 4
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaccounts-glib-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
Obsoletes:	libaccounts-qt < 1.14-2
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
Obsoletes:	libaccounts-qt-devel < 1.14-2

%description devel
Development files for libaccounts-qt library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-qt.

%prep
%setup -q -n libaccounts-qt-VERSION_%{version}-a34ca4b6d250529c900b0382559553b6e5885918

%build
%patch0 -p1
%patch1 -p1

install -d build-qt4
cd build-qt4
qmake-qt4 ../accounts-qt.pro \
	BUILD_DIR=build-qt4 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-qt4 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt.so.1.?

# test suite
%{__rm} $RPM_BUILD_ROOT%{_bindir}/accountstest
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libaccounts-qt-tests
# packaged as %doc in libaccounts-qt.spec
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
