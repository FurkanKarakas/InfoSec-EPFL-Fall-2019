#!bin/bash
sudo hashcat -a 3 -m 1400 -i --increment-min=4 --increment-max=6 target_hashes1a.txt -o cracked_hashes1a.txt -1 0123456789abcdefghijklmnopqrstuvwxyz ?1?1?1?1?1?1 --force
