#
# Conditional build:
%bcond_with	mmx	# use MMX on i[56]86 (no runtime detection!)
#
%ifarch athlon
%define		with_mmx 1
%endif
Summary:	Support library for the movtar video format
Summary(pl):	Biblioteka obs³uguj±ca format obrazu movtar
Name:		libmovtar
Version:	0.1.3
Release:	4
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mjpeg/%{name}-%{version}.tar.gz
# Source0-md5:	3810ba83a90c52676014ab1ea6d8cd9f
Patch0:		%{name}-shared.patch
Patch1:		%{name}-nommx.patch
Patch2:		%{name}-glib.patch
Patch3:		%{name}-am18.patch
URL:		http://mjpeg.sourceforge.net/
BuildRequires:	SDL-devel >= 1.1.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes libmovtar, the support library which implements
the movtar MJPEG video format.

%description -l pl
Ten pakiet zawiera bibliotekê libmovtar, bêd±c± implementacj± obs³ugi
formatu obrazu MJPEG movtar.

%package devel
Summary:	libmovtar header files
Summary(pl):	Pliki nag³ówkowe biblioteki libmovtar
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
libmovtar header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki libmovtar.

%package static
Summary:	libmovtar static library
Summary(pl):	Biblioteka statyczna libmovtar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
libmovtar static library.

%description static -l pl
Biblioteka statyczna libmovtar.

%package progs
Summary:	Various tools for movtar video format
Summary(pl):	Ró¿ne narzêdzia do formatu obrazu movtar
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description progs
This package contains various tools to help you understand the
principles behind the movtar format, and do special tasks which aren't
possible with the library (like movtar_index, which removes a video
index, for experimental and debugging purposes).

%description progs -l pl
Ten pakiet zawiera ró¿ne narzêdzia pomagaj±ce zrozumieæ zasady
dotycz±ce formatu movtar i wykonywaæ specjalne zadania niemo¿liwe
do wykonania z poziomu biblioteki (jak movtar_index, który usuwa
indeks filmu - dla eksperymentów i odpluskwiania).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CPPFLAGS="-I/usr/X11R6/include"
%configure \
%ifarch i586 i686 athlon
	%{?with_mmx:--with-mmx}
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f rtjpeg/README README.rtjpeg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/movtar-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/movtar_*
%attr(755,root,root) %{_bindir}/[^m]*
