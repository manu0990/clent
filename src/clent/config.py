import json
from pathlib import Path


config_path = Path(__file__).parent / "settings.json"
with open(config_path, "r") as file:
  settings = json.load(file)
    

def get_theme():
  return settings["theme"]


def get_api_key():
  api_key = settings["env"]["CLENT_API_KEY"].strip()

  if api_key:
    return api_key
  else:
    raise ValueError("API key is not set. Please set the CLENT_API_KEY in settings.json.")


def get_model_name() -> str:
  model_name = settings["env"]["CLENT_MODEL"].strip()
   
  if model_name:
    return model_name
  else:
    raise ValueError("Model name is not set. Please set the CLENT_MODEL in settings.json.")


def get_base_url() -> str:
  base_url =  settings["env"]["CLENT_BASE_URL"].strip()
  
  return base_url or None


def get_temperature() -> float:
  return float(settings["env"]["CLENT_TEMPERATURE"])


def get_max_token() -> int:
  return int(settings["env"]["CLENT_MAX_TOKENS"])
