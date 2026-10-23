/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   find_min_max.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:49:45 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 12:50:15 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	find_min_pos(t_stack *s)
{
	t_list	*cur;
	t_list	*min_node;
	int		pos;
	int		min_pos;

	if (!s || !s->top)
		return (-1);
	min_node = s->top;
	cur = s->top->next;
	pos = 0;
	min_pos = 0;
	while (cur)
	{
		pos++;
		if (*(int *)cur->content < *(int *)min_node->content)
		{
			min_node = cur;
			min_pos = pos;
		}
		cur = cur->next;
	}
	return (min_pos);
}

int	find_max_pos(t_stack *s)
{
	t_list	*cur;
	t_list	*max_node;
	int		pos;
	int		max_pos;

	if (!s || !s->top)
		return (-1);
	max_node = s->top;
	cur = s->top->next;
	pos = 0;
	max_pos = 0;
	while (cur)
	{
		pos++;
		if (*(int *)cur->content > *(int *)max_node->content)
		{
			max_node = cur;
			max_pos = pos;
		}
		cur = cur->next;
	}
	return (max_pos);
}
