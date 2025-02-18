# Configure GitHub Git credentials
resource "databricks_git_credential" "git_auth" {
    git_provider = "github"
    git_username = var.git_user
    personal_access_token = var.git_pat
}

# Link Git Repository to Databricks Workspace
resource "databricks_repo" "j1_repo" {
    url = "https://github.com/xrscode/framework_j1.git"
    provider = databricks
    path = "/Repos/Git/jf1"
    git_provider = "github"
    # Ensure GitHub credentials are set first:
    depends_on = [ databricks_git_credential.git_auth ]
}