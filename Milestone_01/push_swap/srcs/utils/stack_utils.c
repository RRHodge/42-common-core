/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/31 12:59:36 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_push_int(t_stack *s, int val)
{
	int		*n;
	t_list	*node;

	n = malloc(sizeof(int));
	if (!n)
		return (0);
	*n = val;
	node = ft_lstnew(n);
	if (!node)
	{
		free(n);
		return (0);
	}
	node->next = s->top;
	s->top = node;
	s->size++;
	return (1);
}

void	stack_free(t_stack *s)
{
	t_list	*cur;
	t_list	*nxt;

	cur = s->top;
	while (cur)
	{
		nxt = cur->next;
		free(cur->content);
		free(cur);
		cur = nxt;
	}
	s->top = NULL;
	s->size = 0;
}

int	has_duplicate(t_stack *a)
{
	t_list	*i;
	t_list	*j;

	i = a->top;
	while (i)
	{
		j = i->next;
		while (j)
		{
			if (*(int *)i->content == *(int *)j->content)
				return (1);
			j = j->next;
		}
		i = i->next;
	}
	return (0);
}

int	is_sorted(t_stack *a)
{
	t_list	*cur;

	if (!a || !a->top)
		return (1);
	cur = a->top;
	while (cur && cur->next)
	{
		if (*(int *)cur->content > *(int *)cur->next->content)
			return (0);
		cur = cur->next;
	}
	return (1);
}

void	push_swap_dispatcher(t_stack *a, t_stack *b)
{
	if (is_sorted(a))
		return ;
	if (a->size == 2)
		sa(a);
	else if (a->size == 3)
		sort_3(a);
	else if (a->size <= 5)
		sort_5(a, b);
}
