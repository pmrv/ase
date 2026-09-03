"""This module is waiting for the day that we fix a problem with the testing:

Actual picture icons in the GUI are ready to go but there is a problem in
testing them: they tend to somehow disappear from memory while the test suite
is being run.
"""

import tkinter as tk
from pathlib import Path


class Icons:
    def __init__(self):
        icon_dir = Path(__file__).parent / 'icons'
        self.files = {}
        self.files['play'] = icon_dir / 'CarbonPlay.png'
        self.files['pause'] = icon_dir / 'CarbonPause.png'
        self.files['back'] = icon_dir / 'CarbonArrowLeft.png'
        self.files['forward'] = icon_dir / 'CarbonArrowRight.png'
        self.files['first'] = icon_dir / 'ASESkipBack.png'
        self.files['last'] = icon_dir / 'ASESkipForward.png'
        self.files['movie'] = icon_dir / 'CarbonDataPlayer.png'
        self.files['graph'] = icon_dir / 'CarbonChartLine.png'

        self.images = {}

        self.scale = 3.0

    def create_photoimages(self):
        """Creates PhotoImage objects that Tkinter can use. This must be done
        after the main window is created."""
        # Pillow is super convenient here, but it then needs to be added as
        # a dependency
        try:
            from PIL import Image, ImageTk
        except ModuleNotFoundError:
            ImageTk = None

        for key in self.files:
            if ImageTk is None:
                self.images[key] = tk.PhotoImage(
                    file=self.files[key]
                ).subsample(2)
            else:
                img = Image.open(fp=self.files[key])
                dim = round(self.scale * 20)
                self.images[key] = ImageTk.PhotoImage(img.resize([dim, dim]))

    def set_scaling(self, scale):
        self.scale = scale

    def __getitem__(self, key):
        if not self.images:
            self.create_photoimages()
        return self.images[key]
