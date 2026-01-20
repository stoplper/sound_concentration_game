import enum
import glob
import os
import random

import customtkinter as ctk
from mutagen.mp3 import MP3
from playsound3 import playsound

class SoundConcentration(ctk.CTk):
    VERSION_MAJOR = 1
    VERSION_MINOR = 0
    VERSION_PATCH = 0
    VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

    normal_font:ctk.CTkFont = None
    bold_font:ctk.CTkFont = None

    class Card(ctk.CTkButton):
        class State(enum.Enum):
            PRESENT = enum.auto()
            REMOVED = enum.auto()
            
        def __init__(self, master, sound:str|None = None, **kwargs):
            self.sound = sound
            self.state = self.State.PRESENT
            super().__init__(master, corner_radius=10, border_width=3, width=20, height=20, **kwargs)
            self.revert()

        def grid(self, row:int, col:int, **kwargs):
            return super().grid(row=row, column=col, sticky=ctk.NSEW, padx=4, pady=4, **kwargs)
        
        def open(self) -> int:
            self.configure(state=ctk.DISABLED, text="...", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

            if self.sound is None:
                return 0
            else:
                print(f"Playing: {self.sound}")
                # Play the sound
                playsound(self.sound, False)
                # Return sound duration
                return MP3(self.sound).info.length

        def revert(self):
            self.configure(state=ctk.NORMAL, text="?", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            if self.state == self.State.REMOVED:
                self.state = self.State.PRESENT

        def remove(self):
            self.configure(state=ctk.DISABLED, text="", fg_color="transparent")
            self.state = self.State.REMOVED

        def lock(self):
            self.configure(state=ctk.DISABLED)

        def unlock(self):
            self.configure(state=ctk.NORMAL)
    
    def __init__(self, rows:int, cols:int, **kwargs):
        super().__init__(**kwargs)
        self.minsize(cols*100 + 160, rows*100)
        self.title(f"Sound Concentration Game {self.VERSION}")

        # Find sound files
        self._sound_files = glob.glob(os.path.join("sounds", "*.mp3"))
        
        # Check for maximum card count
        max_cards = len(self._sound_files)*2
        if rows*cols > max_cards:
            raise ValueError(f"Number of cards must be {max_cards} at maximum!")
        
        # Check for even card count
        if (rows*cols)%2 == 1:
            raise ValueError("Number of cards must be even number!")
        
        # Define fonts
        self.normal_font = ctk.CTkFont(size=25)
        self.bold_font = ctk.CTkFont(weight="bold", size=25)
        
        # Create cards
        self._cards:list[SoundConcentration.Card] = list()
        for row in range(rows):
            for col in range(cols):
                # Create the card
                card = self.Card(self, font=self.bold_font)
                card.configure(command=lambda c=card, *args: self._open_card(c))
                card.grid(row, col)
                self._cards.append(card)

        # Create control frame
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=cols, rowspan=rows, sticky=ctk.NSEW)

        self.score = ctk.IntVar(self, 0)
        ctk.CTkButton(control_frame, corner_radius=10, border_width=3, text="Reset", font=self.bold_font, command=self.reset).pack(side=ctk.BOTTOM, padx=(20, 4), pady=4)
        ctk.CTkLabel(control_frame, textvariable=self.score, font=self.normal_font).pack(side=ctk.BOTTOM, padx=(20, 4), pady=(0, 10))
        ctk.CTkLabel(control_frame, text="Score:", font=self.bold_font).pack(side=ctk.BOTTOM, padx=(20, 4))

        # Arrange cards evenly
        for row in range(rows):
            self.rowconfigure(row, weight=1, uniform="cards")
        for col in range(cols):
            self.columnconfigure(col, weight=1, uniform="cards")

        self._selected_cards:list[SoundConcentration.Card] = list()
        
        self._top:ctk.CTkToplevel|None = None

        self.reset()

    def reset(self):
        # Create dictionary of random sounds with counter
        sounds = dict.fromkeys(random.sample(self._sound_files, int(len(self._cards)/2)), 0)

        for card in self._cards:
            # Select random sound for card, increase counter and remove from choices if already two cards have this sound
            sound = random.choice(list(sounds.keys()))
            sounds[sound] += 1
            if sounds[sound] == 2:
                sounds.pop(sound)

            # Revert the card and renew sound
            card.revert()
            card.sound = sound

        # Reset selected cards
        self._selected_cards.clear()

        # Reset score
        self.score.set(0)

        # Close top level if opened
        if self._top is not None:
            self._top.destroy()
            self._top = None

    def _open_card(self, c:Card):     
        # Open card and store it
        lock_time = int((c.open() + 0.5) * 1000)
        self._selected_cards.append(c)

        # Lock for lock_time returned by card
        self._lock_cards()
        self.after(lock_time, self._unlock_cards)
        
        # Check for match, then remove cards or revert them
        if len(self._selected_cards) == 2:
            if self._selected_cards[0].sound == self._selected_cards[1].sound:
                self.after(lock_time, self._remove_cards)
            else:
                self.after(lock_time, self._revert_cards)

    def _revert_cards(self):
        for c in self._selected_cards:
            c.revert()

        # Score -1
        self.score.set(self.score.get() - 1)

        self._selected_cards.clear()

    def _remove_cards(self):
        for c in self._selected_cards:
            c.remove()

        # Score +3
        self.score.set(self.score.get() + 3)

        self._selected_cards.clear()

        # Check for completed game
        if all([c.state == self.Card.State.REMOVED for c in self._cards]):
            self._end_game()

    def _lock_cards(self):
        for card in self._cards:
            if card not in self._selected_cards:
                card.lock()

    def _unlock_cards(self):
        for card in self._cards:
            if card not in self._selected_cards:
                card.unlock()

    def _end_game(self):
        self._top = ctk.CTkToplevel(self)
        self._top.title("Game finished")
        self._top.attributes("-topmost", True)
        self._top.grab_set()
        self._top.protocol("WM_DELETE_WINDOW", self.destroy)

        ctk.CTkLabel(self._top, text="Congratulations!", font=self.bold_font).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        ctk.CTkLabel(self._top, text=f"Score: {self.score.get()}", font=self.normal_font).grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        ctk.CTkButton(self._top, text="END", corner_radius=10, border_width=3, font=self.bold_font, command=self.destroy).grid(row=2, column=0, padx=(20, 10), pady=(0, 20))
        ctk.CTkButton(self._top, text="Reset", corner_radius=10, border_width=3, font=self.bold_font, command=self.reset).grid(row=2, column=1, padx=(0, 20), pady=(0, 20))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sound Concentration Game")
    parser.add_argument("--rows", type=int, default=4, help="Number of rows (default: 4)")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns (default: 4)")
    args = parser.parse_args()
    
    game = SoundConcentration(args.rows, args.cols)
    game.after(1000, lambda:print(game._cards[0].winfo_width()))
    game.after(1000, lambda:print(game._cards[0].winfo_height()))
    game.mainloop()