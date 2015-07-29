# NSIS RPM packages to build go.cd windows installer

[![Build Status](https://snap-ci.com/gocd/nsis-rpm/branch/master/build_image)](https://snap-ci.com/gocd/nsis-rpm/branch/master)

# Usage

Do this on a clean VM running on virtualbox.

This spec file and the sources are extracted from a source rpm from here -
http://koji.fedoraproject.org/koji/buildinfo?buildID=639921

Effectively the source rpm contained the original nsis source, a few patches and most importantly the spec file. The spec file was tweaked a bit.

The resultant rpms are checked into git for long term storage.

```bash
$ sudo yum install -y rpm-build yum-utils epel-release repoview createrepo
$ sudo yum groupinstall 'Development tools'
$ sudo yum-builddep nsis-rpm/mingw-nsis.spec
$ rpmbuild -bb mingw32-nsis.spec --define "_topdir $(pwd)" --define "_rpmdir $(pwd)" --define "_sourcedir $(pwd)"
```

# On CI machines

```bash
$ sudo yum install rubygem-rake
$ rake publish
```
