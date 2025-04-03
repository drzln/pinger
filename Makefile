#!/usr/bin/make -f

%:
	@bin/exec $@ $(foreach var,$(MAKEOVERRIDES),$(var))

.PHONY: %
