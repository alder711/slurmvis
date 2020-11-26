
MKFILE_DIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

run: prereq
	FLASK_APP=app.py \
	FLASK_DEBUG=1 \
	flask run

prereq:
	# Check for Python 3.x
	@/usr/bin/which python3 2>&1 >/dev/null || \
		( echo "Python 3.x not installed, exiting." ; exit 1 )
	# Try to Activate venv
	@. "$(MKFILE_DIR)"bin/activate
	# Check to see if in virtual environment
	@python3 -c "import sys; sys.exit(0) if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else sys.exit(1)" || \
		( echo "Not in a venv, creating..." ; python3 -m venv "$(MKFILE_DIR)" )
	# Activate venv
	@. "$(MKFILE_DIR)"bin/activate
	# Install required Python packages
	@pip install -r "$(MKFILE_DIR)/requirements.txt"

clean:
	@deactivate || cat /dev/null
	rm -rf $(MKFILE_DIR)__pycache__
	rm -rf $(MKFILE_DIR)bin
	rm -rf $(MKFILE_DIR)flask_session
	rm -rf $(MKFILE_DIR)include
	rm -rf $(MKFILE_DIR)lib
	rm -rf $(MKFILE_DIR)lib64
	rm -rf $(MKFILE_DIR)pyvenv.cfg
