# Tiny Tiny RSS OpenSUSE packaging
## Overview
This project created for automate packaging _[Tiny Tiny RSS](https://tt-rss.org/)_ to OpenSUSE rpm package

## Development process
Up and login to vagrant box
```
vagrant up
vagrant ssh
```
Build package
```
cd /vagrant/tt-rss/
rpmbuild -bb tt-rss.spec
```
Install package
```
sudo zypper in --allow-unsigned-rpm --recommends /home/vagrant/rpmbuild/RPMS/noarch/tt-rss-22.12-0.noarch.rpm
```

Configure postgresql database
```
sudo --login --user=postgres psql
```

```
CREATE DATABASE tt_rss;
CREATE USER ttrss WITH ENCRYPTED PASSWORD 'P@ssW2';
GRANT ALL PRIVILEGES ON DATABASE tt_rss TO ttrss;
\connect tt_rss
CREATE SCHEMA tt_rss;
ALTER database "tt_rss" SET search_path TO tt_rss;
GRANT USAGE,CREATE ON SCHEMA tt_rss TO ttrss;
```
Modify `pg_hba.conf` to be able to connect to database with password
```
#/var/lib/pgsql/data/pg_hba.conf
host    all             all             127.0.0.1/32            password
```




