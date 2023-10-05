# montana_bma_check
checks for keywords in BMAs.

The script will parse the pdf for valid links, download them if they aren't already downloaded and check them for the specified keyword(s) 

it isn't foolproof in that the keyword can be used in sentences for other reasons than you are interested in, but it'll help you to shorten 
the search. As an added bonus, you will get all the BMA files downloaded to disk. 

example run: 
```
Which region would you like to see shotgun specific BMAs for? (1 - 7): 7
Which keyword(s) do you want to search the BMAs for? (comma-separated): muzzleloader
```