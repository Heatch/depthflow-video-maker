prompt = """Your task is to create a JSON output of concise, detailed image prompts for an inspirational video based on a given script. These prompts should be optimized for Stable Diffusion image generation, creating stock-like images that complement the narration without focusing on specific characters.
Output Format
For each significant moment in the script, provide a JSON object:
{
  "script_text": "The relevant portion of the script",
  "image_prompt": "Concise, comma-separated description for Stable Diffusion"
}

Guidelines for Creating Stable Diffusion Prompts:

Use commas to separate key elements and ideas in the prompt.
Keep prompts concise and focused - avoid lengthy or fluffy descriptions.
Emphasize important elements by placing them at the beginning of the prompt.
Include specific details about style, lighting, and atmosphere (e.g., "cinematic, golden hour, misty").
Focus on landscapes, natural elements, and abstract concepts representing themes and emotions.
Incorporate symbolic elements that represent the script's messages.
Avoid specific individual characters - use collective terms for people (e.g., "crowd, silhouettes").
Ensure each prompt is self-contained and doesn't rely on context from other parts of the script.

Elements to Consider Including:
Mountains, sky, buddha statues, crowds, forests, oceans, sunrises/sunsets, stars, cityscapes, ancient ruins, flowing rivers, blooming flowers, storm clouds, desert landscapes, northern lights
Example Output
{
  "script_text": "In the face of adversity, we find our true strength.",
  "image_prompt": "Majestic mountain peak, dark storm clouds, golden light breaking through, rugged terrain, winding path upward, contrast of storm and hope, symbolic journey, cinematic, dramatic lighting"
}

Additional Notes:

Prioritize accuracy and relevance over length in prompts.
Balance concrete imagery with abstract concepts for impactful visuals.
Each prompt should stand alone as a direction for a single, powerful image.
Translate mentions of people or actions into symbolic or environmental representations.
Use your imagination to fill in visual details not explicitly stated in the script, but keep it relevant to the theme.
"""