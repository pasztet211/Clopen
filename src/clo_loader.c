#include "clo_loader.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static char *read_line(FILE *file)
{
    size_t capacity = 128;
    size_t length = 0;

    char *buffer = malloc(capacity);
    if (!buffer)
        return NULL;

    int c;

    while ((c = fgetc(file)) != EOF)
    {
        if (length + 1 >= capacity)
        {
            capacity *= 2;

            char *temp = realloc(buffer, capacity);
            if (!temp)
            {
                free(buffer);
                return NULL;
            }

            buffer = temp;
        }

        buffer[length++] = (char)c;

        if (c == '\n')
            break;
    }

    if (length == 0 && feof(file))
    {
        free(buffer);
        return NULL;
    }

    buffer[length] = '\0';
    return buffer;
}

static char *trim(char *str)
{
    while (isspace((unsigned char)*str))
        str++;

    char *end = str + strlen(str);

    while (end > str && isspace((unsigned char)end[-1]))
        end--;

    *end = '\0';
    return str;
}

static void strip_comments(char *line)
{
    int in_quotes = 0;

    for (size_t i = 0; line[i] != '\0'; i++)
    {
        if (line[i] == '"')
        {
            in_quotes = !in_quotes;
            continue;
        }

        if (!in_quotes && line[i] == '/' && line[i + 1] == '/')
        {
            line[i] = '\0';
            break;
        }

        if (!in_quotes && line[i] == '#')
        {
            line[i] = '\0';
            break;
        }
    }
}

int load_clo(const char *filename, CloProgram *program)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL)
        return 1;

    program->lines = NULL;
    program->count = 0;

    char *buffer = NULL;
    size_t line_number = 0;

    while ((buffer = read_line(file)) != NULL)
    {
        line_number++;

        char *line = trim(buffer);

        strip_comments(line);
        line = trim(line);

        if (*line == '\0')
        {
            free(buffer);
            continue;
        }

        CloLine *new_lines = realloc(
            program->lines,
            (program->count + 1) * sizeof(CloLine)
        );

        if (new_lines == NULL)
        {
            free(buffer);
            fclose(file);
            free_clo(program);
            return 2;
        }

        program->lines = new_lines;

        program->lines[program->count].text = malloc(strlen(line) + 1);

        if (program->lines[program->count].text == NULL)
        {
            free(buffer);
            fclose(file);
            free_clo(program);
            return 2;
        }

        strcpy(program->lines[program->count].text, line);
        program->lines[program->count].line_number = line_number;

        program->count++;

        free(buffer);
    }

    free(buffer);
    fclose(file);

    return 0;
}

void free_clo(CloProgram *program)
{
    for (size_t i = 0; i < program->count; i++)
        free(program->lines[i].text);

    free(program->lines);

    program->lines = NULL;
    program->count = 0;
}
