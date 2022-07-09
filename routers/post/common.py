from datetime import datetime

import exceptions


def get_unique_filename(filename: str) -> str:
    filename_splitted = filename.split(".")
    title, extension = "_".join(filename_splitted[:-1]), filename_splitted[-1]
    new_title = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + "____" + title
    new_filename = new_title + "." + extension
    return new_filename


def check_image_filename(filename):
    # TODO: Experiment with allowed_extensions
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if (
        filename[-3:] not in allowed_extensions
        and filename[-4:] not in allowed_extensions
    ):
        raise exceptions.InvalidImageExtension(filename)
