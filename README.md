# AES encryption visualizer
This tool lets you understand the process of AES encryption.  
For germans it may also be interesting to view my presentation with which I explained AES at school.
  
## Executing
To follow the (by the way fantastic) explanations of [this site](http://www.moserware.com/2009/09/stick-figure-guide-to-advanced.html),
you could use something like this where the first parameter is your plaintext and the second is the passphrase:  
`python visualizer.py "ATTACK AT DAWN!" "SOME 128 BIT KEY"`  
If you only want to test the encryption of this tool or you already know how AES works you might want to use this instead:  
`python encrypt.py "ATTACK AT DAWN!" "SOME 128 BIT KEY"`  