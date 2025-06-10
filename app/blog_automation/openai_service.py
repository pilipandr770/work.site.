"""
OpenAI services for content generation and translation
"""
import os
import json
import time
from openai import OpenAI  # Updated import for OpenAI client
import logging

logger = logging.getLogger(__name__)

class OpenAIContentService:
    """Service for interacting with OpenAI for content generation and translation"""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.content_assistant_id = os.environ.get('OPENAI_CONTENT_ASSISTANT_ID')
        self.translation_assistant_id = os.environ.get('OPENAI_TRANSLATION_ASSISTANT_ID')
        # Initialize the OpenAI client with api_key
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_blog_content(self, topic, description="", max_retries=3):
        """Generate blog content based on topic"""
        content_prompt = (
            f"Write a comprehensive, informative blog post about '{topic}'. "
            f"Additional context: {description}\n\n"
            f"The blog post should be well-structured with an introduction, "
            f"multiple paragraphs with interesting information, and a conclusion. "
            f"Make it engaging and informative for readers interested in this topic. "
            f"Use a professional tone and include factual information where appropriate."
        )
        
        try:
            # Create a thread
            thread = self.client.beta.threads.create()
            
            # Add message to thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=content_prompt
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.content_assistant_id
            )
            
            # Wait for completion
            return self._wait_for_completion(thread.id, run.id, max_retries)
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def translate_content(self, content, target_language, max_retries=3):
        """Translate blog content to target language"""
        translation_prompt = (
            f"Translate the following blog post content into {target_language}. "
            f"Maintain the same formatting and structure, but ensure the translation "
            f"sounds natural and fluent in the target language:\n\n{content}"
        )
        
        try:
            # Create a thread
            thread = self.client.beta.threads.create()
            
            # Add message to thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=translation_prompt
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.translation_assistant_id
            )
            
            # Wait for completion
            return self._wait_for_completion(thread.id, run.id, max_retries)
            
        except Exception as e:
            logger.error(f"Error translating content: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_image_prompt(self, topic, description=""):
        """Generate a DALL-E prompt based on topic for image creation"""
        image_prompt_request = (
            f"Create a detailed DALL-E 3 prompt that would generate a visually appealing "
            f"image representing the blog topic: '{topic}'. {description}\n\n"
            f"The image should be professional, suitable for a business blog, and "
            f"visually represent the key concepts of this topic. Make the prompt "
            f"detailed and specific for best results."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": image_prompt_request}]
            )
            return {
                "success": True, 
                "prompt": response.choices[0].message.content.strip()
            }
        except Exception as e:
            logger.error(f"Error generating image prompt: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_image(self, prompt, size="1024x1024"):
        """Generate image using DALL-E 3"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            return {
                "success": True,
                "url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt            }
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _wait_for_completion(self, thread_id, run_id, max_retries=3):
        """Wait for OpenAI Assistant run to complete and fetch response"""
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Check run status
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                
                # If completed, get messages
                if run.status == "completed":
                    messages = self.client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    
                    # Get assistant's response (most recent message from assistant)
                    for message in messages.data:
                        if message.role == "assistant":
                            content = ""
                            # Handle the content structure based on the API version
                            if hasattr(message, 'content'):
                                for content_part in message.content:
                                    if hasattr(content_part, 'type') and content_part.type == "text":
                                        if hasattr(content_part, 'text') and hasattr(content_part.text, 'value'):
                                            content += content_part.text.value
                                        elif hasattr(content_part, 'text'):
                                            content += content_part.text
                            else:
                                # Fallback for different API versions
                                content = str(message)
                                
                            return {"success": True, "content": content}
                    
                    return {"success": False, "error": "No response from assistant"}
                
                # If failed, return error
                elif run.status == "failed":
                    return {"success": False, "error": "Assistant run failed"}
                
                # If expired, return error
                elif run.status == "expired":
                    return {"success": False, "error": "Assistant run expired"}
                
                # Wait and try again
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error waiting for completion: {str(e)}")
                retry_count += 1
        
        return {"success": False, "error": "Max retries reached waiting for assistant response"}
