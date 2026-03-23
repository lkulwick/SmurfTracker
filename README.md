# SmurfTracker
Do you wonder if you are playing against a smurf? This plugin helps you identify them.

It fetches Rocket League profile data directly from `rlstats.net` and shows player wins on the scoreboard. If your opponent has very few wins for the lobby they are in, that can be a strong signal.

## Fork Notice
This repository is a maintained fork of the original SmurfTracker project by `infinitel8p`.

Original repository:
- https://github.com/infinitel8p/SmurfTracker

This fork keeps the original idea and structure, while adding compatibility fixes and maintenance so the plugin can keep working on modern setups.

If you want to see more BakkesMod work from the original author, also check:
- https://github.com/infinitel8p/InstantFF

## Features
- Display wins for players in your current match
- Display MMR for players in your current match
- Use platform-aware RLStats lookups, including Steam profile IDs instead of display names

## Installation
### Build
- Open `SmurfTracker.sln` in Visual Studio 2022
- Build `Release | x64`

### BakkesMod Plugin Installation
- Download a release build from this repository or build the DLL locally
- Move the `.dll` file into `%appdata%\bakkesmod\bakkesmod\plugins`
- Make sure BakkesMod is running and start Rocket League
- Press `F2` to open the BakkesMod menu
- Enable `SmurfTracker` in the Plugin Manager
- Open the plugin settings and choose the mode you want to display

## Usage
Set the mode to `Wins`, `MMR`, or `Score`, then open the scoreboard during a match. In `Wins` mode the plugin requests RLStats directly, so results may take a short moment to appear.

No Docker container, shim service, or local IP configuration is required.

## Notice
Credit for the original plugin belongs to `infinitel8p`. This fork adds maintenance and compatibility work on top of that base.

Feel free to open issues or pull requests if you find regressions or have ideas for improvements.
