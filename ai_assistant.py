import requests
import subprocess

class AIAssistant:
    def __init__(self):
        self.current_model = "llama3.2:3b"
        self._setup_llm()
        
    def _setup_llm(self):
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            llama_models = [m["name"] for m in models if "llama" in m["name"].lower()]
            if llama_models:
                self.current_model = self._get_model(llama_models)
            
    def _get_model(self, models: list) -> str:
        for model in models:
            if "llama3.2:3b" in model.lower():
                return model
        return models[0] if models else "llama3.2:3b"
            
    def generate_response(self, question: str, context: str) -> str:
        prompt = f"""You are a helpful assistant. Use ONLY the information provided in the context below to answer the question. Do not say you don't have access to information - the context contains the answer.

CONTEXT:
{context}

QUESTION: {question}

ANSWER (based only on the context above):"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.current_model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        result = response.json()
        return result.get("response", "No response generated.")
            
    def pull_llama3_2_3b(self) -> bool:
        result = subprocess.run(["ollama", "pull", "llama3.2:3b"], 
                              capture_output=True, text=True, timeout=300)
        return result.returncode == 0