/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils_bonus.c                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 16:44:13 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/04 18:42:10 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

t_fd_node	*get_fd_node(t_fd_node **list, int fd)
{
	t_fd_node	*curr;
	t_fd_node	*new;

	curr = *list;
	while (curr)
	{
		if (curr->fd == fd)
			return (curr);
		curr = curr->next;
	}
	new = malloc(sizeof(t_fd_node));
	if (!new)
		return (NULL);
	new->fd = fd;
	new->head = NULL;
	new->last = NULL;
	new->next = *list;
	*list = new;
	return (new);
}

void	fd_remove_node(t_fd_node **list, int fd)
{
	t_fd_node	*curr;
	t_fd_node	*prev;

	curr = *list;
	prev = NULL;
	while (curr)
	{
		if (curr->fd == fd)
		{
			if (prev)
				prev->next = curr->next;
			else
				*list = curr->next;
			stash_free_all(&curr->head);
			free(curr);
			return ;
		}
		prev = curr;
		curr = curr->next;
	}
}

void	stash_add_buffer(t_fd_node *node, char *buf)
{
	t_buffer	*new;

	new = malloc(sizeof(t_buffer));
	if (!new)
		return (free(buf));
	new->content = buf;
	new->next = NULL;
	if (!node->head)
		node->head = new;
	else
		node->last->next = new;
	node->last = new;
}

t_buffer	*stash_create_after_newline(t_buffer *last)
{
	t_buffer	*new;
	int			i;
	int			j;

	if (!last || !last->content)
		return (NULL);
	i = 0;
	while (last->content[i] && last->content[i] != '\n')
		i++;
	if (!last->content[i] || !last->content[++i])
		return (NULL);
	new = malloc(sizeof(t_buffer));
	if (!new)
		return (NULL);
	j = 0;
	while (last->content[i + j])
		j++;
	new->content = malloc(j + 1);
	if (!new->content)
		return (free(new), NULL);
	j = 0;
	while (last->content[i])
		new->content[j++] = last->content[i++];
	return (new->content[j] = '\0', new->next = NULL, new);
}

void	stash_free_all(t_buffer **stash)
{
	t_buffer	*tmp;

	if (!stash || !*stash)
		return ;
	while (*stash)
	{
		tmp = (*stash)->next;
		free((*stash)->content);
		free(*stash);
		*stash = tmp;
	}
}
