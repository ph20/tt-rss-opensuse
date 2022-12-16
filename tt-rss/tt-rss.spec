Name:           tt-rss
Version:        22.12
Release:        0
Summary:        Tiny Tiny RSS is a free and open source web-based news feed (RSS/Atom) reader and aggregator
License:        GPL-2.0-or-later
Group:          Productivity/Networking/Web/Frontends
URL:            https://tt-rss.org/
Source0:        tt-rss.tar.gz
Source1:        config.php
Source2:        nginx.conf
Source3:        php-fpm.conf
Source4:        tt-rss.service
Source5:        tt-rss-update.service
#
Requires:       php8
Requires:       php8-fpm
Requires:       php8-intl
Requires:       php8-fileinfo
Requires:       php8-mbstring
Requires:       php8-pdo
Requires:       php8-pgsql
Requires:       php8-cli
Requires:       php8-posix
Requires:       php8-pcntl
Requires:       nginx
Recommends:     postgresql
Recommends:     postgresql-server
Recommends:     postgresql-contrib
BuildArch:      noarch

%define         htdocs_root /srv/www/htdocs
%define         app_user    tt-rss
%define         app_group   tt-rss
%define         app_uid     932
%define         app_gid     932

%description
Self-hosted: control your own data and protect your privacy instead of relying on third party services;
Supports:
	* feed aggregation / syndication,
	* keyboard shortcuts,
	* OPML import/export,
	* multiple ways to share stuff: export RSS feeds, plugins for various social sites, sharing by URL, etc,
	* sharing arbitrary content through tt-rss,
	* Plugins and themes,
	* embedding full article content via readability and site-specific plugins,
	* deduplication, including perceptual hashing for images,
	* podcasts,
	* flexible article filtering,
	* JSON API,
	* and much more…

%prep
%setup -q
%autopatch -p1
# clean up
find . -name .gitignore -type f -prune -exec rm -f {} \;
find . -name .empty -type f -prune -exec rm -f {} \;
rm -Rf .eslintrc.js .editorconfig .vscode Jenkinsfile tests utils package.json phpstan.neon phpunit.xml jsconfig.json gulpfile.js composer.json composer.lock

# permissions
find . -type d -exec chmod 755 {} \;
find . ! -name '*.sh' ! -name '*-query' -type f -exec chmod 644 {} \;

%build

%install
# configs
%__install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
%__install -p -D -m 0644 -t %{buildroot}%{_sysconfdir}/%{name}/ %{SOURCE3}

# nginx vhost config
%__install -p -d -m 0755 %{buildroot}%{_sysconfdir}/nginx/vhosts.d/
%__install -p -D -m 0644 -T %{SOURCE2} %{buildroot}%{_sysconfdir}/nginx/vhosts.d/%{name}.conf

# units
%__install -p -d -m 0755 %{buildroot}%{_unitdir}
%__install -p -D -m 0644 -t %{buildroot}%{_unitdir}/ %{SOURCE4}
%__install -p -D -m 0644 -t %{buildroot}%{_unitdir}/ %{SOURCE5}

# htdocs
%__install -p -d -m 0755 %{buildroot}%{htdocs_root}/%{name}
cp -dR . %{buildroot}%{htdocs_root}/%{name}/
%__install -p -D -m 0644 -t %{buildroot}%{htdocs_root}/%{name}/ %{SOURCE1}
%__chmod 777 %{buildroot}%{htdocs_root}/%{name}/cache/{images,upload,export}
%__chmod 777 %{buildroot}%{htdocs_root}/%{name}/feed-icons
%__chmod 777 %{buildroot}%{htdocs_root}/%{name}/lock

%files
%license COPYING
%doc README.md CONTRIBUTING.md
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/nginx/vhosts.d/%{name}.conf
%{htdocs_root}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-update.service

%pre
%service_add_pre %{name}.service
%service_add_pre %{name}-update.service
# create application group, if not existing
if
    getent group %{app_group} >/dev/null
then
    : OK group %{app_group} already present
else
    groupadd -g %{app_gid} -r %{app_group}  2>/dev/null || :
fi
# create application user, if not existing
if
    getent passwd %{app_user} >/dev/null
then
    : OK user %{app_user} already present
else
    useradd  -r -u %{app_uid} -g %{app_group} -s /usr/sbin/nologin -c "Tiny Tiny RSS user" -d %{htdocs_root}/%{name} %{app_user} 2> /dev/null || :
fi