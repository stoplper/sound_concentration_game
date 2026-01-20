# Sound concentration game
- [Installation and launch](#installation-and-launch)
  - [Python](#python)
  - [Windows x64](#windows-x64)
- [Modification](#modification)

## Installation and launch
### Python
#### Prerequisites
- Installed python version >3.10 (tested on 3.13.11), preferably in PATH.
- Installed pip, preferably in PATH.

#### Steps
1. Clone or download this repository.
2. Install required packages with following command in repository directory .
   ```
   pip install -r requirements.txt
   ```
3. Launch the game with double clicking `sound_concentration.py` or from command line in repository directory with following command. 
   ```
   python3 sound_concentration.py
   ```

### Windows x64
#### Steps
1. Download executable from releases.
2. Launch the game with double clicking `sound_concentration.exe` or from command line in repository directory with command `sound_concentration.exe`

## Modification
User can modify the game via adding or replacing mp3 sounds in `sounds` directory (filenames do not matter). 

Another modification can be done by specifying number of rows and columns. This has to be done from command line, for python 
```
python3 sound_concentration.py --rows <number_of_rows> --cols <number_of_columns>
``` 
or for Windows x64.
```
sound_concentration.exe --rows <number_of_rows> --cols <number_of_columns>
```