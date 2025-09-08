#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Использование: %s <имя>\n", argv[0]);
        return 1;
    }
    const char *name = argv[1];

    void *context = zmq_ctx_new();
    void *requester = zmq_socket(context, ZMQ_REQ);
    zmq_connect(requester, "tcp://localhost:5555");

    char message[256];
    char buffer[256];

    while (1)
    {
        printf("%s > ", name);
        fflush(stdout);

        if (!fgets(message, 256, stdin))
            break;
        message[strcspn(message, "\n")] = '\0'; // убрать \n

        // Формируем строку "Имя: сообщение"
        char fullmsg[300];
        snprintf(fullmsg, sizeof(fullmsg), "%s: %s", name, message);

        // Отправляем на сервер
        zmq_send(requester, fullmsg, strlen(fullmsg), 0);

        // Ждём ответ (последнее сообщение от другого клиента)
        int size = zmq_recv(requester, buffer, 255, 0);
        if (size > 0)
        {
            buffer[size] = '\0';
            printf("[Чат] %s\n", buffer);
        }
    }

    zmq_close(requester);
    zmq_ctx_destroy(context);
    return 0;
}