import os
from openai import AsyncOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import requests
from newspaper_recap import create_newspaper_pdf

async def gameRecap(world_guide, style_guide, persona_style, game_input, reportName):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("AI Opened")
    prompt = f"{style_guide}\nWolrd Info:\n{world_guide}\nWriter Style:\n{persona_style}\nGame Info:\n{game_input}"
    
    messages = [
    {"role": "system", "content": "You are a sports journalist creating recaps for College Football 26."},
    {"role": "user", "content": prompt}
    ]
    
    print("Start Article")
    # Step 1: Article
    messages.append({"role": "user", "content": "Write the article"})
    response = await client.chat.completions.create(model="gpt-5", messages=messages)
    article = response.choices[0].message.content
    messages.append({"role": "assistant", "content": article})
    print("Article Done")
    # Step 2: Subtitle
    messages.append({"role": "user", "content": "Write a catchy short subtitle for the article"})
    response = await client.chat.completions.create(model="gpt-5", messages=messages)
    subTitle = response.choices[0].message.content
    print("subtitle Done")

    await client.close() 
    filePath = create_newspaper_pdf("The Dynasty Tribune", subTitle, "Carter Langford", article, reportName)
    return filePath

async def gamePreview(world_guide, style_guide, persona_style, user_input, report_name):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("AI Opened")
    prompt = f"{style_guide}\nWolrd Info:\n{world_guide}\nWriter Style:\n{persona_style}\nGame Info:\n{user_input}"
    
    messages = [
    {"role": "system", "content": "You are a sports journalist creating game previews for a game in College Football 26."},
    {"role": "user", "content": prompt}
    ]
    
    print("Start Article")
    # Step 1: Article
    messages.append({"role": "user", "content": "Write the article"})
    response = await client.chat.completions.create(model="gpt-5", messages=messages)
    article = response.choices[0].message.content
    messages.append({"role": "assistant", "content": article})
    print("Article Done")
    # Step 2: Subtitle
    messages.append({"role": "user", "content": "Write a catchy short subtitle for the article"})
    response = await client.chat.completions.create(model="gpt-5", messages=messages)
    subTitle = response.choices[0].message.content
    print("subtitle Done")

    await client.close() 
    filePath = create_newspaper_pdf("The Dynasty Tribune", subTitle, "RG3", article, report_name)
    return filePath

def recruit_spotlight(style_guide, user_input, report_name):
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"{style_guide}\n{user_input}"
    result = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )

    image_url = result.data[0].url
    response = requests.get(image_url)

    with open(report_name, "wb") as f:
        f.write(response.content)
             
    client.close() 


if __name__ == "__main__":
    load_dotenv()
    print("Image Start")
    prompt = "“high school football linebacker named Marcus ‘Tank’ Johnson, 6'3”, 230 lbs, 5 star from Travis High School. ”"
    styleguid = """Creatoe a realistic carton picture with soft colors. Action shot of player in uniform with 
    opponents visable if necessary. Setting is in a high school football stadium. Weather is location appropriate. Stadium lights and crowd in background. Slight depth blur for cinematic focus
    High detail, dramatic lighting. Avoid any content that may be considered inappropriate or offensive, ensuring the image aligns with content policies"""
    recruit_spotlight(
        style_guide=styleguid,
        user_input=prompt,
        report_name=os.getcwd() + "\\test.png"
    )
    print("Image Done")