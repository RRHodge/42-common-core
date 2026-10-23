/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops_rr.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:38:19 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 12:39:12 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	op_rr_ctx(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	ra(a);
	op_rb(b, ctx);
}

void	op_rrr_ctx(t_stack *a, t_stack *b, t_bit_ctx *ctx)
{
	rra(a);
	op_rrb(b, ctx);
}
