RELEASE_DIR	= release/prototype/_site
DIAZO_DIR       = src/bildergut/theme/theme/generated
LATEST          = $(shell cat LATEST)
BUNDLENAME      = bundle
BUNDLEURL	= https://products.syslab.com/packages/$(BUNDLENAME)/$(LATEST)/$(BUNDLENAME)-$(LATEST).tar.gz

# Add help text after each target name starting with ' \#\# '
help:
	@grep " ## " $(MAKEFILE_LIST) | grep -v MAKEFILE_LIST | sed 's/\([^:]*\).*##/\1   /'

all:: diazo
default: all

########################################################################
## Setup
## You don't run these rules unless you're a prototype dev


jekyll: 
	@cd prototype && bundle exec jekyll build

diazo: jekyll  _diazo ## 	 Generate the theme with jekyll and copy it to src/ploneintranet/theme/static/generated

_diazo:
	# --- (1) --- prepare clean release dir
	@rm -rf ${RELEASE_DIR} && mkdir -p ${RELEASE_DIR}
	cp -R prototype/_site/* $(RELEASE_DIR)/
	# Cleaning up non mission critical elements
	rm -f $(RELEASE_DIR)/*-e
	rm -rf $(RELEASE_DIR)/bundles/*
	# --- (2) --- refresh diazo static/generated
	# html templates referenced in rules.xml - second cut preserves subpath eg open-market-committee/index.html
	# point js sourcing to registered resource and rewrite all other generated sources to point to diazo dir
	for file in `grep 'href="generated' $(DIAZO_DIR)/../rules.xml | cut -f2 -d\" | cut -f2- -d/`; do \
		echo "Rewriting resource URLs in $$file"; \
		sed -i -e 's#src=".*bundle.js"#src="generated/bundles/$(BUNDLENAME).js"#' $(RELEASE_DIR)/$$file; \
		sed -i -e 's#="/\(style\)/#="generated/\1/#g' $(RELEASE_DIR)/$$file; \
		sed -i -e 's#="/\(media\)/#="generated/\1/#g' $(RELEASE_DIR)/$$file; \
		mkdir -p `dirname $(DIAZO_DIR)/$$file`; \
		cp $(RELEASE_DIR)/$$file $(DIAZO_DIR)/$$file; \
	done
	# we want all style elements recursively - and remove old resources not used anymore
	sed -i -e 's#url(/media/#url(../media/#g' $(RELEASE_DIR)/style/base.css;
	@rm -rf $(DIAZO_DIR)/style/ && mkdir $(DIAZO_DIR)/style/
	@cp -R $(RELEASE_DIR)/style/* $(DIAZO_DIR)/style/
	@[ -d $(DIAZO_DIR)/media/ ] || mkdir $(DIAZO_DIR)/media/




# .PHONY: all diazo jekyll
