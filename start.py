import win32service
import win32serviceutil
import win32event
import win32api
import servicemanager
import time
import sys

class RestartService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RestartService"
    _svc_display_name_ = "Restart Service"
    _svc_description_ = "A service to automatically restart another Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False
        self.service_to_restart = args[0]

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        while True:
            try:
                win32serviceutil.RestartService(self.service_to_restart)
                time.sleep(60)
            except Exception as e:
                servicemanager.LogErrorMsg(f'Error occurred while restarting the service: {e}')
            if self.stop_requested:
                break

if __name__ == '__main__':
    if len(sys.argv) == 2:
        RestartService([sys.argv[1]])
        win32serviceutil.HandleCommandLine(RestartService)
    else:
        print("Please provide the name of the service to restart as an argument.")
