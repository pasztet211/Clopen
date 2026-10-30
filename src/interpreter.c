#include "interpreter.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>

static char *copy_string(const char *str)
{
    size_t length = strlen(str);
    char *copy = malloc(length + 1);

    if (copy)
        memcpy(copy, str, length + 1);

    return copy;
}

static Variable *find_variable(
    VariableList *variables,
    const char *name
)
{
    for (size_t i = 0; i < variables->count; i++)
    {
        if (strcmp(variables->items[i].name, name) == 0)
            return &variables->items[i];
    }

    return NULL;
}

static char *parse_value(const char *value, const char *type)
{
    size_t length = strlen(value);

    if (strcmp(type, "str") == 0 &&
        length >= 2 &&
        value[0] == '"' &&
        value[length - 1] == '"')
    {
        char *result = malloc(length - 1);

        if (!result)
            return NULL;

        memcpy(result, value + 1, length - 2);
        result[length - 2] = '\0';

        return result;
    }

    return copy_string(value);
}

static int set_variable(
    VariableList *variables,
    const char *name,
    const char *value,
    const char *type
)
{
    Variable *variable = find_variable(variables, name);

    char *new_value = parse_value(value, type);
    char *new_type = copy_string(type);

    if (!new_value || !new_type)
    {
        free(new_value);
        free(new_type);
        return 1;
    }

    if (variable)
    {
        free(variable->value);
        free(variable->type);

        variable->value = new_value;
        variable->type = new_type;

        return 0;
    }

    char *new_name = copy_string(name);

    if (!new_name)
    {
        free(new_value);
        free(new_type);
        return 1;
    }

    Variable *new_items = realloc(
        variables->items,
        (variables->count + 1) * sizeof(Variable)
    );

    if (!new_items)
    {
        free(new_name);
        free(new_value);
        free(new_type);
        return 1;
    }

    variables->items = new_items;

    variables->items[variables->count++] = (Variable) {
        .name = new_name,
        .value = new_value,
        .type = new_type
    };

    return 0;
}

static void log_value(const char *value, VariableList *variables)
{
    size_t length = strlen(value);

    if (length >= 2 && value[0] == '"' && value[length - 1] == '"')
    {
        printf("%.*s", (int)(length - 2), value + 1);
        return;
    }

    Variable *variable = find_variable(variables, value);

    if (variable)
        printf("%s", variable->value);
    else
        printf("%s", value);
}

typedef struct {
    char *value;
    const char *type;
} Operand;

static char *trim_copy(const char *start, size_t length)
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

static int resolve_operand(
    const char *text,
    VariableList *variables,
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
    Variable *variable = find_variable(variables, result->value);

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

static int is_numeric_type(const char *type)
{
    return strcmp(type, "int") == 0 ||
           strcmp(type, "float") == 0 ||
           strcmp(type, "number") == 0;
}

static int evaluate_condition(
    const char *condition,
    VariableList *variables,
    int *result
)
{
    const char *operator = NULL;
    size_t operator_length = 0;

    /* Find the comparison operator, ignoring quoted text. */
    int in_quotes = 0;

    for (const char *p = condition; *p; p++)
    {
        if (*p == '"')
            in_quotes = !in_quotes;

        if (in_quotes)
            continue;

        if (strncmp(p, "==", 2) == 0 ||
            strncmp(p, "!=", 2) == 0 ||
            strncmp(p, ">=", 2) == 0 ||
            strncmp(p, "<=", 2) == 0)
        {
            operator = p;
            operator_length = 2;
            break;
        }

        if (*p == '>' || *p == '<')
        {
            operator = p;
            operator_length = 1;
            break;
        }
    }

    if (!operator)
        return 1;

    char *left_text = trim_copy(
        condition,
        (size_t)(operator - condition)
    );

    char *right_text = trim_copy(
        operator + operator_length,
        strlen(operator + operator_length)
    );

    if (!left_text || !right_text) {
        free(left_text);
        free(right_text);
        return 1;
    }

    Operand left = {0};
    Operand right = {0};

    if (resolve_operand(left_text, variables, &left) ||
        resolve_operand(right_text, variables, &right))
    {
        free(left_text);
        free(right_text);
        free(left.value);
        free(right.value);
        return 1;
    }

    free(left_text);
    free(right_text);

    int comparison;

    if (is_numeric_type(left.type) && is_numeric_type(right.type))
    {
        double a = strtod(left.value, NULL);
        double b = strtod(right.value, NULL);

        comparison = (a > b) - (a < b);
    }
    else
    {
        comparison = strcmp(left.value, right.value);
        comparison = (comparison > 0) - (comparison < 0);
    }

    if (strncmp(operator, "==", 2) == 0)
        *result = comparison == 0;
    else if (strncmp(operator, "!=", 2) == 0)
        *result = comparison != 0;
    else if (strncmp(operator, ">=", 2) == 0)
        *result = comparison >= 0;
    else if (strncmp(operator, "<=", 2) == 0)
        *result = comparison <= 0;
    else if (*operator == '>')
        *result = comparison > 0;
    else
        *result = comparison < 0;

    free(left.value);
    free(right.value);

    return 0;
}

static int update_variable(
    VariableList *variables,
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

    Variable *variable = find_variable(variables, name);

    if (!variable)
    {
        printf("error on line %zu: unknown variable '%s'\n",
            instruction->line, name);
        return 1;
    }

    if (!is_numeric_type(variable->type))
    {
        printf("error on line %zu: update requires a numeric variable\n",
            instruction->line);
        return 1;
    }

    Operand right = {0};

    if (resolve_operand(right_text, variables, &right))
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

    return set_variable(
        variables,
        name,
        buffer,
        variable->type
    );
}

int execute_instructions(
    const InstructionList *instructions,
    VariableList *variables
)
{
    for (size_t i = 0; i < instructions->count; i++)
    {
        const Instruction *instruction = &instructions->items[i];

        if (strcmp(instruction->type, "if") == 0)
        {
            int executed = 0;

            for (size_t j = 0; j < instruction->branch_count; j++)
            {
                int condition_result;

                if (evaluate_condition(
                    instruction->branches[j].condition,
                    variables,
                    &condition_result
                ))
                {
                    printf("error on line %zu: invalid condition\n",
                        instruction->branches[j].line);
                    return 1;
                }

                if (condition_result)
                {
                    if (execute_instructions(
                        instruction->branches[j].block,
                        variables
                    ))
                        return 1;

                    executed = 1;
                    break;
                }
            }

            if (!executed && instruction->else_block)
            {
                if (execute_instructions(instruction->else_block, variables))
                    return 1;
            }

            continue;
        }

        if (strcmp(instruction->type, "while") == 0)
        {
            while (1)
            {
                int condition_result;

                if (evaluate_condition(
                    instruction->condition,
                    variables,
                    &condition_result
                ))
                {
                    printf("error on line %zu: invalid while condition\n",
                        instruction->line);
                    return 1;
                }

                if (!condition_result)
                    break;

                if (execute_instructions(instruction->block, variables))
                    return 1;
            }

            continue;
        }

        if (strcmp(instruction->type, "command") != 0)
            continue;

        if (instruction->part_count == 0)
            continue;

        const char *command = instruction->parts[0];

        if (strcmp(command, "update") == 0)
        {
            if (update_variable(variables, instruction))
                return 1;
        }
        else if (strcmp(command, "let") == 0)
        {
            if (instruction->part_count != 4)
            {
                printf("error on line %zu: invalid let syntax\n",
                    instruction->line);
                return 1;
            }

            if (set_variable(
                variables,
                instruction->parts[1],
                instruction->parts[2],
                instruction->parts[3]
            ))
            {
                printf("error: memory allocation failed\n");
                return 1;
            }
        }
        else if (strcmp(command, "log") == 0)
        {
            for (size_t j = 1; j < instruction->part_count; j++)
            {
                if (j > 1)
                    printf(" ");

                log_value(instruction->parts[j], variables);
            }

            printf("\n");
        }
        else
        {
            printf("error on line %zu: unknown command '%s'\n",
                instruction->line, command);
            return 1;
        }
    }

    return 0;
}

void free_variables(VariableList *variables)
{
    for (size_t i = 0; i < variables->count; i++)
    {
        free(variables->items[i].name);
        free(variables->items[i].value);
        free(variables->items[i].type);
    }

    free(variables->items);

    variables->items = NULL;
    variables->count = 0;
}
