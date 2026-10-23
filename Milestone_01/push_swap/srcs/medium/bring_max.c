/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bring_max.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:44:13 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 12:48:18 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	bring_back_max(t_stack *a, t_stack *b)
{
	int	max_pos;
	int	nb_rot;

	max_pos = find_max_pos(b);
	if (max_pos <= b->size / 2)
	{
		while (max_pos-- > 0)
			rb(b);
	}
	else
	{
		nb_rot = b->size - max_pos;
		while (nb_rot-- > 0)
			rrb(b);
	}
	pa(a, b);
}
