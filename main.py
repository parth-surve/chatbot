# # import os
# # from dotenv import load_dotenv
# # from groq import Groq

# # # 1. Load credentials securely from .env
# # load_dotenv()
# # api_key = os.getenv("GROQ_API_KEY")
# # if not api_key:
# #     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# # # 2. Initialize the official SDK client
# # client = Groq(api_key=api_key)
# # model = "openai/gpt-oss-20b"

# # # 3. Construct the raw JSON message payload
# # messages = [
# #     {"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."},
# #     {"role": "user", "content": "Explain what an API is in one simple sentence."},
# # ]

# # # 4. Invoke the model synchronously
# # response = client.chat.completions.create(model=model, messages=messages)
# # answer = response.choices[0].message.content
# # print(f"Odyssey: {answer}")

# import os
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# client = Groq(api_key=api_key)
# model = "openai/gpt-oss-20b"

# print("Odyssey AI is ready. Type 'quit' or 'exit' to leave.")

# # Continuous conversational loop
# while True:
#     prompt = input("\nYou: ").strip()

#     # Handle exit conditions
#     if prompt.lower() in {"quit", "exit"}:
#         print("Odyssey: Until next time!")
#         break

#     # Ignore empty submissions
#     if not prompt:
#         continue

#     # Each turn crafts a fresh request (no memory between turns yet)
#     messages = [
#         {"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."},
#         {"role": "user", "content": prompt},
#     ]

#     response = client.chat.completions.create(model=model, messages=messages)
#     answer = response.choices[0].message.content
#     print(f"Odyssey: {answer}")

import os
import groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("Add GROQ_API_KEY to your .env file")

client = groq.Groq(api_key=api_key)
model = "openai/gpt-oss-20b"

# Maintain state in a manual Python list
messages = [{"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."}]

print("Odyssey AI is ready. Type 'quit' to leave.")

while True:
    try:
        prompt = input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nOdyssey: Until next time!")
        break

    if prompt.lower() in {"quit", "exit"}:
        print("Odyssey: Until next time!")
        break
    if not prompt:
        continue

    # Append user turn to in-memory history
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(model=model, messages=messages)
        answer = response.choices[0].message.content or ""
        # Append assistant turn so future turns retain context
        messages.append({"role": "assistant", "content": answer})
        print(f"Odyssey: {answer}")
    except groq.RateLimitError:
        messages.pop()
        print("Odyssey: The service is busy (Rate Limit). Please wait a moment and retry.")
    except groq.APIConnectionError:
        messages.pop()
        print("Odyssey: Network connection failure. Check your internet connection.")
    except groq.APIStatusError as error:
        messages.pop()
        print(f"Odyssey: API returned HTTP status {error.status_code}. Verify your key and model.")