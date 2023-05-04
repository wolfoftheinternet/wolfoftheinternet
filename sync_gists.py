import os
from github import Github

def main():
    github_token = os.environ['GITHUB_TOKEN']
    main_gist_id = os.environ['MAIN_GIST_ID']
    other_gists = os.environ['OTHER_GISTS'].split(',')

    github = Github(github_token)
    main_gist = github.get_gist(main_gist_id)

    for gist_id in other_gists:
        gist = github.get_gist(gist_id)
        for main_file, main_content in main_gist.files.items():
            if main_file in gist.files:
                gist.edit(files={main_file: {'content': main_content.content}})

if __name__ == "__main__":
    main()
