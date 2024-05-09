# Keep in mind that hitting a rate limit doesn't mean
# that the user request failed, because we retry the request after a fail.
grep --no-filename --ignore-case --perl-regexp "((\W429\W)|Too\s?Many\s?Requests)" /root/.pm2/logs/*
