"""
OpenAI service module for CliftonStrengths comparison.
"""

import os
import streamlit as st
from openai import OpenAI


def get_openai_client():
    """
    Initialize and return OpenAI client.
    Works with both local .env and Streamlit Cloud secrets.
    
    Returns:
        OpenAI: Configured OpenAI client
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    # Try Streamlit secrets first (for cloud deployment)
    api_key = None
    
    try:
        if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    # Fall back to environment variable (for local development)
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Please set it in Streamlit secrets (for cloud) or as an environment variable (for local)."
        )
    
    return OpenAI(api_key=api_key)


def create_comparison_prompts(person1_name, person1_strengths, person2_name, person2_strengths):
    """
    Create the three comparison prompts for OpenAI.
    
    Args:
        person1_name (str): Name of first person
        person1_strengths (list): List of 5 CliftonStrengths for person 1
        person2_name (str): Name of second person
        person2_strengths (list): List of 5 CliftonStrengths for person 2
        
    Returns:
        tuple: Three prompts (conflicts, collaboration, communication)
    """
    strengths1_str = ", ".join(person1_strengths)
    strengths2_str = ", ".join(person2_strengths)
    
    context = (
        f"{person1_name}'s top 5 CliftonStrengths are: {strengths1_str}. "
        f"{person2_name}'s top 5 CliftonStrengths are: {strengths2_str}."
    )
    
    conflicts_prompt = (
        f"{context}\n\n"
        f"Based on these CliftonStrengths profiles, what potential conflicts "
        f"might arise between {person1_name} and {person2_name}? "
        f"Please provide specific insights about how their different strengths "
        f"might lead to misunderstandings or tension."
    )
    
    collaboration_prompt = (
        f"{context}\n\n"
        f"How can {person1_name} and {person2_name} work well together? "
        f"What are the complementary aspects of their strengths? "
        f"Please provide specific strategies for effective collaboration."
    )
    
    communication_prompt = (
        f"{context}\n\n"
        f"How should {person1_name} speak to {person2_name} to be most effective? "
        f"What communication style, tone, and approach would resonate best with "
        f"{person2_name} based on their CliftonStrengths?"
    )
    
    return conflicts_prompt, collaboration_prompt, communication_prompt


def get_ai_response(client, prompt, temperature=0.7):
    """
    Get a response from OpenAI GPT-4o.
    
    Args:
        client (OpenAI): OpenAI client instance
        prompt (str): The prompt to send
        temperature (float): Temperature parameter for response variability
        
    Returns:
        str: AI-generated response
        
    Raises:
        Exception: If API call fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in CliftonStrengths assessment and workplace dynamics. "
                        "Provide insightful, practical, and empathetic advice about how people with "
                        "different strength profiles can work together effectively."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def compare_strengths(person1_name, person1_strengths, person2_name, person2_strengths):
    """
    Compare two people's CliftonStrengths using OpenAI.
    
    Args:
        person1_name (str): Name of first person
        person1_strengths (list): List of 5 CliftonStrengths for person 1
        person2_name (str): Name of second person
        person2_strengths (list): List of 5 CliftonStrengths for person 2
        
    Returns:
        tuple: (conflicts_response, collaboration_response, communication_response)
        
    Raises:
        Exception: If any API call fails
    """
    client = get_openai_client()
    
    # Create the three prompts
    conflicts_prompt, collaboration_prompt, communication_prompt = create_comparison_prompts(
        person1_name, person1_strengths, person2_name, person2_strengths
    )
    
    # Get responses for all three questions
    conflicts_response = get_ai_response(client, conflicts_prompt)
    collaboration_response = get_ai_response(client, collaboration_prompt)
    communication_response = get_ai_response(client, communication_prompt)
    
    return conflicts_response, collaboration_response, communication_response
