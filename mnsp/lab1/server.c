#include <zmq.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>

int main(void)
{
    void *context = zmq_ctx_new();
    void *responder = zmq_socket(context, ZMQ_REP);
    int rc = zmq_bind(responder, "tcp://*:5555");
    assert(rc == 0);

    char last_message[256] = "Нет новых сообщений";

    printf("Сервер запущен на tcp://*:5555\n");

    while (1)
    {
        char buffer[256];
        int size = zmq_recv(responder, buffer, 255, 0);
        if (size == -1)
            break; // ошибка или завершение
        buffer[size] = '\0';

        printf("Получено: %s\n", buffer);

        // Отдаём клиенту последнее сообщение
        zmq_send(responder, last_message, strlen(last_message), 0);

        // Запоминаем новое сообщение для следующего клиента
        strncpy(last_message, buffer, sizeof(last_message) - 1);
        last_message[sizeof(last_message) - 1] = '\0';
    }

    zmq_close(responder);
    zmq_ctx_destroy(context);
    return 0;
}