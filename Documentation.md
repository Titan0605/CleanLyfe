# Documentation

---

> ## ***First steps***
* ### Connect to GitHub
1. **Check if Git is installed:** Make sure Git is installed on your computer by running the following command in your terminal:

```bash
git --version
```
If Git is not installed, download it from [git-scm.com](https://git-scm.com) and follow the installation instructions for your operating system.

2. **Configure Git:** If this is your first time using Git on this machine, configure your name and email:

```bash
git config --global user.name "YourName"
git config --global user.email "youremail@example.com"
```

3. **Connect with GitHub using a Personal Access Token:**
    - Generate a Personal Access Token:
        - Log in to your GitHub account.
        - Go to Settings (click on your profile picture in the top right corner and select "Settings").
        - In the left sidebar, click on Developer settings.
        - Click on Personal access tokens and then Tokens (classic).
        - Click on Generate new token.
        - Provide a note to identify the token, set an expiration date if desired, and select the scopes or permissions you want to grant this token (e.g., `repo` for full control of repositories).
        - Click Generate token. Make sure to copy the token as it will not be displayed again.
    - Authenticate Git with your Personal Access Token:
        - When you clone a repository or perform any Git operation that requires authentication, use your GitHub username as the username.
        - For the password, paste the personal access token you generated instead of your GitHub password.

* ### Clone the repository
1. **Get the repository URL:** Go to the repository on GitHub and copy the repository link (either HTTPS or SSH).

2. **Clone the repository:** Open a terminal where you want to clone the project and run:

```bash
git clone <repository_url>
```

The next comand will download the source code of [Cleanlyfe](https://github.com/Titan0605/CleanLyfe) to your local machine:

```bash
git clone https://github.com/Titan0605/CleanLyfe.git
```

* ### Start a local virtual environment
1. **Create a virtual environment:** In the terminal, navigate to the cloned repository folder and run:

```bash
python -m venv env
```

This will create a virtual environment called `env`.

2. Activate the virtual environment:

```bash
env\Scripts\activate
```

* ### Install dependencies
1. **Install dependencies:** Make sure the virtual environment is activated, and then run the following command to install all necessary dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

> ## ***Before coding***
* ### Download GitKraken
1. **Download GitKraken:** Go to the official [GitKraken](https://www.gitkraken.com) website and download the appropriate version for your operating system.

2. **Install GitKraken:** Follow the installation instructions for your OS. Once installed, log in with your GitHub account or configure the necessary credentials.
* ### Start gitflow
1. **Initialize GitFlow:** Open the terminal in GitKraken by clicking on the terminal icon in the left sidebar or by selecting Terminal from the top menu.
    - In the Terminal: Run the following command to initialize GitFlow:

        ```bash
        git flow init
        ```

2. **Configure GitFlow:** GitKraken will prompt you to define default branches like `main` and `develop`. Just accept all the suggested options by pressing Enter.
* ### Create a feature branch
1. **Create a feature branch:** In GitKraken, select Start a Feature from the GitFlow tab. Enter a name for your new feature branch, such as `feature/new-feature`, and click Start.

---

> ## ***Upload local progress to the remote repository (GitHub)***
* ### Add changes to commit
1. **Add files for commit:** In GitKraken or the terminal, select the files you want to include in the commit:
    - In GitKraken: Use the "Commit Panel" tab to select the files you want to stage.
    - In the terminal:

        ```bash
        git add .
        ```

        This will add all modified files.
* ### Make a commit
1. **Commit the changes:** In GitKraken, add a descriptive message about the changes made in the message box and press Commit.

2. **In the terminal:**

```bash
git commit -m "Descriptive message about the changes"
```

* ### Push to the repository
1. **Push the feature branch:** After committing, you need to push the changes to the remote repository:
    - **In GitKraken:** Click Push and select the feature branch you created.
    - **In the terminal:**

        ```bash
        git push origin feature/new-feature
        ```

---

> ## ***Merge from a feature branch to develop***
* ### Check that the branch is up to date
1. **Verify that the branch is up to date:** Ensure that your feature branch has been successfully pushed to GitHub and that there are no pending conflicts.  

* ### Make a pull request
1. **Create a pull request:** From GitHub, select Create Pull Request. Choose the `develop` branch as the target.

* ### Wait for a review
1. **Wait for review:** Since the `develop` branch is protected, you’ll need to wait for the repository owner to review and approve the changes.

* ### Successful merge
1. **Successful merge:** Once the repository owner approves the pull request, your feature branch will be merged into `develop`. Afterward, the repository owner may delete the feature branch.