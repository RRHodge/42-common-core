/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_parse_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 00:00:00 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:20:02 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

static long	parse_long(const char *s)
{
	long	n;
	int		sign;
	int		i;

	n = 0;
	sign = 1;
	i = 0;
	if (s[i] == '-' || s[i] == '+')
	{
		if (s[i++] == '-')
			sign = -1;
		else
			sign = 1;
	}
	while (s[i] >= '0' && s[i] <= '9')
		n = n * 10 + (s[i++] - '0');
	return (n * sign);
}

static int	is_valid_int(const char *s)
{
	int		i;
	long	n;

	if (!s || !*s)
		return (0);
	i = 0;
	if (s[i] == '-' || s[i] == '+')
		i++;
	if (!s[i])
		return (0);
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	n = parse_long(s);
	return (n >= -2147483648L && n <= 2147483647L);
}

static int	has_duplicate_bonus(t_stack *a, int val)
{
	t_list	*cur;

	cur = a->top;
	while (cur)
	{
		if (*(int *)cur->content == val)
			return (1);
		cur = cur->next;
	}
	return (0);
}

static int	push_front(t_stack *a, int val)
{
	t_list	*node;
	int		*v;

	if (has_duplicate_bonus(a, val))
		return (-1);
	v = malloc(sizeof(int));
	if (!v)
		return (-1);
	*v = val;
	node = ft_lstnew(v);
	if (!node)
	{
		free(v);
		return (-1);
	}
	node->next = a->top;
	a->top = node;
	a->size++;
	return (0);
}

int	build_stack(t_stack *a, char **argv, int start, int argc)
{
	int	i;

	i = argc - 1;
	while (i >= start)
	{
		if (!is_valid_int(argv[i]))
			return (-1);
		if (push_front(a, (int)parse_long(argv[i])) == -1)
			return (-1);
		i--;
	}
	return (0);
}
