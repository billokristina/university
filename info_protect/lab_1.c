#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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

        case 0:
            return 0;

        default:
            printf("error choice\n\n");
        }
    }

    return 0;
}