# Toggl Terminal Client

This is a Terminal client to start timers, stop timers, get current timer, and get list of projects in [Toggl](http://toggl.com/). I use Toggle to manage my time across my various classes and projects.

### Dependancies

You will need the following packages installed for Python 2.7:

* `json`
* `requests`
* `datetime`

### Installation

Save the folder in your preferred directory and change that path in `execute.sh`. 

Make the `execute.sh` script executable by running `chmod +x execute.sh` from the directory.

Each Toggl user has an API token, which can be found under "My Profile" in their Toggl account. Copy that API token in `credentials.json`.

**Suggested Use:** Add the alias `toggl='~/<path>/execute.sh'` in your `bashrc`.

### Use

1. `./execute.sh start` or `toggl start`

   Stops any ongoing timers and asks for project name and description to start a new timer from current time.

2. `./execute.sh stop` or `toggl stop`

   Stops any ongoing timers.

3. `./execute.sh current` or `toggl current`

   Get name, description, and duration of current timer.

4. `./execute.sh projects` or `toggl projects`

   Get names of all projects in Toggl.

