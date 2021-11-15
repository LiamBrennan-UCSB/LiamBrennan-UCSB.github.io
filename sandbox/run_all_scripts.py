import os 
import sys 

PERCENT = sys.argv[2]
INTERVAL_DAYS = sys.argv[1]

os.system(f"python generateClassificationSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")
os.system(f"python generatePredictionSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")
os.system(f"python generatePerformanceSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")