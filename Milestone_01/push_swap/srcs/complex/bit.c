/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bit.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 09:34:52 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/17 13:21:14 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	bit_update(int *bit, int n, int rank, int delta)
{
	int	i;

	i = rank + 1;
	while (i <= n)
	{
		bit[i] += delta;
		i += i & (-i);
	}
}

int	bit_query(int *bit, int rank)
{
	int	sum;
	int	i;

	sum = 0;
	i = rank + 1;
	while (i > 0)
	{
		sum += bit[i];
		i -= i & (-i);
	}
	return (sum);
}

int	bit_range(int *bit, int low, int high)
{
	if (low > high)
		return (0);
	if (low == 0)
		return (bit_query(bit, high));
	return (bit_query(bit, high) - bit_query(bit, low - 1));
}

int	bit_find_max(int *bit, int n, int count)
{
	int	pos;
	int	step;
	int	k;

	pos = 0;
	k = count;
	step = 1;
	while (step <= n)
		step <<= 1;
	step >>= 1;
	while (step > 0)
	{
		if (pos + step <= n && bit[pos + step] < k)
		{
			pos += step;
			k -= bit[pos];
		}
		step >>= 1;
	}
	return (pos);
}

void	bit_init(int *bit, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		bit_update(bit, n, i, 1);
		i++;
	}
}
