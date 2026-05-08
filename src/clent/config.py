import json
from pathlib import Path


config_path = Path(__file__).parent.parent / "settings.json"
with open(config_path, "r") as file:
  settings = json.load(file)
    
    
def config():
  def get_env():
    return settings["env"]
  def get_theme():
    return settings["theme"]
  
  
  return {
    "get_env": get_env,
    "get_theme": get_theme
  }