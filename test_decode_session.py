"""
Тест декодирования Session String
Показывает все данные, которые хранятся в Session String
"""

import base64
import struct

# Session String для декодирования
session_string = "AQAAAAQAhIwl0dVvXYdTZkmvNzPHt4h9XzZSYOTCN_xjPAhE4Hfjfmra-NgrvLfZqekR61R48lmF7eiop2EApC82sLNVEFvjNXNi0KPoQuKcV5safsdMZZrC6upppmwyVWafVkWsOUZqUS4JSbVOGE7sMQGSnSPU7oV8ClAXD1A-P0t-rE-K9OOfW-qS9cw0gY3uoTI6EHOsDL_B33tjf-vkSCrwg9z-u2U7oRgTygQJOgVpZyGSy0zfPSwRMwi1P-BZTquUuVBV1TCYfzyunQbOpn_bPMx-rvg0sRYfjQci5_Lm_4o9OoBYfocaK1XXtN95JkIjxMk_b4wOR6JlAnwu2ZqL-wAAAAH5ANSDAA"

# Формат данных Pyrogram
STRING_FORMAT = ">BI?256sQ?"

print("=" * 80)
print("ДЕКОДИРОВАНИЕ PYROGRAM SESSION STRING")
print("=" * 80)

print(f"\nИсходная Session String:")
print(f"Длина: {len(session_string)} символов")
print(f"Первые 80 символов: {session_string[:80]}...")

print("\n" + "=" * 80)
print("ШАГ 1: Восстановление Base64 padding")
print("=" * 80)

# Base64 требует, чтобы длина была кратна 4
padding_needed = -len(session_string) % 4
padding = "=" * padding_needed
session_with_padding = session_string + padding

print(f"Длина строки: {len(session_string)}")
print(f"Нужно добавить padding символов: {padding_needed}")
print(f"Строка с padding: {len(session_with_padding)} символов")

print("\n" + "=" * 80)
print("ШАГ 2: Декодирование из Base64")
print("=" * 80)

try:
    decoded_bytes = base64.urlsafe_b64decode(session_with_padding)
    print(f"✓ Успешно декодировано")
    print(f"Размер декодированных данных: {len(decoded_bytes)} байт")
    print(f"Первые 20 байт (hex): {decoded_bytes[:20].hex()}")
except Exception as e:
    print(f"✗ Ошибка декодирования: {e}")
    exit(1)

print("\n" + "=" * 80)
print("ШАГ 3: Распаковка бинарных данных")
print("=" * 80)

print(f"Формат распаковки: {STRING_FORMAT}")
print("Расшифровка формата:")
print("  > - Big-endian (старший байт первым)")
print("  B - unsigned char (1 байт) = dc_id")
print("  I - unsigned int (4 байта) = api_id")
print("  ? - bool (1 байт) = test_mode")
print("  256s - char[256] (256 байт) = auth_key")
print("  Q - unsigned long long (8 байт) = user_id")
print("  ? - bool (1 байт) = is_bot")
print()

try:
    dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
        STRING_FORMAT, decoded_bytes
    )
    print("✓ Успешно распаковано")
except Exception as e:
    print(f"✗ Ошибка распаковки: {e}")
    exit(1)

print("\n" + "=" * 80)
print("РЕЗУЛЬТАТ ДЕКОДИРОВАНИЯ")
print("=" * 80)

print(f"\n📍 DC ID (Data Center ID): {dc_id}")
dc_locations = {
    1: "США, Майами",
    2: "Нидерланды, Амстердам",
    3: "США, Майами",
    4: "Нидерланды, Амстердам",
    5: "Сингапур",
}
print(f"   Локация: {dc_locations.get(dc_id, 'Неизвестно')}")

print(f"\n🔑 API ID: {api_id}")
api_names = {4: "Telegram Android", 6: "Telegram Desktop", 2496: "Telegram Android X"}
print(f"   Приложение: {api_names.get(api_id, 'Кастомное приложение')}")

print(f"\n🧪 Test Mode: {test_mode}")
print(f"   Режим: {'Тестовый сервер' if test_mode else 'Продакшн сервер'}")

print(f"\n🔐 Auth Key (Ключ авторизации):")
print(f"   Размер: {len(auth_key)} байт")
print(f"   Первые 32 байта (hex): {auth_key[:32].hex()}")
print(f"   Последние 32 байта (hex): {auth_key[-32:].hex()}")
print(f"   ⚠️  КРИТИЧЕСКИ ВАЖНО: Это ваш секретный ключ!")

print(f"\n👤 User ID: {user_id}")

print(f"\n🤖 Is Bot: {is_bot}")
print(f"   Тип аккаунта: {'Бот' if is_bot else 'Обычный пользователь'}")

print("\n" + "=" * 80)
print("ВАЖНАЯ ИНФОРМАЦИЯ")
print("=" * 80)
print("\n✓ Что ЕСТЬ в Session String:")
print("  • DC ID - номер дата-центра")
print("  • API ID - идентификатор приложения")
print("  • Auth Key - секретный ключ авторизации (256 байт)")
print("  • User ID - ваш ID в Telegram")
print("  • Test Mode - флаг тестового режима")
print("  • Is Bot - флаг бот-аккаунта")

print("\n✗ Чего НЕТ в Session String:")
print("  • Server Address (например: 149.154.175.51)")
print("  • Port (например: 443)")
print("  • Peers - кэш контактов и чатов")
print("  • Update State - состояние обновлений")
print("  • Username - имя пользователя")
print("  • Phone Number - номер телефона")

print("\n💡 Как клиент определяет Server Address и Port?")
print("   Клиент использует встроенную таблицу серверов Telegram:")
print(f"   DC {dc_id} → 149.154.175.{50 + dc_id}:443 (примерный адрес)")

print("\n⚠️  БЕЗОПАСНОСТЬ:")
print("   Session String содержит Auth Key - НЕ ПЕРЕДАВАЙТЕ его никому!")
print("   Любой, у кого есть ваш session string, может получить доступ")
print("   к вашему аккаунту Telegram!")

print("\n" + "=" * 80)
