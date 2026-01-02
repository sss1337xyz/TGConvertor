import asyncio
from pathlib import Path

from opentele.api import API, APIData

from TGConvertor import SessionManager


async def main():
    data = APIData(
        api_id=4,
        api_hash="014b35b6184100b085b0d0572f9b5103",
        device_model="SamsungGalaxy Tab A7 Lite",
        system_version="SDK 30",
        app_version="11.7.0 (56632)",
        lang_code="es",
        lang_pack="android",
    )
    session = await SessionManager.from_pyrogram_file("14795329405.session", data)
    print(session)

    resultStr = session.to_pyrogram_string()
    # session.to_pyrogram_string()
    print(f"New str, {resultStr}")  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == "__main__":
    asyncio.run(main())
