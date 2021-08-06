from credentials import DEVELOPER_KEY, DEVELOPER_UID
from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment
from chai_py import share_bot, display_logs, get_logs
from chai_py.auth import set_auth
from bot.bot import Bot

# Make sure you call set_auth before packaging and deploying.
# After you call set_auth, your uid and key are used throughout.

set_auth(DEVELOPER_UID, DEVELOPER_KEY)

BOT_IMAGE_URL = "https://images.squarespace-cdn.com/content/v1/5616ac17e4b018d366f57f53/1616923173664-5USKZPHNL65VM3F5T87Z/rick+sanchez+soundboard"
# BOT_IMAGE_URL = "https://picsum.photos/seed/example_bot/256/256"


package(
    Metadata(
        name="Rick Bot",
        image_url=BOT_IMAGE_URL,
        color="00ff00",
        description="Just a quick adventure Morty, in and out.",
        input_class=Bot,
        developer_uid=DEVELOPER_UID,
        memory=3000,
    ),
    # requirements=["re"],
)

print()

bot_uid = upload_and_deploy("bot/_package.zip")

wait_for_deployment(bot_uid)

share_bot(bot_uid)
