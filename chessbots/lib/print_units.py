
class PrintPixel:
    def __init__(self, unit: float) -> None:
        self.unit = unit

    def to_pixel(self, dpi: int) -> int:
        return int(self.unit)


class PrintMilliMeter(PrintPixel):
    def to_pixel(self, dpi: int) -> int:
        return int((self.unit / 25.4) * dpi)


class PrintInch(PrintPixel):
    def to_pixel(self, dpi: int) -> int:
        return int(self.unit * dpi)
