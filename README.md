First install flower: 

	pip install flwr

git clone this repo: 

	git clone https://github.com/elieli4/FedPoP.git 

Install roast for threshold signatures: 

	pip install git+https://github.com/nicovank/roast.git

Insall pyoprf and dependencies: 
	
	pip install pyoprf
 	pip install pysodium
	sudo apt-get install libsodium-dev
	
	git clone https://github.com/stef/liboprf.git
	cd liboprf/src/
	make
	sudo make install

To test the secure aggregation through flower only, do 

	./run.sh n

 where n is the number of clients.

To run the generate phase, enter the commands:
	
	./gen.sh n t m

where n is the number of clients, t is the threshold for the threshold signature, and m is the number of malicious users for the threshold signature only.
	

Run proof of participation:
In one terminal run: 

	python3 verifier.py

In a second terminal run: 

	python3 prover.py
