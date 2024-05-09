grep --only-matching --no-filename --perl-regexp \
    "translate, done.+?trigger=.+?," /root/.pm2/logs/* \
    | sort | uniq
