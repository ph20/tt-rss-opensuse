# Tiny Tiny RSS OpenSUSE packaging
## Overview
This project created for automate packaging _[Tiny Tiny RSS](https://tt-rss.org/)_ to OpenSUSE rpm package

## Development process
Up and login to vagrant box
```bash
vagrant up
vagrant ssh
```
Build package
```bash
cd /vagrant
./bin/prepare_tarball.sh
cd /vagrant/tt-rss/
rpmbuild -bb tt-rss.spec
rpmlint -f tt-rss-rpmlintrc /home/vagrant/rpmbuild/RPMS/noarch/tt-rss-22.12-0.noarch.rpm
```
## Testing package
Install package
```bash
sudo zypper in --allow-unsigned-rpm --recommends /home/vagrant/rpmbuild/RPMS/noarch/tt-rss-22.12-0.noarch.rpm
```
Configure postgresql database
```bash
sudo systemctl start postgresql.service
sudo --login --user=postgres psql
```

```postgresql
CREATE DATABASE tt_rss;
CREATE USER ttrss WITH ENCRYPTED PASSWORD 'P@ssW2';
GRANT ALL PRIVILEGES ON DATABASE tt_rss TO ttrss;
\connect tt_rss
CREATE SCHEMA tt_rss;
ALTER database "tt_rss" SET search_path TO tt_rss;
GRANT USAGE,CREATE ON SCHEMA tt_rss TO ttrss;
```
Modify `pg_hba.conf` to be able to connect to database with password
```editorconfig
#/var/lib/pgsql/data/pg_hba.conf
host    all             all             127.0.0.1/32            password
```
and restart `postgresql`
```bash
sudo systemctl restart postgresql.service
```
initialise database schemas
```bash
sudo runuser --user tt-rss   -- /usr/bin/php /srv/www/htdocs/tt-rss/update.php --update-schema=force-yes
```
configure and start `nginx`
```bash
sudo cp /etc/tt-rss/nginx.conf /etc/nginx/vhosts.d/tt-rss.conf
sudo systemctl start nginx.service
```
start `tiny tiny rss` services
```bash
sudo systemctl start tt-rss.service
sudo systemctl start tt-rss-update.service
```
Open in you browser application [http://localhost:8032](http://localhost:8032) user: `admin` password: `password`
