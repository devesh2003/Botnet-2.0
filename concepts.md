Botnet 2.0
Update to botnet based on beacons

Domain : www.bolt2003.tk (Nameservers point to digital ocean VPS)

1) Server
2) Client
3) Stager (Java) --> Delivers the main payload

1) Server
# Starts server on port 2003 on VPS server
# Listens for connections(Beacons)
# Client beacon checks for any commands
# Takes command as input and stores as a global variable
# Creates a check list of all bots
# Beacon checks in --> takes the command from the global variable --> bot removed    from check list
# Prints confirmation for all indivisual bots
# Resets the global variable and check list
# Change interval request --> changes command --> creates a check list --> displays results

2) Client
# Stored in the startup directory
# Default interval 5 seconds
# Connects to www.bolt20003.tk on port 2003 every {interval} seconds
# Checks for any commands
# Executes the command (if any) OR pass
# Sends the output instantly in that current TCP socket

3) Stager
# Java based
# Downloads main payload from www.bolt2003.com/bot.exe
# Stores the payload in default startup directory
# Runs the payload using Runtime
