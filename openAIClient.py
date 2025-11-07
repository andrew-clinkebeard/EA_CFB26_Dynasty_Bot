import os
from openai import OpenAI
from pdfCreation import create_pdf
from newspaper_recap import create_newspaper_pdf

# def gameRecap(world_guide, style_guide, persona_style, game_input, reportPath, reportName):
#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     prompt = f"{style_guide} {world_guide} {persona_style} {game_input}"
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=10000
#     )
#     client.close()
#     print(response.choices[0].message.content)
#     filePath = create_pdf(response.choices[0].message.content, reportPath, reportName)
#     create_newspaper_pdf("The Dynasty Tribune", "Dog days of Sooner", "Carter Langford", response.choices[0].message.content, "test.pdf")
#     return filePath

def gameRecap(world_guide, style_guide, persona_style, game_input, reportPath, reportName):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"{style_guide} {world_guide} {persona_style} {game_input}"
    messages = [
    {"role": "system", "content": "You are a sports journalist creating recaps for College Football 26."},
    {"role": "user", "content": prompt}
    ]
    
    # Step 1: Article
    messages.append({"role": "user", "content": "Write the article"})
    response = client.chat.completions.create(model="gpt-5", messages=messages)
    article = response.choices[0].message.content
    messages.append({"role": "assistant", "content": article})
    
    # Step 2: Subtitle
    messages.append({"role": "user", "content": "Write a catchy short subtitle for the article"})
    response = client.chat.completions.create(model="gpt-5", messages=messages)
    subTitle = response.choices[0].message.content
    
    client.close()
    print(response.choices[0].message.content)
    filePath = create_pdf(response.choices[0].message.content, reportPath, reportName)
    create_newspaper_pdf("The Dynasty Tribune", subTitle, "Carter Langford", article, "test.pdf")
    return filePath

# def recruitSpotlight():
#     print("recruit")

# def pressRelease():
#     print("press")

# def fanBlogs()
#     print("fanBlogs")

# def rumorMill():
#     print("rumor")