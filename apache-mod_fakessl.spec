#Module-Specific definitions
%define mod_name mod_fakessl
%define mod_conf A90_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A apache 2.x module for setting an https flag when you are using reverse proxy
Name:		apache-%{mod_name}
Version:	0.4
Release:	8
Group:		System/Servers
License:	Apache License
URL:		http://websupport.sk/~stanojr/projects/mod_fakessl/
Source0:	http://websupport.sk/~stanojr/projects/mod_fakessl/mod_fakessl-%{version}.tar.gz
Source1:	README.%{mod_name}
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_proxy >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file

%description
A apache 2.x module for setting an https flag when you are using reverse proxy

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} .
cp %{SOURCE2} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc README.%{mod_name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.4-7mdv2012.0
+ Revision: 772653
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4-6
+ Revision: 678312
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4-5mdv2011.0
+ Revision: 587978
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4-4mdv2010.1
+ Revision: 516099
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4-3mdv2010.0
+ Revision: 406583
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4-2mdv2009.1
+ Revision: 325737
- rebuild

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4-1mdv2009.0
+ Revision: 270246
- 0.4
- remove redundant patches

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-7mdv2009.0
+ Revision: 234946
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-6mdv2009.0
+ Revision: 215578
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-5mdv2008.1
+ Revision: 181725
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdv2008.0
+ Revision: 82578
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-3mdv2008.0
+ Revision: 65638
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-2mdv2007.1
+ Revision: 140675
- rebuild

* Wed Jan 31 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdv2007.1
+ Revision: 115650
- Import apache-mod_fakessl

* Wed Jan 31 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdv2007.1
- initial Mandriva package

