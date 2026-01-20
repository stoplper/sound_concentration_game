import glob
import os
import random

import customtkinter as ctk

class SoundConcentration(ctk.CTk):
    class Card(ctk.CTkButton):
        def __init__(self, master, row:int, col:int, sound:str, **kwargs):
            self.row = row
            self.col = col
            self.sound = sound
            super().__init__(master, corner_radius=10, border_width=3, width=20, height=20, **kwargs)
            self.revert()

        def grid(self, **kwargs):
            return super().grid(row=self.row, column=self.col, sticky=ctk.NSEW, padx=4, pady=4, **kwargs)
        
        def open(self) -> int:
            self.configure(state=ctk.DISABLED, text="...")

            return 1000

        def revert(self):
            self.configure(state=ctk.NORMAL, text="?")

        def remove(self):
            self.configure(state=ctk.DISABLED, text="", fg_color="transparent")
    
    def __init__(self, rows:int, cols:int, **kwargs):
        super().__init__(**kwargs)
        self.minsize(400, 400)
        self.title("Sound Concentration Game")

        # Find sound files
        sound_files = glob.glob(os.path.join("sounds", "*.wav"))
        
        # Check for maximum card count
        max_cards = len(sound_files)*2
        if rows*cols > max_cards:
            raise ValueError(f"Number of cards must be {max_cards} at maximum!")
        
        # Check for even card count
        if (rows*cols)%2 == 1:
            raise ValueError("Number of cards must be even number!")
        
        # Create dictionary of random sounds with counter
        sounds = dict.fromkeys(random.sample(sound_files, int(rows*cols/2)), 0)
        
        self._cards:list[SoundConcentration.Card] = list()
        for row in range(rows):
            for col in range(cols):
                # Select random sound for card, increase counter and remove from choices if already two cards have this sound
                sound = random.choice(list(sounds.keys()))
                sounds[sound] += 1
                if sounds[sound] == 2:
                    sounds.pop(sound)

                # Create the card
                card = self.Card(self, row=row, col=col, sound=sound)
                card.configure(command=lambda c=card, *args: self._open_card(c))
                card.grid()
                self._cards.append(card)

        # Fill the space with cards
        for row in range(rows):
            self.rowconfigure(row, weight=1, uniform="cards")
        for col in range(cols):
            self.columnconfigure(col, weight=1, uniform="cards")

        self._selected_cards:list[SoundConcentration.Card] = list()
        self._locked = False

    def _open_card(self, c:Card):
        # Return if locked
        if self._locked:
            return
        
        # Open card and store it
        lock_time = c.open()
        self._selected_cards.append(c)

        # Lock for lock_time returned by card
        self._lock()
        self.after(lock_time, self._unlock)
        
        # Check for match, then remove cards or revert them
        if len(self._selected_cards) == 2:
            if self._selected_cards[0].sound == self._selected_cards[1].sound:
                self.after(lock_time, self._remove_cards)
            else:
                self.after(lock_time, self._revert_cards)

    def _revert_cards(self):
        for c in self._selected_cards:
            c.revert()

        self._selected_cards.clear()

    def _remove_cards(self):
        for c in self._selected_cards:
            c.remove()

        self._selected_cards.clear()

    def _lock(self):
        self._locked = True

    def _unlock(self):
        self._locked = False

if __name__ == "__main__":
    game = SoundConcentration(2, 4)
    game.mainloop()