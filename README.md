# 1. Fork: framework_j1
In order to deploy resources, first you will need to fork the following git repository:

<!-- Git repo to fork -->
https://github.com/xrscode/framework_j1.git

Forking will create a personal copy of this repo.  It ensures that ADF and Databricks can
deploy correctly. 

# 2. Git: 
After forking the git repo, make sure you create a personal access token, so that
Terraform can access the repository.   Make a note of the following:
git_user: the git username you use to connect to git. 
git_pat: the git personal access token you created earlier. 
git_url: the url to your forked repo. 

During installation, you will be prompted to enter this information.

# 3. Install Terraform, ODBC & Python:
If you have not already installed Python, Terraform and/or ODBC drivers, do so before running install.ps1.
 <!--Python  -->
 Install Python
 
 <!-- Terraform -->
 First install chocolatey with administrator privileges.  This will make the terraform install easier. 
After chocolatey has been installed run the following command in the terminal:
'choco install terraform --pre'

<!-- ODBC -->
Go to this address:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16&redirectedfrom=MSDN
And install the latest ODBC driver for windows x64.

# 3. Run: .\install.ps1
In order to deploy the project, in the terminal run the following command:
'.\install.ps1'

Follow the prompts within the terminal. 
