
all: help
.PHONY: all

help:
	./menu.sh
.PHONY: help

api:
	@uvicorn main:app --reload
.PHONY: api