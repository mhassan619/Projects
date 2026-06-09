"""
SmartChatbot – Hassan's AI Assistant (Ollama-backed).

Two ways to use it:
  1. CLI :  python chatbot.py
  2. Web :  imported by app.py (Flask UI)

The original class is preserved with the same private attributes
(`__send`, `__history`, etc.) and a few new public methods
(`send`, `stream`, `get_history`, `clear_history`, `model`)
that the Flask app calls.
"""
import requests
import json
from datetime import datetime


class SmartChatbot:
    def __init__(self, name="Hassan's AI", model="llama3.2"):
        self.name = name
        self.__model = model
        self.__base_url = "http://localhost:11434"
        self.__history = []
        self.__system_prompt = (
            "You are a helpful assistant for Hassan, a CS Student learning "
            "AI Automation Engineering. Keep answers concise and practical. "
            "When explaining code, use simple examples."
        )

    @property
    def model(self):
        return self.__model

    @property
    def base_url(self):
        return self.__base_url

    def __send(self, user_message):
        self.__history.append({"role": "user", "content": user_message})
        try:
            response = requests.post(
                f"{self.__base_url}/api/chat",
                json={
                    "model": self.__model,
                    "messages": [
                        {"role": "system", "content": self.__system_prompt}
                    ] + self.__history,
                    "stream": False,
                },
                timeout=60,
            )
            ai_response = response.json()["message"]["content"]
            self.__history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except requests.exceptions.ConnectionError:
            self.__history.pop()  # don't keep a user msg with no assistant reply
            return "❌ Please start Ollama server:  ollama serve"
        except Exception as e:
            self.__history.pop()
            return f"❌ Error: {e}"


    def send(self, user_message):
        """Send a message and return the full AI reply (non-streaming)."""
        return self.__send(user_message)

    def stream(self, user_message):
        """
        Generator that yields text chunks as Ollama streams them.
        Adds the user + assistant turns to history once the stream is done.
        """
        self.__history.append({"role": "user", "content": user_message})
        full_response = ""
        try:
            with requests.post(
                f"{self.__base_url}/api/chat",
                json={
                    "model": self.__model,
                    "messages": [
                        {"role": "system", "content": self.__system_prompt}
                    ] + self.__history,
                    "stream": True,
                },
                stream=True,
                timeout=60,
            ) as response:
                for line in response.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    piece = chunk.get("message", {}).get("content", "")
                    if piece:
                        full_response += piece
                        yield piece
                    if chunk.get("done"):
                        break
            self.__history.append({"role": "assistant", "content": full_response})
        except requests.exceptions.ConnectionError:
            self.__history.pop()
            yield "❌ Please start Ollama server:  ollama serve"
        except Exception as e:
            self.__history.pop()
            yield f"❌ Error: {e}"

    def get_history(self):
        """Return a copy of the conversation history (safe to send to frontend)."""
        return list(self.__history)

    def clear_history(self):
        self.__history = []

    def save_history(self):
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "bot_name": self.name,
                    "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "conversation": self.__history,
                },
                f,
                indent=4,
                ensure_ascii=False,
            )
        return filename

    def show_history(self):
        if not self.__history:
            print("❌ There is no conversation yet!")
            return
        print(f"\n{'=' * 50}")
        print(" 💬 Conversation History")
        print(f"{'=' * 50}")
        for msg in self.__history:
            role = "You" if msg["role"] == "user" else "AI"
            print(f"\n{role}:\n {msg['content'][:100]}...")

    def run(self):
        print(f"{self.name} - Powered by Ollama")
        print("Commands: 'save', 'history', 'clear', 'quit'")
        print(f"{'-' * 50}")
        while True:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            elif user_input.lower() == "quit":
                print("👋 Allah Hafiz!")
                break
            elif user_input.lower() == "save":
                filename = self.save_history()
                print(f"✅ Chat saved: {filename}")
            elif user_input.lower() == "history":
                self.show_history()
            elif user_input.lower() == "clear":
                self.__history = []
                print("✅ History Cleared!")
            else:
                print("\nAI: ", end="", flush=True)
                response = self.__send(user_input)
                print(response)


if __name__ == "__main__":
    bot = SmartChatbot()
    bot.run()
