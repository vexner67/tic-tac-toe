"""Размер главного окна приложения."""

from dataclasses import dataclass

from tic_tac_toe.model.exceptions import InvalidWindowSizeError


@dataclass(frozen=True)
class WindowSize:
    """Допустимый размер окна в пикселях.

    Ограничения гарантируют, что поле и панель статуса всегда помещаются
    в окно, а само окно — на типичный экран.
    """

    MIN_WIDTH = 320
    MIN_HEIGHT = 380
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080

    width: int
    height: int

    def __post_init__(self) -> None:
        if not self.MIN_WIDTH <= self.width <= self.MAX_WIDTH:
            raise InvalidWindowSizeError(
                f"Ширина должна быть от {self.MIN_WIDTH} "
                f"до {self.MAX_WIDTH} пикселей."
            )
        if not self.MIN_HEIGHT <= self.height <= self.MAX_HEIGHT:
            raise InvalidWindowSizeError(
                f"Высота должна быть от {self.MIN_HEIGHT} "
                f"до {self.MAX_HEIGHT} пикселей."
            )

    @classmethod
    def parse(cls, width: str, height: str) -> "WindowSize":
        """Создать размер из строк, введённых пользователем.

        :raises InvalidWindowSizeError: значения не являются целыми
            числами или выходят за допустимые границы.
        """
        try:
            return cls(int(width.strip()), int(height.strip()))
        except ValueError:
            raise InvalidWindowSizeError(
                "Ширина и высота должны быть целыми числами."
            ) from None

    def as_geometry(self) -> str:
        """Строка геометрии в формате tkinter, например ``"480x560"``."""
        return f"{self.width}x{self.height}"


#: Готовые размеры окна, доступные в меню «Настройки».
WINDOW_SIZE_PRESETS: dict[str, WindowSize] = {
    "Маленький (360×420)": WindowSize(360, 420),
    "Средний (480×560)": WindowSize(480, 560),
    "Большой (640×740)": WindowSize(640, 740),
}
