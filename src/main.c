#include <stdio.h>
#include <string.h>

#include "clo_loader.h"
#include "parser.h"
#include "interpreter.h"

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

    //printf("parsed %zu instructions:\n\n", instructions.count);

    //print_instructions(&instructions, 0);

    VariableList variables = {0};

    if (execute_instructions(&instructions, &variables) != 0)
    {
        free_variables(&variables);
        free_instructions(&instructions);
        free_clo(&program);
        return 1;
    }

    free_variables(&variables);

    free_instructions(&instructions);
    free_clo(&program);

    return 0;
}