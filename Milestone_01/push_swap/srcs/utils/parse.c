/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rarabeto <rarabeto@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/07 09:26:26 by rarabeto          #+#    #+#             */
/*   Updated: 2026/03/31 10:31:02 by rarabeto         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_valid_int(char *s)
{
	long	val;
	int		i;
	int		sign;

	i = 0;
	if (ft_strlen(s) > 11)
		return (0);
	sign = (s[i] != '-') - (s[i] == '-');
	if (s[i] == '-' || s[i] == '+')
		i++;
	if (!s[i])
		return (0);
	val = 0;
	while (s[i] >= '0' && s[i] <= '9')
	{
		val = val * 10 + (s[i] - '0');
		i++;
	}
	if ((sign == 1 && val > (long)INT_MAX)
		|| (sign == -1 && val > (long)INT_MAX + 1))
		return (0);
	if (s[i])
		return (0);
	return (1);
}

static void	free_split(char **array)
{
	int	i;

	i = 0;
	if (!array)
		return ;
	while (array[i])
		free(array[i++]);
	free(array);
}

static int	process_array(t_stack *a, char **array)
{
	int	j;

	j = 0;
	while (array[j])
		j++;
	j--;
	while (j >= 0)
	{
		if (!is_valid_int(array[j]) || !stack_push_int(a, ft_atoi(array[j])))
		{
			ft_printf("Error\n");
			return (0);
		}
		j--;
	}
	return (1);
}

int	parse_args(t_stack *a, int argc, char **argv, int start)
{
	int		i;
	char	**array;

	i = argc - 1;
	while (i >= start)
	{
		if (ft_strchr(argv[i], ' '))
			array = ft_split(argv[i], ' ');
		else
			array = ft_split(argv[i], '\n');
		if (!array)
			return (0);
		if (!process_array(a, array))
			return (free_split (array), 0);
		free_split(array);
		i--;
	}
	if (has_duplicate(a))
	{
		ft_printf("Error\n");
		return (0);
	}
	return (1);
}
