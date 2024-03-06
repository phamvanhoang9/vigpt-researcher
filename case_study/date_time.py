from datetime import datetime 

"""
This module is used for manipulating dates and times
"""
now = datetime.now()
print(now)

dt = datetime(2024, 3, 5, 15, 30, 00)
print(dt)

formatted = now.strftime('%Y-%m-%d %H:%M:%S')
print(formatted)