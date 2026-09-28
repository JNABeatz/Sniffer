# Packet Sniffer Toolkit
 
A small, beginner-friendly Python toolkit for capturing network traffic,
labeling the frames you record, and comparing them byte by byte.
 
It is built to help you work out how an undocumented device protocol is
structured: change one setting on the device, capture the traffic, save the
frame under a descriptive name, and see which bytes change.
 
> 🚧 **Work in progress:** this project is under active development.
> Some features are not implemented yet and the API may change.
 
## Features
 
- [x] Save frames with a name to a plain-text file
- [ ] Capture packets to and from a chosen host
- [ ] Load saved frames and compare them byte by byte
## Requirements
 
- Python 3.8 or newer
- [Scapy](https://scapy.net/) (for packet capture)
- **Windows:** [Npcap](https://npcap.com/) installed
- **Linux / macOS:** libpcap (usually already available)
Capturing packets normally needs elevated privileges: run your terminal as
Administrator on Windows, or use `sudo` on Linux / macOS.
 
## Installation
 
```bash
git clone <your-repository-url>
cd <repository-folder>
python -m venv .venv
 
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
 
pip install -r requirements.txt
```
 
## Usage
 
Only the frame-saving module is available for now. Import it from your own
script:
 
```python
from guardar_tramas import guardar_trama
 
# From raw bytes (for example, a captured Scapy packet payload)
guardar_trama("gain_out1_0.1dB", bytes(p[Raw].load))
 
# From a hex string (for example, copied from Wireshark)
guardar_trama("gain_out1_0.2dB", "55 aa 01 03 00 14 5c")
```
 
The hex string can use spaces, colons, dashes or a `0x` prefix; anything that
is not a hexadecimal digit is removed. An odd number of digits raises a
`ValueError`.
 
### Suggested workflow
 
1. Change **one** setting on the device (for example, one gain value).
2. Capture the traffic while you do it.
3. Save the frame with a name that describes the change.
4. Repeat with a different value, channel or parameter.
5. Compare the saved frames to see which bytes change.
Change only one thing per capture, and also record one capture where you
touch nothing, so you can recognize background traffic.
 
### Copying frames from Wireshark
 
Select only the application data (the **Data** field), then use
*Copy → …as a Hex Stream*. The exact menu names can vary between versions.
 
Avoid *Hex Dump* and *C Array*: their extra text (offsets, variable names)
contains characters that look like hex digits and would end up in your saved
frame. Also avoid copying the whole packet, since the Ethernet, IP and
transport headers contain values (MAC addresses, checksums, counters) that
change between captures.
 
## Frame file format
 
Frames are stored in `tramas.txt`, one per line:
 
```
name;hex bytes separated by spaces
```
 
Example (made-up bytes):
 
```
gain_out1_0.1dB;55 aa 01 03 00 0a 5c
gain_out1_0.2dB;55 aa 01 03 00 14 5c
```
 
Semicolons in names are replaced by underscores when saving, because `;` is
the separator. If two lines share a name, tools that read the file should
treat the last one as the current one.
 
## Project structure
 
Planned layout (files marked with ✓ exist):
 
```
├── README.md
├── requirements.txt
├── config.py            # target IP, path to tramas.txt
├── captura.py           # packet capture with Scapy
├── guardar_tramas.py    # ✓ save named frames
├── cargar_tramas.py     # load and compare frames
├── main.py              # ties the pieces together
└── datos/               # captures and saved frames
```
 
Run everything from the repository root so relative paths resolve the same
way for everyone.
 
## Roadmap
 
- [x] Frame saving
- [ ] Packet capture
- [ ] Frame loading and comparison
- [ ] Command-line interface
- [ ] Detect fixed and variable bytes across many frames
## Responsible use
 
Only analyze devices and networks that you own or have permission to test,
and respect the laws and license terms that apply to your case. Do not
commit proprietary manuals, firmware or software from device manufacturers
to this repository.
 
## License
 
Not yet chosen.
 
