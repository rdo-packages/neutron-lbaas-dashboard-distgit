# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_sitearch %python%{pyver}_sitearch
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_test 0

%global up_name neutron-lbaas-dashboard

Name:           openstack-neutron-lbaas-ui
Version:        XXX
Release:        XXX
Summary:        Horizon UI support for Neutron LBaaS

License:        ASL 2.0
URL:            https://github.com/openstack/neutron-lbaas-dashboard/
Source0:        https://tarballs.openstack.org/%{up_name}/%{up_name}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  openstack-dashboard
BuildRequires:  python%{pyver}-barbicanclient
BuildRequires:  python%{pyver}-pbr
BuildRequires:  openstack-macros
Requires:  openstack-dashboard >= 13.0.0
Requires:  python%{pyver}-barbicanclient >= 4.5.2
Requires:  python%{pyver}-pbr
Requires:  python%{pyver}-oslo-log >= 3.36.0

Provides:  neutron-lbaas-dashboard

%description
Horizon panels for Neutron LBaaS v2

%package doc
Summary: Documentation for Neutron LBaaS dashboard
%description doc
Documentation for Neutron LBaaS dashboard


%prep
%autosetup -n %{up_name}-%{upstream_version} -p1 -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

export PBR_VERSION="1.8.1"
export PYTHONPATH="%{_datadir}/openstack-dashboard:%{pyver_sitearch}:%{pyver_sitelib}:%{buildroot}%{pyver_sitelib}"
sphinx-build-%{pyver} -W -b html doc/source doc/build/html

# clean up files after sphinx
rm doc/build/html/.buildinfo
rm -rf doc/build/html/.doctrees


%install
%{pyver_install}

mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
install -p -D -m 640 neutron_lbaas_dashboard/enabled/_1481_project* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

%check
%if %{?with_test}
%{pyver_bin} setup.py test
%endif


%files
%doc README.rst doc
%license LICENSE
%{pyver_sitelib}/neutron_lbaas_dashboard
%{pyver_sitelib}/neutron_lbaas_dashboard-%{version}*-py%{python_version}.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1481*

%files doc
%doc doc/build/html
%license LICENSE


%changelog
