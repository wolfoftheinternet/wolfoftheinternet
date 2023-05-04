import os
from github import Github

def main():
    token = os.environ['GITHUB_TOKEN']
    main_gist_id = os.environ['MAIN_GIST_ID']
    other_gists = os.environ['OTHER_GISTS'].split(',')

    github = Github(token)
    main_gist = github.get_gist(main_gist_id)

    main_file = list(main_gist.files.values())[0]
    main_content = main_file.content

    for gist_id in other_gists:
        gist = github.get_gist(gist_id)
        # Format the files parameter correctly
        main_file_name = main_file.filename.strip()
        files_to_update = {main_file_name: {"content": main_content, "filename": main_file_name}}
        gist.edit(files=files_to_update)

if __name__ == "__main__":
    main()
