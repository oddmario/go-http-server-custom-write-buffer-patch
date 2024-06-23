import subprocess
import os
import sys
import pathlib

if os.name == 'nt':
    import pyuac

def find_go_executable():
    goBinaryPath = ""

    if os.name == 'nt':
        cmd = ["where", "go"]
    else:
        cmd = ["which", "go"]

    try:
        go_path = subprocess.check_output(cmd, text=True).strip().splitlines()[0]

        goBinaryPath = pathlib.Path(go_path)
    except (subprocess.CalledProcessError, IndexError):
        pass

    if not goBinaryPath:
        print("Unable to find the path of the `go` binary file. Have you appended it onto your `PATH` environment variable?")
        sys.exit(1)

    return goBinaryPath

def patcher(undo = False):
    # https://github.com/golang/go/issues/13870
    # https://groups.google.com/g/golang-dev/c/OuFtcKEyGrg

    goSrcHttpServerPath = os.path.join(os.path.dirname(find_go_executable()), "..", "src", "net", "http", "server.go")
    
    patches = [
        {
            "file_path": goSrcHttpServerPath,
            "find": 'type Server struct {',
            "replace": 'type Server struct {\n	// WriteBufferSize optionally specifies the buffer size used to write to a connection.\n	// If not set, a default value of 4 KB is used.\n	WriteBufferSize int\n',
        },
        {
            "file_path": goSrcHttpServerPath,
            "find": 'c.bufw = newBufioWriterSize(checkConnErrorWriter{c}, 4<<10)',
            "replace": 'var writeBufferSize int = 4 << 10\n	if c.server.WriteBufferSize != 0 {\n		writeBufferSize = c.server.WriteBufferSize\n	}\nc.bufw = newBufioWriterSize(checkConnErrorWriter{c}, writeBufferSize)\n',
        },
    ]

    isPatching = False

    for patch in patches:
        filePath = patch['file_path']

        with open(filePath, 'r', encoding="utf8") as file:
            filedata = file.read()

        if "WriteBufferSize int" in filedata and undo == False and isPatching == False:
            print("src/net/http/server.go is already patched. Doing nothing.")

            break

        isPatching = True

        if undo == False:
            filedata = filedata.replace(patch['find'], patch['replace'])
        else:
            filedata = filedata.replace(patch['replace'], patch['find'])

        with open(filePath, 'w', encoding="utf8") as file:
            file.write(filedata)

def main():
    patcher()

    # Uncomment the below line and comment the above `patcher()` to undo the patch
    # patcher(True)

    input("Done. Press any key to exit.")

if __name__ == "__main__":
    if os.name == 'nt':
        if not pyuac.isUserAdmin():
            # https://stackoverflow.com/a/19719292/8524395
            print("Re-launching as admin...")
            pyuac.runAsAdmin()
        else:        
            main()
    else:
        main()