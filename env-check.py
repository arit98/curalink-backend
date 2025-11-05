import os
from dotenv import dotenv_values

env_path = ".env" 
config = dotenv_values(env_path)

print(f"📄 Variables loaded from {env_path}:\n")
if config:
    for key, value in config.items():
        print(f"{key}={value}")
else:
    print("🚨 Error: No variables were loaded. Check if the .env file exists and is readable.")