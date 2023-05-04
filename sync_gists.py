import os
from github import Github, GistFile
from github.GithubObject import NotSet


class CustomGist:
    def __init__(self, gist):
        self._gist = gist

    def edit(self, files=NotSet):
        post_parameters = dict()
        if files is not NotSet:
            post_parameters["files"] = dict()
            for name, value in files.items():
                post_parameters["files"][name] = value
        headers, data = self._gist._requester.requestJsonAndCheck(
            "PATCH", f"/gists/{self._gist.id}", input=post_parameters
        )
        return self._gist._makeBoolAttribute(data["history"][0]["change_status"]["total"])

    def __getattr__(self, attr):
        return getattr(self._gist, attr)


def main():
    token = os.environ['GITHUB_TOKEN']
    main_gist_id = os.environ['MAIN_GIST_ID']
    other_gists = os.environ['OTHER_GISTS'].split(',')

    github = Github(token)
    main_gist = github.get_gist(main_gist_id)
    main_gist = CustomGist(main_gist)

    main_file = list(main_gist.files.values())[0]
    main_content = main_file.content

    for gist_id in other_gists:
        gist = github.get_gist(gist_id)
        gist = CustomGist(gist)
        main_file_name = main_file.filename.strip()
        files_to_update = {main_file_name: {"content": main_content, "filename": main_file_name}}
        gist.edit(files=files_to_update)


if __name__ == "__main__":
    main()
