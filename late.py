import win32service
import win32serviceutil
import time
import smtplib
import ssl
import traceback


def send_email(to, subject, body):
    try:
        # Connect to the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls() 
        server.ehlo()
        server.login('okolichibkay@gmail.com', 'vqevtzouujkqlgkp')
        
        # Send the email
        message = 'Subject: {}\n\n{}'.format(subject, body)
        server.sendmail('okolichibkay@gmail.com', to, message)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def rolling_restart(services_file):
    # Read the list of services to be restarted from the file
    with open(services_file, 'r') as f:
        services = [line.strip() for line in f]
    
    
    
    failed_services = []
    
    # Restart each service
    for service in services:
        try:
            win32serviceutil.StopService(service)
            # Delay of 30 seconds before starting the restart process        
            time.sleep(30)
            win32serviceutil.StartService(service)
            print("Service restarted successfully:", service)
        except Exception as e:
            # Save the name of the failed service to the list
            print("Error occurred while restarting service:", service, e)
            failed_services.append(service)
            # Write the error to the traceback file
            with open('traceback.txt', 'a') as f:
                f.write(traceback.format_exc())
    
    # If any service failed to restart, send an email to the user
    if failed_services:
        with open('failed_services.txt', 'w') as f:
            # Write the names of the failed services to a file
            f.write('\n'.join(failed_services))
        
        # Send an email to the user with the names of the failed services
        send_email('chibk.okoli@gmail.com', 'Failed Services', '\n'.join(failed_services))


if __name__ == '__main__':
    rolling_restart('services.txt')
