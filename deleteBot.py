from DrunkBot.credentials import DEVELOPER_KEY, DEVELOPER_UID
from chai_py.deployment import delete_bot
from chai_py.auth import set_auth

set_auth(DEVELOPER_UID, DEVELOPER_KEY)

delete_bot(bot_uid="_bot_00c42083-9c1c-4a07-9092-51719068fd38")