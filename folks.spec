Summary:	GObject contact aggregation library
Name:		folks
Version:	0.9.5
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.9/%{name}-%{version}.tar.xz
# Source0-md5:	6faaf2c4de0e0863a5272f19837c693e
Patch0:		9c61256d5f92950d7c8a96a7c17ef5a8bd911006.patch
Patch1:		f707b604734f787692cf94a7daffb4edf349a476.patch
URL:		http://telepathy.freedesktop.org/wiki/Folks
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.10.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	libgee-devel
BuildRequires:	libsocialweb-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	telepathy-glib-devel
BuildRequires:	tracker-devel >= 0.16.0
BuildRequires:	vala-vapigen
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Requires:	evolution-data-server
Requires:	libsocialweb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Folks is a library that aggregates people from multiple sources
(eg, Telepathy connection managers and eventually evolution data
server, Facebook, etc.) to create metacontacts. It's written in Vala
(in part to evaluate Vala). The initial goal is for GObject/C support,
though the Vala bindings should basically automatic.

%package libs
Summary:	Folks libraries
Group:		Libraries

%description libs
Folks libraries.

%package devel
Summary:	Header files for Folks library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for Folks library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules 		\
	--enable-tracker-backend	\
	--enable-eds-backend		\
	--enable-vala
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/folks/*/backends/*/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_bindir}/folks-inspect

%dir %{_libdir}/folks
%dir %{_libdir}/folks
%dir %{_libdir}/folks/??
%dir %{_libdir}/folks/??/backends
%dir %{_libdir}/folks/??/backends/eds
%dir %{_libdir}/folks/??/backends/key-file
%dir %{_libdir}/folks/??/backends/libsocialweb
%dir %{_libdir}/folks/??/backends/ofono
%dir %{_libdir}/folks/??/backends/telepathy
%dir %{_libdir}/folks/??/backends/tracker

%attr(755,root,root) %{_libdir}/folks/??/backends/eds/eds.so
%attr(755,root,root) %{_libdir}/folks/??/backends/key-file/key-file.so
%attr(755,root,root) %{_libdir}/folks/??/backends/libsocialweb/libsocialweb.so
%attr(755,root,root) %{_libdir}/folks/??/backends/ofono/ofono.so
%attr(755,root,root) %{_libdir}/folks/??/backends/telepathy/telepathy.so
%attr(755,root,root) %{_libdir}/folks/??/backends/tracker/tracker.so

%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.??
%attr(755,root,root) %ghost %{_libdir}/libfolks-libsocialweb.so.??
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.??
%attr(755,root,root) %ghost %{_libdir}/libfolks-tracker.so.??
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.??
%attr(755,root,root) %{_libdir}/libfolks-eds.so.*.*.*
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so.*.*.*
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %{_libdir}/libfolks-tracker.so.*.*.*
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/folks
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.deps
%{_datadir}/vala/vapi/*.vapi
%{_pkgconfigdir}/*.pc

