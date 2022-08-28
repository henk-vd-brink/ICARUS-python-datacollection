import os
import shutil
import requests
import textwrap
import uuid
import asyncio

IP_ADDRESS = "localhost"
FILE_PATH = "/home/prominendt/datasets/oxford-IIIT-pet-dataset/images/Abyssinian_10.jpg"


def post_file(
    url=f"http://{IP_ADDRESS}:7000/files", file_path=FILE_PATH, tmp_path="/tmp", id=None
):
    tmp_file_name = str(uuid.uuid4()) + ".jpg"
    tmp_file_path = tmp_path + "/" + tmp_file_name

    shutil.copyfile(file_path, tmp_file_path)

    with open(tmp_file_path, "rb") as f:
        file = {"file": f}

        try:
            response = requests.post(url, files=file, verify=False)
            log_msg = textwrap.dedent(
                f"""\
                id: {id}
                    status_code: {response.status_code}
                    tmp_file_name: {tmp_file_name}
                """
            )
            print(log_msg)
        except Exception as e:
            print(e)
        finally:
            os.remove(tmp_file_path)


if __name__ == "__main__":
    for id in range(1000):
        post_file(id=id)
