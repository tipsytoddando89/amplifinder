#!/usr/bin/env python3
"""
Vercel deployment using the two-step SHA approach:
1. Upload each file individually via POST /v2/files
2. Create deployment referencing files by SHA
"""
import urllib.request
import urllib.error
import json
import os
import time
import hashlib

TOKEN = os.environ.get("VERCEL_TOKEN", "")
TEAM_ID = "team_NkHQ6BnNYuGKi4EPJxRSFAHY"
PROJECT_ROOT = "/Users/toddanderson/Documents/claude projects/amplifinder"

# Files to deploy: (local_path, vercel_path, encoding)
# encoding is "utf-8" for text files, "base64" for binary files
FILES = [
    ("index.html", "index.html", "utf-8"),
    ("datasheets.html", "datasheets.html", "utf-8"),
    ("assests/125.1.png", "assests/125.1.png", "base64"),
    ("assests/[MOS36K] -Perpendicular-1000623.png", "assests/[MOS36K] -Perpendicular-1000623.png", "base64"),
    ("assests/LS sat.1517_LSH80S.png", "assests/LS sat.1517_LSH80S.png", "base64"),
    ("assests/AM5600_LCR_OW_nogrille_old.png", "assests/AM5600_LCR_OW_nogrille_old.png", "base64"),
    ("assests/[D85] 45 Angle-3272.png", "assests/[D85] 45 Angle-3272.png", "base64"),
    ("assests/PP80 angle.png", "assests/PP80 angle.png", "base64"),
    ("assests/ASBR.16192.png", "assests/ASBR.16192.png", "base64"),
    ("assests/OA-PRO_AmpliFINDER_Logo_Vector_Final_08-29-25-TM-04.png", "assests/OA-PRO_AmpliFINDER_Logo_Vector_Final_08-29-25-TM-04.png", "base64"),
    ("assests/ProA1200.4.png", "assests/ProA1200.4.png", "base64"),
    ("assests/[ProA 250.2] Origin-Pro-Amp-0180.png", "assests/[ProA 250.2] Origin-Pro-Amp-0180.png", "base64"),
    ("assests/[ProA 1000.1] Origin-Pro-Amp-0086.png", "assests/[ProA 1000.1] Origin-Pro-Amp-0086.png", "base64"),
    ("assests/[ProA 1000.2] Origin-Pro-Amp-0083.png", "assests/[ProA 1000.2] Origin-Pro-Amp-0083.png", "base64"),
    ("assests/[ProA 1000.4] Origin-Pro-Amp-0083 copy.png", "assests/[ProA 1000.4] Origin-Pro-Amp-0083 copy.png", "base64"),
    ("assests/[ProA 1200.1] Origin-Pro-Amp-0091.png", "assests/[ProA 1200.1] Origin-Pro-Amp-0091.png", "base64"),
    ("assests/[ProA 1200.2] Origin-Pro-Amp-0088.png", "assests/[ProA 1200.2] Origin-Pro-Amp-0088.png", "base64"),
    ("assests/[ProA 125.2] Origin-Pro-Amp-0179.png", "assests/[ProA 125.2] Origin-Pro-Amp-0179.png", "base64"),
    ("assests/[ProA 250.1] Origin-Pro-Amp-0183.png", "assests/[ProA 250.1] Origin-Pro-Amp-0183.png", "base64"),
    ("assests/[ProA125.4] Origin Pro Amp-Front.png", "assests/[ProA125.4] Origin Pro Amp-Front.png", "base64"),
    ("assests/[ProA250.4] Origin Pro Amp-Front.png", "assests/[ProA250.4] Origin Pro Amp-Front.png", "base64"),
    ("assests/logo-architectural.svg", "assests/logo-architectural.svg", "utf-8"),
    ("assests/logo-backcan-speaker.svg", "assests/logo-backcan-speaker.svg", "utf-8"),
    ("assests/logo-design.svg", "assests/logo-design.svg", "utf-8"),
    ("assests/logo-invisible-speaker.svg", "assests/logo-invisible-speaker.svg", "utf-8"),
    ("assests/logo-landscape.svg", "assests/logo-landscape.svg", "utf-8"),
    ("assests/logo-outdoor-speaker.svg", "assests/logo-outdoor-speaker.svg", "utf-8"),
    ("assests/logo-paintable-baffle.svg", "assests/logo-paintable-baffle.svg", "utf-8"),
    ("assests/logo-performance.svg", "assests/logo-performance.svg", "utf-8"),
    ("assests/logo-soundbars.svg", "assests/logo-soundbars.svg", "utf-8"),
    # Landscape speaker product images
    ("assests/LSH40.png", "assests/LSH40.png", "base64"),
    ("assests/LSH60.png", "assests/LSH60.png", "base64"),
    ("assests/LSH80.png", "assests/LSH80.png", "base64"),
    ("assests/[LSR40] Quarter Right-0605.png", "assests/[LSR40] Quarter Right-0605.png", "base64"),
    ("assests/[LSR60] Quarter Right-0687.png", "assests/[LSR60] Quarter Right-0687.png", "base64"),
    ("assests/[LSR80] Quarter Right-0729.png", "assests/[LSR80] Quarter Right-0729.png", "base64"),
    ("assests/ALSB64.png", "assests/ALSB64.png", "base64"),
    ("assests/ALSB85.png", "assests/ALSB85.png", "base64"),
    ("assests/ALSB106.png", "assests/ALSB106.png", "base64"),
    ("assests/LS44_SAT_FRONT.png", "assests/LS44_SAT_FRONT.png", "base64"),
    ("assests/LS64_AnglePhoto_1.png", "assests/LS64_AnglePhoto_1.png", "base64"),
    ("assests/ASM63.png", "assests/ASM63.png", "base64"),
    # Design Centric product images
    ("assests/Blends 602, 802 and 803.png", "assests/Blends 602, 802 and 803.png", "base64"),
    # Performance & Theater product images
    ("assests/ASM6500a.png", "assests/ASM6500a.png", "base64"),
    ("assests/AM3600_Surround_OW_nogrille_new.png", "assests/AM3600_Surround_OW_nogrille_new.png", "base64"),
    ("assests/M2500.404.png", "assests/M2500.404.png", "base64"),
    ("assests/[D89] Front-2875.png", "assests/[D89] Front-2875.png", "base64"),
    ("assests/[D109] Front-2912.png", "assests/[D109] Front-2912.png", "base64"),
    ("assests/AMD10OWSUB_ecomm-2.png", "assests/AMD10OWSUB_ecomm-2.png", "base64"),
    # Soundbar product images
    ("assests/SBR4.png", "assests/SBR4.png", "base64"),
    ("assests/SBR4_Black_Netsuite_02-23-26.png", "assests/SBR4_Black_Netsuite_02-23-26.png", "base64"),
    ("assests/ASBR5.1506 1.png", "assests/ASBR5.1506 1.png", "base64"),
    ("assests/ASBR6.1509 1.png", "assests/ASBR6.1509 1.png", "base64"),
    # Dispersion images
    ("assests/lsr80-disp.png", "assests/lsr80-disp.png", "base64"),
    ("assests/12bpig-disp.png", "assests/12bpig-disp.png", "base64"),
    # PDF datasheets
    ("assests/12HDR-AW-NEW_Datasheet_06-21-23.pdf", "assests/12HDR-AW-NEW_Datasheet_06-21-23.pdf", "base64"),
    ("assests/Amb-Marquee_Official_Datasheet_08-22-25_Rebrand_with-AM650OWA.pdf", "assests/Amb-Marquee_Official_Datasheet_08-22-25_Rebrand_with-AM650OWA.pdf", "base64"),
    ("assests/Ambisonic_10BPIG_Startguide_05-03-24.pdf", "assests/Ambisonic_10BPIG_Startguide_05-03-24.pdf", "base64"),
    ("assests/Ambisonic_10HDR_START_GUIDES_06-04-24.pdf", "assests/Ambisonic_10HDR_START_GUIDES_06-04-24.pdf", "base64"),
    ("assests/Ambisonic_12BPIG_Startguide_05-03-24.pdf", "assests/Ambisonic_12BPIG_Startguide_05-03-24.pdf", "base64"),
    ("assests/DSUB6X2 Datasheet_01-17-25.pdf", "assests/DSUB6X2 Datasheet_01-17-25.pdf", "base64"),
    ("assests/OA_CSUBIW10N_Datasheet_NewFonts_03-19-26.pdf", "assests/OA_CSUBIW10N_Datasheet_NewFonts_03-19-26.pdf", "base64"),
    ("assests/OA_CSUBIW10R EX_Datasheet_NewFonts_03-19-26.pdf", "assests/OA_CSUBIW10R EX_Datasheet_NewFonts_03-19-26.pdf", "base64"),
    ("assests/BlendsCSUB10 Datasheet_10-23-25.pdf", "assests/BlendsCSUB10 Datasheet_10-23-25.pdf", "base64"),
    ("assests/BlendsCSUB10-Datasheet_10-23-25-2.pdf", "assests/BlendsCSUB10-Datasheet_10-23-25-2.pdf", "base64"),
    ("assests/Blends-Speakers_DATASHEET_11-05-25_lowres.pdf", "assests/Blends-Speakers_DATASHEET_11-05-25_lowres.pdf", "base64"),
    ("assests/BLENDSSUB800.pdf", "assests/BLENDSSUB800.pdf", "base64"),
    ("assests/AMD210 data.pdf", "assests/AMD210 data.pdf", "base64"),
    ("assests/ASBR_Ambisonic-Soundbars_Datasheet_10-29-25.pdf", "assests/ASBR_Ambisonic-Soundbars_Datasheet_10-29-25.pdf", "base64"),
]

def sha1_of_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def upload_file(file_bytes: bytes, sha: str) -> bool:
    """Upload a single file to Vercel's file store. Returns True on success (200 or 409=already exists)."""
    url = f"https://api.vercel.com/v2/files?teamId={TEAM_ID}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/octet-stream",
        "x-vercel-digest": sha,
        "Content-Length": str(len(file_bytes)),
    }
    req = urllib.request.Request(url, data=file_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return True  # 200 OK
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return True  # Already uploaded
        err = e.read().decode("utf-8")
        print(f"    Upload error {e.code}: {err}")
        return False

print("=== Vercel Deployment (SHA file upload approach) ===\n")

# Step 1: Read all files, compute SHAs, upload individually
print("Step 1: Reading and uploading files...")
file_refs = []  # list of {"file": vercel_path, "sha": sha, "size": size, "encoding": encoding}

for local_path, vercel_path, encoding in FILES:
    full_path = os.path.join(PROJECT_ROOT, local_path)
    if not os.path.exists(full_path):
        print(f"  SKIP (not found): {local_path}")
        continue

    with open(full_path, "rb") as f:
        file_bytes = f.read()

    sha = sha1_of_bytes(file_bytes)
    size = len(file_bytes)
    print(f"  Uploading: {vercel_path} ({size/1024:.1f} KB, sha={sha[:8]}...)")

    ok = upload_file(file_bytes, sha)
    if ok:
        # Use sha+size format — correct way to reference pre-uploaded files
        file_refs.append({"file": vercel_path, "sha": sha, "size": size})
        print(f"    OK")
    else:
        print(f"    FAILED - skipping")

print(f"\nUploaded {len(file_refs)} files successfully.")

# Step 2: Create deployment referencing files by SHA
print("\nStep 2: Creating deployment...")

deploy_payload = {
    "name": "amplifinder",
    "files": file_refs,
    "projectSettings": {"framework": None},
    "target": "production"
}

payload_bytes = json.dumps(deploy_payload).encode("utf-8")
print(f"Deployment payload size: {len(payload_bytes) / 1024:.1f} KB")

url = f"https://api.vercel.com/v13/deployments?teamId={TEAM_ID}"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

req = urllib.request.Request(url, data=payload_bytes, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    err_body = e.read().decode("utf-8")
    print(f"HTTP Error {e.code}: {e.reason}")
    print(err_body)
    raise

deployment_id = result.get("id")
deployment_url = result.get("url")
print(f"Deployment created: {deployment_id}")
print(f"Initial URL: https://{deployment_url}")

# Step 3: Poll for READY
print("\nStep 3: Polling for READY state...")
poll_url = f"https://api.vercel.com/v13/deployments/{deployment_id}?teamId={TEAM_ID}"
poll_headers = {"Authorization": f"Bearer {TOKEN}"}

for i in range(40):
    time.sleep(5)
    poll_req = urllib.request.Request(poll_url, headers=poll_headers, method="GET")
    try:
        with urllib.request.urlopen(poll_req, timeout=30) as resp:
            poll_result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  Poll error: {e}")
        continue

    state = poll_result.get("readyState") or poll_result.get("state")
    print(f"  [{i+1}] State: {state}")

    if state == "READY":
        aliases = poll_result.get("alias", [])
        final_url = f"https://{aliases[0]}" if aliases else f"https://{deployment_url}"
        print(f"\n=== DEPLOYMENT READY ===")
        print(f"Production URL: {final_url}")
        break
    elif state in ("ERROR", "CANCELED"):
        print(f"\nDeployment failed with state: {state}")
        # Print any error details
        if "errorMessage" in poll_result:
            print(f"Error: {poll_result['errorMessage']}")
        break
else:
    print(f"\nTimed out. Last deployment URL: https://{deployment_url}")
