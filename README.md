<<<<<<< HEAD
<<<<<<< HEAD
# Projet-2A



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.ecole.ensicaen.fr/goubraim/projet-2a.git
git branch -M master
git push -uf origin master
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.ecole.ensicaen.fr/goubraim/projet-2a/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# Instagram-Insights
Instagram Insights is a Streamlit application that allows you to analyze and visualize your Instagram data like users not following you back, users you aren't following back, and more.
>>>>>>> 120c295 (Initial commit)
=======

# Carbon Footprint Score Calculator

The Carbon Footprint Score Calculator is a Python Streamlit web application that allows users to answer questions about their lifestyle choices during the pandemic and the current period, helping determine the environmental impact of these choices. The application will display information on how your Carbon Footprint Score has changed from the pandemic to the present. The application is divided into two parts:

1. Carbon_Footprint_Calc.py - main application where users answer the survey
2. Submission_Score.py - where the analysis of all the submissions is displayed

# Web App
Click [Here](https://kaludii-carbon-footprint-calc-bios-carbon-footprint-calc-xgt0yx.streamlit.app/ "Here") To View This Application Online!
![image](https://github.com/Kaludii/Carbon-Footprint-Calc-BIOS365/assets/63890666/cabb3141-96c7-4a27-9f89-b70e8237de35)

## Features

* Survey-style questions to calculate your Carbon Footprint Score
* Comparison of your Carbon Footprint Score from during the pandemic to the current period
* Submissions analysis visualization in the 'pages/Submission_Score.py'

## Usage

1. Fill in the survey questions on the main page of the application.
2. Submit the survey by clicking on the "Submit" button.
3. View your score on the next page, along with comparison charts and suggestions on how to improve it.

## Installation

1. Clone the repository
   ```
   git clone https://github.com/Kaludii/Carbon-Footprint-Score-Calculator.git
   ```
2. Change your directory to the cloned project
   ```
   cd Carbon-Footprint-Score-Calculator
   ```
3. Install necessary dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit application
   ```
   streamlit run Carbon_Footprint_Score_Calculator.py
   ```
5.  Open your web browser and visit `http://localhost:8501`.

## Submission Scores Analysis

The "Submission_Score.py" is a 2nd part of the application that displays all submissions and various visualizations showing the distribution of responses for each question from **[this](https://docs.google.com/spreadsheets/d/1aHgyMoxp7aINImqu3eXiwAzq5QvTqbfhUaKv2fkdHss/edit?usp=sharing)** Google Sheet. You can also download the data for each folder ("Submission-Now" or "Submission-Pandemic") as a CSV file.

## License

[MIT](https://choosealicense.com/licenses/mit/)
