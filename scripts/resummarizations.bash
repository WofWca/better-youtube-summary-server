echo "time,video_id"
grep --no-filename "need to resummarize" /root/.pm2/logs/* \
    | sed "s/^\[//" \
    | sed "s/.[+-][0-9]\{4\}.*need to resummarize, vid=/,/" \
