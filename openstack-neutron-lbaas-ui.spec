%global with_test 0

%global up_name neutron-lbaas-dashboard

Name:           openstack-neutron-lbaas-ui
Version:        XXX
Release:        XXX
Summary:        Horizon UI support for Neutron LBaaS

License:        ASL 2.0
URL:            https://github.com/openstack/neutron-lbaas-dashboard/
Source0:        http://tarballs.openstack.org/%{up_name}/%{up_name}-master.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
Requires:  openstack-dashboard >= 9.0.0
Requires:  python-barbicanclient
Requires:  python-pbr

Provides:  neutron-lbaas-dashboard

%description
Horizon panels for Neutron LBaaS v2

%package doc
Summary: Documentation for Neutron LBaaS dashboard
%description doc
Documentation for Neutron LBaaS dashboard


%prep
%autosetup -n %{up_name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%py2_build

export PBR_VERSION="1.8.1"
sphinx-build doc/source html

# clean up files after sphinx
rm html/.buildinfo
rm -rf html/.doctrees


%install
%py2_install

mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
install -p -D -m 640 neutron_lbaas_dashboard/enabled/_148[01]_project* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

%check
%if %{?with_test}
%{__python2} setup.py test
%endif


%files
%doc README.rst doc
%license LICENSE
%{python2_sitelib}/neutron_lbaas_dashboard
%{python2_sitelib}/neutron_lbaas_dashboard-%{version}*-py%{python_version}.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_148[01]*

%files doc
%doc html
%license LICENSE


%changelog
* Fri Jun  3 2016 Matthias Runge <mrunge@redhat.com> - 1.0.0-3
- initial package
- drop python3 for the time being
- added barbicanclient as dependency
- removed build artifacts from doc-build
