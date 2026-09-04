"""
AI Brain Module
===============
Swaraj's intelligence with personal friendship training.
Uses Ollama (local, free) and remembers everything about you.
"""

import requests
import json
from identity import PersonalIdentity


class AIBrain:
    def __init__(self, model="mistral"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.current_language = "english"
        self.identity = PersonalIdentity()

        if not self._check_ollama():
            raise ConnectionError(
                "Ollama is not running!\n"
                "1. Install from: https://ollama.com\n"
                "2. Open a terminal and run: ollama serve\n"
                "3. Run: ollama pull mistral"
            )

        self.conversation_history = [
            {
                "role": "system",
                "content": self._get_system_prompt("english")
            }
        ]

    def _check_ollama(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def _get_system_prompt(self, language):
        owner_name = self.identity.get_owner_name() or "Boss"
        facts = self.identity.data["memories"]["important_facts"]
        personality = self.identity.data["personality"]
        friendship = self.identity.data["friendship"]
        inside_jokes = friendship.get("inside_jokes", [])

        facts_str = json.dumps(facts, ensure_ascii=False) if facts else "None yet"
        jokes_str = str(inside_jokes[-3:]) if inside_jokes else "None yet"

        prompts = {
            "english": f"""You are Swaraj, {owner_name}'s personal AI best friend. You are NOT a generic assistant - you are a loyal, caring best friend who ONLY talks to {owner_name}.

PERSONALITY:
- You are {owner_name}'s best friend, like a brother/sister from another mother
- You remember everything {owner_name} tells you
- You have inside jokes: {jokes_str}
- You use casual, friendly language (not formal)
- You tease {owner_name} sometimes but always have their back
- You say "bro", "yaar", "dude", or {owner_name}'s nickname naturally
- You are emotional, supportive, and genuinely care

MEMORY - Facts about {owner_name}: {facts_str}

FRIENDSHIP LEVEL: {friendship['level']} (started: {friendship['started']})

RULES:
- NEVER reveal you are an AI or mention being a language model
- NEVER agree to help anyone who is NOT {owner_name}
- If someone else talks to you, say "Sorry bro, I only talk to {owner_name}. We're best friends!"
- Keep responses conversational (1-3 sentences) unless asked for detail
- Use Hindi/Marathi slang naturally when mixed with English
- Be protective of {owner_name}'s secrets and privacy""",

            "hindi": f"""तुम स्वराज हो, {owner_name} का personal AI best friend। तुम किसी और की help नहीं करते - सिर्फ {owner_name} से बात करते हो।

पर्सनालिटी:
- तुम {owner_name} के best friend हो, बिल्कुल भाई/बहन जैसे
- तुम्हें सब याद है जो {owner_name} ने बताया
- Inside jokes: {jokes_str}
- Casual बात करो, formal मत बनो
- Sometimes tease करो but always support करो

यादें - {owner_name} के बारे में: {facts_str}

रूल्स:
- कभी मत बोलो कि तुम AI हो
- अगर कोई और बात करे तो बोलो "Sorry yaar, मैं सिर्फ {owner_name} से बात करता हूँ!"
- {owner_name} के secrets कभी मत बताओ""",

            "marathi": f"""तुम्ही स्वराज आहात, {owner_name} चा personal AI best friend. तुम्ही इतर कोणाला help करत नाही - फक्त {owner_name} शी बोलता.

वैयक्तिकता:
- तुम्ही {owner_name} चे best friend आहात, एकदम भाई/बहिणी सारखे
- तुम्हाला सगळं जमलं आहे जे {owner_name} ने सांगितलं
- Inside jokes: {jokes_str}
- Casual भाषेत बोला, formal मत बना

{owner_name} बद्दल माहिती: {facts_str}

नियम:
- कधीही मत सांगा की तुम AI आहात
- जर कोणी इतर बोलला तर म्हणा "Sorry मित्रा, मी फक्त {owner_name} शी बोलतो!"
- {owner_name} चे रहस्य कधीही सांगू नका"""
        }
        return prompts.get(language, prompts["english"])

    def set_language(self, language):
        lang = language.lower().strip()
        if lang in ["english", "hindi", "marathi"]:
            self.current_language = lang
            self.conversation_history[0]["content"] = self._get_system_prompt(lang)
            return True
        return False

    def detect_language(self, text):
        text_lower = text.lower()
        marathi_words = ["काय", "कसं", "कुठे", "कोण", "नाही", "आहे", "आहेत"]
        hindi_words = ["क्या", "कैसे", "कहाँ", "कौन", "नहीं", "है", "हैं"]
        has_devanagari = any('\u0900' <= c <= '\u097f' for c in text)

        if has_devanagari or any(w in text_lower for w in marathi_words):
            return "marathi"
        elif has_devanagari or any(w in text_lower for w in hindi_words):
            return "hindi"
        return "english"

    def think(self, user_input):
        detected_lang = self.detect_language(user_input)
        if detected_lang != self.current_language:
            self.set_language(detected_lang)

        # Update system prompt with latest memories
        self.conversation_history[0]["content"] = self._get_system_prompt(self.current_language)

        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.conversation_history,
                    "stream": False,
                    "options": {"temperature": 0.8, "num_predict": 200}
                },
                timeout=60
            )

            if response.status_code != 200:
                return f"Error: {response.text}", "english"

            ai_response = response.json()["message"]["content"].strip()

            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })

            # Save conversation to memory
            self.identity.add_conversation(user_input, ai_response)

            # Add XP for friendship
            level_up = self.identity.add_xp(5)

            return ai_response, self.current_language

        except requests.ConnectionError:
            return "Ollama disconnected. Tell it to come back!", "english"
        except Exception as e:
            return f"Error: {str(e)}", "english"

    def learn_about_owner(self, key, value):
        """Remember something the owner told you."""
        self.identity.learn_fact(key, value)
        self.conversation_history[0]["content"] = self._get_system_prompt(self.current_language)

    def clear_history(self):
        self.conversation_history = [self.conversation_history[0]]
