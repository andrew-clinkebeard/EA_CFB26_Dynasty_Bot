import os
from datetime import datetime

current_directory = os.getcwd()  # Get the current working directory
memoryDir = current_directory + "\\memory"
worldGuideLocation = memoryDir + "\\World_Guide.txt"
personalitiesDir = memoryDir + "\\Personalities"
styleDir = memoryDir + "\\Style Guides"
reportDir = current_directory + "\\Reports"

def get_files_in_current_directory(current_directory):
    """
    Retrieves a list of all files in the current running directory.
    """
    files = []
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isfile(item_path):
            files.append(item_path)
    return files


def loadWorld():
    """
    Loads world support files
    """
    #get world guide
    with open(worldGuideLocation, "r", encoding="utf-8") as f:
        global world_guide 
        world_guide = f.read()

    global STYLE_GUIDES 
    STYLE_GUIDES = {}
    style_files = get_files_in_current_directory(styleDir)
    for file in style_files:
        name = os.path.basename(file)
        with open(file, "r", encoding="utf-8") as f:
            STYLE_GUIDES[name] = f.read()
            
    global PERSONALITIES
    PERSONALITIES = {}
    person_files = get_files_in_current_directory(personalitiesDir)
    for file in person_files:
        name = os.path.basename(file)
        with open(file, "r", encoding="utf-8") as f:
            PERSONALITIES[name] = f.read()

def createFileName(ctx):
    """
    creates file name for the generated file based off user who created it and the current time
    """
    # Get the current date and time
    now = datetime.now()
    # Format the datetime object into the desired string format
    timestamp_str = now.strftime("%Y%m%d%H%M%S")
    
    #build preview name
    fileName = reportDir + "\\" + ctx.message.author.display_name + "_" + timestamp_str+  ".pdf"
    
    return fileName

# def load_text_file(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         return f.read()

# # Load guides
# world_guide = load_text_file("memory/world_guide.txt")

# STYLE_GUIDES = {
#     "dispatch": load_text_file("memory/style_guides/dynasty_dispatch.txt"),
#     "greenstandard": load_text_file("memory/style_guides/green_standard.txt"),
#     "boomersedge": load_text_file("memory/style_guides/boomers_edge.txt"),
# }
# Example usage:
# current_directory = os.getcwd()  # Get the current working directory
# memoryDir = current_directory + "\\memory"
# personalitiesDir = memoryDir + "\\Personalities"
# styleDir = memoryDir + "\\Style Guides"

# file_list = get_files_in_current_directory(current_directory)
# print("Files in the current directory:")
# for file_name in file_list:
#     print(file_name)

# file_list = get_files_in_current_directory(personalitiesDir)
# print("Files in the person directory:")
# for file_name in file_list:
#     print(file_name)
    
# file_list = get_files_in_current_directory(styleDir)
# print("Files in the style directory:")
# for file_name in file_list:
#     print(file_name)

# file_list = get_files_in_current_directory(memoryDir)
# print("Files in the memory directory:")
# for file_name in file_list:
#     print(file_name)