import os
from github import Github
from dotenv import load_dotenv
import re
from datetime import datetime

# Chargement des variables d'environnement
load_dotenv()

class GitHubManager:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPO')
        self.github = Github(self.token)
        self.repo = self.github.get_repo(self.repo_name)

    def extract_task_info(self, text):
        """Extrait les informations de la tâche à partir du texte transcrit"""
        # Détection de la priorité
        priority = "medium"  # Par défaut
        if re.search(r'\b(haute|urgent|important)\b', text.lower()):
            priority = "high"
        elif re.search(r'\b(basse|pas urgent)\b', text.lower()):
            priority = "low"

        # Détection de la date d'échéance
        due_date = None
        date_patterns = [
            r'pour le (\d{1,2}/\d{1,2}/\d{4})',
            r'pour (\d{1,2}/\d{1,2}/\d{4})',
            r'le (\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}/\d{1,2}/\d{4})'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    due_date = datetime.strptime(match.group(1), '%d/%m/%Y')
                    break
                except ValueError:
                    continue

        return {
            'title': text.split('.')[0][:100],  # Premier phrase comme titre
            'body': text,
            'priority': priority,
            'due_date': due_date
        }

    def create_issue(self, text):
        """Crée une issue à partir du texte transcrit"""
        try:
            task_info = self.extract_task_info(text)
            
            # Préparation du corps de l'issue
            body = f"""## Description
{task_info['body']}

## Priorité
{task_info['priority'].capitalize()}

"""
            if task_info['due_date']:
                body += f"""## Date d'échéance
{task_info['due_date'].strftime('%d/%m/%Y')}

"""

            # Création de l'issue
            issue = self.repo.create_issue(
                title=f"[TÂCHE] {task_info['title']}",
                body=body,
                labels=['task', f'priority-{task_info["priority"]}']
            )
            
            return {
                'success': True,
                'issue_number': issue.number,
                'issue_url': issue.html_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 