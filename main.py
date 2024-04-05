import os, pickle
from PIL import Image
from rich.progress import track


def store_data(data):
    with open("convert_pickle", "wb") as file:
        pickle.dump(data, file)


def load_data():
    file_name = "convert_pickle"
    if not os.path.exists(file_name):
        return {}
    with open(file_name, "rb") as file:
        data = pickle.load(file)
        return data


def convert_dds_to_png(input_file, output_file):
    try:
        image = Image.open(input_file)
        image.save(output_file, "PNG")
        return True
    except Exception as e:
        print(e)  # comment this line out if there are too many errors
        return False


def find_all_files_by_type(file_type: str) -> list[dict]:
    """
    Returns a list of paths to files found with `file_type`.
    """
    found_files = []
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name.lower().endswith(file_type):
                file_path = os.path.join(root, name)
                found_files.append({"name": name, "path": file_path})
    return found_files


def is_plural(length: int) -> str:
    return "s" if length > 1 else ""


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

    existing_data = load_data().get("failed", None)
    if existing_data:
        total = len(existing_data)
        print(
            f"\nFound {total} file{is_plural(total)} that failed to be converted previously",
            "\nRetrying now",
        )
        found_files = existing_data
    else:
        found_files = find_all_files_by_type(target_file_type)
        total = len(found_files)
        print(f"\nFound {total} file{is_plural(total)} with {target_file_type} type")

    print()
    data = {"converted": [], "failed": []}
    converted = []
    failures = []
    for file in track(found_files, description="Converting Files"):
        # skips non .dds files
        if not file["name"].endswith(target_file_type):
            continue
        # updates name and path to new file type
        new_name = file["name"].replace(target_file_type, final_file_type)
        new_file_path = os.path.join(destination_folder, new_name)
        # adds to file if it succeeded and if it failed
        if convert_dds_to_png(file["path"], new_file_path):
            converted.append(file)
        else:
            failures.append(file)

    if converted:
        total = len(converted)
        print(f"\nSuccessfuly converted {len(converted)} file{is_plural(total)}")
        data["converted"] = converted
    else:
        print(f"\nNo files were found that could be converted")

    if failures:
        data["failed"] = failures
    store_data(data)


if __name__ == "__main__":
    destination_folder = "./converted_pngs/"
    convert_all_dds_files(destination_folder)
