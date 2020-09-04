# spec file for package kodama

%{?!python_module:%define python_module() python-%{**} python3-%{**}}

Name:           kodama
Version:        0.1
Release:        0
Summary:        kodama
License:        GPL-2.0+
Group:          Development/Tools/Building
Url:            https://github.com/dincamihai/kodama/archive/master.tar.gz
Source:         https://github.com/dincamihai/kodama/archive/master.tar.gz
BuildArch:      noarch
BuildRequires:  %{python_module devel}
BuildRequires:  python-setuptools
BuildRequires:  python-rpm-macros
BuildRoot:      %{_tmppath}/%{name}-master

%description
kodama

%prep
%setup -q -n %{name}-master

%build
%python_build

%install
%python_install
%makeinstall

%files
%{python_sitelib}/producer.py
%{python3_sitelib}/producer.py
%{python_sitelib}/consumer.py
%{python3_sitelib}/consumer.py
%{python_sitelib}/kodama-*.egg-info
%{python3_sitelib}/kodama-*.egg-info
 
%changelog
