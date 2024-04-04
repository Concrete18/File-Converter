import os
from PIL import Image
from rich.progress import track


def convert_dds_to_png(input_file, output_file):
    try:
        image = Image.open(input_file)
        image.save(output_file, "PNG")
        return True
    except:
        return False


def find_all_files_by_type(file_type: str) -> list[dict]:
    """
    Returns a list of paths to files found with `file_type`.
    """
    found_files = []
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name.endswith(file_type):
                file_path = os.path.join(root, name)
                found_files.append({"name": name, "path": file_path})
    total = len(found_files)
    print(f"Found {total} file{is_plural(total)} with {file_type} type")
    return found_files


def is_plural(list):
    return "s" if list > 1 else ""


def convert_all_dds_files(destination_folder):
    """
    Finds and converts all .DDS files, within the folder the script is run in, into .PNG's.
    """
    target_file_type = ".dds"
    final_file_type = ".png"
    print(
        "Finding and converting files",
        f"\nConverted files will be located in {destination_folder}",
    )
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    print("----------------------------------------------------")
    total_convers = 0
    failures = []

    found_files = find_all_files_by_type(target_file_type)

    print()
    desc = "Converting Files"
    for file in track(found_files, description=desc):
        # skips non .dds files
        if not file["name"].endswith(target_file_type):
            continue
        # updates name and path to new file type
        new_name = file["name"].replace(target_file_type, final_file_type)
        new_file_path = os.path.join(destination_folder, new_name)

        if convert_dds_to_png(file["path"], new_file_path):
            total_convers += 1
        else:
            failures.append(file["path"])

    if total_convers:
        print(f"\nSuccessfuly converted {total_convers} file{is_plural(total_convers)}")
    else:
        print(f"\nNo files were found that could be converted")

    if failures:
        print(f"\nFailed to convert {len(failures)} files at the following paths\n")
        for n, path in enumerate(failures):
            print(f"{n+1}: {path}")


if __name__ == "__main__":
    destination_folder = "./converted_pngs/"
    convert_all_dds_files(destination_folder)
