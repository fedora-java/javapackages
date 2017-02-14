try:
    import coverage
    coverage.process_startup()
except ModuleNotFoundError:
    pass
