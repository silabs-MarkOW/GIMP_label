# Adjust as necessary
# See Edit->Preferences->Folders->Plug-ins
PLUGIN_DIR = ${HOME}/.config/GIMP/2.10/plug-ins

SCRIPT = highlighted_label.py

diff :
	diff ${PLUGIN_DIR}/${SCRIPT} ${SCRIPT}

install :
	install ${SCRIPT} ${PLUGIN_DIR}
