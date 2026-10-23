/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_bonus.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 00:00:00 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:18:53 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

int	is_sorted_bonus(t_stack *a, t_stack *b)
{
	t_list	*cur;

	if (b->size != 0)
		return (0);
	cur = a->top;
	while (cur && cur->next)
	{
		if (*(int *)cur->content >= *(int *)cur->next->content)
			return (0);
		cur = cur->next;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	t_stack	a;
	t_stack	b;

	if (argc < 2)
		return (0);
	a.top = NULL;
	a.size = 0;
	a.bench = NULL;
	b.top = NULL;
	b.size = 0;
	b.bench = NULL;
	if (build_stack(&a, argv, 1, argc) == -1)
	{
		ft_putstr_fd("Error\n", 2);
		return (1);
	}
	run(&a, &b);
	ft_lstclear(&a.top, free);
	ft_lstclear(&b.top, free);
	return (0);
}
