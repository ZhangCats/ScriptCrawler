import sys

print ("脚本名：", sys.argv[0])

for i in range(1, len(sys.argv)):

    print ("参数", i, sys.argv[i])
    print (type(sys.argv[i]))
