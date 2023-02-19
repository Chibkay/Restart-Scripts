import win32serviceutil
import time

def restart_service(service):
    try:
        win32serviceutil.StopService(service)
        time.sleep(30)
        win32serviceutil.StartService(service)
        print("Service restarted successfully:", service)
    except Exception as e:
        print("Error occurred while restarting service:", service, e)

with open("services.txt") as f:
    services = [line.strip() for line in f]

for service in services:
    restart_service(service)
