import os
import platform
import subprocess
from time import time

def get_project_root():
    return os.path.dirname(os.path.abspath(__file__))

def install_packages():
    try:
        subprocess.run(["pip", "--version"], check=True)
        try:
            subprocess.run(["python", "-m", "venv", ".venv"], check=True)
            try:
                if platform.system() == "Windows":
                    subprocess.run(["source", ".venv\\Scripts\\activate"], check=True)
                else:
                    subprocess.run(["source", ".venv/bin/activate"], check=True)
                try:
                    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
                except subprocess.CalledProcessError:
                    print("Failed to install packages from requirements.txt. Please check your internet connection or try installing them manually.")
                    return
            except subprocess.CalledProcessError:
                print("Failed to activate virtual environment. Please ensure you have the required permissions or try activating it manually.")
                return
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment. Please ensure you have the required permissions or try creating it manually.")
            return
    except subprocess.CalledProcessError:
        print("pip is not installed. Please install pip and try again.")
        return

def clone_and_install_openwa():
    try:
        subprocess.run(["git", "clone", "https://github.com/rmyndharis/OpenWA.git"], check=True)
        try:
            subprocess.run(["cd", "OpenWA"], check=True)
            try:
                subprocess.run(["npm", "install"], check=True)
                try:
                    subprocess.run(["npm", "run", "dev"], check=True)
                except subprocess.CalledProcessError:
                    print("Failed to build OpenWA.")
                    return
            except subprocess.CalledProcessError:
                print("Failed to install OpenWA dependencies. Please ensure you have Node.js and npm installed.")
                return
        except subprocess.CalledProcessError:
            print("Failed to change directory to OpenWA.")
            return
    except subprocess.CalledProcessError:
        print("Failed to clone OpenWA repository.")
        return

#open openwa dashboard in browser ->default url is http://localhost:2886
def copy_api_key_and_open_openwa_dashboard():
    try:
        subprocess.run(["cd", "data"], check=True)
        try: 
            if platform.system() == "Windows":
                subprocess.run("echo $(head -n 1 .api-key) | clip", shell=True, check=True)
                print("API key copied to clipboard.")

            elif platform.system() == "Linux":
                subprocess.run("echo $(head -n 1 .api-key) | xclip -sel clip", shell=True, check=True)
                print("API key copied to clipboard.")

            else:
                subprocess.run("echo $(head -n 1 .api-key) | pbcopy", shell=True, check=True)
                print("API key copied to clipboard.")
        except subprocess.CalledProcessError:
            print("Failed to copy API key to clipboard.")
            return
    except subprocess.CalledProcessError:
        print("Failed to change directory to data.")
        return
    print("Opening OpenWA dashboard in browser in 10 seconds...")
    print("Please paste the API key in the OpenWA dashboard and connect a WhatsApp account.")
    time.sleep(10)
    import webbrowser
    webbrowser.open("http://localhost:2886")
def install_freellmapi():
    try:
        subprocess.run(["git", "clone", "https://github.com/tashfeenahmed/freellmapi.git"], check=True)
        try:
            subprocess.run(["cd", "freellmapi"], check=True)
            try:
                subprocess.run(["npm", "install"], check=True)
                try:
                    subprocess.run(["cp", ".env.example", ".env"], check=True)
                    try:
                        subprocess.run('ENCRYPTION_KEY="$(node -e \'console.log(require("crypto").randomBytes(32).toString("hex"))\')"', shell=True, check=True)
                        try:
                            subprocess.run('printf "ENCRYPTION_KEY=%s\\nPORT=3001\\n" "$ENCRYPTION_KEY" > .env', shell=True, check=True)
                            try:
                                subprocess.run(["npm", "run", "dev"], check=True)
                            except subprocess.CalledProcessError:
                                print("Failed to start freellmapi server.")
                                return
                        except subprocess.CalledProcessError:
                            print("Failed to set ENCRYPTION_KEY in .env.")
                            return
                    except subprocess.CalledProcessError:
                        print("Failed to generate ENCRYPTION_KEY for freellmapi.")
                        return
                except subprocess.CalledProcessError:
                    print("Failed to copy .env.example to .env in freellmapi.")
                    return
            except subprocess.CalledProcessError:
                print("Failed to install freellmapi dependencies. Please ensure you have Node.js and npm installed.")
                return
        except subprocess.CalledProcessError:
            print("Failed to change directory to freellmapi.")
            return
    except subprocess.CalledProcessError:
        print("Failed to clone freellmapi repository.")
        return

def setup_environment():
    if not os.path.exists(".env"):
        print(".env file not found. Please create a .env file with the required environment variables.")
        return

    from dotenv import load_dotenv
    load_dotenv()

    #check if all required env variables are set
    required_env_vars = ["OPENWA_API_KEY", "OPENWA_API_BASE_URL", "POSTGRES_URL", "MONGO_CONNECTION_STRING", "OPENAI_API_KEY", "LLM_BASE_URL"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}. Please set them in the .env file.")
        return
    #set env variables
    os.environ["OPENWA_API_KEY"] = os.getenv("OPENWA_API_KEY")
    os.environ["OPENWA_API_BASE_URL"] = os.getenv("OPENWA_API_BASE_URL")
    os.environ["POSTGRES_URL"] = os.getenv("POSTGRES_URL")
    os.environ["MONGO_CONNECTION_STRING"] = os.getenv("MONGO_CONNECTION_STRING")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LLM_BASE_URL"] = os.getenv("LLM_BASE_URL")
    os.environ["MODE"] = "development"

def setup_db():
    try:
        if platform.system() == "Windows":
            subprocess.run(["python", "-m", "database.setup_db"], check=True)
        else:
            subprocess.run(["python3", "-m", "database.setup_db"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to setup database.")
        return

def main():
    project_root = get_project_root()
    install_packages()
    clone_and_install_openwa()
    copy_api_key_and_open_openwa_dashboard()
    os.chdir(project_root)
    install_freellmapi()
    os.chdir(project_root)
    setup_db()
    setup_environment()
    print("Server setup completed successfully.")