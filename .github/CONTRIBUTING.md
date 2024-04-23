# Helixiora contributing guide

This document provides general guidelines for making meaningful contributions to Helixiora's projects on GitHub. 

## Getting started 

The _**README.md**_ file at the root of each repository is a great resource for getting started with an existing project. Review it and read other related documentation (in the **docs/** folder) if necessary.

## Setting up your IDE
Each project enforces specific codestyle and linting standards, our general requirements per programming language are listed below:

### Python

* We conform to the [PEP8](https://peps.python.org/pep-0008/) style.
* Linting and formatting is to be ensured through [Ruff](https://docs.astral.sh/ruff/)
* All of our CI/CD processes involving Python pass code through Ruff. 
* If checks againts Ruff are failed, then the code **will not** be merged untill fixed.

Your IDE of choice should have the required extensions for Ruff installed for ease of use. While it does handle formatting and linting we also recommend setting up [Pylint](https://pylint.readthedocs.io/en/stable/), [Flake8](https://flake8.pycqa.org/en/latest/) and [Black](https://pypi.org/project/black/) to ensure your code has even better coverage.

## Making changes 
### Sanctity of main branch
We treat our main branches as something of a "source-of-truth". Therefore it is expected by the organization that the code there will **always** work in a predictable manner. **No** changes shall be made to it without review and without conforming to the details described further down. 

To work on some feature, bugfix etc. of your own, please create a new branch which will contain your respective changes.

### Naming a branch 
An ideal branch name contains two to three descriptive words. If the branch is related to an internal project/task, your name should be pre-pended with the task ID from ClickUp.

Example:

```
00aa0aaaa-add-contributing-guide
```

### Testing 
Test all code changes using development and _mock_ production environments to avoid unpleasant surprises.

### Committing changes
1. Our CI process only allows merging commits which are signed. Please make sure to [set that up](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits), prior to pushing commits to *any* branch.
2. We are fans of the [Tim Pope's commit template](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html), please make sure your message conforms as much as possible to this template.

### Submitting and reviewing changes
When confident that the changes made are ready to be merged to the main branch, please submit a pull request. Our pull request template has various fields which helps the team gauge the changes. Please take the time to fill it out when following this process.

We guarantee we will review any changes in a timely manner and provide feedback/collaborate on the new code. At least **one** team member has to approve the change before the merge process is triggered. 

### General advice 

To foster greater collaboration we encourage everybody to contirbute early and often. This means 

An example flow would be:

1. You think of a feature/change (or are assigned the task to work on it).
2. Create a branch per the previously described process.
3. Make a first pass at the changes you are planning. 
4. Push/publish your branch, so long as it conforms to the code style guides outlined previously.
5. Notify the team and continue itterating on your code (either solo or collaboratively, depending on team availability).
6. Once everybody is happy with the changes a/another team member approves them.
7. The approval process triggers an automatic merge to the main branch, which will also trigger the respective CI/CD process create a new build artifact.

## Building new packages

We utilize Github actions and packages for our CI/CD process. By default artifacts are **only** generated for the main branch. A comment on a PR which is "!build" will also trigger an artifact build.

## Reporting/discussing Issues 

### Internal team members
If you're a Helixiora team member, please report the issues to the Engineering team.

### External contributors
If you're a third-party contributor, please check that there's no open issue addressing the problem before creating a new GitHub issue.

## Documentation
Each individual project shall have documentation specific to it. 

## Questions
All questions can be directed to the Engineering team. If you are external we welcome all communication via Github's channels or e-mail.
