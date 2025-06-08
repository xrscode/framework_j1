import os
import sys
import subprocess
import pytest

"""
-----------------------------------------------------------------------------
BROKEN PIPELINE
-----------------------------------------------------------------------------

Uh oh...  The first rule of being a developer is to never make a 
MISTKAE!
That means that you will never have to fix anything - a real time saver!

It seems that a plucky young developer has created a partially working
ADF pipeline.  The problem?  It's not working as it should...

Perhaps you could lend a hand?

Open ADF and look at the pipeline editor.  There is a pipeline called:
'Broken Pipeline'. 

Please ensure that you have completed the preceeding challenges and you have
successfully run a pipeline for Adventure Works.
"""

# Go one level up from current file's directory
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

"""
CHANGE TO TEST 4!!!
"""
# Define path to the test file relative to project_root
pytest_4 = os.path.join(project_root, 'challenges', 'tests', 'test_challenge_5.py')
"""
CHANGE TO TEST 4!!!
"""

# Define function to run test_challenge_4:
def run_tests_and_main():
    """
    This function will run test_challenge_4.py.
    """

    # Run pytest programmatically
    result = pytest.main([pytest_4])  # or your specific test file/folder

    if result == 0:
        print("✅ All tests passed. Running main script...")
        subprocess.run([sys.executable, 'your_script.py'])  # replace with your target script
    else:
        print(f"❌ Tests failed with exit code {result}. Main script not executed.")


# Call the function.
run_tests_and_main()
    