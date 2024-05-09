# Downloads all the logs from the server
# to the `./logs` directory on the machine that this command is run on.
scp -r $YOUR_SSH_TARGET:~/.pm2/logs .

# This is not required to analyze logs, but just in case.
