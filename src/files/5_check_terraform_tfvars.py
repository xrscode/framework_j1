import os
import requests
import json

"""
In order for terraform to deploy correctly, terraform.tfvars will need to be created.
It needs to be populated with GIT credentials. 
"""

# Define path to terraform .tfvars:
path = './terraform/terraform.tfvars'

# Function to check valid git credentials:
def check_git_url(url: str) -> bool:
    # Check inputs are strings:
    if isinstance(url, str):
        print('Credential format is valid, checking if credentials are valid...')

        # Check if url is valid:
        response = requests.get(url)
        # Check url correct:
        if response.status_code == 200:
            print(f'Credentials are valid.  Status code: {response.status_code}')
        else:
            print('Credentials are invalid.')
            raise Exception('Invalid credentials.')
    else:
        raise Exception('Credential is invalid format.  Must be string.')



# Check if terraform.tfvars exists:
if os.path.exists(path):
    print('terraform.tfvars already exists.')
    print('Do you want to overwrite it? (y/n)')
    overwrite = input()
    if overwrite == 'y':
        git_user = input('Please enter your git user name:')
        git_pat = input('Please enter your git personal access token:')
        git_url = input('Please enter the git repository url:')
        
        with open(path, 'w') as f:
            f.write(f'git_user = "{git_user}"\n')
            f.write(f'git_pat = "{git_pat}"\n')
            f.write(f'git_url = "{git_url}"\n')
            print('terraform.tfvars has been overwritten.')
        
        # Check url valid:
        check_git_url(git_url)

    else:
        print('terraform.tfvars has not been overwritten.\nChecking existing credentials...')
        # Extract and read url from terraform.tfvars
        with open(path, 'r') as f:
            data = f.read()
            data = data.split('\n')[2]
            git_url = data[11:-1]
            # Check url valid:
            check_git_url(git_url)


# Create terraform.tfvars:
else:
    # Prompt for git credentials:
    git_user = input('Please enter your git user name:')
    git_pat = input('Please enter your git personal access token:')
    git_url = input('Please enter the git repository url:')

    # Create the file
    with open(path, 'w') as f:
        # Write the user credentials to the file:
        f.write(f'git_user = "{git_user}"\n')
        f.write(f'git_pat = "{git_pat}"\n')
        f.write(f'git_url = "{git_url}"\n')
        print('terraform.tfvars been created.')

            
           

