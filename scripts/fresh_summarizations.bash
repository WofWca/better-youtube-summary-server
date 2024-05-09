# Outputs completed summarizations for videos
# that have not been summarized before
# (are not in our DB).
#
# Sample output
# 2024-01-02 12:30:59,dQw4w9WgXcQ,en,abcdef12-abcd-abcd-bcda-104fffff321

echo "time,video_id,captions_lang,user_id"
grep --no-filename "summarize whole video" /root/.pm2/logs/* \
    | sed "s/^\[//" \
    | sed "s/.[+-][0-9]\{4\}.*vid=/,/" \
    | sed "s/, lang=/,/" \
    | sed "s/, trigger=/,/" \
    | sed "s/, {.*$//"
