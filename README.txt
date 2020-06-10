Install the following libraries:
i. pip install re
ii. pip install googletrans

Run the following command on your console:

python diglot-weave.py 1 2 3 4 5

1: file name containing list of Words
2: file to be translated
3: language in which you want to translate, e.g 'es' for spanish
4: head start count
5: number of words to skip

Example command:
python diglot-weave.py list.txt sample.txt es 5 10

Output:
At the end of execution, the translated text is stored in a file in the same directory.
Note that the program keeps outputting the text that has been translated so the user does not have to wait till the end.

Suggestion:
If you want to test the program, and need instant outputs ( < 3 minutes ), keep the text file limited to 1000 words and the head Start to be less than 20.

Note:
We added a counter as well that is printed, displaying how many "head start words" are left. You'll start seeing the translated text after it hits 0. (kind of works like a countdown)

end