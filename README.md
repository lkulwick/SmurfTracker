# SmurfTracker
Do you wonder if you are playing against a smurf? This plugin will help you to identify them.  
It uses a local compatibility shim on `127.0.0.1:8191` to fetch the wins or mmr of the players in your match.  
If your opponent has few wins in comparison to your lobby and is playing out of his mind, he probably is a smurf.

## Fork Notice
This repository is a fork of the original SmurfTracker project by `infinitel8p`.

The original repository is:
- https://github.com/infinitel8p/SmurfTracker

This fork keeps the original project structure and intent, and currently focuses on compatibility fixes and maintenance so the plugin can keep working on modern setups.

If you want to see the original author's other BakkesMod work, also check:
- https://github.com/infinitel8p/InstantFF

## Table of Contents
- [Fork Notice](#fork-notice)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Notice](#notice)

## Features
- Fetch the wins of all players, all except you or only the opponents in your match (TDB, right now it fetches all players)
- Fetch the mmr of all players in your match - done via scraping so you can see the mmr even in private matches (TBD, uses bakkesmod mmr wrapper for now)

## Installation
### Prerequisites - Local Shim
Build the local compatibility shim image:

```bash
docker build -t smurftracker-shim:local -f shim/Dockerfile .
```

Run it on port `8191`:

```bash
docker run --rm -d --name smurftracker-shim -p 8191:8191 smurftracker-shim:local
```

Optional health check:

```bash
curl http://127.0.0.1:8191/health
```

This should return:

```json
{"status":"ok"}
```

The shim is a transitional component that keeps the current plugin DLL working while the scraping logic is prepared for a future move into the plugin itself.

### BakkesMod Plugin Installation
- Download a release build from the Releases page of this repository.
- Move the downloaded .dll file into %appdata%\bakkesmod\bakkesmod\plugins
- Make sure BakkesMod is running and start Rocket League
- Press F2 to open the BakkesMod menu and navigate to the Plugins tab and there open the Plugin Manager
- Locate the Plugin SmurfTracker in the list and click the checkbox to enable it.
- Go back to the Plugins tab and find SmurfTracker in the list, click it and apply your desired settings  

**Important**: Set the plugin IP to `127.0.0.1` so the current DLL can reach the local shim on `http://127.0.0.1:8191/v1`.

## Usage
Set the mode you want to use in the settings and open the scoreboard in a match to see the wins of the players. (When you open the scoreboard the plugin will start fetching the data, so it might take a few seconds to show up)

## Notice
The current shim talks directly to `rlstats.net` and preserves the old local API contract used by the plugin. It is meant as the first recovery step before Docker is removed from the workflow entirely in a later revision.

Credit for the original plugin belongs to `infinitel8p`. This fork only adds maintenance and compatibility work on top of that base.

Feel free to open issues or pull requests if you have any suggestions or problems.
