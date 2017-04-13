import sys, os
import subprocess as sp
import re


def ourMethod(pathByUser, patchPath):
    command = "(cd /{0} && patch -p0) < {1}".format(pathByUser, patchPath)
    p = sp.Popen(command, stdout=sp.PIPE, shell=True)
    out = p.communicate()[0]
    if out is None:
        out = p.communicate()[1]
    print(out)
    sys.exit(0)


def readPatchFiles(dirPath):
    if dirPath is not None and dirPath != "":
        pathByUser = ""
        patchFiles = [f for f in os.listdir(dirPath) if f.endswith('.patch')]
        for patchFile in patchFiles:
            linePath = ""
            if pathByUser == "":
                with open(os.path.abspath(patchFile), 'r') as f:
                    content = f.read().splitlines()
                if len(content) > 0:
                    index = -1
                    for line in content:
                        index = line.find("---")
                        if index != -1:
                            linePath = re.split(r"\s+", line)[1]
                            pathByUser = raw_input("Enter the path to first dir\n" + linePath)
                            break
                        else:
                            print("Can't find the path in the patch file, skipping!!")
                else:
                    print("empty patch file, skipping!!")
            else :
                ourMethod(pathByUser, os.path.abspath(patchFile))
        print(patchFiles)
    else:
        print("No patch file found in directory.\nExiting...")
        sys.exit(1)


if len(sys.argv) == 2:
    dirPath = sys.argv[1]
    readPatchFiles(dirPath)

else:
    print("Invalid syntax")
    sys.exit(1)
