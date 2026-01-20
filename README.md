# Sound Concentration Game
- [Installation and Launch](#installation-and-launch)
  - [Python](#python)
  - [Windows x64](#windows-x64)
- [Modification](#modification)

## Installation and Launch

### Python

#### Prerequisites
- Python version ≥3.10 (tested on 3.13.11), preferably added to PATH.
- Pip, preferably added to PATH.

#### Steps
1. Clone or download this repository.
2. Install required packages with the following command in the repository directory:
   ```
   pip install -r requirements.txt
   ```
3. Launch the game by double-clicking `sound_concentration.py` or from the command line in the repository directory with:
   ```
   python sound_concentration.py
   ```

### Windows x64

#### Steps
1. Download the executable from releases.
2. Launch the game by double-clicking `sound_concentration.exe` or from the command line in the repository directory with:
   ```
   sound_concentration.exe
   ```

## Modification

You can modify the game by adding or replacing mp3 sounds in the `sounds` directory (filenames do not matter).

Another modification can be done by specifying the number of rows and columns. This must be done from the command line. For Python:
```
python sound_concentration.py --rows <number_of_rows> --cols <number_of_columns>
```
or for Windows x64:
```
sound_concentration.exe --rows <number_of_rows> --cols <number_of_columns>
```