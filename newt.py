import time
import win32serviceutil
import win32service
import smtplib
import sys
import win32api
import win32event
import servicemanager

class RollingRestartService(win32serviceutil.ServiceFramework):
    _svc_name_ = "RollingRestartService"
    _svc_display_name_ = "Rolling Restart Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.log("init")

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec*1000, True)

    def SvcDoRun(self):
        self.log("svc do run")
        f = open("services.txt", "r")
        services = f.readlines()
        f.close()
        failed_services = []
        for service in services:
            service = service.strip()
            try:
                win32serviceutil.StopService(service)
                self.log("Stopped service %s" % service)
                self.sleep(30)
                win32serviceutil.StartService(service)
                self.log("Started service %s" % service)
            except Exception as e:
                self.log("Failed to restart service %s: %s" % (service, e))
                failed_services.append(service)
        if failed_services:
            f = open("failed_services.txt", "w")
            for service in failed_services:
                f.write(service + "\n")
            f.close()
            self.send_email_notification(failed_services)

    def send_email_notification(self, failed_services):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("okolichibkay@gmail.com", "#Chibkay24")
        msg = "The following services failed to restart:\n"
        for service in failed_services:
            msg += service + "\n"
        server.sendmail("okolichibkay@gmail.com", "chibk.okoli@gmail.com", msg)
        server.quit()

    def SvcStop(self):
        self.log("svc do stop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(RollingRestartService)
