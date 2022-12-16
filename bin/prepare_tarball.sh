#!/usr/bin/env bash
git clone --bare --branch master https://git.tt-rss.org/fox/tt-rss.git ../tt-rss.git
git archive --remote=../tt-rss.git --format=tar.gz -o tt-rss/tt-rss.tar.gz --prefix=tt-rss-22.12/ master
rm -Rf ../tt-rss.git