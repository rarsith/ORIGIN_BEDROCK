"""
Gaffer preflight checks.

Runs BEFORE Gaffer starts.
Fails fast if the environment is unsafe.
"""

import sys
import os
import pathlib
import platform

# --------------------------------------------------
# Configuration
# --------------------------------------------------

PIPELINE_ROOT = pathlib.Path(
    r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK"
)

PYTHON_SHARED = PIPELINE_ROOT / "origin" / "python_shared"

REQUIRED_PYTHON_MAJOR = 3
GAFFER_EXPECTED_MINOR = 11   # Gaffer uses 3.11
PIPELINE_PYTHON_MINOR = 10   # pipeline venv is 3.10

# --------------------------------------------------
# Helpers
# --------------------------------------------------

def fail(msg: str, code: int = 1):
    print("\n[GAFFER PREFLIGHT ERROR]")
    print(msg)
    print()
    sys.exit(code)


def info(msg: str):
    print(f"[gaffer-preflight] {msg}")


# --------------------------------------------------
# 1. OS sanity check
# --------------------------------------------------

info(f"Platform: {platform.platform()}")

if platform.system() != "Windows":
    fail("Gaffer Windows build expected, but OS is not Windows.")

# --------------------------------------------------
# 2. Pipeline root exists
# --------------------------------------------------

info(f"Pipeline root: {PIPELINE_ROOT}")

if not PIPELINE_ROOT.exists():
    fail(f"Pipeline root does not exist:\n{PIPELINE_ROOT}")

# --------------------------------------------------
# 3. python_shared exists
# --------------------------------------------------

info(f"python_shared: {PYTHON_SHARED}")

if not PYTHON_SHARED.exists():
    fail(f"python_shared folder missing:\n{PYTHON_SHARED}")

# --------------------------------------------------
# 4. Ensure python_shared is pure Python
# --------------------------------------------------

info("Checking for compiled extensions (.pyd)")

compiled = list(PYTHON_SHARED.rglob("*.pyd"))
if compiled:
    msg = "Compiled Python extensions found in python_shared:\n"
    msg += "\n".join(str(p) for p in compiled)
    msg += "\n\nThis is unsafe across Python versions (3.10 -> 3.11)."
    fail(msg)

info("No compiled extensions found")

# --------------------------------------------------
# 5. Sanity-check critical imports using pipeline Python
# --------------------------------------------------

# We intentionally test imports WITHOUT Gaffer
sys.path.insert(0, str(PYTHON_SHARED))

info("Testing pipeline imports")

try:
    import pydantic
except Exception as e:
    fail(f"Failed to import pydantic from python_shared:\n{e}")

try:
    import pymongo
except Exception as e:
    fail(f"Failed to import pymongo from python_shared:\n{e}")

info(f"pydantic version: {getattr(pydantic, 'VERSION', 'unknown')}")
info(f"pymongo version: {getattr(pymongo, 'version', 'unknown')}")

# --------------------------------------------------
# 6. Guard against pydantic v2 (ABI risk)
# --------------------------------------------------

if hasattr(pydantic, "BaseModel"):
    version = getattr(pydantic, "VERSION", "0")
    if version.startswith("2."):
        fail(
            "pydantic v2 detected.\n"
            "pydantic v2 is NOT safe for python_shared across versions.\n"
            "Pin to pydantic<2."
        )

# --------------------------------------------------
# 7. Export environment variables for the .bat file
# --------------------------------------------------
# These prints are OPTIONAL.
# They can be captured by the .bat using a `for /f` loop.

print(f"set PIPELINE_ROOT={PIPELINE_ROOT}")
print(f"set PIPELINE_PYTHON_SHARED={PYTHON_SHARED}")

# --------------------------------------------------
# 8. Final success
# --------------------------------------------------

info("Preflight checks passed")
sys.exit(0)

