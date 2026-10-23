/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.h                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 16:44:16 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/04 19:04:26 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

typedef struct s_buffer
{
	char				*content;
	struct s_buffer		*next;
}				t_buffer;
typedef struct s_fd_node
{
	int					fd;
	t_buffer			*head;
	t_buffer			*last;
	struct s_fd_node	*next;
}				t_fd_node;

t_fd_node	*get_fd_node(t_fd_node **list, int fd);
void		fd_remove_node(t_fd_node **head, int fd);
void		stash_add_buffer(t_fd_node *node, char *buf);
t_buffer	*stash_create_after_newline(t_buffer *last);
void		stash_free_all(t_buffer **stash);
int			stash_has_newline(t_buffer *stash);
char		*stash_extract_line(t_fd_node *node);
void		stash_clear_until_newline(t_fd_node *node);
char		*get_next_line(int fd);

#endif
