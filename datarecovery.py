import os

drive = "\\\\.\\C:"
fileD = open(drive, "rb")
size = 512
byte = fileD.read(size)
offs = 0
drec = False
rcvd = 0

# Correct folder path
output_folder = r"C:\Users\Sumaee\Pictures\recover"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"==== Created folder: {output_folder} ====")
else:
    print(f"==== Folder already exists: {output_folder} ====")

print(f"==== Files will be saved to: {output_folder} ====")

jpeg_signatures = [
    b'\xff\xd8\xff\xe0',
    b'\xff\xd8\xff\xe1',
    b'\xff\xd8\xff\xe2',
    b'\xff\xd8\xff\xdb',
    b'\xff\xd8\xff\xee',
]

print("==== Scanning C drive... ====")

while byte:
    if offs % 100000 == 0:
        gb_scanned = (offs * size) / (1024**3)
        print(f"[Progress] Scanned: {gb_scanned:.2f} GB | Recovered: {rcvd} file(s)")

    found = -1
    for sig in jpeg_signatures:
        idx = byte.find(sig)
        if idx >= 0:
            found = idx
            break

    if found >= 0:
        drec = True
        print('==== Found JPEG at location: ' + str(hex(found+(size*offs))) + ' ====')

        filepath = os.path.join(output_folder, str(rcvd) + '.jpeg')
        fileN = open(filepath, "wb")
        fileN.write(byte[found:])

        while drec:
            byte = fileD.read(size)
            bfind = byte.find(b'\xff\xd9')
            if bfind >= 0:
                fileN.write(byte[:bfind+2])
                fileD.seek((offs+1)*size)
                fileN.close()

                size_kb = os.path.getsize(filepath) / 1024
                print(f'==== Saved: {filepath} ({size_kb:.1f} KB) ====\n')

                drec = False
                rcvd += 1
            else:
                fileN.write(byte)

    byte = fileD.read(size)
    offs += 1

fileD.close()
print(f'\n==== Recovery complete. {rcvd} file(s) recovered to {output_folder} ====')