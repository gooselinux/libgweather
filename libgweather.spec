Name:           libgweather
Version:        2.28.0
Release:        4%{?dist}
Summary:        A library for weather information

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/libgweather/2.28/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  GConf2-devel >= 2.8.0
BuildRequires:  dbus-devel
BuildRequires:  gtk2-devel >= 2.11.0
BuildRequires:  libsoup-devel >= 2.4
BuildRequires:  libxml2-devel >= 2.6
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk-doc
BuildRequires:  autoconf automake libtool

# Patch from Ubuntu...
Patch0: gettext-not-xml.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=591570
Patch1: better-weather-in-montreal.patch

# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589225
Patch2: libgweather-translations.patch
Patch3: libgweather-translations2.patch

%description
libgweather is a library to access weather information from online
services for numerous locations.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
# libgweather used to be part of gnome-applets, and
# gnome-applets-devel only had the libgweather-devel parts in it
Obsoletes:	gnome-applets-devel < 1:2.21.4-1
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gtk-doc

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .gettext
%patch1 -p1 -b .montreal
%patch2 -p1 -b .translations
%patch3 -p2 -b .translations2

gtkdocize
autoreconf -i -f

%build
%configure --disable-static --disable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gweather.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gweather.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gweather.schemas > /dev/null || :
fi

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_sysconfdir}/gconf/schemas/gweather.schemas
%{_libdir}/libgweather.so.*
%dir %{_datadir}/libgweather
%{_datadir}/libgweather/Locations.xml
%{_datadir}/libgweather/locations.dtd

%files devel
%defattr(-,root,root,-)
%{_includedir}/libgweather
%{_libdir}/libgweather.so
%{_libdir}/pkgconfig/gweather.pc
%{_datadir}/gtk-doc/html/libgweather


%changelog
* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> 2.28.0-4
- Some more translation updates (Kannada)
Resolves: #618495

* Wed May 12 2010 Matthias Clasen <mclasen@redhat.com> 2.28.0-3
- Updated translations
Resolves: #589225

* Thu Oct 15 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-2
- Pick a better weather station for Montreal

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Wed Sep  9 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-5
- Keep locations in gettext catalogs

* Wed Jun 10 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-3
- Fix multilib parallel-installability (#477672)
- Remove some old optimizations that are now no-ops

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-2
- Don't drop schemas translations from po files

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/libgweather/2.26/libgweather-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> 2.25.5-1
- Upate to 2.25.5

* Mon Jan 05 2009 Matthew Barnes <mbarnes@redhat.com> 2.25.4-1
- Update to 2.25.4

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> 2.25.3-2
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> 2.25.2-2
- Update to 2.25.2

* Wed Oct 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.0-2
- Apply %%lang tags to localized xml files

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> 2.23.91-1
- Update to 2.23.91

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> 2.23.6-1
- Update to 2.23.6

* Fri Jul 25 2008 Matthias Clasen <mclasen@redhat.com> 2.23.5-2
- Fix pending request accounting

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> 2.23.5-1
- Update to 2.23.5

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> 2.23.4-1
- Update to 2.23.4

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> 2.23.2-1
- Update to 2.23.2

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> 2.22.1.1-2
- Leave Cairo in Africa (#442793)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> 2.22.1.1-1
- Update to 2.22.1.1

* Tue Mar 11 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> 2.21.92-1
- Update to 2.21.92

* Mon Feb 11 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-6
- Remove obsolete translations

* Sat Feb  9 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-5
- Rebuild for gcc 4.3

* Wed Jan 16 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-4
- Add Obsoletes for gnome-applets-devel

* Wed Jan 16 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-3
- Carry over space-saving hack from gnome-applets

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-2
- Incorporate review feedback (#428739)

* Mon Jan 14 2008  Matthias Clasen <mclasen@redhat.com> 2.21.2-1
- Update to 2.21.2

* Thu Jan 10 2008  Matthias Clasen <mclasen@redhat.com> 2.21.1-1
- Initial packaging

