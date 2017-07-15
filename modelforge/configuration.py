import importlib.util
import os
import traceback


VENDOR = os.getenv("MODELFORGE_VENDOR", None)
BACKEND = os.getenv("MODELFORGE_BACKEND", None)
BACKEND_ARGS = os.getenv("MODELFORGE_BACKEND_ARGS", "")

OVERRIDE_FILE = "modelforgecfg.py"


def refresh():
    override_files = [
        os.path.join(os.path.dirname(stack.filename), OVERRIDE_FILE)
        for stack in traceback.extract_stack()] + [OVERRIDE_FILE]

    for override_file in override_files:
        if not os.path.isfile(override_file):
            continue
        spec = importlib.util.spec_from_file_location(__name__, override_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        globals().update({n: getattr(module, n) for n in dir(module)
                          if not n.startswith("__")})

refresh()