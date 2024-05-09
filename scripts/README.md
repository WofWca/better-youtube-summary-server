# Stats scripts

These help you get some statistics from the logs.

## Usage

The below examples should also work on Windows CMD,
with minor adjustments perhaps.

You're most likely running the scripts on a remote server,
so you want to execute them remotely
and have the output on the local machine.
An example of how you can do this
(replace `fresh_summarizations.bash` with the script file from this
directory that you want, and replace `$YOUR_SERVER_IP` with guess what.
`fresh_summarizations.csv` is the name of the output file - choose any):

```bash
cat scripts/fresh_summarizations.bash \
    | ssh $YOUR_SERVER_IP 'bash -s' \
    > ./fresh_summarizations.csv
```

If you wish to just print the output instead of saving it to a file,
remove the last line (`> ./fresh_summarizations.csv`).

If you want to simply count something, you can pipe the output to `wc --lines`
instead of a file, as such:

```bash
cat scripts/fresh_summarizations.bash \
    | ssh $YOUR_SERVER_IP 'bash -s' \
    | wc --lines
```

## Analysis

For further analysis we use LibreOffice spreadsheets.
There we can filter by time and do other neat stuff.

## TODO

When the scripts start getting complex,
it's probably time to switch to a more specialized solution.
For monitoring, consider [Prometheus](https://prometheus.io/).
For stats and analysis, consider something like Datadog
or [alternatives](https://alternativeto.net/software/datadog/?license=opensource)
(I don't know too much about log parsers).
