import requests
import json
import threading

class AquaBot:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        self.model = "gemma3:4b"  # Using available model
        self.history = []
        self.system_prompt = """You are AquaBot, an expert AI assistant for aquaculture and fish health. 
        Your goal is to help users identify fish species, diagnose diseases, and provide treatment advice.
        Always be helpful, concise, and professional. If you don't know something, admit it.
        Focus on:
        1. Fish disease diagnosis and treatment
        2. Water quality management
        3. Sustainable aquaculture practices
        4. Fish species identification
        """

    def check_status(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def chat(self, user_message):
        """Send message to AI and get response"""
        # Try to check if service is up first with a short timeout
        try:
            requests.get(f"{self.base_url}/tags", timeout=1)
        except:
             return "Note: Local AI service (Ollama) is not running on port 11434. Please start it to chat."

        # Add user message to history
        self.history.append({"role": "user", "content": user_message})
        
        # Prepare context window (keep last 5 messages + system prompt)
        messages = [{"role": "system", "content": self.system_prompt}] + self.history[-5:]

        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=30  # Increased timeout for slower local models
            )
            
            if response.status_code == 200:
                ai_response = response.json().get("message", {}).get("content", "")
                self.history.append({"role": "assistant", "content": ai_response})
                return ai_response
            else:
                return f"Error: AI returned status {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "Error: AI service timed out. It might be loading the model."
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
