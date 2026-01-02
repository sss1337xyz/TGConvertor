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

    session_string = "AQAAAAQAkyv7HRC2O4_3O69RBhIzk8m5WOVodg1tYYy6aI2NSH18InRT_hz2BHTkhyXiXb7_YXBOZWRotF5O4eIGkV-tWSZr2FP5xhV5SFCxh_-N8I4XXk3rw4yql4adHRv3vR2KkDV09YlxdDxicIqfXrmQOBayu8utAaXlHT7a0EhvkyztQc_cgvoUxX7bVIAVKI1JU0JynU-fHSyfIDyTIlLMy7gLxm71tI6PYiDYCO5FndKlrah6o8rBnAw7csm8nKeOnWmDTYwV8biq2ot6z27k4QmLYKAlnzWRgECMt2jadaguEWrj4yw2GhPhbmjmdCpSDKdX_cxbAJ0Fkkl92bvxxAAAAAH_p5DKAA"

    session = SessionManager.from_pyrogram_string(session_string, data)
    print(session)

    resultStr = await session.to_pyrogram_file(Path("14795329405_new.session"))
    # session.to_pyrogram_string()
    print(f"New str, {resultStr}")  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == "__main__":
    asyncio.run(main())
