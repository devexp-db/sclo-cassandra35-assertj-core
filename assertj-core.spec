%bcond_without  memoryfilesystem

Name:           assertj-core
Version:        2.2.0
Release:        3%{?dist}
Summary:        Library of assertions similar to fest-assert
License:        ASL 2.0
URL:            http://joel-costigliola.github.io/assertj/
Source0:        https://github.com/joel-costigliola/%{name}/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(cglib:cglib-nodep)
%if %{with memoryfilesystem}
BuildRequires:  mvn(com.github.marschall:memoryfilesystem)
%endif
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.mockito:mockito-core)

%description
A rich and intuitive set of strongly-typed assertions to use for unit testing
(either with JUnit or TestNG).

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%pom_remove_parent
%pom_xpath_inject "pom:project" "<groupId>org.assertj</groupId>"

%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin org.jacoco:jacoco-maven-plugin
%pom_remove_plugin org.sonatype.plugins:jarjar-maven-plugin

%pom_xpath_inject "pom:project" "
    <properties>
        <maven.compiler.target>1.7</maven.compiler.target>
        <maven.compiler.source>1.7</maven.compiler.source>
    </properties>"

# package org.mockito.internal.util.collections does not exist
rm -rf ./src/test/java/org/assertj/core/error/ShouldContainString_create_Test.java

%if %{without memoryfilesystem}
%pom_remove_dep :memoryfilesystem
rm -r src/test/java/org/assertj/core/internal/{Paths*.java,paths}
%endif

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md CONTRIBUTING.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc CONTRIBUTING.md
%license LICENSE.txt

%changelog
* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.2.0-3
- Add conditional for memoryfilesystem

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 02 2015 Roman Mohr <roman@fenkhuber.at> - 2.2.0-1
- Initial packaging
