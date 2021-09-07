import sys
import csv



def write_csv(argv):
    fName=argv[1]
    min=int(argv[2])
    max=int(argv[3])
    fp=open(fName,'w',encoding='utf-8',newline="")
    csvwriter=csv.writer(fp)
    csvwriter.writerow(["name","type","token"])
    
    for i in range(min,max,1):
        device = "device" + str(i)
        token  = "token" + str(i)
        csvwriter.writerow([device, "default", token])
    fp.close()



if __name__ == "__main__":
       write_csv(sys.argv)
