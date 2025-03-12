import os
import requests
import json
import subprocess
import sys
import inquirer

"""
In order for terraform to deploy correctly, terraform.tfvars will need to be created.
It needs to be populated with GIT credentials. 
"""

# Define path to terraform .tfvars:
path = './terraform/terraform.tfvars'

def validate_git_credentials(url: str, pat: str) -> bool:
    """
    This function determines if the supplied url and pat are valid.

    Args: 
        url (str) the url to the valid github repo.
        pat (str) the pat token to allow access to the github repo.
    
    Returns:
        bool: True if url and pat are valid.

    Raises:
        TypeError: if supplied pat and url are not in string format.
        ValueError: if supplied url is not a valid url.
        Exception: if invalid PAT - after request to GIT.
        Exception: if invalid URL - after request to GIT.

    """
    if not isinstance(url, str):
        raise TypeError('String required for URL.')
    
    if not isinstance(pat, str):
        raise TypeError('String required for PAT.')
    
    if not "https://" in url:
        raise ValueError('Please supply valid url.  https://...')
    
    # Check PAT:
    try:
        result = subprocess.run(
            ["curl", "-s", "-I", "-H", f"Authorization: token {pat}", "https://api.github.com/user"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        # If invalid pat raise exception:
        if not "HTTP/1.1 200 OK" in result.stdout and not "HTTP/2 200" in result.stdout:
            raise RuntimeError('Invalid PAT')

    except Exception as e:
        raise RuntimeError('Invalid PAT')

    # Check URL:
    try:
        repo_check = subprocess.run(
            ["git", "ls-remote", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        # If invalid url raise exception:
        if not repo_check.returncode == 0:
            raise RuntimeError('Invalid url.')
    except Exception as e:
        raise RuntimeError('Invalid url.')
    
    return True, "Valid URL and PAT token."


# Check terraform.tfvars exists:
def create_terraform_tfvars(path: str) -> bool:
    """
    This function checks if terraform tfvars exists.
    If it does not exist, it creates it.
    If it does exit it returns true. 

    Args: 
        path (str) path to terraform.tfvars.
       
    Returns:
        bool: True if terraform.tfvars exists
        bool: True fi terraform.tfvars successfully created.

    Raises:
        TypeError: if supplied path is not a string. 
    """

    # Check path str:
    if not isinstance(path, str):
        raise TypeError('Path must be a string.')

    # If terraform.tfvars does not exist create it:
    if not os.path.exists(path):
        try:
            with open(path, 'w') as f:
                f.write('')
                return True, "terraform.tfvars created successfully."
        except IOError as e:
            raise IOError(f"Failed to create terraform .tfvars: {str(e)}")
    return True, "terraform.tfvars already exists."


def update_terraform_tfvars(path: str):
    """
    This function reads from terraform tfvars. 
    It looks for a git_url, git_pat and git_user.
    If they do not exist, it will prompt the user for them.
    """

    # Check path is string:
    if not isinstance(path, str):
        raise TypeError('Path should be string.')
    
    # Read from terraform.tfvars:
    with open(path, 'r+') as f:
        data = f.read()
        

    # Check git_url exists:
    if not "git_user" in data:
        git_user = input('Please enter your git user name.')
    # If git_url exists overwrite?
    else:
        # Prompt user to overwrite or not:
        questions = [
        inquirer.List('choice',
                      message="Git_user already exists.  Would you like to overwrite?",
                      choices=['yes', 'no'],
                      )]
        answer = inquirer.prompt(questions)
        
        # Prompt to overwrite:
        if answer['choice'] == 'yes':
            # Prompt user to input user:
            git_user = input('Please enter your git user.')
        else:
            # Grab existing git_user:
            git_user = data.split('\n')[0][12:-1]

    # Check git_pat exists:
    if not "git_pat" in data:
        git_pat = input('Please enter your git pat token.')
    else:
        # Prompt user to overwrite or not:
        questions = [
        inquirer.List('choice',
                      message="Git_pat already exists.  Would you like to overwrite?",
                      choices=['yes', 'no'],
                      )]
        answer = inquirer.prompt(questions)
        
        # Prompt to overwrite:
        if answer['choice'] == 'yes':
            # Prompt user to input user:
            git_pat = input('Please enter your git pat.')
        else:
            # Grab existing git_user:
            git_pat = data.split('\n')[1][11:-1]
        

    # Check git_url exists:
    if not "git_url" in data:
        git_url = input('Please enter your git url.')
    else:
        # Prompt user to overwrite or not:
        questions = [
        inquirer.List('choice',
                      message="Git_url already exists.  Would you like to overwrite?",
                      choices=['yes', 'no'],
                      )]
        answer = inquirer.prompt(questions)
        
        # Prompt to overwrite:
        if answer['choice'] == 'yes':
            # Prompt user to input user:
            git_url = input('Please enter your git url.')
        else:
            # Grab existing git_user:
            git_url = data.split('\n')[2][11:-1]

    # Write variables to terraform.tfvars:
    try:  
        with open(path, 'w') as f:
            # Write the user credentials to the file:
            f.write(f'git_user = "{git_user}"\n')
            f.write(f'git_pat = "{git_pat}"\n')
            f.write(f'git_url = "{git_url}"\n')
        return True, 'Terraform.tfvars now exists with variables.'
    except Exception as e:
        print('Error: ', e)
    

def read_terraform_tfvars(path):
    with open(path, 'r') as f:
        data = f.read()
        git_url = data.split('\n')[2][11:-1]
        git_pat = data.split('\n')[1][11:-1]
    return [git_url, git_pat]

    

# Create terraform tfvars if does not exist:
create_terraform_tfvars(path)
# Update terraform tfvars with user cred:
update_terraform_tfvars(path)
# Read data from terraform tfvars:
git_url, git_pat = read_terraform_tfvars(path)
# # Check credentials valid:
validate_git_credentials(git_url, git_pat)








