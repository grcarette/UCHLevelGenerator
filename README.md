# UCH Level Generator
A standalone application that procedurally generates levels for the game Ultimate Chicken Horse. Written in Python

![AppUI](https://github.com/grcarette/UCHMapGenerator/assets/58717176/9661080c-7143-4072-898d-debd0448f079)
### Installation
- Go to the **Releases** section and download **UCHLevelGenerator.zip**
- Extract the folder anywhere you'd like
- Open UCHLevelGenerator.exe and you're ready to go

### Usage
- Select your settings to decide how the map will generate
  - The generation process was designed around the default settings. Everything should still work if you make changes, but certain settings may increase the chance of generating an impossible level
- Enter the number of levels you'd like to generate
- Click the "Generate Level(s)" button
- All generated levels will automatically be sent to C:\\Users\User\AppData\LocalLow\Cleaver Endeavour Games\Ultimate chicken Horse\Snapshots
- To play these levels simply open "Local Levels" in the in game level loader and they should appear on screen
  - Levels will not have thumbnails until you've played them for the first time

### To Do
- Add additional level assets
- Optimize point generation
- Add pathfinding algorithm
- Add "Draw level" functionality

### Known Issues
- On some devices map generation will stall ~25% of the time
