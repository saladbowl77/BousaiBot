import time
import json

import getNewest

while True:
    earthquakeData = getNewest.getEarthquakeData()

    time.sleep(30)