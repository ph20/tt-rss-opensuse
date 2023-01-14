<?php
        putenv('TTRSS_SELF_URL_PATH=http://localhost:8032/');
        define('_SKIP_SELF_URL_PATH_CHECKS', true);
        putenv('TTRSS_DB_TYPE=pgsql');
        putenv('TTRSS_DB_HOST=127.0.0.1');
        putenv('TTRSS_DB_NAME=tt_rss');
        putenv('TTRSS_DB_USER=ttrss');
        putenv('TTRSS_DB_PASS=P@ssW2');
        putenv('TTRSS_PHP_EXECUTABLE=/usr/bin/php');
        putenv('TTRSS_CACHE_DIR=/var/cache/tt-rss');
        putenv('TTRSS_ICONS_DIR=/var/cache/tt-rss/feed-icons');
