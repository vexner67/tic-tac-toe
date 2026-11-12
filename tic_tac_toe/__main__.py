"""Запуск приложения: ``python -m tic_tac_toe``."""

import logging
import sys

from tic_tac_toe.app import run


def main() -> int:
    """Запустить игру; вернуть код завершения процесса."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        run()
    except KeyboardInterrupt:
        return 0
    except Exception:  # noqa: BLE001 — последний рубеж защиты при запуске
        logging.exception("Не удалось запустить приложение")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
