"""
Объяснение работы Session String в Pyrogram

Session String - это компактное представление сессии в виде строки.
Вместо того чтобы хранить файл базы данных, все критически важные данные
упаковываются в одну строку.
"""

import base64
import struct

# Формат данных для упаковки (STRING_FORMAT = ">BI?256sQ?")
# Это описание того, как данные расположены в бинарном виде:
#
# >        - Big-endian (порядок байтов: старший байт первым)
# B        - unsigned char (1 байт) = dc_id
# I        - unsigned int (4 байта) = api_id
# ?        - bool (1 байт) = test_mode
# 256s     - char[256] (256 байт) = auth_key (ключ авторизации)
# Q        - unsigned long long (8 байт) = user_id
# ?        - bool (1 байт) = is_bot

STRING_FORMAT = ">BI?256sQ?"

# Пример данных сессии
dc_id = 1  # Data Center ID
api_id = 4  # Telegram API ID
test_mode = False  # Тестовый режим (обычно False)
auth_key = b"\x00" * 256  # Ключ авторизации (256 байт)
user_id = 7369209597  # ID пользователя
is_bot = False  # Это бот? (обычно False)

print("=" * 70)
print("ШАГ 1: Исходные данные")
print("=" * 70)
print(f"DC ID: {dc_id}")
print(f"API ID: {api_id}")
print(f"Test Mode: {test_mode}")
print(f"Auth Key: {auth_key[:20]}... (256 байт)")
print(f"User ID: {user_id}")
print(f"Is Bot: {is_bot}")

print("\n" + "=" * 70)
print("ШАГ 2: Упаковка в бинарный формат (struct.pack)")
print("=" * 70)
print("struct.pack() преобразует Python-объекты в последовательность байтов")
print(f"Формат упаковки: {STRING_FORMAT}")

packed = struct.pack(
    STRING_FORMAT,
    dc_id,  # 1 байт
    api_id,  # 4 байта
    test_mode,  # 1 байт
    auth_key,  # 256 байт
    user_id,  # 8 байт
    is_bot,  # 1 байт
)

print(f"Размер упакованных данных: {len(packed)} байт")
print(f"Первые 20 байт: {packed[:20]}")

print("\n" + "=" * 70)
print("ШАГ 3: Кодирование в Base64")
print("=" * 70)
print("Base64 преобразует бинарные данные в текстовую строку")
print("Использует только безопасные для URL символы: A-Z, a-z, 0-9, -, _")

encoded = base64.urlsafe_b64encode(packed).decode()
print(f"Длина закодированной строки: {len(encoded)} символов")
print(f"Base64 строка (первые 50 символов): {encoded[:50]}...")

print("\n" + "=" * 70)
print("ШАГ 4: Удаление padding символов '='")
print("=" * 70)
print("Base64 может добавлять '=' в конце для выравнивания")

session_string = encoded.rstrip("=")
print(f"Итоговая Session String (первые 50 символов): {session_string[:50]}...")
print(f"Полная длина: {len(session_string)} символов")

print("\n" + "=" * 70)
print("ОБРАТНЫЙ ПРОЦЕСС: Распаковка Session String")
print("=" * 70)

# ШАГ 1: Восстановление padding
print("\n1. Восстановление padding для Base64")
padding = "=" * (-len(session_string) % 4)
print(f"   Нужно добавить: {len(padding)} символов '='")

# ШАГ 2: Декодирование из Base64
print("\n2. Декодирование Base64 в бинарные данные")
decoded = base64.urlsafe_b64decode(session_string + padding)
print(f"   Получено {len(decoded)} байт")

# ШАГ 3: Распаковка структуры
print("\n3. Распаковка бинарных данных в Python-объекты")
(
    dc_id_decoded,
    api_id_decoded,
    test_mode_decoded,
    auth_key_decoded,
    user_id_decoded,
    is_bot_decoded,
) = struct.unpack(STRING_FORMAT, decoded)

print(f"   DC ID: {dc_id_decoded}")
print(f"   API ID: {api_id_decoded}")
print(f"   Test Mode: {test_mode_decoded}")
print(f"   Auth Key: {auth_key_decoded[:20]}... (256 байт)")
print(f"   User ID: {user_id_decoded}")
print(f"   Is Bot: {is_bot_decoded}")

print("\n" + "=" * 70)
print("ВАЖНО! Что НЕ включено в Session String:")
print("=" * 70)
print("✗ server_address - адрес сервера (149.154.175.51)")
print("✗ port - порт сервера (443)")
print("✗ peers - кэш контактов и чатов")
print("✗ update_state - состояние обновлений")
print("")
print("Эти данные хранятся только в файле сессии (.session)")
print("При использовании session string клиент автоматически определяет")
print("server_address и port по dc_id из встроенной таблицы серверов Telegram")
print("=" * 70)
