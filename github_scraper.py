from flask import Flask, render_template
from pymongo import MongoClient
import requests
import json

app = Flask(__name__)

# Créer la base de données
client = MongoClient('localhost', 27017)
db = client['github_repos_db']
collection = db['repositories']

def scrape_github():
    """
        Méthode pour obtenir les données de Github et les insérer dans la base de données
    """
    base_url = 'https://api.github.com/search/repositories?q=json+in:name&sort=stars&order=desc&per_page=100'
    
    contributors_count = None
    issues = None
    
    # effectuer 2 requêtes pour obtenir 200 dépôts (limitation de Github si non authentifié)
    for i in range(1, 3):
        url = f"{base_url}&page={i}"
        response = requests.get(url)
        data = response.json()

        for repo in data['items']:
            full_name = repo['full_name']
            description = repo['description']
            html_url = repo['html_url']
            stargazers_count = repo['stargazers_count']
            open_issues_count = repo['open_issues_count']

            issues_url = f"https://api.github.com/repos/{full_name}/issues?state=open&per_page=5"
            try:
                issues_response = requests.get(issues_url)
                issues = json.dumps(issues_response.json())
            except Exception as e:
                print(f"Error getting issues: {e}")
                issues = ""

            contributors_url = f"https://api.github.com/repos/{full_name}/contributors"
            try:
                contributors_response = requests.get(contributors_url)
                contributors_count = len(contributors_response.json())
            except Exception as e:
                print(f"Error getting contributors: {e}")
                contributors_count = 0

            # Insérer dans la base de données
            collection.insert_one({
                "full_name": full_name,
                "description": description,
                "html_url": html_url,
                "stargazers_count": stargazers_count,
                "open_issues_count": open_issues_count,
                "issues": issues,
                "contributors_count": contributors_count
            })

# On vide la collection avant de scraper à nouveau
collection.delete_many({})
scrape_github()

# Interface pour afficher les données
@app.route('/')
def show_data():
    data = list(collection.find())
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run()
