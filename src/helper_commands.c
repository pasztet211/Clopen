#include "helper_commands.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *copy_string(const char *str)
{
    size_t length = strlen(str);
    char *copy = malloc(length + 1);

    if (copy)
        memcpy(copy, str, length + 1);

    return copy;
}

Variable *find_variable(Scope *scope, const char *name)
{
    Scope *current = scope;

    while (current)
    {
        for (size_t i = 0; i < current->variables.count; i++)
        {
            if (strcmp(current->variables.items[i].name, name) == 0)
                return &current->variables.items[i];
        }

        current = current->parent;
    }

    return NULL;
}

char *parse_value(const char *value, const char *type)
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

int create_variable(
    Scope *scope,
    const char *name,
    const char *value,
    const char *type
)
{
    /* Prevent duplicate names in this scope or any parent scope. */
    if (find_variable(scope, name))
        return 1;

    char *new_name = copy_string(name);
    char *new_value = parse_value(value, type);
    char *new_type = copy_string(type);

    if (!new_name || !new_value || !new_type)
    {
        free(new_name);
        free(new_value);
        free(new_type);
        return 1;
    }

    Variable *new_items = realloc(
        scope->variables.items,
        (scope->variables.count + 1) * sizeof(Variable)
    );

    if (!new_items)
    {
        free(new_name);
        free(new_value);
        free(new_type);
        return 1;
    }

    scope->variables.items = new_items;

    scope->variables.items[scope->variables.count++] = (Variable) {
        .name = new_name,
        .value = new_value,
        .type = new_type,
        .read_only = 0
    };

    return 0;
}

int change_variable(
    Scope *scope,
    const char *name,
    const char *value,
    const char *type
)
{
    Variable *variable = find_variable(scope, name);

    if (!variable || variable->read_only)
        return 1;

    char *new_value = parse_value(value, type);
    char *new_type = copy_string(type);

    if (!new_value || !new_type)
    {
        free(new_value);
        free(new_type);
        return 1;
    }

    free(variable->value);
    free(variable->type);

    variable->value = new_value;
    variable->type = new_type;

    return 0;
}

int delete_variable(Scope *scope, const char *name)
{
    VariableList *variables = &scope->variables;

    for (size_t i = 0; i < variables->count; i++)
    {
        if (strcmp(variables->items[i].name, name) == 0)
        {
            free(variables->items[i].name);
            free(variables->items[i].value);
            free(variables->items[i].type);

            for (size_t j = i; j + 1 < variables->count; j++)
                variables->items[j] = variables->items[j + 1];

            variables->count--;
            return 0;
        }
    }

    return 1;
}

void free_scope(Scope *scope)
{
    if (!scope)
        return;

    for (size_t i = 0; i < scope->variables.count; i++)
    {
        free(scope->variables.items[i].name);
        free(scope->variables.items[i].value);
        free(scope->variables.items[i].type);
    }

    free(scope->variables.items);

    scope->variables.items = NULL;
    scope->variables.count = 0;
}

void retain_scope(Scope *scope)
{
    if (scope)
        scope->ref_count++;
}

void release_scope(Scope *scope)
{
    if (!scope)
        return;

    if (--scope->ref_count > 0)
        return;

    Scope *parent = scope->parent;

    for (size_t i = 0; i < scope->variables.count; i++)
    {
        free(scope->variables.items[i].name);
        free(scope->variables.items[i].value);
        free(scope->variables.items[i].type);
    }

    free(scope->variables.items);
    free(scope);

    release_scope(parent);
}

Scope *create_scope(Scope *parent)
{
    Scope *scope = calloc(1, sizeof(Scope));

    if (!scope)
        return NULL;

    scope->ref_count = 1;
    scope->parent = parent;

    retain_scope(parent);

    return scope;
}