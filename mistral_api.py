import requests

class MistralChat:
    def __init__(self, api_key, system_prompt):
        self.api_key = api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        # Initial system message
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def send(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        #   Keep only system + last 4 non-system messages
        system = self.messages[0]
        trimmed = self.messages[1:][-4:]
        self.messages = [system] + trimmed
    
        payload = {
            "model": "mistral-tiny-2407",
            "messages": self.messages
        }
    
        response = requests.post(self.url, headers=self.headers, json=payload)
    
        # Print status code and raw response for debugging
        if response.status_code != 200:
            print("HTTP ERROR:", response.status_code)
            print("Response:", response.text)
            raise RuntimeError("Mistral API request failed.")
    
        data = response.json()
    
	    # If 'choices' is missing, print the full res   ponse
        if "choices" not in data:
            print("API ERROR RESPONSE:", data)
            raise RuntimeError("Missing 'choices' in response.")
    
        reply = data["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    chat = MistralChat(
        api_key=os.getenv("MISTRAL_API_KEY"),
        system_prompt="You are a helpful AI assistant."
    )

    print(chat.send("Tell me a short story."))
    print(chat.send("Summarize it."))
    print(chat.send("Continue."))
    print(chat.send("Make it funny."))
    print(chat.send("Give a title."))
