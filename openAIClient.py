import os
from openai import OpenAI
from pdfCreation import create_pdf

def gameRecap(world_guide, style_guide, persona_style, game_input, reportPath, reportName):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"{style_guide} {world_guide} {persona_style} {game_input}, ensure that all sections asked for are provided. Include how many words were generated at the bottom."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10000
    )
    client.close()
    print(response.choices[0].message.content)
    filePath = create_pdf(response.choices[0].message.content, reportPath, reportName)
    return filePath

# def recruitSpotlight():
#     print("recruit")

# def pressRelease():
#     print("press")

# def fanBlogs()
#     print("fanBlogs")

# def rumorMill():
#     print("rumor")