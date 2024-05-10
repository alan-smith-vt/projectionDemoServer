# Projection Demo Server
See https://github.com/alan-smith-vt/projectionDemoProject for full operating instructions.

To set up the server:

Clone this github.

Install Python 3.6 (We used 3.6.8, but shouldn't need to be exact)
Install the requirements (cmd from within the server folder): "pip install -r requirements.txt"

Update lines 141-149 of "server.py" with your IP addresses for the computer running the server and the Hololens itself if deploying to the Hololens.
Change the "editor" boolean on line 141 of "server.py" to True if running the main project in the unity editor, or False if deploying to the Hololens.

Comment out line 78 of "server.py" if deploying to the Hololens. Leave uncommented if running in the unity editor.

To start the server:

Open the command prompt within the server folder and launch the "server.py" file however you normally launch python files 
(in our environment it is "python36 server.py", but this will vary based on your python environmental variables)