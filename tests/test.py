from pathlib import Path

from cfx40_encoder import encode_file

source = Path(__file__).with_name("test.txt")
output_path = Path(__file__).resolve().parent.parent / "output" / "test_output.png"
encode_file(str(source), str(output_path))
print(f"Created: {output_path}")
