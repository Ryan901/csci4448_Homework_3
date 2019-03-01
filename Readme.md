Hardware_Rental.py Readme

Ryan Murphy
Collaborators: None

 A note on syntax: Because python does not support private variables in classes I followed the standard notation of starting all
 private variables and functions with an underscore (_) to indicate that they are private. 

 Note on execution: In my implementation I randomly generate both the customers and tools as well as forcing customers to wait a
 random amount of time before returning to rent a new tool, this amount of time could be between 0 and 4 days for regular and 
 casual customers and between 7 and 12 days for Business customers. However in an attempt to make grading easier I found a seed
 that I believe demonstrates that the program meets all the requirements. If you want to change the seed or remove it you can find it in the first line of the section commented as Main.

 Customers, tools and days are identified by simple numbers and not by real names, real tool names or real dates.

 The program will output in the following order:

 The number of tools in inventory.

 The tool inventory

 Total Income

 The Active Rentals

 The Completed Rentals (sorted by start day)

 The Rental sections are printed in the style of a series of invoices both for plesent viewing and because I felt it was authentic to 
 the hardware rental store idea.