import os
import re

# Folder containing your episode files
folder = "V:\\TV_SERIES02\\Babylon 5 S01-S05 (1993-) + Movies + Crusade (1999-)\\Babylon 5 S03 (360p re-webrip)"

# Regex pattern
pattern = re.compile(r'^(.*) - (\d+)x(\d+) - (.*)$')

for filename in os.listdir(folder):
    match = pattern.match(filename)
    if match:
        show, season, episode, title = match.groups()
        new_name = f"{show} S{int(season):02d}E{int(episode):02d} {title}"
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")