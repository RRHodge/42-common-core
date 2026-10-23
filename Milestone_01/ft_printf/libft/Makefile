# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rarabeto <rarabeto@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 18:30:11 by rarabeto          #+#    #+#              #
#    Updated: 2026/02/25 05:57:30 by rarabeto         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

AR = ar -rcs

CC = cc

RM = rm -f

CFLAGS = -Wall -Wextra -Werror

SRCS_DIR = srcs

OBJS_DIR = objs

BUILD_DIR = build

BUILD = libft.a

NAME = $(BUILD_DIR)/$(BUILD)
  
SRCS = ft_isalpha.c \
		ft_isdigit.c \
		ft_isalnum.c \
		ft_isascii.c \
		ft_isprint.c \
		ft_strlen.c \
		ft_memset.c \
		ft_bzero.c \
		ft_memcpy.c \
		ft_memmove.c \
		ft_strlcpy.c \
		ft_strlcat.c \
		ft_toupper.c \
		ft_tolower.c \
		ft_strchr.c \
		ft_strrchr.c \
		ft_strncmp.c \
		ft_memchr.c \
		ft_memcmp.c \
		ft_strnstr.c \
		ft_atoi.c \
		ft_calloc.c \
		ft_strdup.c \
		ft_substr.c \
		ft_strjoin.c \
		ft_strtrim.c \
		ft_split.c \
		ft_itoa.c \
		ft_strmapi.c \
		ft_striteri.c \
		ft_putchar_fd.c \
		ft_putstr_fd.c \
		ft_putendl_fd.c \
		ft_putnbr_fd.c \
		ft_lstnew.c \
		ft_lstadd_front.c \
		ft_lstsize.c \
		ft_lstlast.c \
		ft_lstadd_back.c \
		ft_lstdelone.c \
		ft_lstclear.c \
		ft_lstiter.c \
		ft_lstmap.c

OBJS = $(addprefix $(OBJS_DIR)/, ${SRCS:%.c=%.o})

all: $(NAME)

$(OBJS_DIR):
	@mkdir -p $(OBJS_DIR)

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

$(NAME):$(OBJS) | $(BUILD_DIR)
	  $(AR) $(NAME) $^


$(OBJS_DIR)/%.o: $(SRCS_DIR)/%.c | $(OBJS_DIR)
	$(CC) $(CFLAGS) -I include -c $< -o $@

clean:
	$(RM) -r $(OBJS_DIR)

fclean: clean
	$(RM) -r $(BUILD_DIR)

re: fclean
	@make all

.PHONY: re fclean clean all
