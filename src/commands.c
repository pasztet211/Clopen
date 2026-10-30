#include "commands.h"
#include "helper_commands.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>

char *trim_copy(const char *start, size_t length)
{
    while (length && isspace((unsigned char)*start)) {
        start++;
        length--;
    }

    while (length && isspace((unsigned char)start[length - 1])) {
        length--;
    }

    char *result = malloc(length + 1);

    if (!result)
        return NULL;

    memcpy(result, start, length);
    result[length] = '\0';

    return result;
}

int resolve_operand(
    const char *text,
    Scope *scope,
    Operand *result
)
{
    result->value = trim_copy(text, strlen(text));

    if (!result->value)
        return 1;

    size_t length = strlen(result->value);

    /* String literal */
    if (length >= 2 &&
        result->value[0] == '"' &&
        result->value[length - 1] == '"')
    {
        memmove(result->value, result->value + 1, length - 2);
        result->value[length - 2] = '\0';
        result->type = "str";
        return 0;
    }

    /* Variable */
    Variable *variable = find_variable(scope, result->value);

    if (variable)
    {
        char *value = copy_string(variable->value);

        if (!value) {
            free(result->value);
            return 1;
        }

        free(result->value);
        result->value = value;
        result->type = variable->type;
        return 0;
    }

    /* Numeric literal */
    char *end;
    errno = 0;
    strtod(result->value, &end);

    if (end != result->value && *end == '\0' && errno != ERANGE)
        result->type = "number";
    else
        result->type = "str";

    return 0;
}

int is_numeric_type(const char *type)
{
    return strcmp(type, "int") == 0 ||
           strcmp(type, "float") == 0 ||
           strcmp(type, "number") == 0;
}


static void log_value(const char *value, Scope *scope)
{
    size_t length = strlen(value);

    if (length >= 2 && value[0] == '"' && value[length - 1] == '"')
    {
        printf("%.*s", (int)(length - 2), value + 1);
        return;
    }

    if (value[0] == '$')
    {
        Variable *variable = find_variable(scope, value + 1);

        if (!variable)
        {
            printf("error: variable does not exist: %s\n", value + 1);
            return;
        }

        printf("%s", variable->value);
        return;
    }

    Variable *variable = find_variable(scope, value);

    if (variable)
        printf("%s", variable->value);
    else
        printf("%s", value);
}

static int update_variable(
    Scope *scope,
    const Instruction *instruction
)
{
    if (instruction->part_count != 4)
    {
        printf("error on line %zu: invalid update syntax\n",
            instruction->line);
        return 1;
    }

    const char *name = instruction->parts[1];
    const char *operation = instruction->parts[2];
    const char *right_text = instruction->parts[3];

    Variable *variable = find_variable(scope, name);

    if (!variable)
    {
        printf("error on line %zu: unknown variable '%s'\n",
            instruction->line, name);
        return 1;
    }

    if (variable->read_only)
    {
        printf("error on line %zu: cannot modify a function parameter\n",
            instruction->line);
        return 1;
    }

    if (!is_numeric_type(variable->type))
    {
        printf("error on line %zu: update requires a numeric variable\n",
            instruction->line);
        return 1;
    }

    Operand right = {0};

    if (resolve_operand(right_text, scope, &right))
        return 1;

    if (!is_numeric_type(right.type))
    {
        printf("error on line %zu: update requires a numeric value\n",
            instruction->line);
        free(right.value);
        return 1;
    }

    char *end;
    errno = 0;
    long double a = strtold(variable->value, &end);

    if (errno == ERANGE || *end != '\0')
    {
        free(right.value);
        return 1;
    }

    errno = 0;
    long double b = strtold(right.value, &end);

    if (errno == ERANGE || *end != '\0')
    {
        free(right.value);
        return 1;
    }

    free(right.value);

    long double result;

    if (strcmp(operation, "+=") == 0)
        result = a + b;
    else if (strcmp(operation, "-=") == 0)
        result = a - b;
    else if (strcmp(operation, "*=") == 0)
        result = a * b;
    else if (strcmp(operation, "/=") == 0)
    {
        if (b == 0)
        {
            printf("error on line %zu: division by zero\n",
                instruction->line);
            return 1;
        }

        result = a / b;
    }
    else
    {
        printf("error on line %zu: unknown update operator '%s'\n",
            instruction->line, operation);
        return 1;
    }

    char buffer[128];

    if (strcmp(variable->type, "int") == 0)
    {
        if (!isfinite(result) ||
            result < (long double)LLONG_MIN ||
            result > (long double)LLONG_MAX ||
            truncl(result) != result)
        {
            printf("error on line %zu: invalid integer result\n",
                instruction->line);
            return 1;
        }

        snprintf(buffer, sizeof(buffer), "%lld", (long long)result);
    }
    else
    {
        if (!isfinite(result))
        {
            printf("error on line %zu: invalid float result\n",
                instruction->line);
            return 1;
        }

        snprintf(buffer, sizeof(buffer), "%.15Lg", result);
    }

    return change_variable(
        scope,
        name,
        buffer,
        variable->type
    );
}

static int get_input(
    const Instruction *instruction,
    Scope *scope
)
{
    if (instruction->part_count != 3)
    {
        printf("error on line %zu: invalid get syntax\n",
            instruction->line);
        return 1;
    }

    const char *name = instruction->parts[1];
    Variable *variable = find_variable(scope, name);

    if (!variable)
    {
        printf("error on line %zu: unknown variable '%s'\n",
            instruction->line, name);
        return 1;
    }

    if (variable->read_only)
    {
        printf("error on line %zu: cannot modify a function parameter\n",
            instruction->line);
        return 1;
    }

    log_value(instruction->parts[2], scope);
    fflush(stdout);

    char buffer[1024];

    if (!fgets(buffer, sizeof(buffer), stdin))
    {
        printf("error on line %zu: failed to read input\n",
            instruction->line);
        return 1;
    }

    buffer[strcspn(buffer, "\r\n")] = '\0';

    if (strcmp(variable->type, "int") == 0)
    {
        char *end;
        errno = 0;
        strtoll(buffer, &end, 10);

        while (isspace((unsigned char)*end))
            end++;

        if (errno == ERANGE || end == buffer || *end != '\0')
        {
            printf("error on line %zu: invalid integer input\n",
                instruction->line);
            return 1;
        }
    }
    else if (strcmp(variable->type, "float") == 0)
    {
        char *end;
        errno = 0;
        long double number = strtold(buffer, &end);

        while (isspace((unsigned char)*end))
            end++;

        if (errno == ERANGE || end == buffer ||
            *end != '\0' || !isfinite(number))
        {
            printf("error on line %zu: invalid float input\n",
                instruction->line);
            return 1;
        }
    }
    else if (strcmp(variable->type, "str") != 0)
    {
        printf("error on line %zu: unsupported variable type '%s'\n",
            instruction->line, variable->type);
        return 1;
    }

    return change_variable(
        scope,
        name,
        buffer,
        variable->type
    );
}

int execute_command(
    const Instruction *instruction,
    Scope *scope
)
{
    if (instruction->part_count == 0)
        return EXEC_OK;

    const char *command = instruction->parts[0];

    if (strcmp(command, "update") == 0)
    {
        return update_variable(scope, instruction);
    }
    else if (strcmp(command, "let") == 0)
    {
        if (instruction->part_count != 4)
        {
            printf("error on line %zu: invalid let syntax\n",
                instruction->line);
            return EXEC_ERROR;
        }

        if (create_variable(
            scope,
            instruction->parts[1],
            instruction->parts[2],
            instruction->parts[3]
        ))
        {
            printf("error on line %zu: cannot declare variable '%s'\n",
                instruction->line, instruction->parts[1]);
            return EXEC_ERROR;
        }
    }
    else if (strcmp(command, "set") == 0)
    {
        if (instruction->part_count != 4)
        {
            printf("error on line %zu: invalid set syntax\n",
                instruction->line);
            return EXEC_ERROR;
        }

        if (change_variable(
            scope,
            instruction->parts[1],
            instruction->parts[2],
            instruction->parts[3]
        ))
        {
            printf("error on line %zu: cannot set variable '%s'\n",
                instruction->line,
                instruction->parts[1]);
            return EXEC_ERROR;
        }
    }
    else if (strcmp(command, "log") == 0)
    {
        for (size_t j = 1; j < instruction->part_count; j++)
        {
            if (j > 1)
                printf(" ");

            log_value(instruction->parts[j], scope);
        }

        printf("\n");
    }
    else if (strcmp(command, "halt") == 0)
    {
        return EXEC_HALT;
    }
    else if (strcmp(command, "shalt") == 0)
    {
        return EXEC_SHALT;
    }
    else if (strcmp(command, "get") == 0)
    {
        return get_input(instruction, scope);
    }
    else if (strcmp(command, "del") == 0)
    {
        if (instruction->part_count != 2)
        {
            printf("error on line %zu: invalid del syntax\n",
                instruction->line);
            return EXEC_ERROR;
        }

        if (delete_variable(scope, instruction->parts[1]))
        {
            printf("error on line %zu: unknown local variable '%s'\n",
                instruction->line, instruction->parts[1]);
            return EXEC_ERROR;
        }
    }
    else
    {
        printf("error on line %zu: unknown command '%s'\n",
            instruction->line, command);
        return EXEC_ERROR;
    }

    return EXEC_OK;
}
