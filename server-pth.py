import socket  # Работа с сетевыми соединениями

# Ввод порта от пользователя
port = int(input("Введите порт для запуска сервера: "))

# Инициализация TCP-сокета на IPv4
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Разрешаем повторное использование адреса
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Привязка сокета ко всем интерфейсам машины и выбранному порту
server_socket.bind(("0.0.0.0", port))

print("▶ Сервер запускается...")

# Слушаем подключения. Число в скобках — макс. число клиентов в очереди
server_socket.listen(1)
print(f"▶ Порт {port} ожидает подключений.")

# Цикл обработки подключений
while True:
    try:
        # Ожидаем клиента
        client_socket, client_addr = server_socket.accept()
        print("🟢 Подключен новый клиент.")
        print(f"📍 IP: {client_addr[0]}  |  Порт: {client_addr[1]}")

        buffer = ""  # Накопление данных

        # Приём и отправка сообщений
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("🔄 Клиент закрыл соединение.")
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(f"📩 Получено сообщение: {line}")

                if line.lower() == "exit":
                    print("❌ Команда 'exit'. Завершение общения с клиентом.")
                    client_socket.send("Сервер закрывает соединение.\n".encode("utf-8"))
                    break

                reply = line.upper()
                client_socket.send((reply + "\n").encode("utf-8"))
                print("📤 Ответ отправлен клиенту.")

            if line.lower() == "exit":
                break

        client_socket.close()
        print("🔒 Соединение завершено. Ожидание новых подключений...")

    except KeyboardInterrupt:
        print("\n⛔ Завершение работы сервера.")
        break

# Финальное закрытие сокета
server_socket.close()
print("🛑 Сервер выключен.")
