echo "time,granted"
grep --no-filename "trial request, " /root/.pm2/logs/* \
    | sed "s/^\[//" \
    | sed "s/.[+-][0-9]\{4\}.*trial request, {'granted': /,/" \
    | sed "s/\}//"
