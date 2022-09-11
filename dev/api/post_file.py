import aiohttp
import asyncio
import uuid

IP_ADDRESS = "localhost"
IMAGE_PATH = (
    "/home/prominendt/datasets/oxford-IIIT-pet-dataset/images/Abyssinian_10.jpg"
)


def get_image_bytes(image_path: str = IMAGE_PATH):
    with open(image_path, "rb") as f:
        return f.read()


def get_tasks(session, url, file_bytes):
    tasks = []
    for _ in range(1000):
        data = aiohttp.FormData()
        data.add_field(
            "file",
            file_bytes,
            filename=get_random_file_name(),
            content_type="image/png",
        )
        tasks.append(session.post(url, data=data, verify_ssl=False))
    return tasks


async def post_images(url, file_bytes):

    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, url, file_bytes)
        responses = await asyncio.gather(*tasks)

        print([r.status for r in responses])


def get_random_file_name():
    return str(uuid.uuid4()) + ".png"


async def main():
    image_bytes = get_image_bytes()

    await post_images(
        url=f"http://{IP_ADDRESS}:7000/files",
        file_bytes=image_bytes,
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
