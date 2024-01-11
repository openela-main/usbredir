Name:           usbredir
Version:        0.13.0
Release:        2%{?dist}
Summary:        USB network redirection protocol libraries
License:        LGPLv2+
URL:            https://spice-space.org/usbredir.html
Source0:        http://spice-space.org/download/%{name}/%{name}-%{version}.tar.xz
Patch0001:      0001-Revert-remove-usbredirserver.patch
Patch0002:      0002-Use-typedef-on-redirect-structure-to-simplify-some-s.patch
Patch0003:      0003-Factor-out-a-function-to-create-watches.patch
Patch0004:      0004-Recreate-watch-if-needed.patch
Patch0005:      0005-Add-documentation-examples-for-using-bus-device-iden.patch
Patch0006:      0006-usbredirect-allow-multiple-devices-by-vendor-product.patch
Patch0007:      0007-usbredirect-use-the-correct-bus-device.patch
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  libusb1-devel >= 1.0.9
BuildRequires:  git-core
BuildRequires:  meson

%description
The usbredir libraries allow USB devices to be used on remote and/or virtual
hosts over TCP.  The following libraries are provided:

usbredirparser:
A library containing the parser for the usbredir protocol

usbredirhost:
A library implementing the USB host side of a usbredir connection.
All that an application wishing to implement a USB host needs to do is:
* Provide a libusb device handle for the device
* Provide write and read callbacks for the actual transport of usbredir data
* Monitor for usbredir and libusb read/write events and call their handlers


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        server
Summary:        Simple USB host TCP server
License:        GPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
A simple USB host TCP server, using libusbredirhost.


%prep
%autosetup -S git_am


%build
%meson \
    -Dgit_werror=disabled \
    -Dtools=enabled \
    -Dfuzzing=disabled

%meson_build

%install
%meson_install


%ldconfig_scriptlets


%files
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%{_libdir}/libusbredir*.so.*

%files devel
%doc docs/usb-redirection-protocol.md docs/multi-thread.md ChangeLog.md TODO
%{_includedir}/usbredir*.h
%{_libdir}/libusbredir*.so
%{_libdir}/pkgconfig/libusbredir*.pc

%files server
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/usbredirect
%{_sbindir}/usbredirserver
%{_mandir}/man1/usbredirect.1*
%{_mandir}/man1/usbredirserver.1*


%changelog
* Thu Jan 05 2023 Victor Toso <victortoso@redhat.com> - 0.13.0-2
- Fixes 100% CPU usage when usbredirect used as TCP server
  Related: rhbz#2157520
- Fixes USB redirection of identical devices
  Resolves: rhbz#2157520

* Wed Nov 30 2022 Victor Toso <victortoso@redhat.com> - 0.13.0-1
- Rebase to latest upstream: 0.13.0
- Keeps usbredirserver binary (removed upstream)
  Related: rhbz#2135760

* Thu Jul 28 2022 Victor Toso <victortoso@redhat.com> - 0.12.0-3
- Fix unserialization (migration regression)
  Related: rhbz#2111368

* Wed Jan 19 2022 Victor Toso <victortoso@redhat.com> - 0.12.0-2
- Fix gating process
  Related: rhbz#2020215

* Mon Nov 15 2021 Victor Toso <victortoso@redhat.com> - 0.12.0-1
- Rebase to latest upstream: 0.12.0
  Related: rhbz#2020215

* Wed Sep 15 2021 Victor Toso <victortoso@redhat.com> - 0.8.0-9
- Avoid use-after-free in serialization
  Related: rhbz#1992873

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.8.0-8
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.8.0-7
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Victor Toso <victortoso@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-6
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Fabiano Fidêncio <fidencio@redhat.com> 0.7.1-1
- Update to upstream 0.7.1 release

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-4
- Use %%license

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Hans de Goede <hdegoede@redhat.com> - 0.7-1
- Update to upstream 0.7 release

* Tue Sep 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.6-5
- Use the new libusb autodetach kernel driver functionality
- Fix a usbredirparser bug which causes tcp/ip redir to not work (rhbz#1005015)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Hans de Goede <hdegoede@redhat.com> - 0.6-3
- Fix usbredirserver not listening for ipv6 connections (rhbz#957470)
- Fix a few (harmless) coverity warnings

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Hans de Goede <hdegoede@redhat.com> - 0.6-1
- Update to upstream 0.6 release

* Tue Sep 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.2-1
- Update to upstream 0.5.2 release

* Wed Sep 19 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.1-1
- Update to upstream 0.5.1 release

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.5-1
- Update to upstream 0.5 release

* Mon Jul 30 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.3-3
- Add 2 fixes from upstream fixing issues with some bulk devices (rhbz#842358)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.3-1
- Update to upstream 0.4.3 release

* Tue Mar  6 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.2-1
- Update to upstream 0.4.2 release

* Sat Feb 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to upstream 0.4.1 release

* Thu Feb 23 2012 Hans de Goede <hdegoede@redhat.com> - 0.4-1
- Update to upstream 0.4 release

* Thu Jan 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.3.3-1
- Update to upstream 0.3.3 release

* Tue Jan  3 2012 Hans de Goede <hdegoede@redhat.com> 0.3.2-1
- Update to upstream 0.3.2 release

* Wed Aug 24 2011 Hans de Goede <hdegoede@redhat.com> 0.3.1-1
- Update to upstream 0.3.1 release

* Thu Jul 14 2011 Hans de Goede <hdegoede@redhat.com> 0.3-1
- Initial Fedora package
