# src/utils/path_utils.py
from pathlib import Path
import shutil

def mirror_directory_structure(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for item in input_path.glob('**/*'):
        if item.is_dir():
            (output_path / item.relative_to(input_path)).mkdir(exist_ok=True)