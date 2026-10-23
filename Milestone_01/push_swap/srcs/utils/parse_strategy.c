/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_strategy.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 12:53:26 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/21 15:47:53 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static char	is_algo_flag(const char *s)
{
	if (!s || s[0] != '-' || s[1] != '-')
		return (0);
	if (ft_strncmp(s, "--simple", 9) == 0)
		return ('s');
	else if (ft_strncmp(s, "--medium", 9) == 0)
		return ('m');
	else if (ft_strncmp(s, "--complex", 10) == 0)
		return ('c');
	else if (ft_strncmp(s, "--adaptive", 11) == 0)
		return ('a');
	else if (ft_strncmp(s, "--bench", 8) == 0)
		return (0);
	else
	{
		ft_printf("Error\n");
		exit(1);
	}
	return (0);
}

char	parse_strategy(int argc, char **argv)
{
	int		i;
	char	flag;

	i = 1;
	while (i < argc && i <= 3)
	{
		flag = is_algo_flag(argv[i]);
		if (flag)
			return (flag);
		i++;
	}
	return ('a');
}
