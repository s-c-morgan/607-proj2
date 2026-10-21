PYTHON ?= python

.PHONY: all simulate analyze figures clean test

all: simulate analyze figures

simulate:
	cd src && $(PYTHON) simulation.py

analyze:
	cd src && $(PYTHON) analyze.py

figures:
	$(PYTHON) results/figures/plot_plugin.py
	$(PYTHON) results/figures/plot_beta2.py

test:
	$(PYTHON) -m pytest tests

clean:
	rm -f data/simulated.pk results/raw/estimates.pk results/summary.csv
	rm -f results/figures/*.png
	rm -rf src/__pycache__ tests/__pycache__ .pytest_cache
