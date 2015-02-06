%define modname varnish
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B23_%{modname}.ini

Summary:	Varnish Cache bindings for PHP
Name:		php-%{modname}
Version:	0.9.3
Release:	2
Group:		Development/PHP
License:	Apache License
URL:		http://pecl.php.net/package/varnish/
Source0:	http://pecl.php.net/get/varnish-%{version}.tgz
Source1:	B23_varnish.ini
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	varnish-devel

%description
Varnish Cache is an open source, state of the art web application accelerator.
The extension makes it possible to interact with a running varnish instance
through TCP socket or shared memory.

%prep

%setup -q -n %{modname}-%{version}

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build

%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make VARNISH_SHARED_LIBADD="-lvarnishapi"
mv modules/*.so .

%install

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%files
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Mon Jun 04 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-1
+ Revision: 802285
- initial Mandriva package
- Created package structure for php-varnish.

