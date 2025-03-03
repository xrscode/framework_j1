import os

"""
In order for terraform to deploy correctly, terraform.tfvars will need to be created.
It needs to be populated with GIT credentials. 
"""

# Define path to terraform .tfvars:
path = './terraform/terraform.tfvars'

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
    else:
        print('terraform.tfvars has not been overwritten.')