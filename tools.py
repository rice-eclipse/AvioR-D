class Color:

    def __init__(self, rgb):
        """
        Create a color.
        :param rgb: (r, g, b) color
        """
        self.rgb = rgb

    @staticmethod
    def from_hex(hex_color):
        """
        Create color from hex string in form #000000.
        :param hex_color: hex string.
        :return:
        """
        color = hex_color[1:]
        rgb = tuple(int(color[i:i + 2], 16) for i in (4, 2, 0))
        return Color(rgb)

    @staticmethod
    def from_rgb(rgb):
        """
        Create color from rgb tuple in form (r, g, b).
        :param rgb: tuple.
        :return:
        """
        return Color(rgb)

