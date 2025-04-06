import os
import shutil

# Files to keep
files_to_keep = [
    'main.py',
    'ui.py',
    'filters.py',
    'image_utils.py',
    'kernel_editor.py',
    'requirements.txt',
    'README.md',
    'cleanup.py',  # Keep this script
    '.clineignore'  # Keep this file if it exists
]

# Files to remove
files_to_remove = [
    'kernel_visualizer.py',
    'kernel_visualizer_simple.py',
    'kernel_visualizer_final.py',
    'step1_basic_setup.py',
    'step2_kernel_grid.py',
    'step3_image_loading.py',
    'step4_kernel_application.py',
    'test_image.py'
]

# Check if files exist and remove them
for file in files_to_remove:
    if os.path.exists(file):
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

# Check for any other .py files not in the keep list
for file in os.listdir('.'):
    if file.endswith('.py') and file not in files_to_keep and file not in files_to_remove:
        try:
            os.remove(file)
            print(f"Removed additional file: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

print("\nCleanup complete. Kept the following files:")
for file in files_to_keep:
    if os.path.exists(file):
        print(f"- {file}")

print("\nRun 'python main.py' to start the application.")