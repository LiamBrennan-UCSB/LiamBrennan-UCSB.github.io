import os 

PERCENT = 2
INTERVAL_DAYS = 180

os.system(f"python generateClassificationSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")
os.system(f"python generatePredictionSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")
# os.system(f"python generatePerformanceSpreadsheet.py {INTERVAL_DAYS} {PERCENT}")