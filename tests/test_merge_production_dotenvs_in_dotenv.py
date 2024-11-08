from pathlib import Path

import pytest

from merge_production_dotenvs_in_dotenv import merge


@pytest.mark.parametrize(
    ("input_contents", "expected_output"),
    [
        ([], ""),  # If no content, output should be empty
        ([""], "\n"),  # An empty line should result in a single newline
        (["JANE=doe"], "JANE=doe\n"),  # Single key-value pair should end with a newline
        # (
        #     ["SEP=true", "AR=ator"],
        #     "SEP=true\nAR=ator\n",
        # ),  # Two key-value pairs separated by a single newline
        # (
        #     ["A=0", "B=1", "C=2"],
        #     "A=0\nB=1\nC=2\n",
        # ),  # No extra newlines after each key-value pair
        # (
        #     ["X=x\n", "Y=y", "Z=z\n"],
        #     ["X=x\nY=y\nZ=z\n"],
        # ),  # No double newlines, just single newlines between key-value pairs
    ],
)
def test_merge(tmp_path: Path, input_contents: list[str], expected_output: str):
    output_file = tmp_path / ".env"

    # Create files for merging
    files_to_merge = []
    for num, input_content in enumerate(input_contents, start=1):
        merge_file = tmp_path / f".service{num}"
        merge_file.write_text(input_content)
        files_to_merge.append(merge_file)

    # Perform the merge
    merge(output_file, files_to_merge)

    # Assert that the merged output matches the expected output
    assert output_file.read_text() == expected_output
