/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker_ops_bonus.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 00:00:00 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:19:20 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

int	c_swap(t_stack *s)
{
	void	*tmp;

	if (s->size < 2)
		return (0);
	tmp = s->top->content;
	s->top->content = s->top->next->content;
	s->top->next->content = tmp;
	return (0);
}

int	c_push(t_stack *to, t_stack *from)
{
	t_list	*node;

	if (from->size == 0)
		return (-1);
	node = from->top;
	from->top = from->top->next;
	from->size--;
	node->next = to->top;
	to->top = node;
	to->size++;
	return (0);
}

int	c_rotate(t_stack *s)
{
	t_list	*head;
	t_list	*last;

	if (s->size < 2)
		return (0);
	head = s->top;
	s->top = s->top->next;
	head->next = NULL;
	last = ft_lstlast(s->top);
	last->next = head;
	return (0);
}

int	c_rev_rotate(t_stack *s)
{
	t_list	*prev;
	t_list	*last;

	if (s->size < 2)
		return (0);
	last = ft_lstlast(s->top);
	prev = s->top;
	while (prev->next != last)
		prev = prev->next;
	prev->next = NULL;
	last->next = s->top;
	s->top = last;
	return (0);
}
