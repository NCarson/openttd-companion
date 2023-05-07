
all: companion/qrc_resources.py
	
companion/qrc_resources.py: resources.qrc
	pyrcc5 -o companion/qrc_resources.py resources.qrc

