#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// Структура для хранения пар (j, a^j mod p)
typedef struct
{
    long long j;
    long long value;
} baby_step;

// 1.быстрое возведение в степень по модулю
long long mod_pow(long long a, long long x, long long p)
{
    long long result = 1;
    a = a % p;
    while (x > 0)
    {
        if (x % 2 == 1)
            result = (result * a) % p;
        a = (a * a) % p;
        x /= 2;
    }
    return result;
}

// Объявление функции заранее
long long euclid_alg(long long a, long long b, long long *x, long long *y);

// Обратное по модулю
long long mod_inverse(long long a, long long p)
{
    long long x, y;
    long long g = euclid_alg(a, p, &x, &y);
    if (g != 1)
        return -1; // обратного не существует
    return (x % p + p) % p;
}

// 2.тест простоты Ферма
int ferm_test(long long p, int k)
{
    if (p <= 1)
        return 0;
    if (p == 2 || p == 3)
        return 1;

    for (int i = 0; i < k; i++)
    {
        long long a = 2 + rand() % (p - 3);
        if (mod_pow(a, p - 1, p) != 1)
            return 0;
    }
    return 1;
}

// 3.алгоритм Евклида
long long euclid_alg(long long a, long long b, long long *x, long long *y)
{
    if (b == 0)
    {
        *x = 1;
        *y = 0;
        return a;
    }
    long long x1, y1;
    long long g = euclid_alg(b, a % b, &x1, &y1);
    *x = y1;
    *y = x1 - (a / b) * y1;
    return g;
}

// 4. Алгоритм "Шаг младенца, шаг великана"
long long baby_step_giant_step(long long a, long long y, long long p)
{
    long long m = (long long)sqrt(p) + 1; // размер шага

    // Массив для baby steps
    baby_step *baby_steps = malloc(m * sizeof(baby_step));

    printf("Выполняем Baby Steps (m = %lld):\n", m);

    // Baby steps: вычисляем a^j mod p для j = 0, 1, ..., m-1
    long long gamma = 1;
    for (long long j = 0; j < m; j++)
    {
        baby_steps[j].j = j;
        baby_steps[j].value = gamma;
        printf("j = %lld: a^%lld ≡ %lld (mod %lld)\n", j, j, gamma, p);
        gamma = (gamma * a) % p;
    }

    printf("\nВыполняем Giant Steps:\n");

    // Giant steps: ищем совпадения
    long long factor = mod_pow(a, m, p);          // a^m mod p
    long long gamma_inv = mod_inverse(factor, p); // (a^m)^(-1) mod p

    if (gamma_inv == -1)
    {
        printf("Не удается найти обратный элемент\n");
        free(baby_steps);
        return -1;
    }

    long long current = y; // y * (a^(-m))^i

    for (long long i = 0; i < m; i++)
    {
        printf("i = %lld: ищем %lld среди baby steps...", i, current);

        // Ищем current среди baby steps
        for (long long j = 0; j < m; j++)
        {
            if (baby_steps[j].value == current)
            {
                long long x = i * m + j;
                printf(" НАЙДЕНО! j = %lld\n", j);
                printf("x = i*m + j = %lld*%lld + %lld = %lld\n", i, m, j, x);

                // Проверяем результат
                long long check = mod_pow(a, x, p);
                printf("Проверка: %lld^%lld ≡ %lld (mod %lld)\n", a, x, check, p);

                free(baby_steps);
                return x;
            }
        }
        printf(" не найдено\n");

        current = (current * gamma_inv) % p;
    }

    printf("Решение не найдено в диапазоне [0, %lld]\n", m * m);
    free(baby_steps);
    return -1;
}

// генерация случайного простого числа
long long simple_num_generate(int bits)
{
    long long num;
    do
    {
        num = rand() % (1 << bits);
        if (num < 3)
            num += 3;
    } while (!ferm_test(num, 5));
    return num;
}

// Функция Диффи-Хеллмана
long long diffie_hellman(long long p, long long g, long long X_A, long long X_B)
{
    long long Y_A = mod_pow(g, X_A, p);
    long long Y_B = mod_pow(g, X_B, p);
    long long K_A = mod_pow(Y_B, X_A, p);
    long long K_B = mod_pow(Y_A, X_B, p);
    printf("Общий ключ (A): %lld\n", K_A);
    printf("Общий ключ (B): %lld\n", K_B);
    return K_A;
}

int main()
{
    srand(time(NULL));

    int choice;
    long long a, b, c, res, x, y, g;

    while (1)
    {
        printf("1. возведение в степень по модулю\n");
        printf("2. тест простоты Ферма\n");
        printf("3. алгоритм Евклида\n");
        printf("4. дискретный логарифм (Baby Step Giant Step)\n");
        printf("5. Диффи-Хеллман (общий ключ)\n");
        printf("0. exit\n\n");

        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            printf("введите a, x, p: ");
            scanf("%lld %lld %lld", &a, &b, &c);
            res = mod_pow(a, b, c);
            printf("результат: %lld\n\n", res);
            break;

        case 2:
            printf("введите число для проверки: ");
            scanf("%lld", &a);
            if (ferm_test(a, 10))
                printf("%lld вероятно простое\n\n", a);
            else
                printf("%lld составное\n\n", a);
            break;

        case 3:
            printf("1. ввод с клавиатуры\n");
            printf("2. генерация случайных чисел\n");
            printf("3. генерация случайных простых чисел\n\n");
            int mode;
            scanf("%d", &mode);

            if (mode == 1)
            {
                printf("введите a и b: ");
                scanf("%lld %lld", &a, &b);
            }
            else if (mode == 2)
            {
                a = rand() % 100 + 1;
                b = rand() % 100 + 1;
                printf("a = %lld, b = %lld\n", a, b);
            }
            else if (mode == 3)
            {
                a = simple_num_generate(10);
                b = simple_num_generate(10);
                printf("a = %lld, b = %lld\n", a, b);
            }
            else
            {
                printf("error choice\n\n");
                break;
            }

            g = euclid_alg(a, b, &x, &y);
            printf("НОД = %lld\n", g);
            printf("x = %lld, y = %lld\n\n", x, y);
            break;

        case 4:
            printf("Решение уравнения a^x ≡ y (mod p)\n");
            printf("1. ввод параметров с клавиатуры\n");
            printf("2. генерация параметров внутри функции\n\n");

            int dl_mode;
            scanf("%d", &dl_mode);

            if (dl_mode == 1)
            {
                printf("введите a, y, p: ");
                scanf("%lld %lld %lld", &a, &y, &c);
            }
            else if (dl_mode == 2)
            {
                // Генерируем параметры
                c = simple_num_generate(8);           // простое число p (небольшое для демонстрации)
                a = 2 + rand() % (c - 2);             // основание a
                long long secret_x = 1 + rand() % 20; // секретный x
                y = mod_pow(a, secret_x, c);          // вычисляем y = a^x mod p

                printf("Сгенерированы параметры:\n");
                printf("p = %lld (простое число)\n", c);
                printf("a = %lld (основание)\n", a);
                printf("Секретный x = %lld\n", secret_x);
                printf("y = a^x mod p = %lld\n\n", y);
            }
            else
            {
                printf("error choice\n\n");
                break;
            }

            if (!ferm_test(c, 5))
            {
                printf("Внимание: p = %lld может быть не простым числом\n", c);
            }

            printf("Решаем: %lld^x ≡ %lld (mod %lld)\n\n", a, y, c);

            long long result_x = baby_step_giant_step(a, y, c);

            if (result_x != -1)
            {
                printf("\nРешение найдено: x = %lld\n", result_x);
            }
            else
            {
                printf("\nРешение не найдено\n");
            }
            printf("\n");
            break;

        case 5:
        {
            printf("Диффи-Хеллман: выбрать режим ввода\n");
            printf("1. Ввод p, g, X_A, X_B с клавиатуры\n");
            printf("2. Генерация p, g, X_A, X_B внутри функции\n\n");
            int dh_mode;
            scanf("%d", &dh_mode);
            long long p, g, X_A, X_B;
            if (dh_mode == 1)
            {
                printf("Введите простое число p: ");
                scanf("%lld", &p);
                printf("Введите генератор g: ");
                scanf("%lld", &g);
                printf("Введите секрет X_A: ");
                scanf("%lld", &X_A);
                printf("Введите секрет X_B: ");
                scanf("%lld", &X_B);
            }
            else if (dh_mode == 2)
            {
                p = simple_num_generate(20);
                g = 2; // Можно заменить на генерацию генератора
                X_A = rand() % (p - 2) + 1;
                X_B = rand() % (p - 2) + 1;
                printf("Сгенерированы параметры:\n");
                printf("p = %lld\n", p);
                printf("g = %lld\n", g);
                printf("X_A = %lld\n", X_A);
                printf("X_B = %lld\n", X_B);
            }
            else
            {
                printf("Неверный выбор режима.\n\n");
                break;
            }
            diffie_hellman(p, g, X_A, X_B);
            break;
        }

        case 0:
            return 0;

        default:
            printf("error choice\n\n");
        }
    }

    return 0;
}