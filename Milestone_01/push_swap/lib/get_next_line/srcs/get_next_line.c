/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 16:44:01 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/04 18:39:51 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	stash_has_newline(t_buffer *stash)
{
	int	len;
	int	i;

	len = 0;
	while (stash)
	{
		i = 0;
		while (stash->content[i])
		{
			len++;
			if (stash->content[i++] == '\n')
				return (len);
		}
		stash = stash->next;
	}
	if (len)
		return (-len);
	return (0);
}

static int	handle_read(t_fd_node *node)
{
	char	*buffer;
	int		read_byte;

	buffer = malloc(BUFFER_SIZE + 1);
	if (!buffer)
		return (-1);
	read_byte = read(node->fd, buffer, BUFFER_SIZE);
	if (read_byte <= 0)
		return (free(buffer), read_byte);
	buffer[read_byte] = '\0';
	stash_add_buffer(node, buffer);
	return (read_byte);
}

char	*stash_extract_line(t_fd_node *node)
{
	t_buffer	*s;
	char		*line;
	int			len;
	int			i;
	int			j;

	if (!node || !node->head)
		return (NULL);
	len = stash_has_newline(node->head);
	if (len < 0)
		len = -len;
	line = malloc(len + 1);
	if (!len || !line)
		return (NULL);
	i = 0;
	s = node->head;
	while (s && i < len)
	{
		j = 0;
		while (s->content[j] && i < len)
			line[i++] = s->content[j++];
		s = s->next;
	}
	return (line[i] = '\0', line);
}

void	stash_clear_until_newline(t_fd_node *node)
{
	t_buffer	*remainder;

	if (!node || !node->head)
		return ;
	remainder = stash_create_after_newline(node->last);
	stash_free_all(&node->head);
	node->head = remainder;
	node->last = remainder;
}

char	*get_next_line(int fd)
{
	static t_fd_node	*list;
	t_fd_node			*node;
	char				*line;
	int					read_byte;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	node = get_fd_node(&list, fd);
	if (!node)
		return (NULL);
	read_byte = 1;
	while (stash_has_newline(node->head) <= 0 && read_byte > 0)
		read_byte = handle_read(node);
	if (read_byte == -1)
		return (fd_remove_node(&list, fd), NULL);
	line = stash_extract_line(node);
	stash_clear_until_newline(node);
	if (!node->head)
		fd_remove_node(&list, fd);
	return (line);
}
