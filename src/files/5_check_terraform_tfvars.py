import os
import subprocess
import inquirer

"""
For terraform to deploy correctly, terraform.tfvars will need to be created.
It needs to be populated with GIT credentials.
This python file will create terraform.tfvars with correct credentials.
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

    if "https://" not in url:
        raise ValueError('Please supply valid url.  https://...')

    # Check PAT:
    try:
        result = subprocess.run(["curl",
                                 "-s",
                                 "-I",
                                 "-H",
                                 f"Authorization: token {pat}",
                                 "https://api.github.com/user"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=10)
        # If invalid pat raise exception:
        if "HTTP/1.1 200 OK" not in result.stdout\
                and "HTTP/2 200" not in result.stdout:
            raise RuntimeError('Invalid PAT')

    except Exception as e:
        print('Error: ', {e})
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
        print('Error: ', {e})
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
    If they do exist, it will prompt user to replace if necessary.
    """

    # Check path is string:
    if not isinstance(path, str):
        raise TypeError('Path should be string.')

    # Read from terraform.tfvars:
    with open(path, 'r+') as f:
        data = f.read()

    # Dictionary to hold variable names:
    variables = {'git_user': None, 'git_pat': None, 'git_url': None}
    

    # Iterate through variables to check if they exist:
    for variable in variables:
        # If variable does not exist prompt user:
        if variable not in data:
            prompt = input(f'Please enter your {variable}.')
            # Update value in variables dictionary:
            variables[variable] = prompt  
        # If variable does exist prompt user to overwrite:
        else:
            # Convert data to list of 'key value pairs':
            values = data.strip().split('\n')
            # Iterate through the list of 'key value pairs':
            for key in values:
                # Check if the variable is in the key:
                if variable in key:
                    # Extract value:
                    value = key.split('=')[1].replace('"', '').strip()
                    
                    # Prompt user to overwrite or not:
                    questions = [
                        inquirer.List('choice',message=f"""
                            \n{variable}: '{value}'.
                            \nWould you like to overwrite?""",
                            choices=[
                                'No',
                                'Yes'],
                        )]
                    # Save the answer:
                    answer = inquirer.prompt(questions)
                    # Prompt to overwrite:
                    if answer['choice'] == 'Yes':
                        # Prompt user to input user:
                        variables[variable] = \
                            input(f'Please enter your {variable}.')
                    else:
                        # Grab existing git_user:
                        variables[variable] = value

    # Write variables to terraform.tfvars:
    try:
        with open(path, 'w') as f:
            # Write the user credentials to the file:
            f.write(f'git_user = "{variables["git_user"]}"\n')
            f.write(f'git_pat = "{variables["git_pat"]}"\n')
            f.write(f'git_url = "{variables["git_url"]}"\n')
        return True, 'Terraform.tfvars now exists with variables.'
    except Exception as e:
        print('Error: ', e)


def read_terraform_tfvars(path):
    """
    This function reads form terraform.tfvars.
    It aims to extract the data.

    Args:
        String path to file.

    Returns:
        list: [git url, git pat token]

    Raises:
        TypeError: if path is not a valid string.
        RuntimeError: if there is no data in terraform.tfvars.
    """
    if not isinstance(path, str):
        raise TypeError('Path should be a string.')

    with open(path, 'r') as f:
        # Open and read:
        data = f.read()
        # If no data error:
        if not data:
            raise RuntimeError('No data to read.')

        git_url = data.split('\n')[2][11:-1]
        git_pat = data.split('\n')[1][11:-1]

    return [git_url, git_pat]


# 1. Check if terraform.tfvars exist.  If not create:
create_terraform_tfvars(path)

# 2. Update credentials in terraform.tfvars:
update_terraform_tfvars(path)

# 3. Read from terraform.tfvars to extract git credentials:
git_url, git_pat = read_terraform_tfvars(path)

# 4. Check git_credentials are valid:
validate_git_credentials(git_url, git_pat)
