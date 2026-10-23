/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_exec_bonus_utils.c                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:27:41 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 12:33:37 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

static int	op_eq(const char *line, const char *op)
{
	size_t	len;

	len = ft_strlen(op);
	return (ft_strncmp(line, op, len + 1) == 0);
}

static int	exec_rotate(t_stack *a, t_stack *b, char *line)
{
	if (op_eq(line, "ra"))
	{
		c_rotate(a);
		return (0);
	}
	if (op_eq(line, "rb"))
	{
		c_rotate(b);
		return (0);
	}
	if (op_eq(line, "rr"))
	{
		c_rotate(a);
		c_rotate(b);
		return (0);
	}
	return (-1);
}

static int	exec_rev_rotate(t_stack *a, t_stack *b, char *line)
{
	if (op_eq(line, "rra"))
	{
		c_rev_rotate(a);
		return (0);
	}
	if (op_eq(line, "rrb"))
	{
		c_rev_rotate(b);
		return (0);
	}
	if (op_eq(line, "rrr"))
	{
		c_rev_rotate(a);
		c_rev_rotate(b);
		return (0);
	}
	return (exec_rotate(a, b, line));
}

static int	exec_swap_push(t_stack *a, t_stack *b, char *line)
{
	if (op_eq(line, "sa"))
		return (c_swap(a), 0);
	if (op_eq(line, "sb"))
		return (c_swap(b), 0);
	if (op_eq(line, "ss"))
		return (c_swap(a), c_swap(b), 0);
	if (op_eq(line, "pa"))
		return (c_push(a, b), 0);
	if (op_eq(line, "pb"))
		return (c_push(b, a), 0);
	return (-1);
}

int	exec_op(t_stack *a, t_stack *b, char *line)
{
	int	res;

	res = exec_swap_push(a, b, line);
	if (res == 0)
		return (0);
	return (exec_rev_rotate(a, b, line));
}
