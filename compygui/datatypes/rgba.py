from dataclasses import dataclass


@dataclass
class RGBAMask:
    """Represents an RGBA color mask/format"""

    def __init__(self, *args, r: int, g: int, b: int, a: int) -> None:
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a

    @staticmethod
    def RGBA() -> RGBAMask:
        """Equivalent to RGBAMask(r=0xFF000000, g=0x00FF0000, b=0x0000FF00, a=0x000000FF)"""
        return RGBAMask(r=0xFF000000, g=0x00FF0000, b=0x0000FF00, a=0x000000FF)

    @staticmethod
    def ARGB() -> RGBAMask:
        """Equivalent to RGBAMask(a=0xFF000000, r=0x00FF0000, g=0x0000FF00, b=0x000000FF)"""
        return RGBAMask(a=0xFF000000, r=0x00FF0000, g=0x0000FF00, b=0x000000FF)

    @staticmethod
    def ABGR() -> RGBAMask:
        """Equivalent to RGBAMask(a=0xFF000000, b=0x00FF0000, g=0x0000FF00, r=0x000000FF)"""
        return RGBAMask(a=0xFF000000, b=0x00FF0000, g=0x0000FF00, r=0x000000FF)

    @staticmethod
    def ZERO() -> RGBAMask:
        """Equivalent to RGBAColor(r=0, g=0, b=0, a=0)"""
        return RGBAMask(r=0, g=0, b=0, a=0)

    def as_int(self) -> int:
        return self.r | self.g | self.b | self.a


@dataclass
class RGBAColor:
    """Represents an RGBA color with variable bit depth
    (when using RGBAColor().as_bytes())
    """

    def __init__(self, *args, r: int, g: int, b: int, a: int) -> None:
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a

    @staticmethod
    def WHITE() -> RGBAColor:
        """Equivalent to RGBAColor(r=255, g=255, b=255, a=255)"""
        return RGBAColor(r=255, g=255, b=255, a=255)

    @staticmethod
    def BLACK() -> RGBAColor:
        """Equivalent to RGBAColor(r=0, g=0, b=0, a=255)"""
        return RGBAColor(r=0, g=0, b=0, a=255)

    @staticmethod
    def TWHITE() -> RGBAColor:
        """Equivalent to RGBAColor(r=255, g=255, b=255, a=0)"""
        return RGBAColor(r=255, g=255, b=255, a=0)

    @staticmethod
    def TBLACK() -> RGBAColor:
        """Equivalent to RGBAColor(r=0, g=0, b=0, a=0)

        Same as RGBAColor.ZERO()
        """
        return RGBAColor(r=0, g=0, b=0, a=0)

    @staticmethod
    def ZERO() -> RGBAColor:
        """Equivalent to RGBAColor(r=0, g=0, b=0, a=0)

        Same as RGBAColor.TBLACK()
        """
        return RGBAColor(r=0, g=0, b=0, a=0)

    # TODO: Add more colors

    def as_int(self, bits_per_channel: int) -> int:
        if bits_per_channel > 8:
            raise ValueError("bits_per_channel must be in range(0, 8) (0-7)")

        return (
            self.a
            | self.b << (bits_per_channel * 1)
            | self.g << (bits_per_channel * 2)
            | self.r << (bits_per_channel * 3)
        )
