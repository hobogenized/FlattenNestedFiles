# Quick and dirty script for flattening nested directories of files
# Aims are to be OS agnostic and non-destructive for relevant data
# Written as an initial attempt to help with Amazon Drive to Photos
#  conversion as Photos only allows flat album directories
import os
import shutil

def extract_ext(filename):
  return str.lower(filename.split('.')[-1])

flattened_path = "./flattened"

relevant_ext = [ "jpg" ]

try:
  os.mkdir(flattened_path)
except:
  print(flattened_path + " already exists")

num_dir = 0

# We'll skip directories as we'll deal with nested directories
# as they come
for path, _, files in os.walk('.'):
  filtered_files = []

  # Filter for relevant files; we are looking for specific file extensions
  for f in files:
    if (extract_ext(f) in relevant_ext):
      filtered_files.append(f)

  # Skip, no relevant files
  if not len(filtered_files):
    continue

  # Directory that files are copied to will be in 6 digit format
  # Ex: 000000, 000001, ..., 999999
  # TODO: Look into resuming instead of starting from scratch each time
  num_dir_str = "/{:06d}".format(num_dir)
  num_dir += 1
  full_new_dirpath = flattened_path + num_dir_str

  try:
    os.mkdir(full_new_dirpath)
  except:
    print("Directory " + full_new_dirpath + " already exists")

  # We write the original path for nested folders that files
  #  were located in; this will help with determining new
  #  name for folders later
  with open(full_new_dirpath + "/__path", 'w') as f:
    f.write(path)
    f.write("\n")

  # Copy each relevant file to new directory; using copy2 for
  #  preservation of metadata
  for f in filtered_files:
    try:
      shutil.copy2(path + "/" + f, full_new_dirpath + "/" + f)
    except Exception as e:
      print(e)
      # Abort program to examine exception
      # TODO: Determine additional exception handling
      return
