import requests
import json
from env import personal_access_token
from github import Github
from flask import Flask, render_template, request, redirect
from repositories import repos_list

app = Flask(__name__)

@app.route('/')
def home():

    g = Github(login_or_token=personal_access_token)

    github_pr_info = {}
    github_pr_info_list = []

    for repo in repos_list:
        if repo == 'takeon-database':
            pulls = g.get_repo('ONSDigital/' + repo).get_pulls(state='open', sort='created', base='master')
        else:
            pulls = g.get_repo('ONSDigital/' + repo).get_pulls(state='open', sort='created', base='main')
        for pr in pulls:
            individual_pr_details = {}
            individual_pr_details['repository'] = repo
            individual_pr_details['pr_number'] = pr.number
            individual_pr_details['pr_url'] = pr.html_url
            individual_pr_details['pr_description'] = pr.body
            individual_pr_details['title'] = pr.title
            github_pr_info_list.append(individual_pr_details)

    github_pr_info['github_repositories'] = github_pr_info_list
    
    return render_template(template_name_or_list='index.html',
                            github_pr_info=github_pr_info)


if __name__ == '__main__':
    app.run(debug=True)




