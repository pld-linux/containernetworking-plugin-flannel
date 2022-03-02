%define		vendor_version		1.0.1
Summary:	CNI plugin designed to work in conjunction with flannel
Name:		containernetworking-plugin-flannel
Version:	1.0.1
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/flannel-io/cni-plugin/archive/v%{version}/flannel-cni-plugin-%{version}.tar.gz
# Source0-md5:	b2df4fbd659fbd6c39e056cc7c1786a4
Source1:	flannel-cni-plugin-vendor-%{vendor_version}.tar.xz
# Source1-md5:	2bc7a1ce22ebdec186280c942a4d29c9
URL:		https://github.com/flannel-io/cni-plugin
BuildRequires:	golang >= 1.16
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	containernetworking-plugins
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
CNI plugin designed to work in conjunction with flannel.

%prep
%setup -q -n cni-plugin-%{version} -a1

%{__mv} cni-plugin-%{vendor_version}/vendor .

%build
ldflags="-X main.Version=%{version} \
	-X main.Program=flannel \
	-X main.buildDate=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
%__go build -mod=vendor -ldflags="$ldflags" -tags="netgo osusergo no_stage" -o target/flannel

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libexecdir}/cni

cp -p target/flannel $RPM_BUILD_ROOT%{_libexecdir}/cni

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libexecdir}/cni/flannel
