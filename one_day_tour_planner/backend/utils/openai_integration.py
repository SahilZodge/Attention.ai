from transformers import pipeline, set_seed
from typing import Optional

class HuggingFaceIntegration:
    """
    This class integrates with Hugging Face's transformers library to generate text completions based on provided prompts.

    Attributes:
        model_name (str): The model name to use for text generation (e.g., 'gpt-2').
    """

    def __init__(self, model_name: str = "gpt2"):
        """
        Initializes the HuggingFaceIntegration instance with the provided model.

        Args:
            model_name (str): The model name for generating text (default is 'gpt2').
        """
        self.generator = pipeline("text-generation", model=model_name)
        set_seed(42)  # Optional: Set a fixed random seed for reproducibility

    def get_response(self, prompt: str, max_length: int = 150, num_return_sequences: int = 1) -> dict:
        """
        Generates a response from the Hugging Face model based on the given prompt.

        Args:
            prompt (str): The prompt text that the model will respond to.
            max_length (int, optional): The maximum length of the generated text (default is 150).
            num_return_sequences (int, optional): The number of responses to generate (default is 1).

        Returns:
            dict: The response object containing the generated text.
        """
        try:
            # Use Hugging Face's pipeline to generate text
            response = self.generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
            return response  # Return the response object
        except Exception as e:
            # Handle any errors during the generation process
            return {"error": f"An error occurred: {str(e)}"}

    def get_text_from_response(self, response: dict) -> Optional[str]:
        """
        Extracts the generated text from the Hugging Face model response.

        Args:
            response (dict): The response object returned from the Hugging Face API.

        Returns:
            str or None: The generated text if available, or None if the response doesn't contain valid text.
        """
        if isinstance(response, list) and len(response) > 0:
            return response[0]["generated_text"].strip()
        else:
            return None

    def chat_with_model(self, prompt: str, max_length: int = 150, num_return_sequences: int = 1) -> str:
        """
        A higher-level method for a simpler integration. It returns only the generated text.

        Args:
            prompt (str): The prompt text that the model will respond to.
            max_length (int, optional): The maximum length of the generated text (default is 150).
            num_return_sequences (int, optional): The number of responses to generate (default is 1).

        Returns:
            str: The generated text from the Hugging Face model.
        """
        response = self.get_response(prompt, max_length, num_return_sequences)
        generated_text = self.get_text_from_response(response)
        if generated_text:
            return generated_text
        else:
            return "Error: No valid response generated."
