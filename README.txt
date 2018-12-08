These files are our work for Civil IoT Taiwan competition, including the dashboard showing the result, file connecting to our database, and district data downloaded from government websites.

There are two main functions on our dashboard. The following content records the files each function they needed and how to run the code.

To know the details about exhaust emissions of every company, we have to use cems_api.py to make two tables about SOx and NOx. This helps us select which company we must pay attention to instantly and then we can track on the company we selected. 

To make our dashboard show the analysis result on the map, we have to download the airbox data from the government. Then we use make_towncode.py to distinguish the coordinate from districts to calculate the average of pm25 on every district by pm25_mean.py. The we calculate the amount of cems and factory on every district. So, we can combine airbox data, cems distribution, and factory distribution to show the result on the map, giving an advice on where the government should set more airbox to detect the exhaust emissions.

These files become a project but we can¡¦t provide you with the connection to our databas. So, if you want to use these code, you have to replace the data with the new one.
