#include "interpreter.h"
#include "helper_commands.h"
#include "commands.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <math.h>

static int evaluate_condition(
    const char *condition,
    ExecutionContext *context,
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

    if (resolve_operand(left_text, context->scope, &left) ||
        resolve_operand(right_text, context->scope, &right))
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

int execute_instructions(
    const InstructionList *instructions,
    ExecutionContext *context
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
                    context,
                    &condition_result
                ))
                {
                    printf("error on line %zu: invalid condition\n",
                        instruction->branches[j].line);
                    return 1;
                }

                if (condition_result)
                {
                    int result = execute_instructions(
                        instruction->branches[j].block,
                        context
                    );

                    if (result != EXEC_OK)
                        return result;

                    executed = 1;
                    break;
                }
            }

            if (!executed && instruction->else_block)
            {
                int result = execute_instructions(
                    instruction->else_block,
                    context
                );

                if (result != EXEC_OK)
                    return result;
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
                    context,
                    &condition_result
                ))
                {
                    printf("error on line %zu: invalid while condition\n",
                        instruction->line);
                    return 1;
                }

                if (!condition_result)
                    break;

                int result = execute_instructions(
                    instruction->block,
                    context
                );

                if (result == EXEC_SHALT)
                    break;

                if (result != EXEC_OK)
                    return result;
            }

            continue;
        }

        if (strcmp(instruction->type, "for") == 0)
        {
            /* Initialization */
            char *init_parts[instruction->init_count + 1];

            init_parts[0] = "let";

            for (size_t j = 0; j < instruction->init_count; j++)
                init_parts[j + 1] = instruction->init[j];

            Instruction init = {0};
            init.type = "command";
            init.line = instruction->line;
            init.parts = init_parts;
            init.part_count = instruction->init_count + 1;

            if (execute_command(&init, context->scope))
                return 1;
                
            /* Loop */
            while (1)
            {
                int condition_result;

                if (evaluate_condition(
                    instruction->condition,
                    context,
                    &condition_result
                ))
                {
                    printf("error on line %zu: invalid for condition\n",
                        instruction->line);
                    return 1;
                }

                if (!condition_result)
                    break;

                int result = execute_instructions(
                    instruction->block,
                    context
                );

                if (result == EXEC_SHALT)
                    break;

                if (result != EXEC_OK)
                    return result;

                /* Update */
                Instruction update = {0};
                update.type = "command";
                update.line = instruction->line;
                update.parts = instruction->update;
                update.part_count = instruction->update_count;

                result = execute_command(&update, context->scope);

                if (result != EXEC_OK)
                    return result;
            }

            continue;
        }

        if (strcmp(instruction->type, "command") == 0)
        {
            int result = execute_command(instruction, context->scope);

            if (result != EXEC_OK)
                return result;
        }

        if (instruction->part_count == 0)
            continue;
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
