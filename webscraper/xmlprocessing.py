my_file = open("jeuxvideo.xml", "rb")
write_to = open("jeuxvideo-process.xml", "w")

for line in my_file.readlines():
    if "</s>" in line:
        if "<s>" in line:
            if '<utt uid = "2">' not in line :
                print line
                continue
    write_to.write(line)
