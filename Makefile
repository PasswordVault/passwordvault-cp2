#
passwd.txt: passwd.raw
	python3 mkdb.py

clean::
	rm -f passwd.txt
