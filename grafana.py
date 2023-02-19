import subprocess

def restart_grafana():
    try:
        print('Stopping Grafana service...')
        subprocess.call(["net", "stop", "grafana-server"])
        print('Grafana service stopped successfully')
        print('Starting Grafana service...')
        subprocess.call(["net", "start", "grafana-server"])
        print('Grafana service started successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while restarting Grafana service : {e}')

if __name__ == '__main__':
    restart_grafana()
