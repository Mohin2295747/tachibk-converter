import json
import gzip
import varint
from base64 import b64encode
from argparse import ArgumentParser
from struct import pack
from google.protobuf.json_format import Parse, ParseError

# ✅ Make sure schema_pb2 can be found
import sys
sys.path.insert(0, './manga/proto')
from schema_pb2 import Backup

# Argument setup
parser = ArgumentParser(description="Convert output.json to .tachibk")
parser.add_argument("--input", "-i", required=True, help="Path to JSON backup (e.g., output.json)")
parser.add_argument("--output", "-o", required=True, help="Path to save the .tachibk file")
args = parser.parse_args()

# Re-encode preference values
def bytes_preference(preference_value: dict):
    true_value = preference_value['value']['truevalue']
    ptype = preference_value['value']['type'].split('.')[-1].removesuffix('PreferenceValue')

    if ptype == 'Boolean':
        return b64encode(b'\x08' + (b'\x01' if true_value else b'\x00')).decode()
    elif ptype in ['Int', 'Long']:
        return b64encode(b'\x08' + varint.encode(int(true_value))).decode()
    elif ptype == 'Float':
        return b64encode(b'\r' + pack('f', float(true_value))).decode()
    elif ptype == 'String':
        encoded = true_value.encode('utf-8')
        length = len(encoded)
        return b64encode(b'\n' + length.to_bytes(2, 'little') + encoded).decode()
    elif ptype == 'StringSet':
        new_bytes = b''
        for val in true_value:
            encoded = val.encode('utf-8')
            length = len(encoded)
            new_bytes += b'\n' + length.to_bytes(2, 'little') + encoded
        return b64encode(new_bytes).decode()
    else:
        return ''

# Encode .json to protobuf bytes
def convert_json_to_bytes(path: str) -> bytes:
    with open(path, "r", encoding="utf-8") as f:
        message_dict = json.load(f)

    def needs_encoding(val):
        # If it's already a base64-encoded string (likely ends with '='), skip it
        return not isinstance(val, str) or not val.endswith("=")

    # Encode backupPreferences
    for pref in message_dict.get("backupPreferences", []):
        if needs_encoding(pref["value"]["truevalue"]):
            pref["value"]["truevalue"] = bytes_preference(pref)

    # Encode backupSourcePreferences
    for source in message_dict.get("backupSourcePreferences", []):
        for pref in source.get("prefs", []):
            if needs_encoding(pref["value"]["truevalue"]):
                pref["value"]["truevalue"] = bytes_preference(pref)

    try:
        return Parse(json.dumps(message_dict), Backup()).SerializeToString()
    except ParseError as e:
        print("❌ Invalid JSON backup:", e)
        exit(1)

# Write final .tachibk file
def write_tachibk(message_bytes: bytes, output_path: str):
    with gzip.open(output_path, "wb") as f:
        f.write(message_bytes)
    print(f"✅ Compressed backup written to {output_path}")

# Run
if __name__ == "__main__":
    msg = convert_json_to_bytes(args.input)
    write_tachibk(msg, args.output)