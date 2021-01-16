SCENARIOS =
SCENARIOS += bonk.py
SCENARIOS += figure_8s.py
SCENARIOS += thermal_inside_turn.py

.PHONY: all
all: $(SCENARIOS)

.PHONY: clean
clean:
	rm -f *.png *.svg
	rm -fR __pycache__

.PHONY: $(SCENARIOS)
$(SCENARIOS):
	@echo $@
