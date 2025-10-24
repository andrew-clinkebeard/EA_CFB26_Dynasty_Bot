from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text)






# def gameRecap():
#     print("game")
#     filePath = r'C:\\Users\\Andrew Clinkenbeard\\Desktop\\8.jpg' #make pdf path eventually
#     return filePath

# def recruitSpotlight():
#     print("recruit")

# def pressRelease():
#     print("press")

# def fanBlogs()
#     print("fanBlogs")

# def rumorMill():
#     print("rumor")