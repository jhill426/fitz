import os
import shutil

from textnode import TextNode, TextType


def copy_static_to_public(source_dir: str, dest_dir: str) -> None:
    """
    Recursively copy all contents from source_dir to dest_dir.
    First deletes all contents of dest_dir to ensure a clean copy.
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Create destination directory
    os.mkdir(dest_dir)

    def copy_recursive(src: str, dst: str) -> None:
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copied: {src_path} -> {dst_path}")
            else:
                os.mkdir(dst_path)
                copy_recursive(src_path, dst_path)

    copy_recursive(source_dir, dest_dir)


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")

    copy_static_to_public(static_dir, public_dir)

    text_node = TextNode("Hello", TextType.TEXT, "https://www.justinhill.xyz")
    print(text_node)


if __name__ == "__main__":
    main()
