import os
import ctypes
import time
from datetime import datetime

class GlobalBot:
    def __init__(self, image_folder, interval_minutes):
        self.image_folder = image_folder
        self.interval_seconds = interval_minutes * 60
        self.images = self._load_images()
        self.current_image_index = 0

    def _load_images(self):
        """
        Load all image paths from the specified folder.

        Returns:
            list: A list of full paths to images.
        """
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
        return [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder)
                if f.lower().endswith(supported_formats)]

    def _set_wallpaper(self, image_path):
        """
        Set the desktop wallpaper to the specified image.

        Args:
            image_path (str): The path to the image file.
        """
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

    def _get_next_image(self):
        """
        Get the next image path from the collection.

        Returns:
            str: The path to the next image.
        """
        image_path = self.images[self.current_image_index]
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        return image_path

    def start(self):
        """
        Start the wallpaper changing process.
        """
        if not self.images:
            print("No images found in the specified folder.")
            return

        try:
            while True:
                next_image = self._get_next_image()
                self._set_wallpaper(next_image)
                print(f"{datetime.now()}: Wallpaper changed to {next_image}")
                time.sleep(self.interval_seconds)
        except KeyboardInterrupt:
            print("GlobalBot has been stopped.")

if __name__ == "__main__":
    image_folder = input("Enter the path to your image folder: ")
    interval_minutes = int(input("Enter the interval in minutes to change wallpaper: "))
    bot = GlobalBot(image_folder, interval_minutes)
    bot.start()