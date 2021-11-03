from DrunkBot.credentials import DEVELOPER_KEY, DEVELOPER_UID
from chai_py.deployment import delete_bot
from chai_py.auth import set_auth
import sys

set_auth(DEVELOPER_UID, DEVELOPER_KEY)
delete_bot(bot_uid=sys.argv[1])