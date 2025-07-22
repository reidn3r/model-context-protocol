from dotenv import load_dotenv
import os
load_dotenv() 

envsConfig = {
  "GEMINI_KEY": os.environ.get('GEMINI_API_KEY'),
  "GEMINI_MODEL": os.environ.get('GEMINI_MODEL'),
}