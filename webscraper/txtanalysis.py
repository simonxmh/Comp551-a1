with open("analysis.txt","w") as analysis:
    count = {}
    for w in open('FVFC_fre.xml').read().split("<s>"):
        print len(w)

        analysis.write(str(len(w)))
