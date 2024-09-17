import sys

custom_path = r'C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK'
pymongo_parent_dir = r'C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\venv\Lib\site-packages'  # For Windows

if custom_path not in sys.path:
    sys.path.append(custom_path)

print(sys.path)

if pymongo_parent_dir not in sys.path:
    sys.path.append(pymongo_parent_dir)

try:
    import pymongo
    from pydantic import BaseModel

except ImportError as e:
    print("Error importing pymongo:", e)