import sys
import os

# Add the parent directory of pymongo to sys.path (i.e., site-packages)
pymongo_parent_dir = r'C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\venv\Lib\site-packages'  # For Windows

if pymongo_parent_dir not in sys.path:
    sys.path.append(pymongo_parent_dir)

# Now try importing pymongo
try:
    import pymongo
    from dcc.maya.dcc_context_env import MAYA_SESSION
except ImportError as e:
    print("Error importing pymongo:", e)

