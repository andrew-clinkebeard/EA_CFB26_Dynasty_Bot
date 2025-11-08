import os
from openai import AsyncOpenAI
from pdfCreation import create_pdf
from newspaper_recap import create_newspaper_pdf

async def gameRecap(world_guide, style_guide, persona_style, game_input, reportPath, reportName):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("AI Opened")
    prompt = f"{style_guide} {world_guide} {persona_style} {game_input}"
    
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
    reportPath += reportName
    filePath = create_newspaper_pdf("The Dynasty Tribune", subTitle, "Carter Langford", article, reportPath)
    return filePath

# def recruitSpotlight():
#     print("recruit")

# def pressRelease():
#     print("press")

# def fanBlogs()
#     print("fanBlogs")

# def rumorMill():
#     print("rumor")