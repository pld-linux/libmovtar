#
# Conditional build:
%bcond_without	mmx	# don't use MMX on ix86 (no runtime detection!)

%ifnarch athlon pentium2 pentium3 pentium4
%undefine	with_mmx
%endif

Summary:	Support library for the movtar video format
Summary(pl.UTF-8):	Biblioteka obsługująca format obrazu movtar
Name:		libmovtar
Version:	0.1.3
Release:	8
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mjpeg/%{name}-%{version}.tar.gz
# Source0-md5:	3810ba83a90c52676014ab1ea6d8cd9f
Patch0:		%{name}-shared.patch
Patch1:		%{name}-mmx.patch
Patch2:		%{name}-glib.patch
Patch3:		%{name}-am18.patch
Patch4:		%{name}-gcc4.patch
URL:		http://mjpeg.sourceforge.net/
BuildRequires:	SDL-devel >= 1.1.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes libmovtar, the support library which implements
the movtar MJPEG video format.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę libmovtar, będącą implementacją obsługi
formatu obrazu MJPEG movtar.

%package devel
Summary:	libmovtar header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmovtar
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libmovtar header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmovtar.

%package static
Summary:	libmovtar static library
Summary(pl.UTF-8):	Biblioteka statyczna libmovtar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libmovtar static library.

%description static -l pl.UTF-8
Biblioteka statyczna libmovtar.

%package progs
Summary:	Various tools for movtar video format
Summary(pl.UTF-8):	Różne narzędzia do formatu obrazu movtar
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description progs
This package contains various tools to help you understand the
principles behind the movtar format, and do special tasks which aren't
possible with the library (like movtar_index, which removes a video
index, for experimental and debugging purposes).

%description progs -l pl.UTF-8
Ten pakiet zawiera różne narzędzia pomagające zrozumieć zasady
dotyczące formatu movtar i wykonywać specjalne zadania niemożliwe do
wykonania z poziomu biblioteki (jak movtar_index, który usuwa indeks
filmu - dla eksperymentów i odpluskwiania).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

# for movtar_play and rtjpeg.
%{?with_mmx:CPPFLAGS="-DMMX -DHAVE_MMX_ATT_MNEMONICS"}
%configure
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
