# All the YouTube videos IDs that our server has worked with
grep --only-matching --no-filename --perl-regexp \
    "vid=.+?," /root/.pm2/logs/* \
    | sed "s/vid=//" \
    | sed "s/,//" \
    | sort | uniq
