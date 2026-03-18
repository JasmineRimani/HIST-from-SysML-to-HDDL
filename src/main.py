"""Legacy compatibility shim for running HIST from the old entry point."""

from hist.cli import main


if __name__ == "__main__":
    main()
