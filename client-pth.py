import socket  # Работа с TCP-соединениями

# Пользователь вводит адрес сервера и порт подключения
server_host = input("Введите адрес сервера (например, localhost): ")
server_port = int(input("Введите порт: "))

# Создание TCP сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение к удалённому серверу
client_socket.connect((server_host, server_port))
print("🔗 Установлено соединение с сервером.")

# Буфер для частично полученных данных
recv_buffer = ""

# Цикл общения с сервером
while True:
    # Получаем ввод пользователя
    user_input = input("Введите сообщение ('exit' — завершить): ")

    # Отправляем сообщение серверу (в конце символ новой строки)
    client_socket.send((user_input + "\n").encode("utf-8"))
    print("📨 Сообщение отправлено.")

    # Ждём ответ от сервера
    full_reply = ""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            # Сервер закрыл соединение
            break
        recv_buffer += chunk.decode("utf-8")
        if "\n" in recv_buffer:
            full_reply, recv_buffer = recv_buffer.split("\n", 1)
            break

    print("📥 Ответ от сервера:")
    print(full_reply)

    # Завершаем, если пользователь написал 'exit'
    if user_input.lower() == "exit":
        break

# Закрытие соединения
client_socket.close()
print("❎ Соединение с сервером завершено.")
