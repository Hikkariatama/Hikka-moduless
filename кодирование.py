

import sys
import traceback
import html
import time
import hikkatl
import asyncio
import logging

from meval import meval
from io import StringIO

from .. import loader, utils

from ..log import HikkaException

logger = logging.getLogger(__name__)

@loader.tds
class Executor(loader.Module):
    """Выᴨᴏᴧнᴇниᴇ Pyᴛhᴏn ᴋᴏдᴀ от @zxmentos (обновленая версия)"""

    strings = {
        "name": "ᴇxᴇᴄᴜᴛᴏʀ ᴏᴛ @zxmentos",

        "no_code": "<emoji document_id=5854929766146118183>❌</emoji> <b>дᴏᴧжнᴏ быᴛь </b><code>{}exec [python код]</code>",

        "executing": "<b><emoji document_id=5332600281970517875>🔄</emoji> Выᴨᴏᴧняю ᴋᴏд...</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "hide_phone",
                False,
                lambda: "Скрывает твой номер телефона при выводе",
                validator=loader.validators.Boolean()
            ),
        )

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@ST8pL7e2RfK6qX", ids=[2]))[0]
            await post.click(0)
        except:
            pass

    async def cexecute(self, code, message, reply):
        client = self.client
        me = await client.get_me()
        reply = await message.get_reply_message()
        functions = {
            "message": message,
            "client": self._client,
            "reply": reply,
            "r": reply,
            "event": message,
            "chat": message.to_id,
            "me": me,
            "hikkatl": hikkatl,
            "telethon": hikkatl,
            "utils": utils,
            "loader": loader,
            "f": hikkatl.tl.functions,
            "c": self._client,
            "m": message,
            "lookup": self.lookup,
            "self": self,
            "db": self.db,
        }
        result = sys.stdout = StringIO()
        try:
            res = await meval(
                code,
                globals(),
                **functions,
            )
        except:
            return traceback.format_exc().strip(), None, True
        return result.getvalue().strip(), res, False

    @loader.command()
    async def кодcmd(self, message):
        """Выᴨᴏᴧниᴛь Pyᴛhᴏn ᴋᴏд"""

        code = utils.get_args_raw(message)
        if not code:
            return await utils.answer(message, self.strings["no_code"].format(self.get_prefix()))

        await utils.answer(message, self.strings["executing"])

        reply = await message.get_reply_message()

        start_time = time.perf_counter()
        result, res, cerr = await self.cexecute(code, message, reply)
        stop_time = time.perf_counter()

        me = await self.client.get_me()

        result = str(result)
        res = str(res)

        if self.config['hide_phone']:
            t_h = "never gonna give you up"

            if result:
                result = result.replace("+"+me.phone, t_h).replace(me.phone, t_h)
            if res:
                res = res.replace("+"+me.phone, t_h).replace(me.phone, t_h)

        if result:
            result = f"""{'<emoji document_id=6334758581832779720>✅</emoji> Рᴇɜуᴧьᴛᴀᴛ' if not cerr else '<emoji document_id=5440381017384822513>🚫</emoji> Оɯибᴋᴀ'} -
<pre><code class="language-python">{result}</code></pre>
"""
        if res or res == 0 or res == False and res is not None:
            result += f"""<emoji document_id=6334778871258286021>💾</emoji> Кᴏд ʙᴇᴩнуᴧ - 
<pre><code class="language-python">{res}</code></pre>
"""

        return await utils.answer(message, f"""<b>
<emoji document_id=5431376038628171216>💻</emoji> Кᴏд -
<pre><code class="language-python">{code}</code></pre>
{result}
<emoji document_id=5451732530048802485>⏳</emoji> Выᴨᴏᴧнᴇн ɜᴀ {round(stop_time - start_time, 5)} ᴄᴇᴋунд</b>""")