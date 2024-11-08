# ruff: noqa
import os
from collections.abc import Sequence
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
PRODUCTION_DOTENVS_DIR = BASE_DIR / ".envs" / ".production"
PRODUCTION_DOTENV_FILES = [
    PRODUCTION_DOTENVS_DIR / ".django",
    PRODUCTION_DOTENVS_DIR / ".postgres",
]
DOTENV_FILE = BASE_DIR / ".env"





def merge(output_file: Path, files_to_merge: Sequence[Path]) -> None:
    merged_content = ""

    # Iterate through each file to merge
    for i,  merge_file in enumerate(files_to_merge):
        content = (
            merge_file.read_text().strip()
        )  # Strip unnecessary leading/trailing spaces/newlines
        merged_content += content
        # If it's not the last file, append two newlines to separate them
        merged_content += "\n\n" if i < len(files_to_merge) - 1 else "\n"
    # Write the merged content to the output file
    output_file.write_text(merged_content)


if __name__ == "__main__":
    merge(DOTENV_FILE, PRODUCTION_DOTENV_FILES)
