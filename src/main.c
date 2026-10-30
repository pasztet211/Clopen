#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "clo_loader.h"
#include "parser.h"
#include "interpreter.h"
#include "helper_commands.h"


static void print_instructions(const InstructionList *instructions, int depth)
{
    for (size_t i = 0; i < instructions->count; i++)
    {
        const Instruction *instruction = &instructions->items[i];

        for (int j = 0; j < depth; j++)
            printf("    ");

        printf("[%zu] %s:", instruction->line, instruction->type);

        if (strcmp(instruction->type, "command") == 0)
        {
            for (size_t j = 0; j < instruction->part_count; j++)
                printf(" {%s}", instruction->parts[j]);
        }

        printf("\n");

        if (strcmp(instruction->type, "for") == 0)
        {
            for (int j = 0; j < depth + 1; j++)
                printf("    ");

            printf("init:");
            for (size_t j = 0; j < instruction->init_count; j++)
                printf(" {%s}", instruction->init[j]);
            printf("\n");

            for (int j = 0; j < depth + 1; j++)
                printf("    ");

            printf("condition: %s\n", instruction->condition);

            for (int j = 0; j < depth + 1; j++)
                printf("    ");

            printf("update:");
            for (size_t j = 0; j < instruction->update_count; j++)
                printf(" {%s}", instruction->update[j]);
            printf("\n");

            print_instructions(instruction->block, depth + 1);
        }

        if (strcmp(instruction->type, "while") == 0)
        {
            for (int j = 0; j < depth + 1; j++)
                printf("    ");

            printf("condition: %s\n", instruction->condition);

            print_instructions(instruction->block, depth + 1);
        }

        if (strcmp(instruction->type, "if") == 0)
        {
            for (size_t j = 0; j < instruction->branch_count; j++)
            {
                for (int k = 0; k < depth + 1; k++)
                    printf("    ");

                printf("branch: %s\n", instruction->branches[j].condition);

                print_instructions(instruction->branches[j].block, depth + 2);
            }

            if (instruction->else_block)
            {
                for (int j = 0; j < depth + 1; j++)
                    printf("    ");

                printf("else:\n");

                print_instructions(instruction->else_block, depth + 2);
            }
        }
    }
}


int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("usage: clopen <file.clo>\n");
        return 1;
    }

    CloProgram program = {0};

    if (load_clo(argv[1], &program) != 0)
    {
        printf("error: could not load file\n");
        return 1;
    }

    InstructionList instructions = {0};

    if (parse_program(&program, &instructions) != 0)
    {
        printf("error: parsing failed\n");
        free_clo(&program);
        return 1;
    }

    printf("parsed %zu instructions:\n\n", instructions.count);

    print_instructions(&instructions, 0);

    Scope *global_scope = create_scope(NULL);
    FunctionList functions = {0};

    if (!global_scope)
    {
        printf("error: could not create global scope\n");
        free_instructions(&instructions);
        free_clo(&program);
        return 1;
    }

    ExecutionContext context = {
        .scope = global_scope,
        .functions = {0},
        .in_function = 0,
        .returned = 0,
        .return_value = NULL,
        .return_type = NULL
    };

    if (execute_instructions(&instructions, &context) != EXEC_OK)
    {
        release_scope(global_scope);
        free(functions.items);
        free_instructions(&instructions);
        free_clo(&program);
        return 1;
    }

    release_scope(global_scope);
    free(functions.items);
    free_instructions(&instructions);
    free_clo(&program);

    return 0;
}