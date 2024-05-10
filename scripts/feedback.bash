# Keep in mind that when a video summary gets too much negative feedback,
# we re-summarize it (see `need_to_resummarize`).
# See `./resummarizations.bash`
echo "time,video_id,good_or_bad"
grep --no-filename " feedback, vid=" /root/.pm2/logs/* \
    | sed "s/^\[//" \
    | sed "s/.[+-][0-9]\{4\}.* feedback, vid=/,/" \
    | sed "s/, body={'good': False, 'bad': True}/,bad/" \
    | sed "s/, body={'good': True, 'bad': False}/,good/"
