import datetime

class Character:
    def __init__(self, data, url, character_name):
        """Parse the data and return the character info"""
        lines = data.splitlines()

        # Get the image link -- Find line containing this string
        image_line = [line for line in lines if "var SELECTED_SKIN =" in line][0]
        image_link = image_line.split('=')[1]
        for _ in ["'", '"', ";"]:
            image_link = image_link.replace(_, "")
        image_link.strip()

        self.name = character_name.title()
        self.title = f"{character_name.title()} - Epic Seven Wiki"
        self.description = f"{character_name}"
        self.color = 0xd700ff
        self.image = image_link
        self.url = url
        self.timestamp = datetime.datetime.utcnow()