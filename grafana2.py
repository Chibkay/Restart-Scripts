import subprocess

def restart_grafana():
    try:
        print('Stopping Grafana container...')
        subprocess.call(["docker", "stop", "grafana"])
        print('Grafana container stopped successfully')
        print('Starting Grafana container...')
        subprocess.call(["docker", "start", "grafana"])
        print('Grafana container started successfully')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while restarting Grafana container : {e}')

if __name__ == '__main__':
    restart_grafana()
