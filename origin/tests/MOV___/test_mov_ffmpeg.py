import os

import ffmpeg
import subprocess
from pathlib import Path

img_path = 'X:\\projects\\Small_Rock\\assets\\characters\\red_hulk\\modeling\\publishes\\images\\geometry__red_hulk__red_hulk_MAIN\\characters__red_hulk__red_hulk_MAIN__v0027\\source_jpg\\characters__red_hulk__red_hulk_MAIN__v0027.####.jpg'
out_path = 'X:\\projects\\Small_Rock\\assets\\characters\\red_hulk\\modeling\\publishes\\images\\geometry__red_hulk__red_hulk_MAIN\\characters__red_hulk__red_hulk_MAIN__v0027\\source_jpg\\characters__red_hulk__red_hulk_MAIN__v0027_func.mov'

def images_to_mov(
                  input_path,
                  output_path,
                  fps=24,
                  codec="prores_ks",
                  pix_fmt="yuv422p10le"):
    conform_input_path = None

    if not isinstance(input_path, Path):
        conform_input_path = Path(input_path).as_posix()

    ffmpeg_conform_path = hash_to_ffmpeg_patern(str(conform_input_path))

    if not isinstance(output_path, Path):
        conform_output_path = Path(output_path).as_posix()


    (
        ffmpeg.input(ffmpeg_conform_path,
                     framerate=fps,
                     start_number='1001').output(
            conform_output_path,
            vcodec=codec,
            pix_fmt=pix_fmt,
            r=fps,
            movflags="faststart"
        )
        .overwrite_output().run()
    )

def hash_to_ffmpeg_patern(path):
    if "####" in path:
        count = path.count("#")
        return path.replace('#' * count, f'%0{count}d')
    return path


images_to_mov(input_path=str(img_path), output_path=out_path)