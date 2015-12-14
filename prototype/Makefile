BOWER 		?= node_modules/.bin/bower
JSHINT 		?= node_modules/.bin/jshint
PEGJS		?= node_modules/.bin/pegjs
PHANTOMJS	?= node_modules/.bin/phantomjs
HTTPSERVE   ?= node_modules/.bin/http-server
BUNDLE      ?= ./.bundle/bin/bundle
SASS        ?= bundle

SOURCES		= $(wildcard src/*.js) $(wildcard src/pat/*.js) $(wildcard src/pat/calendar/*.js) $(wildcard src/lib/*.js)
BUNDLES		= bundles/patterns.js bundles/patterns.min.js

GENERATED	= patternslib/src/lib/depends_parse.js


########################################################################
## Install dependencies

stamp-npm: package.json
	npm install
	touch stamp-npm

stamp-bower: stamp-npm bower.json
	$(BOWER) install
	touch stamp-bower

stamp-bundler:
	mkdir -p .bundle
	gem install --user bundler --bindir .bundle/bin
	$(BUNDLE) install --path .bundle --binstubs .bundle/bin
	touch stamp-bundler

clean::
	rm -f stamp-npm stamp-bower
	rm -rf node_modules src/bower_components

########################################################################
## Build JS

patternslib::  
	@if [ ! -d "patternslib" ]; then \
		git clone https://github.com/Patternslib/Patterns.git patternslib; \
	fi;

bundle bundle.js: patternslib $(GENERATED) $(SOURCES) build.js stamp-bower
	mkdir -p bundles
	node_modules/.bin/r.js -o build.js
	node_modules/.bin/r.js -o build.js optimize=uglify out=bundles/bundle.min.js

src/lib/depends_parse.js: patternslib/src/lib/depends_parse.pegjs stamp-npm
	$(PEGJS) $<
	sed -i~ -e '1s/.*/define(function() {/' -e '$$s/()//' $@ || rm -f $@




# Add help text after each target name starting with ' \#\# '
help:
	@grep " ## " $(MAKEFILE_LIST) | grep -v MAKEFILE_LIST | sed 's/\([^:]*\).*##/\1    /'

jekyll-serve:: stamp-bundler   ## run jekyll, serve and watch
	bundle exec jekyll serve

jekyll-serve-blank:: stamp-bundler  ## run jekyll, serve and watch (ignoring the baseurl and host settings)
	bundle exec jekyll serve  --baseurl "" --host "0.0.0.0" 



.PHONY: compile-all clean jekyll-serve jekyll-serve-blank bundle patternslib help


