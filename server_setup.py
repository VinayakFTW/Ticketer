import subprocess
import platform

from schemas.postgredb_schema import Base, Engine
from schemas.postgredb_schema import User, Ticket

try:
    subprocess.run("python --version", shell=True, check=True)
    try:
        subprocess.run("uv --version", shell=True, check=True)
        try:
            subprocess.run("uv install", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("package installation failed. Please install packages manually.")
    except subprocess.CalledProcessError:
            print("uv is not installed. Installing uv...")
            if platform.system() == "Windows":
                subprocess.run('powershell -c "irm https://astral.sh | iex"', shell=True, check=True)
                try:
                    subprocess.run("uv install", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print("uv installation failed. Please install uv manually.")
            else:
                subprocess.run("curl -sSL https://astral.sh | sh", shell=True, check=True)
                try:
                    subprocess.run("uv install", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print("package installation failed. Please install packages manually.")
except subprocess.CalledProcessError:
    print("installing python...")
    if platform.system() == "Windows":
        try:
            subprocess.run('powershell -c "irm https://astral.sh | iex"', shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Failed to install uv. Please install uv manually.")
    else:
        try:
            subprocess.run("curl -sSL https://astral.sh | sh", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Failed to install uv. Please install uv manually.")
    try:
        subprocess.run("uv python install 3.14 --default", shell=True, check=True)
        try:
            subprocess.run("uv install", shell=True, check=True)
            print("setup completed successfully.")
        except subprocess.CalledProcessError:
                print("package installation failed. Please install packages manually.")
    except subprocess.CalledProcessError:
        print("python installation failed. Please install python manually.")

Base.metadata.create_all(Engine)

print("Database tables created successfully.")
