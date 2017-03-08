%{?scl:%scl_package assertj-core}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}assertj-core
Version:	2.2.0
Release:	3%{?dist}
Summary:	Library of assertions similar to fest-assert
License:	ASL 2.0
URL:		http://joel-costigliola.github.io/assertj/
Source0:	https://github.com/joel-costigliola/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz#/%{pkg_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix}cglib
# don't need in scl package
%{!?scl:BuildRequires:	mvn(com.github.marschall:memoryfilesystem)}
BuildRequires:	%{?scl_prefix_java_common}junit
BuildRequires:	%{?scl_prefix_maven}mockito
%{?scl:Requires: %scl_runtime}

%description
A rich and intuitive set of strongly-typed assertions to use for unit testing
(either with JUnit or TestNG).

%package javadoc
Summary:	API documentation for %{name}

%description javadoc
This package provides API documentation for %{name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
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

# remove in scl pakcgae as it is not needed
%pom_remove_dep :memoryfilesystem
rm -r src/test/java/org/assertj/core/internal/{Paths*.java,paths}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md CONTRIBUTING.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc CONTRIBUTING.md
%license LICENSE.txt

%changelog
* Tue Mar 07 2017 Tomas Repik <trepik@redhat.com> - 2.2.0-3
- scl conversion

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 02 2015 Roman Mohr <roman@fenkhuber.at> - 2.2.0-1
- Initial packaging
