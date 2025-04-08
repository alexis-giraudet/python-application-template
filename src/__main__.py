import sys
import os

from textual.demo.demo_app import DemoApp


def main() -> int:
    app = DemoApp()
    app.run()
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
