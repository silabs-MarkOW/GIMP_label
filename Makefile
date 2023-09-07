PLUGIN_DIR = ${HOME}/.config/GIMP/2.10/plug-ins

diff :
	diff ${PLUGIN_DIR}/dot.py dot.py

install :
	install dot.py ${PLUGIN_DIR}
