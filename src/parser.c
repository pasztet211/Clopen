#include "parser.h"

#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static char *copy_string(const char *str)
{
    size_t length = strlen(str);
    char *copy = malloc(length + 1);

    if (copy)
        memcpy(copy, str, length + 1);

    return copy;
}

static void remove_comment(char *line)
{
    int in_quotes = 0;
    int escaped = 0;

    for (size_t i = 0; line[i]; i++)
    {
        if (escaped)
        {
            escaped = 0;
            continue;
        }

        if (line[i] == '\\' && in_quotes)
        {
            escaped = 1;
            continue;
        }

        if (line[i] == '"')
        {
            in_quotes = !in_quotes;
            continue;
        }

        if (!in_quotes && line[i] == '#')
        {
            line[i] = '\0';
            break;
        }
    }
}

static int add_part(Instruction *instruction, const char *start,
                    size_t length)
{
    char **new_parts = realloc(
        instruction->parts,
        (instruction->part_count + 1) * sizeof(char *)
    );

    if (!new_parts)
        return 1;

    instruction->parts = new_parts;

    char *part = malloc(length + 1);
    if (!part)
        return 1;

    memcpy(part, start, length);
    part[length] = '\0';

    instruction->parts[instruction->part_count++] = part;

    return 0;
}

static int tokenize(Instruction *instruction, const char *line, int keep_quotes)
{
    size_t i = 0;

    while (line[i])
    {
        while (isspace((unsigned char)line[i]))
            i++;

        if (!line[i])
            break;

        size_t capacity = 32;
        size_t length = 0;
        char *token = malloc(capacity);

        if (!token)
            return 1;

        int in_quotes = 0;

        while (line[i])
        {
            char c = line[i];

            if (c == '"')
            {
                in_quotes = !in_quotes;

                if (keep_quotes)
                {
                    if (length + 2 > capacity)
                    {
                        capacity *= 2;
                        char *temp = realloc(token, capacity);

                        if (!temp)
                        {
                            free(token);
                            return 1;
                        }

                        token = temp;
                    }

                    token[length++] = c;
                }

                i++;
                continue;
            }

            if (!in_quotes && isspace((unsigned char)c))
                break;

            if (length + 2 > capacity)
            {
                capacity *= 2;
                char *temp = realloc(token, capacity);

                if (!temp)
                {
                    free(token);
                    return 1;
                }

                token = temp;
            }

            token[length++] = c;
            i++;
        }

        token[length] = '\0';

        if (add_part(instruction, token, length))
        {
            free(token);
            return 1;
        }

        free(token);

        while (isspace((unsigned char)line[i]))
            i++;
    }

    return 0;
}

static int parse_block(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions,
    int nested
);

int parse_program(const CloProgram *program, InstructionList *instructions)
{
    instructions->items = NULL;
    instructions->count = 0;

    size_t index = 0;

    if (parse_block(program, &index, instructions, 0) != 0)
    {
        free_instructions(instructions);
        return 1;
    }

    return 0;
}

static int append_instruction(InstructionList *list, Instruction instruction)
{
    Instruction *items = realloc(
        list->items,
        (list->count + 1) * sizeof(Instruction)
    );

    if (!items)
        return 1;

    list->items = items;
    list->items[list->count++] = instruction;
    return 0;
}

static char *get_condition(const char *line)
{
    const char *start = strchr(line, '(');
    const char *end = strrchr(line, ')');

    if (!start || !end || end <= start)
        return NULL;

    size_t length = (size_t)(end - start - 1);
    char *condition = malloc(length + 1);

    if (!condition)
        return NULL;

    memcpy(condition, start + 1, length);
    condition[length] = '\0';

    return condition;
}

static int starts_with(const char *text, const char *prefix)
{
    return strncmp(text, prefix, strlen(prefix)) == 0;
}

static InstructionList *parse_nested_block(
    const CloProgram *program,
    size_t *index
)
{
    InstructionList *block = malloc(sizeof(InstructionList));

    if (!block)
        return NULL;

    *block = (InstructionList){0};

    if (parse_block(program, index, block, 1))
    {
        free_instructions(block);
        free(block);
        return NULL;
    }

    return block;
}

static int parse_if(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
);

static int parse_while(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
);

static int parse_for(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
);

static int parse_fn(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
);

static int is_keyword(const char *line, const char *keyword)
{
    size_t length = strlen(keyword);

    return strncmp(line, keyword, length) == 0 &&
           (line[length] == '\0' ||
            isspace((unsigned char)line[length]) ||
            line[length] == '{');
}

static int parse_block(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions,
    int nested
)
{
    while (*index < program->count)
    {
        const char *line = program->lines[*index].text;

        if (strcmp(line, "}") == 0)
        {
            if (!nested)
                return 1;

            (*index)++;
            return 0;
        }

        if (is_keyword(line, "elif") || is_keyword(line, "else")) {
            if (nested) {
                return 0;
            }

            return 1;
        }

        if (starts_with(line, "if ")) {
            if (parse_if(program, index, instructions))
                return 1;

            continue;
        }
        else if (starts_with(line, "while "))
        {
            if (parse_while(program, index, instructions))
                return 1;
        }
        else if (starts_with(line, "for "))
        {
            if (parse_for(program, index, instructions))
                return 1;
        }
        else if (starts_with(line, "fn "))
        {
            if (parse_fn(program, index, instructions))
                return 1;
        }
        else
        {
            Instruction instruction = {0};

            instruction.type = copy_string("command");
            instruction.line = program->lines[*index].line_number;

            if (!instruction.type ||
                tokenize(&instruction, line, 1))
            {
                free(instruction.type);

                for (size_t i = 0; i < instruction.part_count; i++)
                    free(instruction.parts[i]);

                free(instruction.parts);
                return 1;
            }

            if (append_instruction(instructions, instruction))
            {
                free(instruction.type);

                for (size_t i = 0; i < instruction.part_count; i++)
                    free(instruction.parts[i]);

                free(instruction.parts);
                return 1;
            }

            (*index)++;
        }
    }

    return nested ? 1 : 0;
}

static int parse_if(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
)
{
    Instruction instruction = {0};

    instruction.type = copy_string("if");
    instruction.line = program->lines[*index].line_number;

    if (!instruction.type)
        goto error;

    IfBranch branch = {0};

    branch.condition = get_condition(program->lines[*index].text);
    branch.line = instruction.line;

    if (!branch.condition)
        goto error;

    (*index)++;

    branch.block = parse_nested_block(program, index);

    if (!branch.block)
    {
        free(branch.condition);
        goto error;
    }

    instruction.branches = malloc(sizeof(IfBranch));

    if (!instruction.branches)
    {
        free(branch.condition);
        free_instructions(branch.block);
        free(branch.block);
        goto error;
    }

    instruction.branches[0] = branch;
    instruction.branch_count = 1;

    while (*index < program->count)
    {
        const char *line = program->lines[*index].text;

        if (is_keyword(line, "elif"))
        {
            IfBranch next = {0};

            next.condition = get_condition(line);
            next.line = program->lines[*index].line_number;

            if (!next.condition)
                goto error;

            (*index)++;

            next.block = parse_nested_block(program, index);

            if (!next.block)
            {
                free(next.condition);
                goto error;
            }

            IfBranch *branches = realloc(
                instruction.branches,
                (instruction.branch_count + 1) * sizeof(IfBranch)
            );

            if (!branches)
            {
                free(next.condition);
                free_instructions(next.block);
                free(next.block);
                goto error;
            }

            instruction.branches = branches;
            instruction.branches[instruction.branch_count++] = next;
        }
        else if (is_keyword(line, "else"))
        {
            (*index)++;

            instruction.else_block =
                parse_nested_block(program, index);

            if (!instruction.else_block)
                goto error;

            break;
        }
        else
        {
            break;
        }
    }

    if (append_instruction(instructions, instruction))
        goto error;

    return 0;

error:
    free(instruction.type);

    for (size_t i = 0; i < instruction.branch_count; i++)
    {
        free(instruction.branches[i].condition);
        free_instructions(instruction.branches[i].block);
        free(instruction.branches[i].block);
    }

    free(instruction.branches);

    if (instruction.else_block)
    {
        free_instructions(instruction.else_block);
        free(instruction.else_block);
    }

    return 1;
}

static int parse_while(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
)
{
    const char *line = program->lines[*index].text;

    Instruction instruction = {0};

    instruction.type = copy_string("while");
    instruction.line = program->lines[*index].line_number;
    instruction.condition = get_condition(line);

    if (!instruction.type || !instruction.condition)
    {
        free(instruction.type);
        free(instruction.condition);
        return 1;
    }

    /* Move past the while header. */
    (*index)++;

    instruction.block = parse_nested_block(program, index);

    if (!instruction.block)
    {
        free(instruction.type);
        free(instruction.condition);
        return 1;
    }

    if (append_instruction(instructions, instruction))
    {
        free(instruction.type);
        free(instruction.condition);
        free_instructions(instruction.block);
        free(instruction.block);
        return 1;
    }

    return 0;
}

static int parse_for(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
) {
    const char *line = program->lines[*index].text;
    char *data = get_condition(line);

    if (!data) {
        return 1;
    }

    char *first = strchr(data, ';');
    if (!first) {
        free(data);
        return 1;
    }

    char *second = strchr(first + 1, ';');
    if (!second) {
        free(data);
        return 1;
    }

    *first = '\0';
    *second = '\0';

    Instruction instruction = {0};
    instruction.type = copy_string("for");
    instruction.line = program->lines[*index].line_number;

    /* init */
    Instruction init_tokens = {0};

    if (tokenize(&init_tokens, data, 0)) {
        free(data);
        free(instruction.type);
        return 1;
    }

    instruction.init = init_tokens.parts;
    instruction.init_count = init_tokens.part_count;

    /* condition */
    char *condition = second + 1;
    while (isspace((unsigned char)*condition)) {
        condition++;
    }

    instruction.condition = copy_string(condition);

    /* update */
    Instruction update_tokens = {0};

    if (tokenize(&update_tokens, second + 1, 0)) {
        free(data);
        free(instruction.type);
        free(instruction.condition);
        for (size_t i = 0; i < instruction.init_count; i++)
            free(instruction.init[i]);
        free(instruction.init);
        return 1;
    }

    instruction.update = malloc(
        (update_tokens.part_count + 1) * sizeof(char *)
    );

    if (!instruction.update) {
        free(data);
        free(instruction.type);
        free(instruction.condition);
        return 1;
    }

    instruction.update[0] = copy_string("update");
    instruction.update_count = update_tokens.part_count + 1;

    for (size_t i = 0; i < update_tokens.part_count; i++) {
        instruction.update[i + 1] = update_tokens.parts[i];
    }

    free(update_tokens.parts);
    free(data);

    /* block */
    instruction.block = parse_nested_block(program, index);

    if (!instruction.block) {
        return 1;
    }

    if (append_instruction(instructions, instruction)) {
        return 1;
    }

    return 0;
}

static int parse_fn(
    const CloProgram *program,
    size_t *index,
    InstructionList *instructions
) {
    const char *line = program->lines[*index].text;

    Instruction instruction = {0};

    instruction.type = copy_string("fn");
    instruction.line = program->lines[*index].line_number;

    const char *name = line + 2;

    while (isspace((unsigned char)*name)) {
        name++;
    }

    const char *name_end = name;

    while (*name_end &&
           !isspace((unsigned char)*name_end) &&
           *name_end != '(') {
        name_end++;
    }

    instruction.name = malloc((size_t)(name_end - name) + 1);

    if (!instruction.name) {
        free(instruction.type);
        return 1;
    }

    memcpy(instruction.name, name, (size_t)(name_end - name));
    instruction.name[name_end - name] = '\0';

    char *inputs = get_condition(line);

    if (!inputs) {
        free(instruction.type);
        free(instruction.name);
        return 1;
    }

    char *current = inputs;

    while (*current) {
        char *comma = strchr(current, ',');

        if (comma) {
            *comma = '\0';
        }

        while (isspace((unsigned char)*current)) {
            current++;
        }

        char *end = current + strlen(current);

        while (end > current && isspace((unsigned char)end[-1])) {
            *--end = '\0';
        }

        if (*current) {
            char **new_inputs = realloc(
                instruction.inputs,
                (instruction.input_count + 1) * sizeof(char *)
            );

            if (!new_inputs) {
                free(inputs);
                return 1;
            }

            instruction.inputs = new_inputs;
            instruction.inputs[instruction.input_count] = copy_string(current);

            if (!instruction.inputs[instruction.input_count]) {
                free(inputs);
                return 1;
            }

            instruction.input_count++;
        }

        if (!comma) {
            break;
        }

        current = comma + 1;
    }

    free(inputs);

    instruction.block = parse_nested_block(program, index);

    if (!instruction.block) {
        return 1;
    }

    if (append_instruction(instructions, instruction)) {
        return 1;
    }

    return 0;
}

void free_instructions(InstructionList *instructions)
{
    if (!instructions)
        return;

    for (size_t i = 0; i < instructions->count; i++)
    {
        Instruction *instruction = &instructions->items[i];

        free(instruction->type);

        for (size_t j = 0; j < instruction->part_count; j++)
            free(instruction->parts[j]);

        free(instruction->parts);

        for (size_t j = 0; j < instruction->branch_count; j++)
        {
            free(instruction->branches[j].condition);

            free_instructions(instruction->branches[j].block);
            free(instruction->branches[j].block);
        }

        free(instruction->branches);

        if (instruction->else_block)
        {
            free_instructions(instruction->else_block);
            free(instruction->else_block);
        }

        if (instruction->block)
        {
            free_instructions(instruction->block);
            free(instruction->block);
        }
    }

    free(instructions->items);

    instructions->items = NULL;
    instructions->count = 0;
}
