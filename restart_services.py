import win32service
import win32serviceutil
import time
import smtplib
import traceback
from email.mime.text import MIMEText


def send_email(to, subject, body):
    try:
        # Connect to the email server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('okolichibkay@gmail.com', 'vqevtzouujkqlgkp')

        #create the email message
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = 'okolichibkay@gmail.com'
        message['To'] = 'chibk.okoli@gmail.com'
            
        # Send the email
        server.sendmail('okolichibkay@gmail.com', to, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"failed to send email: {e}")

def rolling_restart(services_file):
    # Read the list of services to be restarted from the file
    with open(services_file, 'r') as f:
        services = [line.strip() for line in f]
    
    
    successful_services = []
    failed_services = []
    
    # Restart each service
    for service in services:
        try:
            win32serviceutil.StopService(service)
    # Delay of 30 seconds before starting the restart process        
            time.sleep(30)
            win32serviceutil.StartService(service)
            print("Service restarted successfully:", service)
            successful_services.append(service)
            #send_email('chibk.okoli@gmail.com', 'Successful Service Restarts', '\n'.join(successful_services))
        except Exception as e:
            # Save the name of the failed service to the list
            print("Error occurred while restarting service:", service, e)
            failed_services.append(service)
            # Write the error to the traceback file
            with open('traceback.txt', 'a') as f:
                f.write(traceback.format_exc())
    
    # If any service failed to restart, wait for 1 minute and try again
    if failed_services:
        time.sleep(60)
        for service in failed_services:
            try:
                win32serviceutil.StopService(service)
                # Delay of 30 seconds before starting the restart process        
                time.sleep(30)
                win32serviceutil.StartService(service)
                print("Service restarted successfully on retry:", service)
                successful_services.append(service)
            except Exception as e:
                # Write the error to the traceback file
                print("Error occurred while restarting service:", service, e)
                with open('traceback.txt', 'a') as f:
                    f.write(traceback.format_exc())
    
    # Update the list of services in the original file
    with open(services_file, 'w') as f:
        f.write('\n'.join(successful_services + failed_services))

    # If any service failed to restart, send an email to the user
    if failed_services:
        with open('failed_services.txt', 'w') as f:
            # Write the names of the failed services to a file
            f.write('\n'.join(failed_services))
        
        # Send an email to the user with the names of the failed services
        send_email('chibk.okoli@gmail.com', 'Failed Services', '\n'.join(failed_services))

    # If any service restarted successfully, send an email to the user
    if successful_services:
        send_email('chibk.okoli@gmail.com', 'Successful Service Restarts', '\n'.join(successful_services))
    


if __name__ == '__main__':
    rolling_restart('services.txt')
