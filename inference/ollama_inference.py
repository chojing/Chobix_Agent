import ollama

class OllamaInference:
    def __init__(self, model_name:str):
        self.model_name = model_name
        pass

    def inference(self, system_prompt, user_prompt):
        response = ollama.chat(model=self.model_name, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ])
        content = response['message']['content']

        return content