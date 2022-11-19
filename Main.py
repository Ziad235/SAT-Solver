import os
from time import sleep

print("Running frontend...")
os.system("python3 Front_End.py")

sleep(4)

print("Running davis putnam...")
os.system("python3 DP_Algo.py")

sleep(4)

print("Running backend...")
os.system("python3 Back_End.py")
