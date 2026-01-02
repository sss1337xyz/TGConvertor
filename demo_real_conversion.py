"""
Демонстрация реальной конвертации между форматами
"""

import asyncio
from pathlib import Path

from opentele.api import APIData

from TGConvertor.manager import SessionManager


async def main():
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ: Конвертация Telethon -> Pyrogram")
    print("=" * 70)

    # API данные
    data = APIData(
        api_id=4,
        api_hash="014b35b6184100b085b0d0572f9b5103",
        device_model="Samsung Galaxy Tab A7 Lite",
        system_version="SDK 30",
        app_version="11.7.0 (56632)",
        lang_code="es",
        lang_pack="android",
    )

    print("\n1. Загрузка Telethon сессии из файла")
    print("-" * 70)
    session = await SessionManager.from_telethon_file("573155734650.session", data)

    print(f"   ✓ DC ID: {session.dc_id}")
    print(f"   ✓ Server Address: {session.server_address}")
    print(f"   ✓ Port: {session.port}")
    print(f"   ✓ User ID: {session.user_id}")
    print(f"   ✓ Auth Key: {session.auth_key[:20].hex()}... (256 байт)")

    print("\n2. Конвертация в Pyrogram Session String")
    print("-" * 70)
    session_string = session.to_pyrogram_string()
    print(f"   Session String (первые 80 символов):")
    print(f"   {session_string[:80]}...")
    print(f"   Полная длина: {len(session_string)} символов")

    print("\n3. Что содержится в Session String:")
    print("-" * 70)
    print("   ✓ DC ID (1 байт)")
    print("   ✓ API ID (4 байта)")
    print("   ✓ Test Mode (1 байт)")
    print("   ✓ Auth Key (256 байт) - САМОЕ ВАЖНОЕ!")
    print("   ✓ User ID (8 байт)")
    print("   ✓ Is Bot (1 байт)")
    print("   " + "-" * 50)
    print("   ИТОГО: 271 байт -> ~362 символа в Base64")

    print("\n4. Что НЕ сохраняется в Session String:")
    print("-" * 70)
    print("   ✗ Server Address (149.154.175.51)")
    print("   ✗ Port (443)")
    print("   ✗ Peers (контакты, чаты)")
    print("   ✗ Update State")
    print("   ")
    print("   Примечание: Клиент автоматически узнает server_address")
    print("   и port по DC ID из встроенной таблицы Telegram серверов")

    print("\n5. Сохранение в Pyrogram файл (.session)")
    print("-" * 70)
    await session.to_pyrogram_file(Path("demo_output.session"))
    print("   ✓ Файл demo_output.session создан")

    # Проверяем содержимое
    import aiosqlite

    async with aiosqlite.connect("demo_output.session") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM sessions") as cursor:
            saved_session = await cursor.fetchone()
            result = dict(saved_session)

    print("\n6. Содержимое сохраненного файла:")
    print("-" * 70)
    print(f"   ✓ DC ID: {result['dc_id']}")
    print(f"   ✓ Server Address: {result['server_address']}")
    print(f"   ✓ Port: {result['port']}")
    print(f"   ✓ API ID: {result['api_id']}")
    print(f"   ✓ Test Mode: {result['test_mode']}")
    print(f"   ✓ User ID: {result['user_id']}")
    print(f"   ✓ Is Bot: {result['is_bot']}")
    print(f"   ✓ Auth Key: {result['auth_key'][:20].hex()}... (256 байт)")

    print("\n" + "=" * 70)
    print("ИТОГ:")
    print("=" * 70)
    print("Session String - компактный формат для передачи")
    print("Session File - полный формат с кэшем и дополнительными данными")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
