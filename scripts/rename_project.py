import os
import sys

from scripts.gitignore_parser import parse_gitignore

original_author = "wjshan"
original_name = "user_role"
original_urlname = "user-role"
original_description = "Awesome user_role created by wjshan"


def sed(path, origin: str, dest: str) -> None:
    matches = parse_gitignore(os.path.join(path, ".gitignore"))
    for root, dirs, files in os.walk(path):
        if matches(root):
            continue
        for file in files:
            if file == "rename_project.py":
                continue
            file_path = os.path.join(root, file)
            if matches(file_path):
                continue
            try:
                with open(file_path) as f:
                    contents = f.read()
            except:
                continue
            new_contents = contents.replace(origin, dest)
            with open(file_path, "w") as f:
                f.write(new_contents)


def wait_user_input(message: str, default: str = "") -> str:
    print(f"{message} (default is '{default}'): ", end="")
    return input() or default


if __name__ == "__main__":

    author = wait_user_input("please input auth", default="shujian")
    name = wait_user_input("please input user_role", default="user_role")
    url_name = wait_user_input("please input url name", default=name)
    description = wait_user_input("please input description", default="")

    yon = wait_user_input(
        f"whether to confirm that:\n\t auth={author}\n\t user-role={name}\n\t url_name={url_name}\n\t description={description}\n\t",
        default="Y")
    root_path, *other = sys.argv[1:]
    if yon.lower() in ['y', 'yes']:
        sed(path=".", origin=original_author, dest=author)
        sed(path=root_path, origin=original_name, dest=name)
        sed(path=root_path, origin=original_urlname, dest=url_name)
        sed(path=root_path, origin=original_description, dest=description)
        os.rename(f"{root_path}/{original_name}", os.path.join(root_path, name))
