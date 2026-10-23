/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 00:00:00 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:16:00 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CHECKER_H
# define CHECKER_H

# include "push_swap.h"
# include "../lib/get_next_line/include/get_next_line.h"
# include <unistd.h>

int		is_sorted_bonus(t_stack *a, t_stack *b);

int		build_stack(t_stack *a, char **argv, int start, int argc);

int		c_push(t_stack *to, t_stack *from);
int		c_swap(t_stack *s);
int		c_rotate(t_stack *s);
int		c_rev_rotate(t_stack *s);

int		exec_op(t_stack *a, t_stack *b, char *line);
void	run(t_stack *a, t_stack *b);

#endif
