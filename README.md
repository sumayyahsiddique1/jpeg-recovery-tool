# JPEG File Recovery Tool

A low-level **disk forensics and file carving** tool written in Python that recovers deleted or lost JPEG images by scanning raw disk sectors for JPEG file signatures.

> **Educational Purpose Only** — This tool is intended for cybersecurity learning, digital forensics study, and data recovery on drives you own. Do not use on systems without explicit permission.

---

## Sample Output

![Recovered JPEG files shown in Windows Explorer](recovered_sample.png)

*Screenshot showing recovered JPEG files — handwritten notes, wallpapers, and application icons successfully carved from raw disk data.*

---

## How It Works

This tool performs **file carving** — a classic digital forensics technique that recovers files from raw disk data without relying on the filesystem (FAT, NTFS, etc.).

### Core Concept: JPEG Signature Detection

Every JPEG file starts and ends with known magic bytes:

| Marker | Hex Bytes | Meaning |
|--------|-----------|---------|
| **SOI** (Start of Image) | `FF D8 FF` | Beginning of a JPEG |
| **EOI** (End of Image) | `FF D9` | End of a JPEG |

The tool reads the disk **512 bytes at a time** (one sector), scans for any of these SOI signatures:

```
FF D8 FF E0  → JFIF format
FF D8 FF E1  → EXIF format (camera photos)
FF D8 FF E2  → ICC profile
FF D8 FF DB  → Quantization table
FF D8 FF EE  → Adobe format
```

When a signature is found, it **writes bytes to a new file** until it hits `FF D9` (end marker), then saves and moves on.

### Flow Diagram

```
Open Raw Disk (\\.\C:)
        │
        ▼
Read 512-byte sector
        │
        ▼
Scan for JPEG header (FF D8 FF E*)
        │
    Found? ──Yes──► Open new .jpeg file
        │                   │
       No                   ▼
        │            Keep reading sectors
        │            and writing to file
        ▼                   │
  Next sector         Found FF D9?
        ▲               │
        └──────No────────┘
                    │
                   Yes
                    │
                    ▼
             Close file, save to disk
             Continue scanning...
```

---

## Requirements

- **OS:** Windows (uses `\\.\C:` raw disk access)
- **Python:** 3.x
- **Privileges:** Must be run as **Administrator**

---

## Usage

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/jpeg-recovery-tool.git
cd jpeg-recovery-tool
```

### 2. Edit the output folder path
Open `datarecovery.py` and change the output folder to your desired path:
```python
output_folder = r"C:\Users\YourUsername\Pictures\recover"
```

### 3. Change the target drive (optional)
```python
drive = "\\\\.\\C:"  # Change C: to D:, E:, etc.
```

### 4. Run as Administrator
```bash
# Right-click CMD → "Run as Administrator", then:
python datarecovery.py
```

### 5. Watch the output
```
==== Scanning C drive... ====
[Progress] Scanned: 0.05 GB | Recovered: 0 file(s)
==== Found JPEG at location: 0x1a3f200 ====
==== Saved: C:\Users\...\recover\0.jpeg (84.3 KB) ====

[Progress] Scanned: 0.10 GB | Recovered: 1 file(s)
...
==== Recovery complete. 9694 file(s) recovered ====
```

---

## Project Structure

```
jpeg-recovery-tool/
│
├── datarecovery.py       # Main recovery script
├── recovered_sample.png  # Sample screenshot of recovered files
└── README.md             # This file
```

---

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `drive` | `\\.\C:` | Raw disk path to scan |
| `size` | `512` | Sector size in bytes |
| `output_folder` | `C:\Users\Sumaee\Pictures\recover` | Where recovered files are saved |

---

## Cybersecurity Concepts Covered

This project is a hands-on introduction to several key **digital forensics** and **cybersecurity** concepts:

| Concept | Description |
|---------|-------------|
| **File Carving** | Recovering files from raw disk without filesystem metadata |
| **Magic Bytes / File Signatures** | Using hex headers to identify file types |
| **Raw Disk Access** | Bypassing the OS filesystem layer entirely |
| **Sector-by-Sector Scanning** | How data is physically stored on disk |
| **Deleted File Recovery** | Why "deleted" files often still exist on disk |
| **Digital Forensics** | Foundational technique used in real-world investigations |

---

## Limitations & Known Issues

- **Windows only** — uses `\\.\DriveLetter:` syntax for raw access
- **Slow on large drives** — scans every single sector (512 bytes at a time)
- **Partial files** — if a file was overwritten mid-way, recovery may be incomplete
- **False positives** — some recovered files may be corrupt or incomplete
- **Requires Admin rights** — raw disk access is a privileged operation

---

## Possible Improvements

Add support for PNG, PDF, DOCX signatures
Multi-threaded scanning for speed
Linux/macOS support (`/dev/sda` style paths)
GUI interface using Tkinter or PyQt
Skip already-recovered sectors (journal/checkpoint file)
Validate recovered files using PIL/Pillow before saving

---

## Learning Resources

- [File Signature Database (Gary Kessler)](https://www.garykessler.net/library/file_sigs.html)
- [The Sleuth Kit — Open Source Forensics](https://www.sleuthkit.org/)
- [Autopsy Forensics Browser](https://www.autopsy.com/)
- [NIST Digital Forensics Tools](https://www.nist.gov/programs-projects/digital-forensics)

---

## License

This project is released for **educational and research purposes only**.  
Use responsibly and only on systems you own or have explicit permission to analyze.

---

*Built as part of a cybersecurity learning journey — exploring how deleted data persists and how forensic tools recover it.*
