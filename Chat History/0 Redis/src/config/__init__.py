import os

from dotenv import load_dotenv
from envyaml import EnvYAML

# Load the environment variables from the .env file
_current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(_current_dir, f"../../.env")
load_dotenv(env_file_path)

# Determine the environment (default to 'dev' if not set)
env = os.getenv("ENV").lower()
envs_dir = os.getenv("ENVS_DIR")

# Load the environment variables from the appropriate .env file based on the environment (.e.g. .env.dev, .env.prod)
env_file_path = os.path.join(_current_dir, f"../../{envs_dir}/.env.{env}")
load_dotenv(env_file_path)

CONFIG = EnvYAML(os.path.join(_current_dir, "config.yaml"), strict=False)