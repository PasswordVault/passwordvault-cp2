#
passwd.mpy: passwd.txt
	python3 mkdb.py > passwd.py
	~/Dokumente/circuitpython/mpy-cross/build/mpy-cross passwd.py 

clean::
	rm -f passwd.mpy