#!/usr/bin/env python3
"""
Extract individual .zcp speaker preset files from an Origin PRO .zcl library.
Usage: python3 zcl_to_zcp.py <library.zcl> [output_dir]
"""
import sys, os, json, gzip, base64, re

def safe(s):
    return re.sub(r'[^\w\-. ]', '_', s).strip()

def walk(node, parts, out_dir, count):
    name = node.get('name', 'unnamed')
    if 'preset' in node:
        folder = os.path.join(out_dir, *[safe(p) for p in parts])
        os.makedirs(folder, exist_ok=True)
        blob = base64.b64decode(node['preset'])
        with open(os.path.join(folder, safe(name) + '.zcp'), 'wb') as f:
            f.write(blob)
        count[0] += 1
    for c in node.get('children', []):
        walk(c, parts + [name], out_dir, count)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 zcl_to_zcp.py <library.zcl> [output_dir]")
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'zcp_out'
    with gzip.open(src, 'rb') as f:
        data = json.load(f)
    count = [0]
    walk(data, [], out, count)
    print(f"Wrote {count[0]} .zcp files to {out}/")

if __name__ == '__main__':
    main()
