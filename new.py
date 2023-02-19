import time
import win32service
import win32serviceutil
import sys

class RollingRestartService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RollingRestartService"
    _svc_display_name_ = "Rolling Restart Service"
    _svc_description_ = "Service to perform rolling restart of another service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

    def SvcDoRun(self):
        import servicemanager
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )

        # Read target service name from command line argument
        target_service = sys.argv[1]

        # Read time to wait between restarts from command line argument
        wait_time = int(sys.argv[2])

        while True:
            try:
                # Stop the target service
                win32serviceutil.StopService(target_service)
                self.logger.info("Stopped service: %s", target_service)

                # Start the target service
                win32serviceutil.StartService(target_service)
                self.logger.info("Started service: %s", target_service)

                # Wait for a specified time before performing the next restart
                time.sleep(wait_time)
                
            except Exception as e:
                self.logger.error("Error during rolling restart: %s", str(e))
                # Wait for a specified time before attempting the restart again
                time.sleep(60)

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(RollingRestartService)
