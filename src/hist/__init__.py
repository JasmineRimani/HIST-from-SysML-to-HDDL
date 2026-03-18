"""HIST package."""


def run_translation(*args, **kwargs):
    from .cli import run_translation as _run_translation

    return _run_translation(*args, **kwargs)


__all__ = ["run_translation"]
