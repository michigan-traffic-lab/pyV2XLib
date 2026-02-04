import os
import importlib.util


def load_v2xlib(
    env_var: str = "PYV2XLIB_VENDOR_DIR",
    module_filename: str = "v2xlib.py",
):
    """
    Load vendor-provided v2xlib.py from a directory specified by an environment variable.

    Usage:
        v2xlib = load_v2xlib()
    """
    vendor_dir = os.environ.get(env_var)
    if not vendor_dir:
        raise RuntimeError(
            f"Missing environment variable {env_var}. "
            f"Set it to the folder that contains {module_filename} (and v2xlib.json if needed)."
        )

    module_path = os.path.join(vendor_dir, module_filename)
    if not os.path.isfile(module_path):
        raise FileNotFoundError(f"Vendor module file not found: {module_path}")

    spec = importlib.util.spec_from_file_location("v2xlib_vendor", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to create import spec for: {module_path}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
