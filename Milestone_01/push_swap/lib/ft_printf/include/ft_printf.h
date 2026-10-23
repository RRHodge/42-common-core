/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tny-onin <tny-onin@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/10 11:30:25 by tny-onin          #+#    #+#             */
/*   Updated: 2026/03/17 11:14:00 by tny-onin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <stdint.h>
# include "../../libft/include/libft.h"

int	ft_printf(const char *format, ...);
int	print_char(char c);
int	print_str(char *str);
int	print_hex(uintptr_t n, char format);
int	print_nbr(int n);
int	print_pointer(void *ptr);
int	print_unsigned(unsigned int n);

#endif
