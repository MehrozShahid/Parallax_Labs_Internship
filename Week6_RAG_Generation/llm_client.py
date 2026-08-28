import requests

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    LLM_MODEL,
    REQUEST_TIMEOUT
)


def generate_answer(system_prompt, user_prompt):

    # Check if the API key was loaded correctly
    if not OPENROUTER_API_KEY:
        return "ERROR: OpenRouter API key is missing."


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }


    data = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }


    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )


        # Print the status so we can see what OpenRouter returns
        print("Status code:", response.status_code)


        # If there is an error, show OpenRouter's actual message
        if response.status_code != 200:
            print("OpenRouter response:")
            print(response.text)

            return (
                f"ERROR: OpenRouter returned "
                f"status code {response.status_code}"
            )


        # Convert successful response to JSON
        result = response.json()


        # Check that an answer was returned
        if "choices" not in result:
            return "ERROR: Unexpected response from OpenRouter."


        if not result["choices"]:
            return "ERROR: OpenRouter returned no answer."


        answer = result["choices"][0]["message"].get(
            "content"
        )


        if not answer:
            return "ERROR: No answer was returned."


        return answer.strip()


    except requests.exceptions.Timeout:

        return "ERROR: OpenRouter request timed out."


    except requests.exceptions.ConnectionError:

        return "ERROR: Could not connect to OpenRouter."


    except requests.exceptions.RequestException as error:

        return f"ERROR: API request failed: {error}"


    except Exception as error:

        return f"ERROR: Unexpected error: {error}"