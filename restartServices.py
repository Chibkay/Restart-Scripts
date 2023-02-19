import win32service
import win32serviceutil
import win32event
import win32api
import servicemanager
import time
import sys

class RollingRestartService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RollingRestartService"
    _svc_display_name_ = "Rolling Restart Service"
    _svc_description_ = "A service to perform a rolling restart of another Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False
        self.service_to_restart = args[0]
        self.num_servers = int(args[1])

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
            for i in range(self.num_servers):
                try:
                    win32serviceutil.RestartService(self.service_to_restart)
                    time.sleep(60)
                except Exception as e:
                    servicemanager.LogErrorMsg(f'Error occurred while restarting the service: {e}')
            if self.stop_requested:
                break

if __name__ == '__main__':
    if len(sys.argv) == 3:
        RollingRestartService([sys.argv[1], sys.argv[2]])
        win32serviceutil.HandleCommandLine(RollingRestartService)
    else:
        print("Please provide the name of the service to restart and the number of servers as arguments.")
