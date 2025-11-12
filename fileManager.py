import os
from datetime import datetime


def format_time_fixed(seconds):
    days, remainder = divmod(seconds, 86400)   # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600) # 3600 seconds in an hour
    minutes, secs = divmod(remainder, 60)      # 60 seconds in a minute
    
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {secs:.2f} seconds"


def check_directories(directory):
    """
    make sure directories exist before program runs
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

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

current_directory = os.getcwd()  # Get the current working directory
memoryDir = check_directories(current_directory + "\\memory")
worldGuideLocation = check_directories(memoryDir + "\\World_Guide.txt")
personalitiesDir = check_directories(memoryDir + "\\Personalities")
styleDir = check_directories(memoryDir + "\\Style Guides")
reportDir = check_directories(current_directory + "\\Reports")
imageDir = check_directories(reportDir + "\\Images")