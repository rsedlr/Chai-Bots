from credentials import DEVELOPER_KEY, DEVELOPER_UID
from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment
from chai_py import share_bot, display_logs, get_logs
from chai_py.auth import set_auth
from bot.bot import Bot

# Make sure you call set_auth before packaging and deploying.
# After you call set_auth, your uid and key are used throughout.

set_auth(DEVELOPER_UID, DEVELOPER_KEY)

BOT_IMAGE_URL = "https://image.emojipng.com/971/35971.jpg"
# BOT_IMAGE_URL = "https://picsum.photos/seed/example_bot/256/256"


package(
    Metadata(
        name="Joe",
        image_url=BOT_IMAGE_URL,
        color="0000ff",
        description="Hey, come chat with me!",
        input_class=Bot,
        developer_uid=DEVELOPER_UID,
        memory=512,
    ),
    # requirements=["re"],
)

print()

bot_uid = upload_and_deploy("bot/_package.zip")

wait_for_deployment(bot_uid)

share_bot(bot_uid)
