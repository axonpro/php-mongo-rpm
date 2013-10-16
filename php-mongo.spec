%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary: PEAR: MongoDB database driver
Name: php-mongo
Version: 1.4.4
Release: 3
License: Apache License
Group: Development/Libraries
Source0: http://pecl.php.net/get/mongo-%{version}.tgz
Source1: php-mongo.ini
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL: http://pecl.php.net/package/mongo
#BuildArchitectures: x86_64
BuildRequires: php-pear >= 1.4.7
Requires: php-common


%description
This package provides an interface for communicating with the MongoDB
database in PHP.

%prep
%setup -c -T
# XXX Source files location is missing here in pear cmd
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
rm -rf %{buildroot}
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}
        
# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock

mv %{buildroot}/docs .


# Install XML package description
mkdir -p %{buildroot}%{xmldir}
#tar -xzf %{SOURCE0} package2.xml
#cp -p package2.xml %{buildroot}%{xmldir}/mongo.xml
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/mongo.xml
rm -rf %{buildroot}/var/tmp
mkdir -p %{buildroot}/etc/php.d/
cp %{SOURCE1} %{buildroot}/etc/php.d/

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/mongo.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only mongo
fi

%files
%defattr(-,root,root)
#%doc docs/mongo/{README.md,LICENSE.md}
%{peardir}/
/usr/lib64/php/modules/
%{xmldir}/mongo.xml
/etc/php.d/
