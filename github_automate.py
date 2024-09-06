
import os
import subprocess
from github import Github
import requests

# Authenticate with GitHub
g = Github('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')

# Keywords to search for
keywords = ["talent acquisition LLM", "Recruiter LLM", "skill recognition LLM", "job recommendation LLM"]

# Directory to store the files (local clone of your target GitHub repo)
repo_dir = 'C://Users//Varshini//careerPred_scraping2'

if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)

for keyword in keywords:
    query = keyword + " language:python"
    repos = g.search_repositories(query)
    
    for repo in repos:
        repo_name = repo.name
        repo_folder = os.path.join(repo_dir, repo_name)
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)
        
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "file" and file_content.path.endswith(".py"):
                file_data = requests.get(file_content.download_url).text
                file_path = os.path.join(repo_folder, file_content.name)
                
                # Specify utf-8 encoding when writing the file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_data)
            elif file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))

# Navigate to the repo directory
os.chdir(repo_dir)

# Add all files to the git staging area
subprocess.run(["git", "add", "."])

# Commit the changes
commit_message = "Add Python files from scraped GitHub repositories"
subprocess.run(["git", "commit", "-m", commit_message])

# Push the changes to your GitHub repository
subprocess.run(["git", "push", "origin", "main"])
