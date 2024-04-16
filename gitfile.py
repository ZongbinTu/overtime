from datetime import datetime, timedelta
import argparse
import git
repo = None
def is_commit_by_author_and_after_7pm(commit,author_name):
    commit_time = commit.authored_datetime
    return commit_time.hour >= 19 and commit.author.name == author_name # Assuming 24-hour time; 19 corresponds to 7 PM

def get_commits_by_author_and_after_7pm(repo_path, author_name, start_date=None):
    repo = git.Repo(repo_path)

    if start_date is None:
        start_date = datetime.now() - timedelta(days=10000)  # Default to the last day
    commits = list(repo.iter_commits('HEAD', after=start_date))

    return [commit for commit in commits if is_commit_by_author_and_after_7pm(commit,author_name)]

def get_branch_name(repo, commit):
    try:
        # Try to find the branch that contains the commit
        branches = repo.branches if hasattr(repo, 'branches') else repo.heads  # For compatibility with older GitPython versions
        for branch in branches:
            if branch.commit == commit:
                return branch.name
    except Exception as e:
        print(f"Warning: Failed to determine branch for commit {commit.hexsha}. Reason: {e}")

    return "(unknown branch)"

def main():
    parser = argparse.ArgumentParser(description='Get commits by a specific author after 7 PM on a given branch.')
    parser.add_argument('repo_path', help='Path to the Git repository')
    parser.add_argument('author_name', help='Name of the author to filter commits by')
    args = parser.parse_args()

    commits = get_commits_by_author_and_after_7pm(args.repo_path,args.author_name)

    for commit in commits:
        #branch_name = get_branch_name(repo, commit)
        print(f"{commit.hexsha}: {commit.authored_datetime} by {commit.author.name}")
        print(f"     Message: {commit.message}")

if __name__ == '__main__':
    main()
